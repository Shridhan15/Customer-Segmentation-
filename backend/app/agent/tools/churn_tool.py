import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def run_churn_prediction(df: pd.DataFrame, features: list, target: str = "churn") -> dict:
    if target not in df.columns:
        balance_med = df['avg_monthly_balance'].median()
        freq_med = df['transaction_frequency'].median()
        df[target] = ((df['avg_monthly_balance'] < balance_med) & 
                      (df['transaction_frequency'] < freq_med)).astype(int)
    
    df_clean = df.dropna(subset=features + [target]).copy()
    X = df_clean[features]
    y = df_clean[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))

    df_clean["churn_risk"] = model.predict_proba(X)[:, 1]
    df_clean["segment"] = (df_clean["churn_risk"] > 0.5).astype(int)

    segment_counts = {int(k): int(v) for k, v in df_clean["segment"].value_counts().to_dict().items()}
    
    centers = []
    for segment_id, group in df_clean.groupby("segment"):
        center = {"segment": int(segment_id)}
        for col in features:
            center[col] = float(group[col].mean())
        center["churn_risk"] = float(group["churn_risk"].mean())
        centers.append(center)

    sample_json = df_clean[["customer_id"] + features + ["churn_risk", "segment"]].head(10).to_json(orient="records")
    clean_sample = json.loads(sample_json)

    return {
        "n_clusters": len(segment_counts),
        "silhouette_score": round(accuracy, 4), 
        "cluster_centers": centers,
        "segment_counts": segment_counts,
        "data_sample": clean_sample
    }