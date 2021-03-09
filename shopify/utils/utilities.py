from .exceptions import *

import jwt
import re
import sys

if sys.version_info[0] < 3:  # Backwards compatibility for python < v3.0.0
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


class SessionTokenUtility:
    ALGORITHM = "HS256"
    PREFIX = "Bearer "
    REQUIRED_FIELDS = ["iss", "dest", "sub", "jti", "sid"]

    @classmethod
    def get_decoded_session_token(cls, authorization_header, api_key, secret):
        session_token = cls.__extract_session_token(authorization_header)
        decoded_payload = cls.__decode_session_token(session_token, api_key, secret)
        cls.__validate_issuer(decoded_payload)

        return decoded_payload

    @classmethod
    def __extract_session_token(cls, authorization_header):
        if not authorization_header.startswith(cls.PREFIX):
            raise TokenAuthenticationError("The HTTP_AUTHORIZATION_HEADER provided does not contain a Bearer token")

        return authorization_header[len(cls.PREFIX) :]

    @classmethod
    def __decode_session_token(cls, session_token, api_key, secret):
        return jwt.decode(
            session_token,
            secret,
            audience=api_key,
            algorithms=[cls.ALGORITHM],
            options={"require": cls.REQUIRED_FIELDS},
        )

    @classmethod
    def __validate_issuer(cls, decoded_payload):
        cls.__validate_issuer_hostname(decoded_payload)
        cls.__validate_issuer_and_dest_match(decoded_payload)

    @classmethod
    def __validate_issuer_hostname(cls, decoded_payload):
        hostname_pattern = r"[a-z0-9][a-z0-9-]*[a-z0-9]"
        shop_domain_re = re.compile(r"^https://{h}\.myshopify\.com/$".format(h=hostname_pattern))

        issuer_root = urljoin(decoded_payload["iss"], "/")

        if not shop_domain_re.match(issuer_root):
            raise InvalidIssuerError()

    @classmethod
    def __validate_issuer_and_dest_match(cls, decoded_payload):
        issuer_root = urljoin(decoded_payload["iss"], "/")
        dest_root = urljoin(decoded_payload["dest"], "/")

        if issuer_root != dest_root:
            raise MismatchedHostsError()
