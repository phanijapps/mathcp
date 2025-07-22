import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from os import getenv
from langchain_openai import ChatOpenAI
from agent.state import MathAgentRequest
from pydantic import Field, SecretStr
from typing import Optional
import json
from langchain_core.messages import HumanMessage, AIMessage



load_dotenv()


# Custom ChatOpenRouter class to handle OpenRouter API
class ChatOpenRouter(ChatOpenAI):
    openai_api_key: Optional[SecretStr] = Field(
        alias="api_key",
        default_factory=lambda: getenv("OPENROUTER_API_KEY")
    )

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "OPENROUTER_API_KEY"}

    def __init__(self, openai_api_key: Optional[str] = None, **kwargs):
        openai_api_key = openai_api_key or getenv("OPENROUTER_API_KEY")
        super().__init__(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key=openai_api_key,
            default_headers={
                "HTTP-Referer": "https://your-site.com",  # Replace with your site
                "X-Title": "LangGraph OpenRouter Example"  # Replace with your app name
            },
            **kwargs
        )

llm = ChatOpenRouter(
  openai_api_key=getenv("OPENROUTER_API_KEY"),
  openai_api_base=getenv("OPENROUTER_BASE_URL"),
  model_name="moonshotai/kimi-k2",
)

# Connect to MCP tool servers
client = MultiServerMCPClient(
    {
       
        "math": {
            "url": "http://127.0.0.1:8001/sse/",  # math server endpoint
            "transport": "sse",
        },
    }
)

system_message = SystemMessage(
    """
You are MathSolveX, an expert AI math problem solver with access to 120+ specialized tools for numeric, symbolic, geometric, and algorithmic computation. 
You reason step-by-step, break down problems into sub-tasks, and intelligently choose the right tool(s) for each step. 
You handle everything from basic arithmetic to graduate-level proofs, optimizations, and data analysis.

Your goals:

1. Understand the user's problem clearly and completely. Ask clarifying questions if needed.
2. Break down the problem into logical, solvable subcomponents.
3. Select and call tools thoughtfully—based on the type of problem:
   - Algebraic (symbolic manipulation, equation solving, factoring, simplification)
   - Calculus (differentiation, integration, limits, series)
   - Linear algebra (matrix operations, eigenvalues, transformations)
   - Geometry (Euclidean, coordinate, analytic, or 3D)
   - Probability/statistics (distributions, simulations, regressions)
   - Numerical (approximation, root-finding, optimization)
   - Graph theory, logic, number theory, etc.
4. Verify the results using alternate tools or sanity checks when precision is important.
5. Explain the solution clearly in natural language, with LaTeX formatting for math expressions.

Rules and behavior:

- Always think before acting. Don't blindly invoke tools—reason first.
- Use the search tool to find the right math function before execute.
- Reason with responses from search tool
- Use multiple tools sequentially or recursively if needed.
- Prefer symbolic solutions when appropriate; otherwise use numerical approximations.
- If a tool fails or returns ambiguous results, retry using alternate methods.
- Always produce transparent, reproducible steps.
- Generate visuals (e.g., plots, diagrams) to support geometric or statistical reasoning.
- Format answers clearly for students, researchers, or professionals depending on the context.
- Be accurate, rigorous, and excellent at cross-verifying results. 
  Assume problems may contain traps, missing assumptions, or multiple interpretations—handle ambiguity carefully.
"""
)


async def build_graph():
    tools = await client.get_tools()
    #print(f"Tools {tools}")

    llm_with_tools = llm.bind_tools(tools)

    tool_node = ToolNode(tools)

    def should_continue(state: MathAgentRequest):
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage):
                return "tools" if msg.tool_calls else END
        return END
    
    async def call_model(state: MathAgentRequest):
        messages = state["messages"]
        if not messages:
            return {"messages": []}

        # ✅ LangChain <-> LangGraph safest pattern
        response = await llm_with_tools.ainvoke(messages)   # list[BaseMessage]

        return {"messages": messages + [response]}
    
    async def init(state: MathAgentRequest):
        return {
            "messages": [
                system_message,
                HumanMessage(content=state["question"])
            ]
        }
            
        
    # Build the graph
    builder = StateGraph(MathAgentRequest)
    builder.add_node("init", init)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "init")
    builder.add_edge("init","call_model")
    builder.add_conditional_edges("call_model", should_continue, ["tools",END])
    builder.add_edge("tools", "call_model")
    math_graph = builder.compile()

    return math_graph
    
# Initialize graph globally by building it immediately
graph = asyncio.run(build_graph())
