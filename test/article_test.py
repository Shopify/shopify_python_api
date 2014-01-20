import shopify
from test_helper import TestCase

class ArticleTest(TestCase):

    def test_create_article(self):
        self.fake("blogs/1008414260/articles", method='POST', body=self.load_fixture('article'), headers={'Content-type': 'application/json'})
        article = shopify.Article({'blog_id':1008414260})
        article.save()
        self.assertEqual("First Post", article.title)

    def test_get_article(self):
        self.fake('articles/6242736', method='GET', body=self.load_fixture('article'))
        article = shopify.Article.find(6242736)
        self.assertEqual("First Post", article.title)

    def test_get_articles(self):
        self.fake("articles", method='GET', body=self.load_fixture('articles'))
        articles = shopify.Article.find()
        self.assertEqual(3, len(articles))

    def test_get_articles_namespaced(self):
        self.fake("blogs/1008414260/articles", method='GET', body=self.load_fixture('articles'))
        articles = shopify.Article.find(blog_id=1008414260)
        self.assertEqual(3, len(articles))

    def test_get_article_namespaced(self):
        self.fake("blogs/1008414260/articles/6242736", method='GET', body=self.load_fixture('article'))
        article = shopify.Article.find(6242736, blog_id=1008414260)
        self.assertEqual("First Post", article.title)

    def test_get_authors(self):
        self.fake("articles/authors", method='GET', body=self.load_fixture('authors'))
        authors = shopify.Article.authors()
        self.assertEqual("Shopify", authors[0])
        self.assertEqual("development shop", authors[-1])

    def test_get_authors_for_blog_id(self):
        self.fake("blogs/1008414260/articles/authors", method='GET', body=self.load_fixture('authors'))
        authors = shopify.Article.authors(blog_id=1008414260)
        self.assertEqual(3, len(authors))

    def test_get_tags(self):
        self.fake("articles/tags", method='GET', body=self.load_fixture('tags'))
        tags = shopify.Article.tags()
        self.assertEqual("consequuntur", tags[0])
        self.assertEqual("repellendus", tags[-1])

    def test_get_tags_for_blog_id(self):
        self.fake("blogs/1008414260/articles/tags", method='GET', body=self.load_fixture('tags'))
        tags = shopify.Article.tags(blog_id=1008414260)
        self.assertEqual("consequuntur", tags[0])
        self.assertEqual("repellendus", tags[-1])

    def test_get_popular_tags(self):
        self.fake("articles/tags.json?limit=1&popular=1", extension=False, method='GET', body=self.load_fixture('tags'))
        tags = shopify.Article.tags(popular=1, limit=1)
        self.assertEqual(3, len(tags))
