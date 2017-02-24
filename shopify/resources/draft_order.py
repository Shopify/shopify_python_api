from ..base import ShopifyResource
from shopify import mixins
from .draft_order_invoice import DraftOrderInvoice


class DraftOrder(ShopifyResource, mixins.Metafields):
    def send_invoice(self, draft_order_invoice = DraftOrderInvoice()):
        resource = self.post("send_invoice", draft_order_invoice.encode())
        return DraftOrderInvoice(DraftOrder.format.decode(resource.body))

    def complete(self, params = {}):
        if params.get('payment_pending', False):
          self._load_attributes_from_response(self.put("complete", payment_pending='true'))
        else:
          self._load_attributes_from_response(self.put("complete"))
