import shopify
from test_helper import TestCase

class BlogTest(TestCase):
    
    def test_blog_creation(self):
        self.fake('blogs', method='POST', code=202, body=self.load_fixture('blog'), headers={'Content-type': 'application/json'})
        blog = shopify.Blog.create({'title': "Test Blog"})
        self.assertEqual("Test Blog", blog.title)
