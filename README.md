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

2. For a private App you just need to set the base site url as 
    follows (where hostname is your site)

    ```python
    shop_url = "https://%s:%s@SHOP_NAME.myshopify.com/admin" % (API_KEY, PASSWORD)
    shopify.ShopifyResource.set_site(shop_url)
    ```

    That's it you're done, skip to step 7 and start using the API!

    For a partner App you will need to supply two parameters to the 
    Session class before you instantiate it:

    ```python
    shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)
    ```

3.  To access a shop's data apps need an access token from that specific shop.
    This is a two-stage process. Before interacting with a shop for the first 
    time an app should redirect the user to the following URL:

     GET https://SHOP_NAME.myshopify.com/admin/oauth/authorize

    with the following parameters:

     * client_id – Required – The API key for your app
     * scope – Required – The list of required scopes (explained here:
     http://docs.shopify.com/api/tutorials/oauth)
     * redirect_uri – Optional – The URL that the merchant will be sent 
       to once authentication is complete. Must be the same host as the 
       Return URL specified in the application settings

    We've added the create_permision_url method to make this easier:
     ```python
     scope=["write_products"]
     permission_url = shopify.Session.create_permission_url("SHOP_NAME.myshopify.com", scope, redirect_uri=None) 
     ```

4. Once authorized, the shop redirects the owner to the return URL of your
   application with a parameter named 'code'. This is a temporary token
   that the app can exchange for a permanent access token. Make the following call:

    POST https://SHOP_NAME.myshopify.com/admin/oauth/access_token

   with the following parameters:
   
    * client_id – Required – The API key for your app
    * client_secret – Required – The shared secret for your app
    * code – Required – The token you received in step 3

   and you'll get your permanent access token back in the response.

    There is also a method to create this url for you:
     ```python
     auth_url = shopify.Session.create_auth_url("SHOP_NAME.myshopify.com", code)
     ```

5.  Use that token to instantiate a session that is ready to make 
    calls to the given shop.

    ```python
    session = shopify.Session("SHOP_NAME.myshopify.com", token)
    session.valid # returns True
    ```

6.  Now you can activate the session and you're set:

    ```python
    shopify.ShopifyResource.activate_session(session)
    ```

7.  Start making authorized API requests for that shop. Data is returned as
    ActiveResource instances:

    ```python
    shop = shopify.Shop.current

    # Get a specific product
    product = shopify.Product.find(179761209)

    # Create a new product
    new_product = shopify.Product()
    new_product.title = "Burton Custom Freestlye 151"
    new_product.product_type = "Snowboard"
    new_product.vendor = "Burton"
    new_product.save()

    # Update a product
    product.handle = "burton-snowboard"
    product.save()
    ```

    Alternatively, you can use temp to initialize a Session and execute a command which also handles temporarily setting ActiveResource::Base.site:

     ```python
     products = shopify.Session.temp("SHOP_NAME.myshopify.com", token, "shopify.Product.find()")
     ```

8.  Finally, you can also clear the session (for example if you want to work with another shop):

     ```python
     shopify.ShopifyResource.clear_session
     ```

### Console

This package also includes the `shopify_api.py` script to make it easy to
open up an interactive console to use the API with a shop.

1.  Obtain a private API key and password to use with your shop 
    (step 2 in "Getting Started")

2.  Use the `shopify_api.py` script to save the credentials for the
    shop to quickly login. The script uses [PyYAML](http://pyyaml.org/) to save
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

4.  Enter the following for the full list of the commands.

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

## Limitations

Currently there is no support for:

* python 3
* asynchronous requests
* persistent connections
* json format for API requests

## Additional Resources

* [Shopify API](http://api.shopify.com) <= Read the tech docs!
* [Ask questions on the Shopify forums](http://ecommerce.shopify.com/c/shopify-apis-and-technology) <= Ask questions on the forums!

## Copyright

Copyright (c) 2012 "Shopify inc.". See LICENSE for details.
