"""Graph State"""
from typing import Optional, Annotated,TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class MathAgentRequest(TypedDict):
    """Math Agent State Request"""
    question: str
    messages: Annotated[list[BaseMessage],add_messages]
    max_iterations: Optional[int]
    final_answer: Optional[str]
