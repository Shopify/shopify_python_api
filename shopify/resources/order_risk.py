from ..base import ShopifyResource

class OrderRisk(ShopifyResource):
  _prefix_source = "/admin/orders/$order_id/"
  _plural = "risks"
