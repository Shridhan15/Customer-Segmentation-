
import pandas as pd
import json
from langchain_groq import ChatGroq
from app.agent.state import AgentState, ExtractedIntent
from app.agent.tools.segmentation_tool import run_segmentation
from app.agent.tools.eda_tool import run_eda
from app.core.config import settings

 
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)


def intent_extraction_node(state: AgentState) -> AgentState:
    """Uses LLM Structured Output to extract intent, features, filters, and ambiguity."""
    structured_llm = llm.with_structured_output(ExtractedIntent)
    
    prompt = f"""
    You are an expert banking analytics AI assistant. 
    Analyze the following user query regarding bank customer data:
    "{state['raw_query']}"
    
    Extract:
    1. Intent type ('segmentation', 'eda', 'explainability', 'conversion_analysis', or 'ambiguous')
    2. Relevant features/columns needed (Available columns: age, monthly_income, avg_monthly_balance, transaction_frequency, avg_transaction_amount)
    3. Target segments or filters mentioned.
    4. Flag 'is_ambiguous' as True ONLY if the request is too vague to execute (e.g., "Group my data" without specifying attributes).
    """
    
    result: ExtractedIntent = structured_llm.invoke(prompt)
     
    if state.get("human_clarification"):
        result.is_ambiguous = False
    
    state["intent_data"] = result.dict()
    state["requires_human_input"] = result.is_ambiguous
    state["human_clarification"] = result.clarification_question if result.is_ambiguous else None
    
    return state

 
def data_prep_node(state: AgentState) -> AgentState:
    """Loads CSV dataset and filters/scales columns dynamically based on Node 1 intent."""
    df = pd.read_csv(settings.DATASET_PATH)
    intent = state["intent_data"]
     
    selected_features = intent.get("features_requested") or ["avg_monthly_balance", "transaction_frequency"]
     
    valid_features = [f for f in selected_features if f in df.columns]
    if not valid_features:
        valid_features = ["avg_monthly_balance", "transaction_frequency"]
        
    state["prepared_data"] = {
        "features": valid_features,
        "record_count": len(df)
    }
    return state

 
def execution_engine_node(state: AgentState) -> AgentState:
    """Executes clustering, EDA, or conversion targeting based on intent."""
    df = pd.read_csv(settings.DATASET_PATH)
    intent_type = state["intent_data"]["intent_type"]
    features = state["prepared_data"]["features"]
    
    if intent_type == "segmentation":
        results = run_segmentation(df, features=features, n_clusters=3)
    elif intent_type == "eda":
        results = run_eda(df)
    elif intent_type == "conversion_analysis": 
        priority_cutoff = df["avg_monthly_balance"].quantile(0.8)
        near_priority = df[(df["avg_monthly_balance"] >= priority_cutoff * 0.7) & 
                           (df["avg_monthly_balance"] < priority_cutoff)]
        results = {
            "conversion_candidates": near_priority[["customer_id", "avg_monthly_balance", "transaction_frequency"]].head(10).to_dict(orient="records"),
            "target_threshold": priority_cutoff
        }
    else:
        results = run_eda(df) 
        
    state["execution_results"] = results
    return state

 
def persona_explainability_node(state: AgentState) -> AgentState:
    """Uses LLM to interpret mathematical outputs into human-understandable personas and rules."""
    intent_type = state["intent_data"]["intent_type"]
    results = state["execution_results"]
    
    prompt = f"""
    You are an expert Bank Customer Analytics Strategist.
    Analyze the execution results of the following query: "{state['raw_query']}"
    
    Execution Results Data:
    {json.dumps(results, indent=2, default=str)}
    
    Task:
    1. Explain WHY customers were grouped or flagged in plain business English.
    2. Define clear personas (e.g., "High-Value Wealthy Savers", "Active Transactors").
    3. Recommend specific cross-selling or retention strategies for each group.
    """
    
    response = llm.invoke(prompt)
    state["persona_explanations"] = {
        "explanation_markdown": response.content
    }
    return state

 
def response_synthesis_node(state: AgentState) -> AgentState:
    """Compiles the final structured JSON response payload for the React frontend."""
    state["final_output"] = {
        "query": state["raw_query"],
        "agent_reasoning": {
            "detected_intent": state["intent_data"]["intent_type"],
            "features_used": state["prepared_data"]["features"],
            "evaluation_metrics": state["execution_results"].get("silhouette_score", "N/A")
        },
        "insights": state["persona_explanations"]["explanation_markdown"],
        "data_payload": state["execution_results"]
    }
    return state