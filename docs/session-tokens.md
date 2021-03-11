# Session tokens

The Shopify Python API library provides helper methods to decode [session tokens](https://shopify.dev/concepts/apps/building-embedded-apps-using-session-tokens). You can use the `decode_from_header` function to extract and decode a session token from an HTTP Authorization header.

## Basic usage

```python
from shopify import session_token

decoded_payload = session_token.decode_from_header(
    authorization_header=your_auth_request_header,
    api_key=your_api_key,
    secret=your_api_secret,
)
```

## Create a decorator using `session_token`

Here's a sample decorator that protects your app views/routes by requiring the presence of valid session tokens as part of a request's headers.

```python
from shopify import session_token


def session_token_required(func):
    def wrapper(*args, **kwargs):
        request = args[0]  # Or flask.request if you use Flask
        try:
            decoded_session_token = session_token.decode_from_header(
                authorization_header = request.headers.get('Authorization'),
                api_key = SHOPIFY_API_KEY,
                secret = SHOPIFY_API_SECRET
            )
            with shopify_session(decoded_session_token):
                return func(*args, **kwargs)
        except session_token.SessionTokenError as e:
            # Log the error here
            return unauthorized_401_response()

    return wrapper


def shopify_session(decoded_session_token):
    shopify_domain = decoded_session_token.get("dest")
    access_token = get_offline_access_token_by_shop_domain(shopify_domain)

    return shopify.Session.temp(shopify_domain, SHOPIFY_API_VERSION, access_token)


@session_token_required  # Requests to /products require session tokens
def products(request):
    products = shopify.Product.find()
    ...
```
