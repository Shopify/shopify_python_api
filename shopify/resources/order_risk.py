from ..base import ShopifyResource

class OrderRisk(ShopifyResource):
  _prefix_source = "/admin/orders/$order_id/"
  _singular = "risk"
  _plural = "risks"
