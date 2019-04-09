from ..base import ShopifyResource
from shopify import mixins
from .comment import Comment


class Article(ShopifyResource, mixins.Metafields, mixins.Events):
    _prefix_source = "/blogs/$blog_id/"

    @classmethod
    def _prefix(cls, options={}):
        blog_id = options.get("blog_id")
        if blog_id:
            return "%s/blogs/%s" % (cls.site, blog_id)
        else:
            return cls.site

    def comments(self):
        return Comment.find(article_id=self.id)

    @classmethod
    def authors(cls, **kwargs):
        return cls.get('authors', **kwargs)

    @classmethod
    def tags(cls, **kwargs):
        return cls.get('tags', **kwargs)
