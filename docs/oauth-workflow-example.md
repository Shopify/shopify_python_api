# Example OAuth workflow

The Shopify Python API [validates HMAC and timing attacks](https://shopify.dev/apps/auth/oauth/getting-started#step-2-verify-the-installation-request) with the `request_token` function. Below is a basic example OAuth workflow for a FastAPI app.


## Setup

1. Create a new application in the Partners Dashboard, and retrieve your API key and API secret.

2. Configure your app URL and Admin API version. Initialize your `shopify.Session` class with your API key and API secret for authentication.

```python
import shopify

VERSION = "2022-07"
HOST = "https://app-url"

API_KEY = "api-key"
API_SECRET = "api-secret"

shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)
```

3. Request permissions from the merchant with the `auth_url` from the `create_permission_url` function. Once the merchant acccepts, a temporary token `code` is sent to the specified `redirect_uri` of your app.

```python
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

@app.get("/", response_class=RedirectResponse)
async def install(shop_name: str):
    shop_url = f"{shop_name}.myshopify.com"
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = f"{HOST}/auth/shopify/callback"
    scopes = ['read_products']

    new_session = shopify.Session(shop_url, VERSION)
    auth_url = new_session.create_permission_url(scopes, redirect_uri, state)
    return RedirectResponse(
        url=auth_url,
        status_code=303
    )
```

4. To capture the `code`, set up a callback handler in your app. To exchange the temporary token for a permanent access token, supply the parameters from this request to the `request_token` function. See an [example query string here](https://shopify.dev/apps/auth/oauth/getting-started#step-2-verify-the-installation-request) to be passed as the `request_params`.

```python
@app.get("/auth/shopify/callback")
async def auth_callback(request: Request):
    request_params = dict(request.query_params)
    shop_url = request_params.get("shop")

    session = shopify.Session(shop_url, VERSION)
    access_token = session.request_token(request_params)
    # store access_token
```
