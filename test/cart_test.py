import shopify
from test_helper import TestCase

class CartTest(TestCase):
  
  def test_all_should_return_all_carts(self):
    self.fake('carts')
    carts = shopify.Cart.find()
    self.assertEqual(2, len(carts))
    self.assertEqual(2, carts[0].id)
    self.assertEqual("3eed8183d4281db6ea82ee2b8f23e9cc", carts[0].token)
    self.assertEqual(1, len(carts[0].line_items))
    self.assertEqual('test', carts[0].line_items[0].title)
