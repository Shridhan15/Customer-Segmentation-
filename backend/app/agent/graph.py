
import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.agent.state import AgentState
from app.agent.nodes import (
    intent_extraction_node,
    data_prep_node,
    execution_engine_node,
    persona_explainability_node,
    response_synthesis_node
)
 
def route_after_intent(state: AgentState):
    """If intent is ambiguous, route to human interrupt. Otherwise proceed to data prep."""
    if state.get("requires_human_input"):
        return "human_hitl_node"
    return "data_prep_node"

def human_hitl_node(state: AgentState) -> AgentState:
    """Pause node holding state for human intervention.""" 
    return state
 
builder = StateGraph(AgentState)
 
builder.add_node("intent_extraction_node", intent_extraction_node)
builder.add_node("human_hitl_node", human_hitl_node)
builder.add_node("data_prep_node", data_prep_node)
builder.add_node("execution_engine_node", execution_engine_node)
builder.add_node("persona_explainability_node", persona_explainability_node)
builder.add_node("response_synthesis_node", response_synthesis_node)
 
builder.set_entry_point("intent_extraction_node")
 
builder.add_conditional_edges(
    "intent_extraction_node",
    route_after_intent,
    {
        "human_hitl_node": "human_hitl_node",
        "data_prep_node": "data_prep_node"
    }
)
 
builder.add_edge("human_hitl_node", END)  
builder.add_edge("data_prep_node", "execution_engine_node")
builder.add_edge("execution_engine_node", "persona_explainability_node")
builder.add_edge("persona_explainability_node", "response_synthesis_node")
builder.add_edge("response_synthesis_node", END)

# Set up SQLite Memory Checkpointer
conn = sqlite3.connect("sqlite_state.db", check_same_thread=False)
memory = SqliteSaver(conn)

agent_graph = builder.compile(checkpointer=memory)