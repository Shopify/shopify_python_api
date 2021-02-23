import shopify
import json
from test.test_helper import TestCase


class CollectionPublicationTest(TestCase):
    def test_find_all_collection_publications(self):
        self.fake(
            'publications/55650051/collection_publications',
            method='GET',
            body=self.load_fixture('collection_publications')
        )
        collection_publications = shopify.CollectionPublication.find(publication_id=55650051)

        self.assertEqual(96062799894, collection_publications[0].id)
        self.assertEqual(60941828118, collection_publications[0].collection_id)

    def test_find_collection_publication(self):
        self.fake(
            'publications/55650051/collection_publications/96062799894',
            method='GET',
            body=self.load_fixture('collection_publication'),
            code=200
        )
        collection_publication = shopify.CollectionPublication.find(96062799894, publication_id=55650051)

        self.assertEqual(96062799894, collection_publication.id)
        self.assertEqual(60941828118, collection_publication.collection_id)

    def test_create_collection_publication(self):
        self.fake(
            'publications/55650051/collection_publications',
            method='POST',
            headers={'Content-type': 'application/json'},
            body=self.load_fixture('collection_publication'),
            code=201
        )

        collection_publication = shopify.CollectionPublication.create({
            'publication_id': 55650051,
            'published_at': "2018-01-29T14:06:08-05:00",
            'published': True,
            'collection_id': 60941828118
        })

        expected_body = {
            'collection_publication': {
                'published_at': "2018-01-29T14:06:08-05:00",
                'published': True,
                'collection_id': 60941828118,
            }
        }

        self.assertEqual(expected_body, json.loads(self.http.request.data.decode("utf-8")))

    def test_destroy_collection_publication(self):
        self.fake(
            'publications/55650051/collection_publications/96062799894',
            method='GET',
            body=self.load_fixture('collection_publication'),
            code=200
        )
        collection_publication = shopify.CollectionPublication.find(96062799894, publication_id=55650051)

        self.fake(
            'publications/55650051/collection_publications/96062799894',
            method='DELETE',
            body='{}',
            code=200
        )
        collection_publication.destroy()

        self.assertEqual('DELETE', self.http.request.get_method())
