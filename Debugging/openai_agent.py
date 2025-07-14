from langchain_groq import ChatGroq
from typing import TypedDict
from langchain_core.messages import AnyMessage
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

import os


from dotenv import load_dotenv
load_dotenv()

import os
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

model= ChatGroq(model="gemma2-9b-it")

def make_default_graph():
    graph_workflow=StateGraph(State)

    def call_model(state):
        return {"messages": model.invoke(state["messages"])}

    graph_workflow.add_node("agent",call_model)
    graph_workflow.add_edge("agent",  END)
    graph_workflow.add_edge(START, "agent")

    agent=graph_workflow.compile()

    return agent
agent=make_default_graph()