from ..base import ShopifyResource
import shopify.mixins as mixins

class Article(ShopifyResource, mixins.Metafields, mixins.Events):
    _prefix_source = "/admin/blogs/$blog_id/"

    @classmethod
    def _prefix(cls, options={}):
        blog_id = options.get("blog_id")
        return "/admin/" if blog_id is None else "/admin/blogs/%s" % (blog_id)

    def comments(self):
        return Comment.find(article_id=self.id)