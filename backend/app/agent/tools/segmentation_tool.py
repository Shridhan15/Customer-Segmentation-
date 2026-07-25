import pandas as pd
from sklearn.cluster import KMeans

def run_segmentation(df: pd.DataFrame, features: list, n_clusters: int = 3) -> dict:
    valid_features = [f for f in features if f in df.columns]
    X = df[valid_features].fillna(0)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["segment"] = kmeans.fit_predict(X)
    
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=valid_features)
    
    return {
        "n_clusters": n_clusters,
        "features_used": valid_features,
        "cluster_centers": centers.to_dict(orient="records"),
        "segment_counts": df["segment"].value_counts().to_dict()
    }