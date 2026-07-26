from typing import Dict, List

from .product_catalog import Product


class ProductScorer:

    def __init__(self):
        self.weights = {
            "income": 20,
            "balance": 25,
            "credit_score": 25,
            "existing_product": 15,
            "transaction_frequency": 10,
            "age": 5,
        }

    def score_product(
        self,
        customer: Dict,
        product: Product,
        scoring_features: List[str],
    ):

        score = 0
        max_score = sum(self.weights.values())
        reasons = []

        eligibility = product.eligibility

        # Read customer values once
        income = customer.get("monthly_income", 0)
        balance = customer.get("avg_monthly_balance", 0)
        credit = customer.get("credit_score", 0)
        txn = customer.get("transaction_frequency", 0)
        age = customer.get("age", 0)

         
        if (
            "monthly_income" in scoring_features
            and "min_income" in eligibility
        ):

            required = eligibility["min_income"]

            if income >= required:
                score += self.weights["income"]
                reasons.append(
                    f"Income (${income:,.0f}) satisfies minimum requirement."
                )
            else:
                reasons.append(
                    f"Income below required ${required:,.0f}."
                )

         
        if (
            "avg_monthly_balance" in scoring_features
            and "min_balance" in eligibility
        ):

            required = eligibility["min_balance"]

            if balance >= required:
                score += self.weights["balance"]
                reasons.append(
                    "Strong average account balance."
                )
            else:
                reasons.append(
                    "Average balance below requirement."
                )

         
        if (
            "credit_score" in scoring_features
            and "credit_score" in eligibility
        ):

            required = eligibility["credit_score"]

            if credit >= required:

                score += self.weights["credit_score"]

                reasons.append(
                    f"Credit score ({credit}) is eligible."
                )

            elif credit >= required - 30:

                score += int(
                    self.weights["credit_score"] * 0.5
                )

                reasons.append(
                    "Credit score is close to eligibility."
                )

            else:

                reasons.append(
                    "Credit score below eligibility."
                )

         
        if "has_credit_card" in eligibility:

            expected = eligibility["has_credit_card"]
            actual = customer.get("has_credit_card", False)

            if actual == expected:

                score += self.weights["existing_product"]

                reasons.append(
                    "Product ownership matches eligibility."
                )

            else:

                score -= 10

         
        if "has_personal_loan" in eligibility:

            expected = eligibility["has_personal_loan"]
            actual = customer.get("has_personal_loan", False)

            if actual == expected:

                score += self.weights["existing_product"]

            else:

                score -= 10

         
        if "transaction_frequency" in scoring_features:

            if txn >= 30:

                score += self.weights["transaction_frequency"]

                reasons.append(
                    "Highly active customer."
                )

            elif txn >= 15:

                score += int(
                    self.weights["transaction_frequency"] * 0.6
                )

                reasons.append(
                    "Moderately active customer."
                )

        
        if (
            "age" in scoring_features
            and product.category == "Insurance"
        ):

            if age >= 40:

                score += self.weights["age"]

                reasons.append(
                    "Suitable age for insurance."
                )

         
        if (
            "monthly_income" in scoring_features
            and "avg_monthly_balance" in scoring_features
            and income >= 10000
            and balance >= 100000
        ):

            score += 10

            reasons.append(
                "Premium customer profile."
            )

        
        confidence = max(
            0,
            min(
                100,
                round(score / max_score * 100)
            )
        )

        return {

            "product_id": product.id,
            "product_name": product.name,
            "category": product.category,
            "score": score,
            "confidence": confidence,
            "description": product.description,
            "benefits": product.benefits,
            "reasons": reasons

        }