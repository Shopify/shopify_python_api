import shopify
from test.test_helper import TestCase

class PublicationTest(TestCase):
    def test_find_all_publications(self):
        self.fake('publications')
        publications = shopify.Publication.find()

        self.assertEqual(55650051, publications[0].id)
        self.assertEqual("Buy Button", publications[0].name)
