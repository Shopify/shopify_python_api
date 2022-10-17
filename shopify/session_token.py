import jwt
import re
import six
import sys

from shopify.utils import shop_url

if sys.version_info[0] < 3:  # Backwards compatibility for python < v3.0.0
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


ALGORITHM = "HS256"
PREFIX = "Bearer "
REQUIRED_FIELDS = ["iss", "dest", "sub", "jti", "sid"]
LEEWAY_SECONDS = 10


class SessionTokenError(Exception):
    pass


class InvalidIssuerError(SessionTokenError):
    pass


class MismatchedHostsError(SessionTokenError):
    pass


class TokenAuthenticationError(SessionTokenError):
    pass


def decode_from_header(authorization_header, api_key, secret):
    session_token = _extract_session_token(authorization_header)
    decoded_payload = _decode_session_token(session_token, api_key, secret)
    _validate_issuer(decoded_payload)

    return decoded_payload


def _extract_session_token(authorization_header):
    if not authorization_header.startswith(PREFIX):
        raise TokenAuthenticationError("The HTTP_AUTHORIZATION_HEADER provided does not contain a Bearer token")

    return authorization_header[len(PREFIX) :]


def _decode_session_token(session_token, api_key, secret):
    try:
        return jwt.decode(
            session_token,
            secret,
            audience=api_key,
            algorithms=[ALGORITHM],
            # AppBridge frequently sends future `nbf`, and it causes `ImmatureSignatureError`.
            # Accept few seconds clock skew to avoid this error.
            leeway=LEEWAY_SECONDS,
            options={"require": REQUIRED_FIELDS},
        )
    except jwt.exceptions.PyJWTError as exception:
        six.raise_from(SessionTokenError(str(exception)), exception)


def _validate_issuer(decoded_payload):
    _validate_issuer_hostname(decoded_payload)
    _validate_issuer_and_dest_match(decoded_payload)


def _validate_issuer_hostname(decoded_payload):
    issuer_root = urljoin(decoded_payload["iss"], "/")

    if not shop_url.sanitize_shop_domain(issuer_root):
        raise InvalidIssuerError("Invalid issuer")


def _validate_issuer_and_dest_match(decoded_payload):
    issuer_root = urljoin(decoded_payload["iss"], "/")
    dest_root = urljoin(decoded_payload["dest"], "/")

    if issuer_root != dest_root:
        raise MismatchedHostsError("The issuer and destination do not match")
