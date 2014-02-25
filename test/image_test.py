import shopify
from test_helper import TestCase

class ImageTest(TestCase):

  def test_create_image(self):
    self.fake("products/632910392/images", method='POST', body=self.load_fixture('image'), headers={'Content-type': 'application/json'})
    image = shopify.Image({'product_id':632910392})
    image.position = 1
    image.attachment = "R0lGODlhbgCMAPf/APbr48VySrxTO7IgKt2qmKQdJeK8lsFjROG5p/nz7Zg3MNmnd7Q1MLNVS9GId71hSJMZIuzTu4UtKbeEeakhKMl8U8WYjfr18YQaIbAf=="
    image.save()

    self.assertEqual('http://cdn.shopify.com/s/files/1/0006/9093/3842/products/ipod-nano.png?v=1389388540', image.src)
    self.assertEqual(850703190, image.id)

  def test_get_images(self):
    self.fake("products/632910392/images", method='GET', body=self.load_fixture('images'))
    image = shopify.Image.find(product_id=632910392)
    self.assertEqual(2, len(image))

  def test_get_image(self):
    self.fake("products/632910392/images/850703190", method='GET', body=self.load_fixture('image'))
    image = shopify.Image.find(850703190, product_id=632910392)
    self.assertEqual(850703190, image.id)
