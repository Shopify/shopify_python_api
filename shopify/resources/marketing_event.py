import json

from shopify.resources.marketing_event_engagement import MarketingEventEngagement
from ..base import ShopifyResource


class MarketingEvent(ShopifyResource):
    def engagements(self, *engagements):
        resource = self.post("engagements", body=json.dumps(dict(engagements=engagements)).encode('utf8'))
        return [MarketingEventEngagement(item) for item in MarketingEventEngagement.format.decode(resource.body)]
