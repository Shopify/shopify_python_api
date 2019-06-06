from ..base import ShopifyResource
from graphqlclient import GraphQLClient
import ast

class GraphQL(ShopifyResource):

    @classmethod
    def execute(cls, query):
        client = GraphQLClient(cls.site + "/graphql.json")
        client.inject_token(
            cls.headers['X-Shopify-Access-Token'], 
            'X-Shopify-Access-Token'
        )
        result = client.execute(query)
        return ast.literal_eval(result)