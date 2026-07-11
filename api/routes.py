from fastapi import APIRouter

from api.schemas import ChatRequest, ChatResponse

from agent.agent import customer_support_agent

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = customer_support_agent.invoke(
        message=request.message,
        thread_id=request.conversation_id,
    )

    return ChatResponse(
        response=response
    )