from shopify import session_token
from test.test_helper import TestCase
from datetime import datetime, timedelta

import jwt
import sys

if sys.version_info[0] < 3:  # Backwards compatibility for python < v3.0.0
    import time


def timestamp(date):
    return time.mktime(date.timetuple()) if sys.version_info[0] < 3 else date.timestamp()


class TestSessionTokenGetDecodedSessionToken(TestCase):
    @classmethod
    def setUpClass(self):
        self.secret = "API Secret"
        self.api_key = "API key"

    @classmethod
    def setUp(self):
        current_time = datetime.now()
        self.payload = {
            "iss": "https://test-shop.myshopify.com/admin",
            "dest": "https://test-shop.myshopify.com",
            "aud": self.api_key,
            "sub": "1",
            "exp": timestamp((current_time + timedelta(0, 60))),
            "nbf": timestamp(current_time),
            "iat": timestamp(current_time),
            "jti": "4321",
            "sid": "abc123",
        }

    @classmethod
    def build_auth_header(self):
        mock_session_token = jwt.encode(self.payload, self.secret, algorithm="HS256")
        return "Bearer {session_token}".format(session_token=mock_session_token)

    def test_raises_if_token_authentication_header_is_not_bearer(self):
        authorization_header = "Bad auth header"

        with self.assertRaises(session_token.TokenAuthenticationError) as cm:
            session_token.decode_from_header(authorization_header, api_key=self.api_key, secret=self.secret)

        self.assertEqual("The HTTP_AUTHORIZATION_HEADER provided does not contain a Bearer token", str(cm.exception))

    def test_raises_jwt_error_if_session_token_is_expired(self):
        self.payload["exp"] = timestamp((datetime.now() + timedelta(0, -11)))

        with self.assertRaises(session_token.SessionTokenError) as cm:
            session_token.decode_from_header(self.build_auth_header(), api_key=self.api_key, secret=self.secret)

        self.assertEqual("Signature has expired", str(cm.exception))

    def test_raises_jwt_error_if_invalid_alg(self):
        bad_session_token = jwt.encode(self.payload, None, algorithm="none")
        invalid_header = "Bearer {session_token}".format(session_token=bad_session_token)

        with self.assertRaises(session_token.SessionTokenError) as cm:
            session_token.decode_from_header(invalid_header, api_key=self.api_key, secret=self.secret)

        self.assertEqual("The specified alg value is not allowed", str(cm.exception))

    def test_raises_jwt_error_if_invalid_signature(self):
        bad_session_token = jwt.encode(self.payload, "bad_secret", algorithm="HS256")
        invalid_header = "Bearer {session_token}".format(session_token=bad_session_token)

        with self.assertRaises(session_token.SessionTokenError) as cm:
            session_token.decode_from_header(invalid_header, api_key=self.api_key, secret=self.secret)

        self.assertEqual("Signature verification failed", str(cm.exception))

    def test_raises_if_aud_doesnt_match_api_key(self):
        self.payload["aud"] = "bad audience"

        with self.assertRaises(session_token.SessionTokenError) as cm:
            session_token.decode_from_header(self.build_auth_header(), api_key=self.api_key, secret=self.secret)

        self.assertEqual("Audience doesn't match", str(cm.exception))

    def test_raises_if_issuer_hostname_is_invalid(self):
        self.payload["iss"] = "bad_shop_hostname"

        with self.assertRaises(session_token.InvalidIssuerError) as cm:
            session_token.decode_from_header(self.build_auth_header(), api_key=self.api_key, secret=self.secret)

        self.assertEqual("Invalid issuer", str(cm.exception))

    def test_raises_if_iss_and_dest_dont_match(self):
        self.payload["dest"] = "bad_shop.myshopify.com"

        with self.assertRaises(session_token.MismatchedHostsError) as cm:
            session_token.decode_from_header(self.build_auth_header(), api_key=self.api_key, secret=self.secret)

        self.assertEqual("The issuer and destination do not match", str(cm.exception))

    def test_returns_decoded_payload(self):
        decoded_payload = session_token.decode_from_header(
            self.build_auth_header(), api_key=self.api_key, secret=self.secret
        )

        self.assertEqual(self.payload, decoded_payload)

    def test_allow_10_seconds_clock_skew_in_nbf(self):
        self.payload["nbf"] = timestamp((datetime.now() + timedelta(seconds=10)))

        session_token.decode_from_header(self.build_auth_header(), api_key=self.api_key, secret=self.secret)
