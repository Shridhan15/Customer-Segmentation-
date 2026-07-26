import json
import logging

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from .recommendation_engine import RecommendationEngine

logger = logging.getLogger("recommendation_tool")


def run_product_recommendation(
    df: pd.DataFrame,
    features: list,
    n_clusters: int = 4
):

     

    df_clean = df.dropna(subset=features).copy()

    logger.info(
        f"Running recommendation engine on {len(df_clean)} customers."
    )

     

    scaler = StandardScaler()

    X = scaler.fit_transform(
        df_clean[features]
    )

     

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init="auto"
    )

    df_clean["segment"] = model.fit_predict(X)

     

    score = silhouette_score(
        X,
        df_clean["segment"]
    )

     

    segment_counts = (
        df_clean["segment"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

     

    centers = []

    grouped = (
        df_clean
        .groupby("segment")
    )

    for segment_id, group in grouped:

        center = {}

        for col in features:

            center[col] = float(
                group[col].mean()
            )

        center["segment"] = int(segment_id)

        center["customer_count"] = len(group)

        centers.append(center)

     

    engine = RecommendationEngine()

    segment_recommendations = []

    for center in centers:

        representative_customer = {

            "age":
                center.get("age", 0),

            "monthly_income":
                center.get("monthly_income", 0),

            "avg_monthly_balance":
                center.get(
                    "avg_monthly_balance",
                    0
                ),

            "transaction_frequency":
                center.get(
                    "transaction_frequency",
                    0
                ),

            "credit_score":
                center.get(
                    "credit_score",
                    700
                ),

            "has_credit_card":
                False,

            "has_personal_loan":
                False
        }

        recommendations = engine.recommend_products(
    representative_customer,
    scoring_features=features,
    top_k=3
)

        segment_recommendations.append({

            "segment":

                center["segment"],

            "customer_count":

                center["customer_count"],

            "recommended_products":

                recommendations

        })

     

    customers = df_clean.to_dict(
        orient="records"
    )

    customer_recommendations = (
    engine.recommend_batch(
        customers,
        scoring_features=features,
        top_k=3
    )
)

     

    sample = json.loads(

        df_clean[
            [
                "customer_id",
                "customer_name",
                *features,
                "segment"
            ]
        ]
        .head(10)
        .to_json(
            orient="records"
        )

    )

     

    return {

        "n_clusters":

            n_clusters,

        "silhouette_score":

            round(float(score), 3),

        "segment_counts":

            {
                int(k): int(v)
                for k, v in segment_counts.items()
            },

        "cluster_centers":

            centers,

        "segment_recommendations":

            segment_recommendations,

        "customer_recommendations":

            customer_recommendations,

        "data_sample":

            sample
    }