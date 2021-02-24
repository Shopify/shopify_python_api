import json
import shopify
from test.test_helper import TestCase


class ResourceFeedbackTest(TestCase):
    def test_get_resource_feedback(self):
        body = json.dumps({'resource_feedback': [{'resource_type': 'Shop'}]})
        self.fake('resource_feedback', method='GET', body=body)

        feedback = shopify.ResourceFeedback.find()

        self.assertEqual('Shop', feedback[0].resource_type)

    def test_save_with_resource_feedback_endpoint(self):
        body = json.dumps({'resource_feedback': {}})
        self.fake('resource_feedback', method='POST', body=body, headers={'Content-Type': 'application/json'})

        shopify.ResourceFeedback().save()

        self.assertEqual(body, self.http.request.data.decode("utf-8"))

    def test_get_resource_feedback_with_product_id(self):
        body = json.dumps({'resource_feedback': [{'resource_type': 'Product'}]})
        self.fake('products/42/resource_feedback', method='GET', body=body)

        feedback = shopify.ResourceFeedback.find(product_id=42)

        self.assertEqual('Product', feedback[0].resource_type)

    def test_save_with_product_id_resource_feedback_endpoint(self):
        body = json.dumps({'resource_feedback': {}})
        self.fake(
            'products/42/resource_feedback', method='POST', body=body, headers={'Content-Type': 'application/json'}
        )

        feedback = shopify.ResourceFeedback({'product_id': 42})
        feedback.save()

        self.assertEqual(body, self.http.request.data.decode("utf-8"))
