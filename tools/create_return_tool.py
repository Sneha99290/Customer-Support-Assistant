from langchain_core.tools import tool

from services.return_service import ReturnService


return_service = ReturnService()


@tool
def create_return_tool(
    order_id: str,
    reason: str
) -> dict:
    """
    Create a return request for an eligible order.

    Use this tool only when the customer explicitly asks
    to return a product.
    """

    return return_service.create_return(
        order_id=order_id,
        reason=reason
    )