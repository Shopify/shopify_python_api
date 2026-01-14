import time
import hmac
import json
from hashlib import sha256

try:
    import simplejson as json
except ImportError:
    import json
import re
from contextlib import contextmanager
from six.moves import urllib
from shopify.api_access import ApiAccess
from shopify.api_version import ApiVersion, Release, Unstable
import six


class ValidationException(Exception):
    pass


class OAuthException(Exception):
    """Exception raised for OAuth-related errors"""
    pass


class Session(object):
    api_key = None
    secret = None
    protocol = "https"
    myshopify_domain = "myshopify.com"
    port = None

    @classmethod
    def setup(cls, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(cls, k, v)

    @classmethod
    @contextmanager
    def temp(cls, domain, version, token):
        import shopify

        original_domain = shopify.ShopifyResource.url
        original_token = shopify.ShopifyResource.get_headers().get("X-Shopify-Access-Token")
        original_version = shopify.ShopifyResource.get_version() or version
        original_session = shopify.Session(original_domain, original_version, original_token)

        session = Session(domain, version, token)
        shopify.ShopifyResource.activate_session(session)
        yield
        shopify.ShopifyResource.activate_session(original_session)

    def __init__(self, shop_url, version=None, token=None, access_scopes=None):
        self.url = self.__prepare_url(shop_url)
        self.token = token
        self.version = ApiVersion.coerce_to_version(version)
        self.access_scopes = access_scopes
        return

    def _requires_client_credentials(self):
        """
        Check if the API version requires OAuth 2.0 Client Credentials Grant.

        Starting from API version 2026-01, Shopify requires apps created in
        Dev Dashboard to use OAuth 2.0 client credentials instead of permanent
        access tokens.

        Returns:
            bool: True if version is 2026-01 or higher, False otherwise
        """
        if not self.version:
            return False

        # Get numeric version (e.g., 202601 for "2026-01")
        version_number = self.version.numeric_version

        # 2026-01 = 202601, check if >= this threshold
        return version_number >= 202601

    def create_permission_url(self, redirect_uri, scope=None, state=None):
        query_params = {"client_id": self.api_key, "redirect_uri": redirect_uri}
        # `scope` should be omitted if provided by app's TOML
        if scope:
            query_params["scope"] = ",".join(scope)
        if state:
            query_params["state"] = state
        return "https://%s/admin/oauth/authorize?%s" % (self.url, urllib.parse.urlencode(query_params))

    def request_token(self, params):
        """
        Exchange authorization code for access token (Authorization Code Grant).

        Note: This method is for the traditional OAuth Authorization Code Grant flow
        and will not work with API version 2026-01 or higher. For 2026-01+, use
        request_token_client_credentials() instead, or use request_access_token()
        which automatically selects the correct method based on API version.

        Args:
            params: OAuth callback parameters including 'code', 'hmac', 'timestamp'

        Returns:
            str: The access token

        Raises:
            ValidationException: If HMAC validation fails
        """
        if self.token:
            return self.token

        # Warn if using old auth method with new API version
        if self._requires_client_credentials():
            raise ValidationException(
                "API version %s requires OAuth 2.0 Client Credentials Grant. "
                "Use request_token_client_credentials() or request_access_token() instead."
                % self.version.name
            )

        if not self.validate_params(params):
            raise ValidationException("Invalid HMAC: Possibly malicious login")

        code = params["code"]

        url = "https://%s/admin/oauth/access_token?" % self.url
        query_params = {"client_id": self.api_key, "client_secret": self.secret, "code": code}
        request = urllib.request.Request(url, urllib.parse.urlencode(query_params).encode("utf-8"))
        response = urllib.request.urlopen(request)

        if response.code == 200:
            json_payload = json.loads(response.read().decode("utf-8"))
            self.token = json_payload["access_token"]
            self.access_scopes = json_payload["scope"]

            return self.token
        else:
            raise Exception(response.msg)

    def request_token_client_credentials(self):
        """
        Exchange client credentials for an access token.

        OAuth 2.0 Client Credentials Grant (RFC 6749, Section 4.4)
        https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/client-credentials-grant

        This method is used for server-to-server authentication where the app
        authenticates with its own credentials rather than on behalf of a user.

        Requirements:
        - Session.api_key (client_id) must be set
        - Session.secret (client_secret) must be set
        - Shop URL must be valid

        Returns:
            dict: Token response containing:
                - access_token (str): The access token for API requests
                - scope (str): Comma-separated list of granted scopes
                - expires_in (int): Seconds until token expires (typically 86399 = 24 hours)

        Raises:
            ValidationException: If required credentials are missing
            OAuthException: If OAuth request fails

        Example:
            >>> session = shopify.Session("mystore.myshopify.com", "2026-01")
            >>> shopify.Session.setup(api_key="client_id", secret="client_secret")
            >>> token_response = session.request_token_client_credentials()
            >>> session.token = token_response["access_token"]
            >>> shopify.ShopifyResource.activate_session(session)
        """
        # Validate required credentials
        if not self.api_key:
            raise ValidationException("api_key (client_id) is required for client credentials grant")
        if not self.secret:
            raise ValidationException("secret (client_secret) is required for client credentials grant")
        if not self.url:
            raise ValidationException("shop_url is required for client credentials grant")

        # Return existing token if already set
        if self.token:
            return {
                "access_token": self.token,
                "scope": str(self.access_scopes) if self.access_scopes else "",
                "expires_in": None  # Unknown if token was set manually
            }

        # Construct OAuth endpoint URL
        url = "https://%s/admin/oauth/access_token" % self.url

        # Prepare request data (form-encoded)
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret
        }

        # Prepare request headers
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            # Make OAuth request
            request = urllib.request.Request(
                url,
                urllib.parse.urlencode(data).encode("utf-8"),
                headers=headers
            )

            # Set timeout to prevent hanging
            response = urllib.request.urlopen(request, timeout=10)

            if response.code == 200:
                # Parse response
                json_payload = json.loads(response.read().decode("utf-8"))

                # Store token and scopes in session
                self.token = json_payload["access_token"]
                self.access_scopes = json_payload.get("scope", "")

                # Return full response for caller
                return {
                    "access_token": self.token,
                    "scope": self.access_scopes,
                    "expires_in": json_payload.get("expires_in", 86399)
                }
            else:
                raise OAuthException("OAuth request failed with status %d: %s" % (response.code, response.msg))

        except urllib.error.HTTPError as e:
            # Parse error response if available
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
                error_json = json.loads(error_body)
                error_message = error_json.get("error_description", error_json.get("error", error_body))
            except (ValueError, KeyError):
                error_message = error_body if error_body else str(e)

            raise OAuthException("OAuth request failed: %s (HTTP %d)" % (error_message, e.code))

        except urllib.error.URLError as e:
            raise OAuthException("OAuth request failed: %s" % str(e.reason))

        except Exception as e:
            raise OAuthException("Unexpected error during OAuth request: %s" % str(e))

    def request_access_token(self, params=None):
        """
        Automatically select and execute the appropriate OAuth flow based on API version.

        For API versions 2026-01 and higher: Uses OAuth 2.0 Client Credentials Grant
        For API versions before 2026-01: Uses Authorization Code Grant

        This is the recommended method for obtaining access tokens as it automatically
        adapts to the API version requirements.

        Args:
            params: OAuth callback parameters (required for versions < 2026-01)
                   Should include 'code', 'hmac', 'timestamp' for authorization code flow.
                   Not used for client credentials flow (versions >= 2026-01).

        Returns:
            For versions >= 2026-01: dict with 'access_token', 'scope', 'expires_in'
            For versions < 2026-01: str (access token)

        Raises:
            ValidationException: If required credentials or parameters are missing
            OAuthException: If OAuth request fails (versions >= 2026-01)

        Example:
            # For 2026-01+ (automatic client credentials)
            >>> session = shopify.Session("store.myshopify.com", "2026-01")
            >>> shopify.Session.setup(api_key="client_id", secret="client_secret")
            >>> response = session.request_access_token()
            >>> token = response["access_token"]

            # For older versions (authorization code)
            >>> session = shopify.Session("store.myshopify.com", "2024-10")
            >>> token = session.request_access_token(callback_params)
        """
        if self._requires_client_credentials():
            # API version 2026-01+: Use client credentials grant
            return self.request_token_client_credentials()
        else:
            # Older API versions: Use authorization code grant
            if params is None:
                raise ValidationException(
                    "params are required for authorization code grant (API versions < 2026-01). "
                    "For API version 2026-01+, client credentials are used automatically."
                )
            return self.request_token(params)

    @property
    def api_version(self):
        return self.version

    @property
    def site(self):
        return self.version.api_path("%s://%s" % (self.protocol, self.url))

    @property
    def valid(self):
        return self.url is not None and self.token is not None

    @property
    def access_scopes(self):
        return self._access_scopes

    @access_scopes.setter
    def access_scopes(self, scopes):
        if scopes is None or type(scopes) == ApiAccess:
            self._access_scopes = scopes
        else:
            self._access_scopes = ApiAccess(scopes)

    @classmethod
    def __prepare_url(cls, url):
        if not url or (url.strip() == ""):
            return None
        url = re.sub("^https?://", "", url)
        shop = urllib.parse.urlparse("https://" + url).hostname
        if shop is None:
            return None
        idx = shop.find(".")
        if idx != -1:
            shop = shop[0:idx]
        if len(shop) == 0:
            return None
        shop += "." + cls.myshopify_domain
        if cls.port:
            shop += ":" + str(cls.port)
        return shop

    @classmethod
    def validate_params(cls, params):
        # Avoid replay attacks by making sure the request
        # isn't more than a day old.
        one_day = 24 * 60 * 60
        if int(params.get("timestamp", 0)) < time.time() - one_day:
            return False

        return cls.validate_hmac(params)

    @classmethod
    def validate_hmac(cls, params):
        if "hmac" not in params:
            return False

        hmac_calculated = cls.calculate_hmac(params).encode("utf-8")
        hmac_to_verify = params["hmac"].encode("utf-8")

        # Try to use compare_digest() to reduce vulnerability to timing attacks.
        # If it's not available, just fall back to regular string comparison.
        try:
            return hmac.compare_digest(hmac_calculated, hmac_to_verify)
        except AttributeError:
            return hmac_calculated == hmac_to_verify

    @classmethod
    def calculate_hmac(cls, params):
        """
        Calculate the HMAC of the given parameters in line with Shopify's rules for OAuth authentication.
        See http://docs.shopify.com/api/authentication/oauth#verification.
        """
        encoded_params = cls.__encoded_params_for_signature(params)
        # Generate the hex digest for the sorted parameters using the secret.
        return hmac.new(cls.secret.encode(), encoded_params.encode(), sha256).hexdigest()

    @classmethod
    def __encoded_params_for_signature(cls, params):
        """
        Sort and combine query parameters into a single string, excluding those that should be removed and joining with '&'
        """

        def encoded_pairs(params):
            for k, v in six.iteritems(params):
                if k == "hmac":
                    continue

                if k.endswith("[]"):
                    # foo[]=1&foo[]=2 has to be transformed as foo=["1", "2"] note the whitespace after comma
                    k = k.rstrip("[]")
                    v = json.dumps(list(map(str, v)))

                # escape delimiters to avoid tampering
                k = str(k).replace("%", "%25").replace("=", "%3D")
                v = str(v).replace("%", "%25")
                yield "{0}={1}".format(k, v).replace("&", "%26")

        return "&".join(sorted(encoded_pairs(params)))
