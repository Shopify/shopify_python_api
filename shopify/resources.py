from shopify.base import ShopifyResource
import shopify.mixins as mixins
import base64
import re

class Shop(ShopifyResource):
    @classmethod
    def current(cls):
        return cls.find_one("/admin/shop." + cls.format.extension)

    def metafields(self):
        return Metafield.find()

    def add_metafield(self, metafield):
        if self.is_new():
            raise ValueError("You can only add metafields to a resource that has been saved")
        metafield.save()
        return metafield

    def events(self):
        return Event.find()


class CustomCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return Product.find(collection_id=self.id)

    def add_product(self, product):
        return Collect.create(dict(collection_id=self.id, product_id=product.id))

    def remove_product(self, product):
        collect = Collect.find_first(collection_id=self.id, product_id=product.id)
        if collect:
            collect.destroy()


class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return Product.find(collection_id=self.id)


class Collect(ShopifyResource):
    pass


class ShippingAddress(ShopifyResource):
    pass


class BillingAddress(ShopifyResource):
    pass


class LineItem(ShopifyResource):
    pass


class ShippingLine(ShopifyResource):
    pass


class NoteAttribute(ShopifyResource):
    pass


class Order(ShopifyResource, mixins.Metafields, mixins.Events):
    def close(self):
        self._load_attributes_from_response(self.post("close"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def cancel(self, **kwargs):
        self._load_attributes_from_response(self.post("cancel", **kwargs))

    def transactions(self):
        return Transaction.find(order_id=self.id)

    def capture(self, amount=""):
        return Transaction.create(amount=amount, kind="capture", order_id=self.id)


class Product(ShopifyResource, mixins.Metafields, mixins.Events):
    def price_range(self):
        prices = [variant.price for variant in self.variants]
        f = "%0.2f"
        min_price = min(prices)
        max_price = max(prices)
        if min_price != max_price:
            return "%s - %s" % (f % min_price, f % max_price)
        else:
            return f % min_price

    def collections(self):
        return CustomCollection.find(product_id = self.id)

    def smart_collections(self):
        return SmartCollection.find(product_id = self.id)

    def add_to_collection(self, collection):
        return collection.add_product(self)

    def remove_from_collection(self, collection):
        return collection.remove_product(self)


class Variant(ShopifyResource, mixins.Metafields):
    _prefix_source = "/admin/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        return "/admin/" if product_id is None else "/admin/products/%s" % (product_id)


class Image(ShopifyResource):
    _prefix_source = "/admin/products/$product_id/"

    def __getattr__(self, name):
        if name in ["pico", "icon", "thumb", "small", "compact", "medium", "large", "grande", "original"]:
            return re.sub(r"/(.*)\.(\w{2,4})", r"/\1_%s.\2" % (name), self.src)
        else:
            return super(Image, self).__getattr__(name)

    def attach_image(self, data, filename=None):
        self.attributes["attachment"] = base64.b64encode(data)
        if filename is not None:
            self.attributes["filename"] = filename


class Transaction(ShopifyResource):
    _prefix_source = "/admin/orders/$order_id/"


class Fulfillment(ShopifyResource):
    _prefix_source = "/admin/orders/$order_id/"


class Country(ShopifyResource):
    pass


class Page(ShopifyResource, mixins.Metafields, mixins.Events):
    pass


class Blog(ShopifyResource, mixins.Metafields, mixins.Events):
    def articles(self):
        return Article.find(blog_id=self.id)


class Article(ShopifyResource, mixins.Metafields, mixins.Events):
    _prefix_source = "/admin/blogs/$blog_id/"

    @classmethod
    def _prefix(cls, options={}):
        blog_id = options.get("blog_id")
        return "/admin/" if blog_id is None else "/admin/blogs/%s" % (blog_id)

    def comments(self):
        return Comment.find(article_id=self.id)


class Metafield(ShopifyResource):
    _prefix_source = "/admin/$resource/$resource_id/"

    @classmethod
    def _prefix(cls, options={}):
        return "/admin/" if options.get("resource") is None else "/admin/%s/%s" % (options["resource"], options["resource_id"])


class Comment(ShopifyResource):
    def remove(self):
        self._load_attributes_from_response(self.post("remove"))

    def spam(self):
        self._load_attributes_from_response(self.post("spam"))

    def approve(self):
        self._load_attributes_from_response(self.post("approve"))

    def restore(self):
        self._load_attributes_from_response(self.post("restore"))

    def not_spam(self):
        self._load_attributes_from_response(self.post("not_spam"))


class Province(ShopifyResource):
    _prefix_source = "/admin/countries/$country_id/"


class Redirect(ShopifyResource):
    pass


class Webhook(ShopifyResource):
    def __get_format(self):
        return self.attributes.get("format")

    def __set_format(self, data):
        self.attributes["format"] = data

    format = property(__get_format, __set_format, None, "Format attribute")


class Event(ShopifyResource):
    _prefix_source = "/admin/$resource/$resource_id/"

    @classmethod
    def _prefix(cls, options={}):
        return "/admin/" if options.get("resource") is None else "/admin/%s/%s/" % (options["resource"], options["resource_id"])


class Customer(ShopifyResource, mixins.Metafields):
    @classmethod
    def search(cls, **kwargs):
        """Search for customers matching supplied query

        Args:
           q: Text to search for customers ("q" is short for query)
           f: Filters to apply to customers ("f" is short for query)
           page: Page to show (default: 1)
           limit: Maximum number of results to show (default: 50, maximum: 250)
        Returns:
           An array of customers.
        """
        return cls._build_list(cls.get("search", **kwargs))


class CustomerGroup(ShopifyResource):
    def customers(cls, **kwargs):
        """Get a list of customers matching a customer group

        Args:
           page: Page to show (default: 1)
           limit: Maximum number of results to show (default: 50, maximum: 250)
        Returns:
           An array of customers.
        """
        return Customer._build_list(cls.get("customers", **kwargs))


class Theme(ShopifyResource):
    pass


class Asset(ShopifyResource):
    _primary_key = "key"
    _prefix_source = "/admin/themes/$theme_id/"

    @classmethod
    def _prefix(cls, options={}):
        return "/admin/" if options.get("theme_id") is None else "/admin/themes/%s/" % (options["theme_id"])

    @classmethod
    def _element_path(cls, id, prefix_options={}, query_options=None):
        if query_options is None:
            prefix_options, query_options = cls._split_options(prefix_options)
        return "%s%s.%s%s" % (cls._prefix(prefix_options), cls.plural,
                              cls.format.extension, cls._query_string(query_options))

    @classmethod
    def find(cls, key=None, **kwargs):
        """Find an asset by key
        E.g.
            shopify.Asset.find('layout/theme.liquid', theme_id=99)
        """
        if not key:
            return super(Asset, cls).find(**kwargs)
        params = {"asset[key]": key}
        params.update(kwargs)
        theme_id = params.get("theme_id")
        path_prefix = "/admin/themes/%s" % (theme_id) if theme_id else "/admin"
        resource = cls.find_one("%s/assets.%s" % (path_prefix, cls.format.extension), **params)
        if theme_id and resource:
            resource._prefix_options["theme_id"] = theme_id
        return resource

    def __get_value(self):
        data = self.attributes.get("value")
        if data:
            return data
        data = self.attributes.get("attachment")
        if data:
            return base64.b64decode(data)

    def __set_value(self, data):
        self.__wipe_value_attributes()
        self.attributes["value"] = data

    value = property(__get_value, __set_value, None, "The asset's value or attachment")

    def attach(self, data):
        self.attachment = base64.b64encode(data)

    def destroy(self):
        options = {"asset[key]": self.key}
        options.update(self._prefix_options)
        return self.__class__.connection.delete(self._element_path(self.key, options), self.__class__.headers)

    def is_new(self):
        return False

    def __setattr__(self, name, value):
        if name in ("value", "attachment", "src", "source_key"):
            self.__wipe_value_attributes()
        return super(Asset, self).__setattr__(name, value)

    def __wipe_value_attributes(self):
        for attr in ("value", "attachment", "src", "source_key"):
            if self.attributes.has_key(attr):
                del self.attributes[attr]


class RecurringApplicationCharge(ShopifyResource):
    @classmethod
    def current(cls):
        return cls.find_first(status="active")

    def cancel(self):
        self._load_attributes_from_response(self.destroy)

    def activate(self):
        self._load_attributes_from_response(self.post("activate"))


class ApplicationCharge(ShopifyResource):
    def activate(self):
        self._load_attributes_from_response(self.post("activate"))


class ProductSearchEngine(ShopifyResource):
    pass


class ScriptTag(ShopifyResource):
    pass


# attribute of Customer
class Address(ShopifyResource):
    pass


# attribute of Product
class Option(ShopifyResource):
    pass


# attribute of Order
class PaymentDetails(ShopifyResource):
    pass


# attribute of Fulfillment and Transaction
class Receipt(ShopifyResource):
    pass


# attribute of SmartCollection
class Rule(ShopifyResource):
    pass


# attribute of Order
class TaxLine(ShopifyResource):
    pass
