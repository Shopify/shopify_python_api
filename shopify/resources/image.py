from ..base import ShopifyResource
from ..resources import Metafield
from six.moves import urllib
import base64
import re


class Image(ShopifyResource):
    _prefix_source = "/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        if product_id:
            return "%s/products/%s" % (cls.site, product_id)
        else:
            return cls.site

    def __getattr__(self, name):
        if name in ["pico", "icon", "thumb", "small", "compact", "medium", "large", "grande", "original"]:
            return re.sub(r"/(.*)\.(\w{2,4})", r"/\1_%s.\2" % (name), self.src)
        else:
            return super(Image, self).__getattr__(name)

    def attach_image(self, data, filename=None):
        self.attributes["attachment"] = base64.b64encode(data).decode()
        if filename:
            self.attributes["filename"] = filename

    def metafields(self):
        if self.is_new():
            return []
        query_params = {"metafield[owner_id]": self.id, "metafield[owner_resource]": "product_image"}
        return Metafield.find(
            from_="%s/metafields.json?%s" % (ShopifyResource.site, urllib.parse.urlencode(query_params))
        )

    def save(self):
        if "product_id" not in self._prefix_options:
            self._prefix_options["product_id"] = self.product_id
        return super(ShopifyResource, self).save()
