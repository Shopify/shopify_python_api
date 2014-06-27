from ..base import ShopifyResource
from shopify import mixins
from .comment import Comment


class Article(ShopifyResource, mixins.Metafields, mixins.Events):
    _prefix_source = "/admin/blogs/$blog_id/"

    @classmethod
    def _prefix(cls, options={}):
        blog_id = options.get("blog_id")
        if blog_id:
            return "/admin/blogs/%s" % (blog_id)
        else:
            return "/admin"

    def comments(self):
        return Comment.find(article_id=self.id)

    @classmethod
    def authors(cls, **kwargs):
        return cls.get('authors', **kwargs)

    @classmethod
    def tags(cls, **kwargs):
        return cls.get('tags', **kwargs)
