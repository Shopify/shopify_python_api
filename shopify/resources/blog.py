from ..base import ShopifyResource
import shopify.mixins as mixins

class Blog(ShopifyResource, mixins.Metafields, mixins.Events):
    def articles(self):
        return Article.find(blog_id=self.id)
