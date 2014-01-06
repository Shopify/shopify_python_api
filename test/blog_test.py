from test_helper import *

class BlogTest(TestCase):
    
    def test_blog_creation(self):
        self.fake('blogs', method = 'POST', code = 202, body = self.load_fixture('blog'))
        blog = shopify.Blog.create({'title': "Test Blog"})
        self.assertEqual("Test Blog", blog.title)
