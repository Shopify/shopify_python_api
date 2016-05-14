[![Build Status](https://travis-ci.org/Shopify/shopify_python_api.svg?branch=master)](https://travis-ci.org/Shopify/shopify_python_api)
[![PyPI version](https://badge.fury.io/py/shopifyapi.svg)](https://badge.fury.io/py/shopifyapi)

# Shopify API

The ShopifyAPI library allows Python developers to programmatically
access the admin section of stores.

The API is accessed using pyactiveresource in order to provide an
interface similar to the
[ruby Shopify API](https://github.com/shopify/shopify_api) gem.
The data itself is sent as XML over HTTP to communicate with Shopify,
which provides a web service that follows the REST principles as
much as possible.

## Usage

### Requirements

All API usage happens through Shopify applications, created by
either shop owners for their own shops, or by Shopify Partners for
use by other shop owners:

* Shop owners can create applications for themselves through their
own admin: <http://docs.shopify.com/api/tutorials/creating-a-private-app>
* Shopify Partners create applications through their admin:
  <http://app.shopify.com/services/partners>

For more information and detailed documentation about the API visit
<http://api.shopify.com>

### Installation

To easily install or upgrade to the latest release, use
[pip](http://www.pip-installer.org/)

```shell
pip install --upgrade ShopifyAPI
```

or [easy_install](http://packages.python.org/distribute/easy_install.html)

```shell
easy_install -U ShopifyAPI
```

### Getting Started

ShopifyAPI uses pyactiveresource to communicate with the REST web
service. pyactiveresource has to be configured with a fully authorized
URL of a particular store first. To obtain that URL you can follow
these steps:

1.  First create a new application in either the partners admin or
    your store admin. For a private App you'll need the API_KEY and
    the PASSWORD otherwise you'll need the API_KEY and SHARED_SECRET.

2.  For a private App you just need to set the base site url as
    follows:

     ```python
     shop_url = "https://%s:%s@SHOP_NAME.myshopify.com/admin" % (API_KEY, PASSWORD)
     shopify.ShopifyResource.set_site(shop_url)
     ```

     That's it you're done, skip to step 6 and start using the API!
     For a partner App you will need to supply two parameters to the
     Session class before you instantiate it:

     ```python
     shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)
     ```

3.  In order to access a shop's data, apps need an access token from that
    specific shop. This is a two-stage process. Before interacting with
    a shop for the first time an app should redirect the user to the
    following URL:

    `GET https://SHOP_NAME.myshopify.com/admin/oauth/authorize`

    with the following parameters:

   * ``client_id``– Required – The API key for your app
   * ``scope`` – Required – The list of required scopes (explained here: http://docs.shopify.com/api/tutorials/oauth)
   * ``redirect_uri`` – Required – The URL where you want to redirect the users after they authorize the client. The complete URL specified here must be identical to one of the Application Redirect URLs set in the App's section of the Partners dashboard. Note: in older applications, this parameter was optional, and redirected to the Application Callback URL when no other value was specified.
   * ``state`` – Optional – A randomly selected value provided by your application, which is unique for each authorization request. During the OAuth callback phase, your application must check that this value matches the one you provided during authorization. [This mechanism is important for the security of your application](https://tools.ietf.org/html/rfc6819#section-3.6).

    We've added the create_permision_url method to make this easier, first
    instantiate your session object:

    ```python
    session = shopify.Session("SHOP_NAME.myshopify.com")
    ```

    Then call:

    ```python
    scope=["write_products"]
    permission_url = session.create_permission_url(scope)
    ```

    or if you want a custom redirect_uri:

    ```python
    permission_url = session.create_permission_url(scope, "https://my_redirect_uri.com")
    ```

4. Once authorized, the shop redirects the owner to the return URL of your application with a parameter named 'code'. This is a temporary token that the app can exchange for a permanent access token.

   Before you proceed, make sure your application performs the following security checks. If any of the checks fails, your application must reject the request with an error, and must not proceed further.

   * Ensure the provided ``state`` is the same one that your application provided to Shopify during Step 3.
   * Ensure the provided hmac is valid. The hmac is signed by Shopify as explained below, in the Verification section.
   * Ensure the provided hostname parameter is a valid hostname, ends with myshopify.com, and does not contain characters other than letters (a-z), numbers (0-9), dots, and hyphens.

   If all security checks pass, the authorization code can be exchanged once for a permanent access token. The exchange is made with a request to the shop.

   ```
   POST https://SHOP_NAME.myshopify.com/admin/oauth/access_token
   ```

    with the following parameters:

    ```
    * client_id – Required – The API key for your app
    * client_secret – Required – The shared secret for your app
    * code – Required – The code you received in step 3
    ```

    and you'll get your permanent access token back in the response.

    There is a method to make the request and get the token for you. Pass
    all the params received from the previous call (shop, code, timestamp,
    signature) as a dictionary and the method will verify
    the params, extract the temp code and then request your token:

    ```python
    token = session.request_token(params)
    ```

    This method will save the token to the session object
    and return it. For future sessions simply pass the token when
    creating the session object.

    ```python
    session = shopify.Session("SHOP_NAME.myshopify.com", token)
    ```

5.  The session must be activated before use:

    ```python
    shopify.ShopifyResource.activate_session(session)
    ```

6.  Now you're ready to make authorized API requests to your shop!
    Data is returned as [ActiveResource](https://github.com/Shopify/pyactiveresource) instances:

    ```python
    # Get the current shop
    shop = shopify.Shop.current()

    # Get a specific product
    product = shopify.Product.find(179761209)

    # Create a new product
    new_product = shopify.Product()
    new_product.title = "Burton Custom Freestyle 151"
    new_product.product_type = "Snowboard"
    new_product.vendor = "Burton"
    success = new_product.save() #returns false if the record is invalid
    # or
    if new_product.errors:
        #something went wrong, see new_product.errors.full_messages() for example

    # Update a product
    product.handle = "burton-snowboard"
    product.save()

    # Remove a product
    product.destroy()
    ```

    Alternatively, you can use temp to initialize a Session and execute a command which also handles temporarily setting ActiveResource::Base.site:

     ```python
     with shopify.Session.temp("SHOP_NAME.myshopify.com", token):
        product = shopify.Product.find()
     ```

7.  If you want to work with another shop, you'll first need to clear the session::

     ```python
     shopify.ShopifyResource.clear_session()
     ```

### Console

This package also includes the `shopify_api.py` script to make it easy to
open up an interactive console to use the API with a shop.

1.  Obtain a private API key and password to use with your shop
    (step 2 in "Getting Started")

2.  Use the `shopify_api.py` script to save the credentials for the
    shop to quickly log in. The script uses [PyYAML](http://pyyaml.org/) to save
    and load connection configurations in the same format as the ruby
    shopify\_api.

    ```shell
    shopify_api.py add yourshopname
    ```

    Follow the prompts for the shop domain, API key and password.

3.  Start the console for the connection.

    ```shell
    shopify_api.py console
    ```

4.  To see the full list of commands, type:

    ```shell
    shopify_api.py help
    ```

## Using Development Version

The development version can be built using

```shell
python setup.py sdist
```

then the package can be installed using pip

```shell
pip install --upgrade dist/ShopifyAPI-*.tar.gz
```

or easy_install

```shell
easy_install -U dist/ShopifyAPI-*.tar.gz
```

Note Use the `bin/shopify_api.py` script when running from the source tree.
It will add the lib directory to start of sys.path, so the installed
version won't be used.

To run tests, simply open up the project directory in a terminal and run:

```shell
python setup.py test
```

Alternatively, use [tox](http://tox.readthedocs.org/en/latest/) to
sequentially test against different versions of Python in isolated
environments:

```shell
pip install tox
tox
```

See the tox documentation for help on running only specific environments
at a time. The related tool [detox](https://pypi.python.org/pypi/detox)
can be used to run tests in these environments in parallel:

```shell
pip install detox
detox
```

## Limitations

Currently there is no support for:

* asynchronous requests
* persistent connections

## Additional Resources

* [Shopify API](http://api.shopify.com) <= Read the tech docs!
* [Ask questions on the Shopify forums](http://ecommerce.shopify.com/c/shopify-apis-and-technology) <= Ask questions on the forums!

## Copyright

Copyright (c) 2012 "Shopify inc.". See LICENSE for details.
