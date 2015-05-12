import shopify
from test.test_helper import TestCase

class GiftCardTest(TestCase):

    def test_gift_card_creation(self):
        self.fake('gift_cards', method='POST', code=202, body=self.load_fixture('gift_card'), headers={'Content-type': 'application/json'})
        gift_card = shopify.GiftCard.create({'code': 'd7a2bcggda89c293', 'note': "Gift card note."})
        self.assertEqual("Gift card note.", gift_card.note)
        self.assertEqual("c293", gift_card.last_characters)

    def test_fetch_gift_cards(self):
        self.fake('gift_cards', method='GET', code=200, body=self.load_fixture('gift_cards'))
        gift_cards = shopify.GiftCard.find()
        self.assertEqual(1, len(gift_cards))

    def test_disable_gift_card(self):
        self.fake('gift_cards/4208208', method='GET', code=200, body=self.load_fixture('gift_card'))
        self.fake('gift_cards/4208208/disable', method='POST', code=200, body=self.load_fixture('gift_card_disabled'), headers={'Content-length': '0', 'Content-type': 'application/json'})
        gift_card = shopify.GiftCard.find(4208208)
        self.assertFalse(gift_card.disabled_at)
        gift_card.disable()
        self.assertTrue(gift_card.disabled_at)
