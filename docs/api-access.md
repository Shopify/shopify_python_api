# Handling access scope operations

#### Table of contents

- [Common ApiAccess operations](#common-apiaccess-operations)
- [Using ApiAccess to handle changes in app access scopes](#using-apiaccess-to-handle-changes-in-app-access-scopes)

There are common operations that are used for managing [access scopes](https://shopify.dev/docs/admin-api/access-scopes) in apps. Such operations include serializing, deserializing and normalizing scopes. Other operations can include checking whether two sets of scopes grant the same API access or whether one set covers the access granted by another set.

To encapsulate the access granted by access scopes, you can use the `ApiAccess` value object.

## Common ApiAccess operations

### Constructing an ApiAccess

```python
api_access = ApiAccess(["read_products", "write_orders"]) # List of access scopes
another_api_access = ApiAccess("read_products, write_products, unauthenticated_read_themes") # String of comma-delimited access scopes
```

### Serializing ApiAccess

```python
api_access = ApiAccess(["read_products", "write_orders", "unauthenticated_read_themes"])

access_scopes_list = list(api_access) # ["read_products", "write_orders", "unauthenticated_read_themes"]
comma_delimited_access_scopes = str(api_access) # "read_products,write_orders,unauthenticated_read_themes"
```

### Comparing ApiAccess objects

#### Checking for API access equality

```python
expected_api_access = ApiAccess(["read_products", "write_orders"])

actual_api_access = ApiAccess(["read_products", "read_orders", "write_orders"])
non_equal_api_access = ApiAccess(["read_products", "write_orders", "read_themes"])

actual_api_access == expected_api_access # True
non_equal_api_access == expected_api_access # False
```

#### Checking if ApiAccess covers the access of another

```python
superset_access = ApiAccess(["write_products", "write_orders", "read_themes"])
subset_access = ApiAccess(["read_products", "write_orders"])

superset_access.covers(subset_access) # True
```

## Using ApiAccess to handle changes in app access scopes

If your app has changes in the access scopes it requests, you can use the `ApiAccess` object to determine whether the merchant needs to go through OAuth based on the scopes currently granted. A sample decorator shows how this can be achieved when loading an app.

```python
from shopify import ApiAccess


def oauth_on_access_scopes_mismatch(func):
  def wrapper(*args, **kwargs):
    shop_domain = get_shop_query_parameter(request) # shop query param when loading app
    current_shop_scopes = ApiAccess(ShopStore.get_record(shopify_domain = shop_domain).access_scopes)
    expected_access_scopes = ApiAccess(SHOPIFY_API_SCOPES)

    if current_shop_scopes != expected_access_scopes:
      return redirect_to_login() # redirect to OAuth to update access scopes granted

    return func(*args, **kwargs)

  return wrapper
```
