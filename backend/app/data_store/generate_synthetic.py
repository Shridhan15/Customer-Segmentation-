import os
import numpy as np
import pandas as pd
from faker import Faker

np.random.seed(42)
fake = Faker()
Faker.seed(42)

def generate_synthetic_banking_data(num_records: int = 1000, output_filename: str = "customer_banking_data.csv"):
    """
    Generates a synthetic banking dataset with distinct financial personas 
    and saves it as a CSV file in the data_store directory.
    """
    
    
    p1_count = int(num_records * 0.20)
    p1_age = np.random.randint(35, 70, p1_count)
    p1_income = np.random.normal(120000, 25000, p1_count).clip(75000, 300000)
    p1_balance = np.random.normal(85000, 20000, p1_count).clip(40000, 250000)
    p1_tx_freq = np.random.poisson(lam=12, size=p1_count).clip(2, 30)
    p1_tx_amt = np.random.normal(1200, 300, p1_count).clip(200, 5000)

    p2_count = int(num_records * 0.50)
    p2_age = np.random.randint(22, 55, p2_count)
    p2_income = np.random.normal(55000, 15000, p2_count).clip(25000, 95000)
    p2_balance = np.random.normal(12000, 4000, p2_count).clip(1500, 35000)
    p2_tx_freq = np.random.poisson(lam=35, size=p2_count).clip(15, 80)
    p2_tx_amt = np.random.normal(180, 50, p2_count).clip(20, 800)

    p3_count = num_records - p1_count - p2_count
    p3_age = np.random.randint(18, 65, p3_count)
    p3_income = np.random.normal(28000, 8000, p3_count).clip(10000, 45000)
    p3_balance = np.random.normal(800, 400, p3_count).clip(50, 2500)
    p3_tx_freq = np.random.poisson(lam=3, size=p3_count).clip(0, 8)
    p3_tx_amt = np.random.normal(45, 20, p3_count).clip(5, 200)

    ages = np.concatenate([p1_age, p2_age, p3_age])
    incomes = np.concatenate([p1_income, p2_income, p3_income])
    balances = np.concatenate([p1_balance, p2_balance, p3_balance])
    tx_freqs = np.concatenate([p1_tx_freq, p2_tx_freq, p3_tx_freq])
    tx_amts = np.concatenate([p1_tx_amt, p2_tx_amt, p3_tx_amt])

    data = []
    for i in range(num_records):
        data.append({
            "customer_id": f"CUST_{1001 + i}",
            "customer_name": fake.name(),
            "age": int(ages[i]),
            "monthly_income": round(float(incomes[i] / 12), 2),
            "avg_monthly_balance": round(float(balances[i]), 2),
            "transaction_frequency": int(tx_freqs[i]),
            "avg_transaction_amount": round(float(tx_amts[i]), 2),
            "account_type": np.random.choice(["Savings", "Checking", "Premium"], p=[0.5, 0.4, 0.1]),
            
            
            "credit_score": int(np.clip(np.random.normal(710, 60), 550, 850)),
            
            "has_credit_card": bool(np.random.choice([True, False], p=[0.65, 0.35])),
            "has_personal_loan": bool(np.random.choice([True, False], p=[0.25, 0.75]))
        })

    df = pd.DataFrame(data)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, output_filename)
    
    df.to_csv(file_path, index=False)
    print(f"Successfully generated {num_records} synthetic customer records at:")
    print(f" -> {file_path}")

if __name__ == "__main__":
    generate_synthetic_banking_data()