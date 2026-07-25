import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def run_segmentation(df: pd.DataFrame, features: list, n_clusters: int = 3) -> dict:
    X = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    score = silhouette_score(X_scaled, clusters) if len(set(clusters)) > 1 else 0.0

    df_clustered = df.copy()
    df_clustered["segment"] = clusters
 
    real_cluster_means = df_clustered.groupby("segment")[features].mean().values.tolist()

    return {
        "silhouette_score": round(float(score), 4),
        "cluster_centers": real_cluster_means,
        "data_sample": df_clustered[["customer_id"] + features + ["segment"]].head(10).to_dict(orient="records")
    }