import shopify
from six.moves import urllib
import json


class GraphQL:
    def __init__(self):
        self.endpoint = shopify.ShopifyResource.get_site() + "/graphql.json"
        self.headers = shopify.ShopifyResource.get_headers()

    def merge_headers(self, *headers):
        merged_headers = {}
        for header in headers:
            merged_headers.update(header)
        return merged_headers

    def execute(self, query, variables=None, operation_name=None):
        default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers = self.merge_headers(default_headers, self.headers)
        data = {"query": query, "variables": variables, "operationName": operation_name}

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode("utf-8"), headers)

        response = urllib.request.urlopen(req)
        return response.read().decode("utf-8")
