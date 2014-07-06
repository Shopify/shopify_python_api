import shopify
from test.test_helper import TestCase

class AssetTest(TestCase):

    def test_get_assets(self):
        self.fake("assets", method='GET', body=self.load_fixture('assets'))
        v = shopify.Asset.find()

    def test_get_asset(self):
        self.fake("assets.json?asset%5Bkey%5D=templates%2Findex.liquid", extension=False, method='GET', body=self.load_fixture('asset'))
        v = shopify.Asset.find('templates/index.liquid')

    def test_update_asset(self):
        self.fake("assets.json?asset%5Bkey%5D=templates%2Findex.liquid", extension=False, method='GET', body=self.load_fixture('asset'))
        v = shopify.Asset.find('templates/index.liquid')

        self.fake("assets", method='PUT', body=self.load_fixture('asset'), headers={'Content-type': 'application/json'})
        v.save()

    def test_get_assets_namespaced(self):
        self.fake("themes/1/assets", method='GET', body=self.load_fixture('assets'))
        v = shopify.Asset.find(theme_id = 1)

    def test_get_asset_namespaced(self):
        self.fake("themes/1/assets.json?asset%5Bkey%5D=templates%2Findex.liquid&theme_id=1", extension=False, method='GET', body=self.load_fixture('asset'))
        v = shopify.Asset.find('templates/index.liquid', theme_id=1)

    def test_update_asset_namespaced(self):
        self.fake("themes/1/assets.json?asset%5Bkey%5D=templates%2Findex.liquid&theme_id=1", extension=False, method='GET', body=self.load_fixture('asset'))
        v = shopify.Asset.find('templates/index.liquid', theme_id=1)

        self.fake("themes/1/assets", method='PUT', body=self.load_fixture('asset'), headers={'Content-type': 'application/json'})
        v.save()

    def test_delete_asset_namespaced(self):
        self.fake("themes/1/assets.json?asset%5Bkey%5D=templates%2Findex.liquid&theme_id=1", extension=False, method='GET', body=self.load_fixture('asset'))
        v = shopify.Asset.find('templates/index.liquid', theme_id=1)

        self.fake("themes/1/assets.json?asset%5Bkey%5D=templates%2Findex.liquid", extension=False, method='DELETE', body="{}")
        v.destroy()
