import json
import logging
import pandas as pd

from app.core.config import settings
from app.agent.state import AgentState

from app.recommendation.recommendation_tool import (
    run_product_recommendation
)

from langchain_groq import ChatGroq
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0,
    api_key=settings.GROQ_API_KEY
)

logger = logging.getLogger(__name__)


def product_recommendation_node(
    state: AgentState
) -> AgentState:

    logger.info(
        "===== PRODUCT RECOMMENDATION NODE ====="
    )

    ###########################################################
    # Load Dataset
    ###########################################################

    df = pd.read_csv(
        settings.DATASET_PATH
    )

    ###########################################################
    # Read Intent
    ###########################################################

    intent = state["intent_data"]

    requested_features = (
        intent.get("features_requested")
        or
        [
            "age",
            "monthly_income",
            "avg_monthly_balance",
            "transaction_frequency",
            "credit_score"
        ]
    )

    valid_features = [

        f

        for f in requested_features

        if f in df.columns

    ]

    if len(valid_features) == 0:

        valid_features = [

            "age",

            "monthly_income",

            "avg_monthly_balance",

            "transaction_frequency",

            "credit_score"

        ]

    ###########################################################
    # ML Recommendation Engine
    ###########################################################

    results = run_product_recommendation(

        df,

        valid_features

    )

    ###########################################################
    # Build Segment Summary
    ###########################################################

    segment_summary = []

    for segment in results["segment_recommendations"]:

        cluster = next(

            c

            for c in results["cluster_centers"]

            if c["segment"] == segment["segment"]

        )

        summary = {

            "segment":

                segment["segment"],

            "customer_count":

                segment["customer_count"],

            "average_profile":{

                "age":
                    round(cluster.get("age",0),1),

                "income":
                    round(cluster.get("monthly_income",0),2),

                "balance":
                    round(cluster.get("avg_monthly_balance",0),2),

                "credit_score":
                    round(cluster.get("credit_score",0),1),

                "transaction_frequency":
                    round(cluster.get(
                        "transaction_frequency",
                        0
                    ),1)

            },

            "recommended_products":[

                {

                    "product":

                        p["product_name"],

                    "confidence":

                        p["confidence"],

                    "reason":

                        ", ".join(
                            p["reasons"]
                        )

                }

                for p in segment[
                    "recommended_products"
                ]

            ]

        }

        segment_summary.append(
            summary
        )

    ###########################################################
    # Prompt
    ###########################################################

    prompt = f"""
You are a Senior Banking Product Strategist.

A machine learning recommendation engine has already
identified the best products for every customer segment.

DO NOT invent new banking products.

Use ONLY the recommended products below.

Business Query

{state["raw_query"]}

Segment Recommendation Data

{json.dumps(segment_summary, indent=4)}

Generate a professional executive report.

Include

1 Executive Summary

2 Customer Segment Description

3 Explain WHY every recommended product matches
that customer segment.

4 Cross Selling Opportunities

5 Marketing Campaign Ideas

6 Revenue Opportunities

7 Possible Risks

8 Next Best Action

Write in business language.

Use Markdown formatting.
"""

    ###########################################################
    # LLM
    ###########################################################

    response = llm.invoke(
        prompt
    )

    ###########################################################
    # Dashboard Payload
    ###########################################################

    final_output = {

        "query":

            state["raw_query"],

        "agent_reasoning":{

            "detected_intent":

                "recommend_products",

            "features_used":

                valid_features,

            "evaluation_metrics":

                results[
                    "silhouette_score"
                ]

        },

        "insights":

            response.content,

        "data_payload":

            results

    }

    ###########################################################
    # Chat Response
    ###########################################################

    response_message = (

        "Product recommendation analysis completed successfully. "

        "The dashboard now contains customer segments, "

        "recommended banking products, "

        "AI business insights, "

        "and campaign strategies."

    )

    ###########################################################
    # Return
    ###########################################################

    return {

    "execution_results":
        results,

    "persona_explanations": {

        "explanation_markdown":
            response.content

    }

}