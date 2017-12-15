import shopify
from shopify.resources.marketing_event_engagement import MarketingEventEngagement
from test.test_helper import TestCase


class MarketingEventsTest(TestCase):
    def setUp(self):
        super(MarketingEventsTest, self).setUp()
        self.fake("marketing_events/998730532", method="GET", body=self.load_fixture('marketing_event'))
        self.event = shopify.MarketingEvent.find(998730532)
        self.assertEqual(998730532, self.event.id)

    def test_fetch_marketing_events(self):
        self.fake("marketing_events", method="GET", body=self.load_fixture('marketing_events'))
        events = shopify.MarketingEvent.find()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].id, 998730532)
        self.assertEqual(events[1].id, 998730542)

    def test_fetch_marketing_events_count(self):
        self.fake("marketing_events/count", method="GET", body=self.load_fixture('marketing_events_count'))
        count = shopify.MarketingEvent.count()
        self.assertEqual(count, 2)

    def test_fetch_marketing_event_engagements(self):
        self.fake("marketing_events/998730532/engagements", method="POST", code=201,
                  body=self.load_fixture('marketing_event_engagements'), headers=({'Content-type': 'application/json'}))
        new_engagements = self.event.engagements({
            "occurred_on": "2017-01-15",
            "views_count": 0,
            "clicks_count": 0,
            "favorites_count": 0,
            "ad_spend": 10.0,
            "is_cumulative": True
        })
        self.assertEqual(len(new_engagements), 1)
        self.assertEqual(type(new_engagements[0]), MarketingEventEngagement)
        self.assertEqual(new_engagements[0].occurred_on, "2017-01-15")
        self.assertEqual(new_engagements[0].ad_spend, "10.00")
