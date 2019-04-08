import json

from ..base import ShopifyResource


class Refund(ShopifyResource):
    _prefix_source = "/orders/$order_id/"

    @classmethod
    def calculate(cls, order_id, shipping=None, refund_line_items=None):
        """
        Calculates refund transactions based on line items and shipping.
        When you want to create a refund, you should first use the calculate
        endpoint to generate accurate refund transactions.

        Args:
           order_id: Order ID for which the Refund has to created.
           shipping: Specify how much shipping to refund.
           refund_line_items: A list of line item IDs and quantities to refund.
        Returns:
           Unsaved refund record
        """
        data = {}
        if shipping:
            data['shipping'] = shipping
        data['refund_line_items'] = refund_line_items or []
        body = {'refund': data}
        resource = cls.post(
            "calculate", order_id=order_id, body=json.dumps(body).encode()
        )
        return cls(
            cls.format.decode(resource.body),
            prefix_options={'order_id': order_id}
        )
