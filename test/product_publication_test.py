import shopify
import json
from test.test_helper import TestCase


class ProductPublicationTest(TestCase):
    def test_find_all_product_publications(self):
        self.fake(
            'publications/55650051/product_publications',
            method='GET',
            body=self.load_fixture('product_publications')
        )
        product_publications = shopify.ProductPublication.find(publication_id=55650051)

        self.assertEqual(647162527768, product_publications[0].id)
        self.assertEqual(8267093571, product_publications[0].product_id)

    def test_find_product_publication(self):
        self.fake(
            'publications/55650051/product_publications/647162527768',
            method='GET',
            body=self.load_fixture('product_publication'),
            code=200
        )
        product_publication = shopify.ProductPublication.find(647162527768, publication_id=55650051)

        self.assertEqual(647162527768, product_publication.id)
        self.assertEqual(8267093571, product_publication.product_id)

    def test_create_product_publication(self):
        self.fake(
            'publications/55650051/product_publications',
            method='POST',
            headers={'Content-type': 'application/json'},
            body=self.load_fixture('product_publication'),
            code=201
        )

        product_publication = shopify.ProductPublication.create({
            'publication_id': 55650051,
            'published_at': "2018-01-29T14:06:08-05:00",
            'published': True,
            'product_id': 8267093571
        })

        expected_body = {
            'product_publication': {
                'published_at': "2018-01-29T14:06:08-05:00",
                'published': True,
                'product_id': 8267093571,
            }
        }

        self.assertEqual(expected_body, json.loads(self.http.request.data.decode("utf-8")))

    def test_destroy_product_publication(self):
        self.fake(
            'publications/55650051/product_publications/647162527768',
            method='GET',
            body=self.load_fixture('product_publication'),
            code=200
        )
        product_publication = shopify.ProductPublication.find(647162527768, publication_id=55650051)

        self.fake(
            'publications/55650051/product_publications/647162527768',
            method='DELETE',
            body='{}',
            code=200
        )
        product_publication.destroy()

        self.assertEqual('DELETE', self.http.request.get_method())
