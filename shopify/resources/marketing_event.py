import json
from ..base import ShopifyResource


class MarketingEvent(ShopifyResource):
    def add_engagements(self, engagements):
        engagements_json = json.dumps({"engagements": engagements})
        return self.post("engagements", engagements_json.encode())
