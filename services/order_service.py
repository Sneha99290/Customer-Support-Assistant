from datetime import datetime

from data.orders import ORDERS


class OrderService:

    DATE_FORMAT = "%Y-%m-%d"

    def validate_order_id(self, order_id: str) -> None:
        """
        Validate the order ID format.
        """

        if not order_id:
            raise ValueError("Order ID cannot be empty.")

        if not order_id.startswith("ORD"):
            raise ValueError("Invalid Order ID format.")

    def get_order(self, order_id: str):
        """
        Retrieve an order from the database.
        """

        return ORDERS.get(order_id)

    def calculate_days_since_purchase(self, purchase_date: str) -> int:
        """
        Calculate number of days since purchase.
        """

        purchase_date = datetime.strptime(
            purchase_date,
            self.DATE_FORMAT
        )

        return (datetime.today() - purchase_date).days

    def calculate_days_since_delivery(self, delivery_date: str):

        if not delivery_date:
            return None

        delivery_date = datetime.strptime(
            delivery_date,
            self.DATE_FORMAT
        )

        return (datetime.today() - delivery_date).days

    def build_summary(self, order: dict) -> dict:
        """
        Build useful information for the agent.
        """

        return {
            "delivered": order["status"] == "Delivered",
            "cancelled": order["status"] == "Cancelled",
            "returned": order["status"] == "Returned",
            "shipped": order["status"] == "Shipped",
            "payment_complete": order["payment_status"] == "Paid",
            "tracking_available": order["tracking_id"] is not None,
            "days_since_purchase": self.calculate_days_since_purchase(
                order["purchase_date"]
            ),
            "days_since_delivery": self.calculate_days_since_delivery(
                order["delivery_date"]
            )
        }

    def get_order_summary(self, order_id: str) -> dict:
        """
        Main service method used by the Order Tool.
        """

        try:
            self.validate_order_id(order_id)
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }

        order = self.get_order(order_id)

        if order is None:
            return {
                "success": False,
                "message": f"No order found with ID '{order_id}'."
            }

        return {
            "success": True,
            "message": "Order found.",
            "order": order,
            "summary": self.build_summary(order)
        }