from typing import Dict, List

from .product_catalog import PRODUCT_CATALOG
from .scoring import ProductScorer


class RecommendationEngine:

    def __init__(self):

        self.products = PRODUCT_CATALOG
        self.scorer = ProductScorer()

     

    def recommend_products(
    self,
    customer: Dict,
    scoring_features: list,
    top_k: int = 3
) -> List[Dict]:

        recommendations = []

        for product in self.products:

            recommendation = self.scorer.score_product(
    customer,
    product,
    scoring_features
)

            recommendations.append(recommendation)

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return recommendations[:top_k]

     

    def recommend_batch(
    self,
    customers: List[Dict],
    scoring_features: list,
    top_k: int = 3
) -> List[Dict]:

        output = []

        for customer in customers:

            output.append({

                "customer_id":
                    customer.get("customer_id"),

                "customer_name":
                    customer.get("customer_name"),

                "recommendations":
    self.recommend_products(
        customer,
        scoring_features=scoring_features,
        top_k=top_k
    )

            })

        return output