import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def run_segmentation(df: pd.DataFrame, features: list, n_clusters: int = 3) -> dict:
    df_clustered = df.dropna(subset=features).copy()
    
    X = df_clustered[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    score = silhouette_score(X_scaled, clusters) if len(set(clusters)) > 1 else 0.0

    df_clustered["segment"] = clusters
 
    segment_counts = {int(k): int(v) for k, v in df_clustered["segment"].value_counts().to_dict().items()}
    
    cluster_centers_raw = df_clustered.groupby("segment")[features].mean().values.tolist()
    cluster_centers = [[float(val) for val in row] for row in cluster_centers_raw]

    sample_json = df_clustered[["customer_id"] + features + ["segment"]].head(10).to_json(orient="records")
    clean_sample = json.loads(sample_json)

    return {
        "n_clusters": n_clusters,
        "silhouette_score": round(float(score), 4),
        "cluster_centers": cluster_centers,
        "segment_counts": segment_counts,
        "data_sample": clean_sample
    }