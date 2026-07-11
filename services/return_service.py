from datetime import datetime

from data.orders import ORDERS
from data.returns import RETURNS


class ReturnService:

    DATE_FORMAT = "%Y-%m-%d"

    def get_order(self, order_id: str):
        """
        Retrieve an order by ID.
        """
        return ORDERS.get(order_id)

    def get_return_by_order(self, order_id: str):
        """
        Retrieve the return request associated with an order.
        """
        for return_record in RETURNS.values():
            if return_record["order_id"] == order_id:
                return return_record

        return None

    def is_return_window_open(self, order: dict) -> bool:
        """
        Check whether the order is still within the return window.
        """

        today = datetime.today().date()

        window_end = datetime.strptime(
            order["return_window_end"],
            self.DATE_FORMAT
        ).date()

        return today <= window_end

    def check_return_eligibility(self, order_id: str) -> dict:
        """
        Determine whether an order is eligible for return.
        """

        order = self.get_order(order_id)

        if order is None:
            return {
                "eligible": False,
                "reason": "Order not found."
            }

        if order["status"] != "Delivered":
            return {
                "eligible": False,
                "reason": "Only delivered orders can be returned."
            }

        existing_return = self.get_return_by_order(order_id)

        if existing_return:
            return {
                "eligible": False,
                "reason": "A return request already exists."
            }

        if not self.is_return_window_open(order):
            return {
                "eligible": False,
                "reason": "Return window has expired."
            }

        return {
            "eligible": True,
            "reason": "Order is eligible for return."
        }

    def get_return_summary(self, order_id: str) -> dict:
        """
        Retrieve return information for an order.
        """

        order = self.get_order(order_id)

        if order is None:
            return {
                "success": False,
                "message": "Order not found."
            }

        return_record = self.get_return_by_order(order_id)

        eligibility = self.check_return_eligibility(order_id)

        # include return window info so tools/agents can report it directly
        window_end = None
        days_left = None
        try:
            window_end = order.get("return_window_end")
            if window_end:
                window_date = datetime.strptime(window_end, self.DATE_FORMAT).date()
                today = datetime.today().date()
                days_left = (window_date - today).days
        except Exception:
            # fall back to raw value if parsing fails
            window_end = order.get("return_window_end")
        print(window_end)

        return {
            "success": True,
            "order_id": order_id,
            "return": return_record,
            "eligibility": eligibility,
            "return_window_end": window_end,
            "return_window_days_left": days_left,
        }
    
    def generate_return_id(self) -> str:
        if not RETURNS:
            return "RET2001"

        max_id = max(
            int(return_id.replace("RET", ""))
            for return_id in RETURNS.keys()
        )

        return f"RET{max_id + 1}"

    def create_return(
        self,
        order_id: str,
        reason: str
    ) -> dict:
        """
        Create a new return request.
        """

        eligibility = self.check_return_eligibility(order_id)

        if not eligibility["eligible"]:
            return {
                "success": False,
                "message": eligibility["reason"]
            }

        return_id = f"RET{2000 + len(RETURNS) + 1}"

        today = datetime.today().strftime(self.DATE_FORMAT)

        order = self.get_order(order_id)

        new_return = {
            "return_id": return_id,
            "order_id": order_id,
            "customer_id": order["customer_id"],
            "reason": reason,
            "status": "Requested",
            "requested_date": today,
            "approved_date": None,
            "pickup_date": None,
            "completed_date": None
        }

        RETURNS[return_id] = new_return

        return {
            "success": True,
            "message": "Return request created successfully.",
            "return": new_return
        }