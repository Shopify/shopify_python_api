from ..base import ShopifyResource
from .metafield import Metafield
from .event import Event


class Shop(ShopifyResource):
    @classmethod
    def current(cls):
        return cls.find_one(cls.site + "/shop." + cls.format.extension)

    def metafields(self):
        return Metafield.find()

    def add_metafield(self, metafield):
        if self.is_new():
            raise ValueError("You can only add metafields to a resource that has been saved")
        metafield.save()
        return metafield

    def events(self):
        return Event.find()
