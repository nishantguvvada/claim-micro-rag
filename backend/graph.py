from rag_pipeline import DocumentLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from langgraph.graph import MessagesState, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field
from typing import Literal, Optional
from models import embeddings_model, llm
import uuid

loader = DocumentLoader()
docs = loader.load(path="data")
chunks = loader.split(docs=docs)

vector_store = InMemoryVectorStore.from_documents(
    documents=chunks, embedding=embeddings_model
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2, "score_threshold": 0.7})
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="insurance_policy_documents",
    description="Retrieve information on insurance policy, FAQ, KYC rules and hospitals",
)

@tool
def gather_information_tool(query: str) -> str:
    """Use this tool if the user's query cannot be answered from documents or knowledge alone. 
    It will INTERRUPT the flow and ask the human for additional details (like missing policy number, contact details, dates, or any information the LLM does not know)."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tools = [retriever_tool, gather_information_tool]
# tool_response = retriever_tool.invoke({"query": "TAT"})

class State(MessagesState):
    pass

llm_with_tools = llm.bind_tools(tools=tools)

def chatbot_node(state: State):
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful assistant. If you don't have enough info "
            "to answer a question completely, ALWAYS call the gather_information_tool "
            "to request missing details from the human."
        ),
    }
    response = llm_with_tools.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

# input = {"messages": [{"role": "user", "content": "What is the TAT for filing the claim?"}]}
# print(chatbot_node(input)["messages"][-1])

tools_node = ToolNode(tools)

memory = InMemorySaver()
graph = StateGraph(State)
graph.set_entry_point("chatbot_node")
graph.add_node("chatbot_node", chatbot_node).add_node("tools_node", tools_node)
graph.add_conditional_edges("chatbot_node", tools_condition, {"tools": "tools_node", "__end__":"__end__"})
graph.add_edge("tools_node", "chatbot_node")

compiled_graph = graph.compile(checkpointer=memory)

# config = {"configurable": {"thread_id": uuid.uuid4()}}
# response = compiled_graph.invoke({"messages": [{"role": "user", "content": "What is the policy for people over 60 years of age?"}]}, config)
# print(response)

# compiled_graph.get_graph().draw_mermaid_png(output_file_path="./graph.png")

def ask_graph(user_query: str, id: Optional[uuid.UUID] = None, resume_data: Optional[str] = None):
    if not id:
        thread_id = uuid.uuid4()
    else:
        thread_id = id
    config = {"configurable": {"thread_id": thread_id}}

    if resume_data:
        response = compiled_graph.resume(
            command=Command(resume={"data": resume_data}),
            config=config
        )
    else:
        response = compiled_graph.invoke({"messages": [{"role": "user", "content": user_query}]}, config)

    return {"response": response, "thread_id": thread_id}
