class Countable(object):
    @classmethod
    def count(cls, options={}):
        return int(cls.get("count", **options))


class Metafields(object):
    def metafields(self):
        return Metafield.find(resource=self.__class__.plural, resource_id=self.id)

    def add_metafield(self, metafield):
        if self.is_new():
            raise ValueError("You can only add metafields to a resource that has been saved")

        metafield._prefix_options = dict(resource=self.__class__.plural, resource_id=self.id)
        metafield.save()
        return metafield


class Events(object):
    def events(self):
        return Event.find(resource=self.__class__.plural, resource_id=self.id)
