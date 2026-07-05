from langchain_core.tools import tool

from services.refund_service import RefundService


refund_service = RefundService()


@tool
def initiate_refund_tool(order_id: str) -> dict:
    """
    Initiate a refund request for an eligible order.
    """
    return refund_service.initiate_refund(order_id)