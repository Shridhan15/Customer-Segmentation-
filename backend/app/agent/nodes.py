import pandas as pd
import json
from langchain_groq import ChatGroq
from app.agent.state import AgentState, ExtractedIntent
from app.agent.tools.segmentation_tool import run_segmentation
from app.agent.tools.eda_tool import run_eda
from app.agent.tools.churn_tool import run_churn_prediction
from app.agent.tools.recommendation_tool import run_product_recommendation
from app.core.config import settings
import logging
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("agent_nodes")

llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0,
    api_key=settings.GROQ_API_KEY
)

def human_hitl_node(state: AgentState) -> AgentState:
    return state

def intent_extraction_node(state: AgentState) -> AgentState:
    logger.info(f"--- Entering INTENT EXTRACTION NODE ---")
    logger.debug(f"Raw query: {state['raw_query']}")
    
    structured_llm = llm.with_structured_output(ExtractedIntent)
    
    prompt = f"""
    You are an expert banking analytics AI assistant. 
    Analyze the following user query regarding bank customer data:
    "{state['raw_query']}"
    
    CRITICAL INSTRUCTIONS: 
    Your tool call must use strictly valid JSON syntax. When generating boolean values, you MUST use lowercase 'true' or 'false'. Do not use Python's 'True' or 'False'.
    If the user is simply greeting you, saying goodbye, or making general conversation (e.g., "hi", "how are you", "thanks")(basically not related to analyis, report etc), set intent_type to 'chit_chat'.
    If the user asks to find, analyze, or identify specific groups like "High Value Customers" or "Loyal Customers", you MUST set intent_type to 'segmentation'.
    
    Extract:
    1. Intent type ('segmentation', 'predict_churn', 'recommend_products', 'eda', 'explainability', 'conversion_analysis', or 'ambiguous')
    2. Relevant features/columns needed (Available columns: age, monthly_income, avg_monthly_balance, transaction_frequency, avg_transaction_amount)
    3. Target segments or filters mentioned.
    4. Flag 'is_ambiguous' as true ONLY if the request is too vague to execute.
    """
    
    result: ExtractedIntent = structured_llm.invoke(prompt)
      
    if state.get("human_clarification"):
        result.is_ambiguous = False
    
    state["intent_data"] = result.dict()
    state["requires_human_input"] = result.is_ambiguous
    state["human_clarification"] = result.clarification_question if result.is_ambiguous else None
    
    return state

def general_conversation_node(state: AgentState) -> AgentState:
    logger.info(f"--- Entering GENERAL CONVERSATION NODE ---")
    query = state["raw_query"]

    prompt = f"""
    You are an expert banking analytics AI assistant. 
    The user sent this conversational message: "{query}"
    
    Respond politely, concisely, and naturally. 
    - If they are saying goodbye (e.g., "bye", "see you"), wish them well and say goodbye without asking how to help them further.
    - If they are greeting you or saying thanks, respond warmly and briefly offer your assistance with banking data.
    """
    
    response = llm.invoke(prompt)
    state["response_message"] = response.content
    
    state["final_output"] = {
        "data_payload": None 
    }
    logger.info(f"General conversation response generated: {state['response_message']}")
    return state


def data_prep_node(state: AgentState) -> AgentState:
    logger.info(f"--- Entering DATA PREP NODE ---")
    logger.info(f"Loading dataset from {settings.DATASET_PATH}")
    df = pd.read_csv(settings.DATASET_PATH)
    intent = state["intent_data"]
      
    selected_features = intent.get("features_requested") or ["avg_monthly_balance", "transaction_frequency"]
    logger.info(f"Features requested by intent: {selected_features}")


    valid_features = [f for f in selected_features if f in df.columns]
    if not valid_features:
        logger.warning("No valid features found from request. Falling back to default features.")
        valid_features = ["avg_monthly_balance", "transaction_frequency"]
        
    state["prepared_data"] = {
        "features": valid_features,
        "record_count": len(df)
    }
    logger.info(f"Prepared data with {len(valid_features)} features and {len(df)} records.")
    return state

def execution_engine_node(state: AgentState) -> AgentState:
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
    intent_type = state["intent_data"]["intent_type"]
    results = state["execution_results"]
    
    prompt = f"""
    You are an expert Bank Customer Analytics Strategist.
    Analyze the execution results of the following query: "{state['raw_query']}"
    
    Execution Results Data:
    {json.dumps(results, indent=2, default=str)}
    
    Task:
    1. Explain WHY customers were grouped or flagged in plain business English.
    2. Define clear personas.
    3. Recommend specific cross-selling or retention strategies for each group.
    """
    
    response = llm.invoke(prompt)
    state["persona_explanations"] = {
        "explanation_markdown": response.content
    }
    return state

def response_synthesis_node(state: AgentState) -> AgentState:

    intent = state["intent_data"]["intent_type"]
    formatted_intent = intent.replace("_", " ").title()

    state["response_message"] = (
        f"{formatted_intent} completed successfully. "
        "The dashboard has been updated with the latest insights."
    )

    explanation = ""

    if state.get("persona_explanations"):
        explanation = state["persona_explanations"].get(
            "explanation_markdown",
            ""
        )

    state["final_output"] = {

        "query": state["raw_query"],

        "agent_reasoning": {

            "detected_intent":
                intent,

            "features_used":
                (
                    state.get("prepared_data", {})
                    .get("features", [])
                ),

            "evaluation_metrics":
                (
                    state.get("execution_results", {})
                    .get("silhouette_score", "N/A")
                )

        },

        "insights":
            explanation,

        "data_payload":
            state.get("execution_results", {})

    }

    logger.info("Response synthesis completed.")

    return state

def churn_prep_node(state: AgentState) -> AgentState:
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

def churn_execution_node(state: AgentState) -> AgentState:
    df = pd.read_csv(settings.DATASET_PATH)
    features = state["prepared_data"]["features"]
    
    results = run_churn_prediction(df, features)
    state["execution_results"] = results
    
    prompt = f"""
    You are an expert Bank Customer Analytics Strategist.
    Analyze the churn prediction execution results of the following query: "{state['raw_query']}"
    
    Execution Results Data:
    {json.dumps(results, indent=2, default=str)}
    
    Task:
    1. Look at the 'churn_risk' metric inside the cluster_centers data. Explain the primary factors driving this risk in plain business English.
    2. Define the risk groups clearly, explicitly stating their average churn probability.
    3. Recommend specific retention strategies for the high-risk group.
    
    Use Markdown formatting. Do not use placeholders.
    """
    response = llm.invoke(prompt)
    
    state["persona_explanations"] = {
        "explanation_markdown": response.content
    }
    return state
 