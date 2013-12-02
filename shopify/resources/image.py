from ..base import ShopifyResource
import base64
import re

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