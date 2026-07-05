from langchain_core.tools import tool

from services.return_service import ReturnService


return_service = ReturnService()


@tool
def check_return_status_tool(order_id: str) -> dict:
    """
    Retrieve return information for an order.

    Use this tool when the customer asks:

    - What is my return status?
    - Has my return been approved?
    - Is my order eligible for return?
    """

    return return_service.get_return_summary(order_id)