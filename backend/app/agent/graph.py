import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.agent.state import AgentState
from app.agent.nodes import (
    intent_extraction_node,
    human_hitl_node,
    data_prep_node,
    execution_engine_node,
    persona_explainability_node,
    response_synthesis_node,
    churn_prep_node,
    churn_execution_node,
    product_recommendation_node,
    general_conversation_node
)
import logging

logger = logging.getLogger("agent_router")


def route_after_intent(state: AgentState):
    logger.info("--- EVALUATING ROUTING ---")
    if state.get("requires_human_input"):
        logger.info("Routing to: human_hitl_node")
        return "human_hitl_node"
    
    
    intent = state.get("intent_data", {}).get("intent_type", "segmentation").lower()

    if intent == "chit_chat":
        logger.info("Routing to: general_conversation_node")
        return "general_conversation_node"
    
    if "churn" in intent:
        logger.info("Routing to: churn_prep_node")
        return "churn_prep_node"
    elif "recommend" in intent:
        logger.info("Routing to: product_recommendation_node")
        return "product_recommendation_node"

    logger.info("Routing to: data_prep_node")
    return "data_prep_node"

builder = StateGraph(AgentState)

builder.add_node("intent_extraction_node", intent_extraction_node)
builder.add_node("human_hitl_node", human_hitl_node)
builder.add_node("general_conversation_node", general_conversation_node) 
builder.add_node("data_prep_node", data_prep_node)
builder.add_node("execution_engine_node", execution_engine_node)
builder.add_node("persona_explainability_node", persona_explainability_node)
builder.add_node("churn_prep_node", churn_prep_node)
builder.add_node("churn_execution_node", churn_execution_node)
builder.add_node("product_recommendation_node", product_recommendation_node)
builder.add_node("response_synthesis_node", response_synthesis_node)

builder.set_entry_point("intent_extraction_node")

builder.add_conditional_edges(
    "intent_extraction_node",
    route_after_intent,
    {
        "human_hitl_node": "human_hitl_node",
        "general_conversation_node": "general_conversation_node",
        "data_prep_node": "data_prep_node",
        "churn_prep_node": "churn_prep_node",
        "product_recommendation_node": "product_recommendation_node"
    }
)

builder.add_edge("human_hitl_node", END)  
builder.add_edge("data_prep_node", "execution_engine_node")
builder.add_edge("execution_engine_node", "persona_explainability_node")
builder.add_edge("persona_explainability_node", "response_synthesis_node")
builder.add_edge("churn_prep_node", "churn_execution_node")
builder.add_edge("churn_execution_node", "response_synthesis_node")
builder.add_edge("product_recommendation_node", "response_synthesis_node")
builder.add_edge("response_synthesis_node", END)
builder.add_edge("general_conversation_node", END)

conn = sqlite3.connect("sqlite_state.db", check_same_thread=False)
memory = SqliteSaver(conn)

agent_graph = builder.compile(checkpointer=memory)