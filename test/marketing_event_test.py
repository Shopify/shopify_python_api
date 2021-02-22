import shopify
import json
from test.test_helper import TestCase


class MarketingEventTest(TestCase):
    def setUp(self):
        super(MarketingEventTest, self).setUp()

    def test_get_marketing_event(self):
        self.fake('marketing_events/1', method='GET', body=self.load_fixture('marketing_event'))
        marketing_event = shopify.MarketingEvent.find(1)
        self.assertEqual(marketing_event.id, 1)

    def test_get_marketing_events(self):
        self.fake('marketing_events', method='GET', body=self.load_fixture('marketing_events'))
        marketing_events = shopify.MarketingEvent.find()
        self.assertEqual(len(marketing_events), 2)

    def test_create_marketing_event(self):
        self.fake('marketing_events', method='POST', body=self.load_fixture(
            'marketing_event'), headers={'Content-type': 'application/json'})

        marketing_event = shopify.MarketingEvent()
        marketing_event.currency_code = 'GBP'
        marketing_event.event_target = 'facebook'
        marketing_event.event_type = 'post'
        marketing_event.save()

        self.assertEqual(marketing_event.event_target, 'facebook')
        self.assertEqual(marketing_event.currency_code, 'GBP')
        self.assertEqual(marketing_event.event_type, 'post')

    def test_delete_marketing_event(self):
        self.fake('marketing_events/1', method='GET', body=self.load_fixture('marketing_event'))
        self.fake('marketing_events/1', method='DELETE', body='destroyed')

        marketing_event = shopify.MarketingEvent.find(1)
        marketing_event.destroy()

        self.assertEqual('DELETE', self.http.request.get_method())

    def test_update_marketing_event(self):
        self.fake('marketing_events/1', method='GET', code=200, body=self.load_fixture('marketing_event'))
        self.fake('marketing_events/1', method='PUT', code=200,
                  body=self.load_fixture('marketing_event'), headers={'Content-type': 'application/json'})

        marketing_event = shopify.MarketingEvent.find(1)
        marketing_event.currency = 'USD'

        self.assertTrue(marketing_event.save())

    def test_count_marketing_events(self):
        self.fake('marketing_events/count', method='GET', body='{"count": 2}')
        marketing_events_count = shopify.MarketingEvent.count()
        self.assertEqual(marketing_events_count, 2)

    def test_add_engagements(self):
        self.fake('marketing_events/1', method='GET', body=self.load_fixture('marketing_event'))
        self.fake(
            'marketing_events/1/engagements',
            method='POST',
            code=201,
            body=self.load_fixture('engagement'),
            headers={'Content-type': 'application/json'}
        )

        marketing_event = shopify.MarketingEvent.find(1)
        response = marketing_event.add_engagements([{
            'occurred_on': '2017-04-20',
            'impressions_count': None,
            'views_count': None,
            'clicks_count': 10,
            'shares_count': None,
            'favorites_count': None,
            'comments_count': None,
            'ad_spend': None,
            'is_cumulative': True
        }])

        request_data = json.loads(self.http.request.data.decode("utf-8"))['engagements']
        self.assertEqual(len(request_data), 1)
        self.assertEqual(request_data[0]['occurred_on'], '2017-04-20')

        response_data = json.loads(response.body.decode("utf-8"))['engagements']
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['occurred_on'], '2017-04-20')
