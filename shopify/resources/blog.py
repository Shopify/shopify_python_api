from ..base import ShopifyResource
from shopify import mixins
from article import Article


class Blog(ShopifyResource, mixins.Metafields, mixins.Events):

    def articles(self):
        return Article.find(blog_id=self.id)
