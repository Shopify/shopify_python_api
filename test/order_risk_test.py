import shopify
from test.test_helper import TestCase

class OrderRiskTest(TestCase):

  def test_create_order_risk(self):
    self.fake("orders/450789469/risks", method='POST', body= self.load_fixture('order_risk'), headers={'Content-type': 'application/json'})
    v = shopify.OrderRisk({'order_id':450789469})
    v.message = "This order was placed from a proxy IP"
    v.recommendation = "cancel"
    v.score = "1.0"
    v.source = "External"
    v.merchant_message = "This order was placed from a proxy IP"
    v.display = True
    v.cause_cancel = True
    v.save()

    self.assertEqual(284138680, v.id)

  def test_get_order_risks(self):
    self.fake("orders/450789469/risks", method='GET', body= self.load_fixture('order_risks'))
    v = shopify.OrderRisk.find(order_id=450789469)
    self.assertEqual(2, len(v))

  def test_get_order_risk(self):
    self.fake("orders/450789469/risks/284138680", method='GET', body= self.load_fixture('order_risk'))
    v = shopify.OrderRisk.find(284138680, order_id=450789469)
    self.assertEqual(284138680, v.id)

  def test_delete_order_risk(self):
    self.fake("orders/450789469/risks/284138680", method='GET', body= self.load_fixture('order_risk'))
    self.fake("orders/450789469/risks/284138680", method='DELETE', body="destroyed")
    v = shopify.OrderRisk.find(284138680, order_id=450789469)
    v.destroy()

  def test_delete_order_risk(self):
    self.fake("orders/450789469/risks/284138680", method='GET', body= self.load_fixture('order_risk'))
    self.fake("orders/450789469/risks/284138680", method='PUT', body= self.load_fixture('order_risk'), headers={'Content-type': 'application/json'})

    v = shopify.OrderRisk.find(284138680, order_id=450789469)
    v.position = 3
    v.save()
