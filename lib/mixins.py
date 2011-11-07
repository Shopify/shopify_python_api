import shopify.resources

class Countable(object):
    @classmethod
    def count(cls, _options=None, **kwargs):
        if _options is None:
            _options = kwargs
        return int(cls.get("count", **_options))


class Metafields(object):
    def metafields(self):
        return shopify.resources.Metafield.find(resource=self.__class__.plural, resource_id=self.id)

    def add_metafield(self, metafield):
        if self.is_new():
            raise ValueError("You can only add metafields to a resource that has been saved")

        metafield._prefix_options = dict(resource=self.__class__.plural, resource_id=self.id)
        metafield.save()
        return metafield


class Events(object):
    def events(self):
        return shopify.resources.Event.find(resource=self.__class__.plural, resource_id=self.id)
