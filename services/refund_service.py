from datetime import datetime
from data.orders import ORDERS
from data.returns import RETURNS
from data.refunds import REFUNDS


class RefundService:

    DATE_FORMAT = "%Y-%m-%d"

    def get_order(self, order_id: str):
        """
        Retrieve an order by its ID.
        """
        return ORDERS.get(order_id)

    def get_return_by_order(self, order_id: str):
        """
        Retrieve the return associated with an order.
        """
        for return_record in RETURNS.values():
            if return_record["order_id"] == order_id:
                return return_record

        return None

    def get_refund_by_order(self, order_id: str):
        """
        Retrieve the refund associated with an order.
        """
        for refund in REFUNDS.values():
            if refund["order_id"] == order_id:
                return refund

        return None

    def check_refund_eligibility(self, order_id: str) -> dict:
        """
        Check whether a refund can be initiated.
        """

        order = self.get_order(order_id)

        if order is None:
            return {
                "eligible": False,
                "reason": "Order not found."
            }

        return_record = self.get_return_by_order(order_id)

        if return_record is None:
            return {
                "eligible": False,
                "reason": "No return request exists for this order."
            }

        if return_record["status"] != "Completed":
            return {
                "eligible": False,
                "reason": "Refund can only be initiated after the return is completed."
            }

        existing_refund = self.get_refund_by_order(order_id)

        if existing_refund:
            return {
                "eligible": False,
                "reason": "A refund has already been initiated for this order."
            }

        return {
            "eligible": True,
            "reason": "Order is eligible for refund."
        }

    def get_refund_summary(self, order_id: str) -> dict:
        """
        Retrieve refund information for an order.
        """

        order = self.get_order(order_id)

        if order is None:
            return {
                "success": False,
                "message": "Order not found."
            }

        refund = self.get_refund_by_order(order_id)

        eligibility = self.check_refund_eligibility(order_id)

        return {
            "success": True,
            "order_id": order_id,
            "refund": refund,
            "eligibility": eligibility
        }

    def generate_refund_id(self):

        if not REFUNDS:
            return "REF3001"

        max_id = max(
            int(refund_id.replace("REF", ""))
            for refund_id in REFUNDS.keys()
        )

        return f"REF{max_id + 1}"

    def initiate_refund(self, order_id: str) -> dict:
        """
        Initiate a refund for an eligible order.
        """

        eligibility = self.check_refund_eligibility(order_id)

        if not eligibility["eligible"]:
            return {
                "success": False,
                "message": eligibility["reason"]
            }

        order = self.get_order(order_id)

        refund_id = self.generate_refund_id()

        today = datetime.today().strftime(self.DATE_FORMAT)

        refund = {
            "refund_id": refund_id,
            "return_id": self.get_return_by_order(order_id)["return_id"],
            "order_id": order_id,
            "customer_id": order["customer_id"],
            "amount": order["total_amount"],
            "status": "Initiated",
            "refund_method": order["payment_method"],
            "initiated_date": today,
            "processed_date": None
        }

        REFUNDS[refund_id] = refund

        return {
            "success": True,
            "message": "Refund initiated successfully.",
            "refund": refund
        }