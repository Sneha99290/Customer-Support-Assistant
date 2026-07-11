from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from tools.order_tool import order_tool
from tools.create_return_tool import create_return_tool
from tools.check_return_status_tool import check_return_status_tool
from tools.check_refund_status_tool import check_refund_status_tool
from tools.create_refund_tool import initiate_refund_tool
from tools.knowledge_base import knowledge_base_tool

from .system_prompt import SYSTEM_PROMPT
from llm_client import LLMClient

class Agent:
    def __init__(self):
        self.llm = LLMClient().create_client()
        self.tools = [
            order_tool,
            create_return_tool,
            check_return_status_tool,
            check_refund_status_tool,
            initiate_refund_tool,
            knowledge_base_tool
        ]
        self.checkpointer = InMemorySaver()
        self.middleware = SummarizationMiddleware(model =self.llm, max_tokens_before_summary = 4000, messages_to_keep = 10)
        self.agent = create_agent(
            tools=self.tools,
            model=self.llm,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=self.checkpointer,
            middleware=[self.middleware]
        )

    def invoke(self, message, thread_id):
        response = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )
        return response["messages"][-1].content


# module-level instance expected by api.routes
customer_support_agent = Agent()
