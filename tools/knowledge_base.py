from langchain_core.tools import tool
import os

from rag.retrieval_service import Retriever

retriever = Retriever()


@tool
def knowledge_base_tool(query: str) -> str:
    """
    Search the company knowledge base for policies, FAQs,
    warranty, shipping, returns, refunds, cancellations,
    and other support-related information.

    Args:
        query: The user's question.

    Returns:
        A formatted string containing the most relevant
        document chunks along with their source metadata.
    """

    results = retriever.retrieve(query)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return "No relevant information was found in the knowledge base."

    context = []

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        source = os.path.basename(
            metadata.get("source", "Unknown")
        )

        page = metadata.get("page", "Unknown")

        context.append(
            f"""
            ========== Document {index} ==========
            Source: {source}
            Page: {page}

            Content:
            {document}
            """.strip()
        )

    return "\n\n".join(context)