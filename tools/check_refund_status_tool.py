from langchain_core.tools import tool

from services.refund_service import RefundService


refund_service = RefundService()


@tool
def check_refund_status_tool(order_id: str) -> dict:
    """
    Check the refund status of an order.
    Use for refund status or refund eligibility queries.
    """
    return refund_service.get_refund_summary(order_id)