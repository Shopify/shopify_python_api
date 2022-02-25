import shopify
import json
from test.test_helper import TestCase


class GraphQLTest(TestCase):
    def setUp(self):
        super(GraphQLTest, self).setUp()
        shopify.ApiVersion.define_known_versions()
        shopify_session = shopify.Session("this-is-my-test-show.myshopify.com", "unstable", "token")
        shopify.ShopifyResource.activate_session(shopify_session)
        self.client = shopify.GraphQL()
        self.fake(
            "graphql",
            method="POST",
            code=201,
            headers={
                "X-Shopify-Access-Token": "token",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    def test_fetch_shop_with_graphql(self):
        query = """
            {
                shop {
                    name
                    id
                }
            }
        """
        result = self.client.execute(query)
        self.assertTrue(json.loads(result)["shop"]["name"] == "Apple Computers")

    def test_specify_operation_name(self):
        query = """
            query GetShop{
                shop {
                    name
                    id
                }
            }
        """
        result = self.client.execute(query, operation_name="GetShop")
        self.assertTrue(json.loads(result)["shop"]["name"] == "Apple Computers")
