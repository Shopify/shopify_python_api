from ..base import ShopifyResource
import base64


class Asset(ShopifyResource):
    _primary_key = "key"
    _prefix_source = "/themes/$theme_id/"

    @classmethod
    def _prefix(cls, options={}):
        theme_id = options.get("theme_id")
        if theme_id:
            return "%s/themes/%s" % (cls.site, theme_id)
        else:
            return cls.site

    @classmethod
    def _element_path(cls, id, prefix_options={}, query_options=None):
        if query_options is None:
            prefix_options, query_options = cls._split_options(prefix_options)
        return "%s%s.%s%s" % (cls._prefix(prefix_options)+'/', cls.plural,
                              cls.format.extension, cls._query_string(query_options))

    @classmethod
    def find(cls, key=None, **kwargs):
        """
        Find an asset by key
        E.g.
            shopify.Asset.find('layout/theme.liquid', theme_id=99)
        """
        if not key:
            return super(Asset, cls).find(**kwargs)

        params = {"asset[key]": key}
        params.update(kwargs)
        theme_id = params.get("theme_id")
        path_prefix = "%s/themes/%s" % (cls.site, theme_id) if theme_id else cls.site

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
            return base64.b64decode(data).decode()

    def __set_value(self, data):
        self.__wipe_value_attributes()
        self.attributes["value"] = data

    value = property(__get_value, __set_value, None, "The asset's value or attachment")

    def attach(self, data):
        self.attachment = base64.b64encode(data).decode()

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
            if attr in self.attributes:
                del self.attributes[attr]
