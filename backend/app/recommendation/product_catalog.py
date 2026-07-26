from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Product:

    id: int

    name: str

    category: str

    description: str

    eligibility: Dict

    benefits: List[str]


PRODUCT_CATALOG = [

    Product(
        id=1,
        name="Premium Savings Account",
        category="Deposit",
        description="High interest savings account for affluent customers.",
        eligibility={
            "min_balance":50000,
            "min_income":5000
        },
        benefits=[
            "Higher Interest",
            "Priority Banking",
            "Unlimited Transfers"
        ]
    ),

    Product(
        id=2,
        name="Travel Credit Card",
        category="Credit Card",
        description="Reward card for frequent travelers.",
        eligibility={
            "credit_score":700,
            "min_income":7000,
            "has_credit_card":False
        },
        benefits=[
            "Airport Lounge",
            "Reward Points",
            "Travel Insurance"
        ]
    ),

    Product(
        id=3,
        name="Cashback Credit Card",
        category="Credit Card",
        description="Cashback on shopping and groceries.",
        eligibility={
            "credit_score":650,
            "has_credit_card":False
        },
        benefits=[
            "5% Cashback",
            "Movie Offers",
            "Fuel Cashback"
        ]
    ),

    Product(
        id=4,
        name="Personal Loan",
        category="Loan",
        description="Quick unsecured personal loan.",
        eligibility={
            "credit_score":650,
            "min_income":4000,
            "has_personal_loan":False
        },
        benefits=[
            "Fast Approval",
            "Flexible EMI",
            "Low Interest"
        ]
    ),

    Product(
        id=5,
        name="Home Loan",
        category="Loan",
        description="Affordable housing finance.",
        eligibility={
            "credit_score":720,
            "min_income":9000
        },
        benefits=[
            "Low Interest",
            "30 Year Tenure"
        ]
    ),

    Product(
        id=6,
        name="Fixed Deposit",
        category="Investment",
        description="Secure investment with guaranteed returns.",
        eligibility={
            "min_balance":100000
        },
        benefits=[
            "Guaranteed Returns",
            "Flexible Tenure"
        ]
    ),

    Product(
        id=7,
        name="Mutual Fund SIP",
        category="Investment",
        description="Monthly wealth creation.",
        eligibility={
            "min_balance":50000,
            "min_income":6000
        },
        benefits=[
            "Professional Fund Management",
            "Long Term Growth"
        ]
    ),

    Product(
        id=8,
        name="Wealth Management",
        category="Investment",
        description="Dedicated financial advisor.",
        eligibility={
            "min_balance":150000,
            "min_income":12000
        },
        benefits=[
            "Dedicated Advisor",
            "Tax Planning",
            "Portfolio Optimization"
        ]
    ),

    Product(
        id=9,
        name="Business Credit Card",
        category="Credit Card",
        description="Business expense management.",
        eligibility={
            "credit_score":720,
            "min_income":10000
        },
        benefits=[
            "Business Rewards",
            "Expense Tracking"
        ]
    ),

    Product(
        id=10,
        name="Health Insurance",
        category="Insurance",
        description="Medical insurance coverage.",
        eligibility={
            "age":40
        },
        benefits=[
            "Cashless Hospitalization",
            "Family Coverage"
        ]
    )

]