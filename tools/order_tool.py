from langchain_core.tools import tool

from services.order_service import OrderService


order_service = OrderService()


@tool
def order_tool(order_id: str) -> dict:
    """
    Retrieve complete information about an order.

    Use this tool whenever the customer asks about:
    - Order status
    - Delivery status
    - Tracking
    - Purchased items
    - Payment status
    - Purchase date
    - Delivery date
    """

    return order_service.get_order_summary(order_id)