from ..base import ShopifyResource
from shopify import mixins

class Blog(ShopifyResource, mixins.Metafields, mixins.Events):

    def articles(self):
        return Article.find(blog_id=self.id)
