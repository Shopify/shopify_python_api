from ..base import ShopifyResource


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
