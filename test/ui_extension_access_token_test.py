from shopify import session_token
from test.test_helper import TestCase
from datetime import datetime, timedelta

import jwt
import sys

if sys.version_info[0] < 3:  # Backwards compatibility for python < v3.0.0
    import time


def timestamp(date):
    return time.mktime(date.timetuple()) if sys.version_info[0] < 3 else date.timestamp()


class UIExtensionAccessTokenTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.secret = "API Secret"
        cls.api_key = "API key"

    @classmethod
    def setUp(cls):
        current_time = datetime.now()
        cls.payload = {
            "dest": "https://test-shop.myshopify.com",
            "aud": cls.api_key,
            "exp": timestamp((current_time + timedelta(0, 60))),
            "nbf": timestamp(current_time),
            "iat": timestamp(current_time),
            "jti": "6c992878-dbaf-48d1-bb9d-6d9b59814fd1",
        }

    @classmethod
    def build_auth_header(cls):
        mock_session_token = jwt.encode(cls.payload, cls.secret, algorithm="HS256")
        return "Bearer {session_token}".format(session_token=mock_session_token)

    def test_raises_if_token_authentication_header_is_not_bearer(self):
        authorization_header = "Bad auth header"

        with self.assertRaises(session_token.TokenAuthenticationError) as cm:
            session_token.decode_from_header(
                authorization_header, api_key=self.api_key, secret=self.secret, is_extension=True
            )

        self.assertEqual("The HTTP_AUTHORIZATION_HEADER provided does not contain a Bearer token", str(cm.exception))

    def test_raises_extension_is_false_and_invalid_payload(self):
        authorization_header = self.build_auth_header()

        with self.assertRaises(session_token.SessionTokenError) as cm:
            session_token.decode_from_header(
                authorization_header, api_key=self.api_key, secret=self.secret, is_extension=False
            )

        self.assertEqual('Token is missing the "iss" claim', str(cm.exception))
