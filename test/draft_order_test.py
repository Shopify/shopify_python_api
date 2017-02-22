import shopify
from test.test_helper import TestCase
import json


class DraftOrderTest(TestCase):
    def setUp(self):
        super(DraftOrderTest, self).setUp()
        self.fake('draft_orders/517119332', body=self.load_fixture('draft_order'))
        self.draft_order = shopify.DraftOrder.find(517119332)

    def test_get_draft_order(self):
        self.fake('draft_orders/517119332', method='GET', status=200, body=self.load_fixture('draft_order'))
        draft_order = shopify.DraftOrder.find(517119332)
        self.assertEqual(517119332, draft_order.id)

    def test_get_all_draft_orders(self):
        self.fake('draft_orders', method='GET', status=200, body=self.load_fixture('draft_orders'))
        draft_orders = shopify.DraftOrder.find()
        self.assertEqual(1, len(draft_orders))
        self.assertEqual(517119332, draft_orders[0].id)

    def test_get_count_draft_orders(self):
        self.fake('draft_orders/count', method='GET', status=200, body='{"count": 16}')
        draft_orders_count = shopify.DraftOrder.count()
        self.assertEqual(16, draft_orders_count)

    def test_create_draft_order(self):
        self.fake('draft_orders', method='POST', status=201, body=self.load_fixture('draft_order'), headers={'Content-type': 'application/json'})
        draft_order = shopify.DraftOrder.create({"line_items": [{ "quantity": 1, "variant_id": 39072856 }]})
        self.assertEqual(json.loads('{"draft_order": {"line_items": [{"quantity": 1, "variant_id": 39072856}]}}'), json.loads(self.http.request.data.decode("utf-8")))

    def test_create_draft_order_202(self):
        self.fake('draft_orders', method='POST', status=202, body=self.load_fixture('draft_order'), headers={'Content-type': 'application/json'})
        draft_order = shopify.DraftOrder.create({"line_items": [{ "quantity": 1, "variant_id": 39072856 }]})
        self.assertEqual(39072856, draft_order.line_items[0].variant_id)

    def test_update_draft_order(self):
        self.draft_order.note = 'Test new note'
        self.fake('draft_orders/517119332', method='PUT', status=200, body=self.load_fixture('draft_order'), headers={'Content-type': 'application/json'})
        self.draft_order.save()
        self.assertEqual('Test new note', json.loads(self.http.request.data.decode("utf-8"))['draft_order']['note'])

    def test_send_invoice_with_no_params(self):
        draft_order_invoice_fixture = self.load_fixture('draft_order_invoice')
        draft_order_invoice = json.loads(draft_order_invoice_fixture.decode("utf-8"))
        self.fake('draft_orders/517119332/send_invoice', method='POST', body=draft_order_invoice_fixture, headers={'Content-type': 'application/json'})
        draft_order_invoice_response = self.draft_order.send_invoice()
        self.assertEqual(json.loads('{"draft_order_invoice": {}}'), json.loads(self.http.request.data.decode("utf-8")))
        self.assertIsInstance(draft_order_invoice_response, shopify.DraftOrderInvoice)
        self.assertEqual(draft_order_invoice['draft_order_invoice']['to'], draft_order_invoice_response.to)

    def test_send_invoice_with_params(self):
        draft_order_invoice_fixture = self.load_fixture('draft_order_invoice')
        draft_order_invoice = json.loads(draft_order_invoice_fixture.decode("utf-8"))
        self.fake('draft_orders/517119332/send_invoice', method='POST', body=draft_order_invoice_fixture, headers={'Content-type': 'application/json'})
        draft_order_invoice_response = self.draft_order.send_invoice(shopify.DraftOrderInvoice(draft_order_invoice['draft_order_invoice']))
        self.assertEqual(draft_order_invoice, json.loads(self.http.request.data.decode("utf-8")))
        self.assertIsInstance(draft_order_invoice_response, shopify.DraftOrderInvoice)
        self.assertEqual(draft_order_invoice['draft_order_invoice']['to'], draft_order_invoice_response.to)

    def test_delete_draft_order(self):
        self.fake('draft_orders/517119332', method='DELETE', body='destroyed')
        self.draft_order.destroy()
        self.assertEqual('DELETE', self.http.request.get_method())

    def test_add_metafields_to_draft_order(self):
        self.fake('draft_orders/517119332/metafields', method='POST', status=201, body=self.load_fixture('metafield'), headers={'Content-type': 'application/json'})
        field = self.draft_order.add_metafield(shopify.Metafield({'namespace': 'contact', 'key': 'email', 'value': '123@example.com', 'value_type': 'string'}))
        self.assertEqual(json.loads('{"metafield":{"namespace":"contact","key":"email","value":"123@example.com","value_type":"string"}}'), json.loads(self.http.request.data.decode("utf-8")))
        self.assertFalse (field.is_new())
        self.assertEqual('contact', field.namespace)
        self.assertEqual('email', field.key)
        self.assertEqual('123@example.com', field.value)

    def test_get_metafields_for_draft_order(self):
        self.fake('draft_orders/517119332/metafields', body=self.load_fixture('metafields'))
        metafields = self.draft_order.metafields()
        self.assertEqual(2, len(metafields))
        self.assertIsInstance(metafields[0], shopify.Metafield)
        self.assertIsInstance(metafields[1], shopify.Metafield)
