from test_helper import *

class AssetTest(TestCase):
  def test_get_assetss(self):
    self.fake("themes/1//assets", method = 'GET', body = self.load_fixture('assets'))
    v = shopify.Asset.find(theme_id = 1)

  def test_get_asset_namespaced(self):
    self.fake("themes/1/assets.json?asset%5Bkey%5D=templates%2Findex.liquid&theme_id=1", extension = False, method = 'GET', body = self.load_fixture('asset'))
    v = shopify.Asset.find('templates/index.liquid', theme_id = 1)

  def test_get_asset(self):
    self.fake("assets.json?asset%5Bkey%5D=templates%2Findex.liquid", extension = False, method = 'GET', body = self.load_fixture('asset'))
    v = shopify.Asset.find('templates/index.liquid')
