from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "annual_income", "total_balance", "successful_transactions",
    "total_transaction_value", "average_transaction_value",
    "products_owned", "customer_tenure_years"
]


def fit_customer_segments(customer_360: pd.DataFrame, k_min: int = 3, k_max: int = 6, random_state: int = 42):
    """Segment active customers; keep inactive customers as an explicit operational segment.

    This avoids a trivial ML result where customers with zero successful transactions
    dominate the clustering objective. Cluster count is selected by silhouette score
    over a business-relevant candidate range.
    """
    df = customer_360.copy()
    active_mask = df["successful_transactions"].gt(0)
    active = df.loc[active_mask].copy()
    inactive = df.loc[~active_mask].copy()

    X = active[FEATURES].replace([np.inf, -np.inf], np.nan).fillna(0)
    for col in ["annual_income", "total_balance", "successful_transactions", "total_transaction_value", "average_transaction_value"]:
        X[col] = np.log1p(X[col].clip(lower=0))

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    max_k = min(k_max, max(3, len(active) - 1))
    evaluations = []
    models = {}
    for k in range(k_min, max_k + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=20)
        labels = model.fit_predict(Xs)
        score = silhouette_score(Xs, labels)
        evaluations.append({"k": k, "silhouette_score": float(score)})
        models[k] = (model, labels)

    evaluation_df = pd.DataFrame(evaluations)
    best_k = int(evaluation_df.loc[evaluation_df.silhouette_score.idxmax(), "k"])
    model, labels = models[best_k]

    active_out = active[["customer_id"]].copy()
    active_out["cluster_id"] = labels
    active_out = active_out.merge(active, on="customer_id", how="left")
    inactive_out = inactive[["customer_id"]].copy()
    inactive_out["cluster_id"] = -1
    inactive_out = inactive_out.merge(inactive, on="customer_id", how="left")

    result = pd.concat([active_out, inactive_out], ignore_index=True)
    result = result.sort_values("customer_id").reset_index(drop=True)

    profile = (active_out.groupby("cluster_id")
               .agg(customers=("customer_id","count"),
                    median_income=("annual_income","median"),
                    median_balance=("total_balance","median"),
                    median_transactions=("successful_transactions","median"),
                    median_transaction_value=("total_transaction_value","median"),
                    median_products=("products_owned","median"))
               .reset_index())

    rank_value = profile.set_index("cluster_id")["median_balance"].rank(pct=True)
    rank_activity = profile.set_index("cluster_id")["median_transactions"].rank(pct=True)
    names = {}
    for cid in profile.cluster_id:
        v = rank_value.loc[cid]
        a = rank_activity.loc[cid]
        if v >= .67 and a >= .67:
            name = "High Value & Active"
        elif a >= .67:
            name = "High Activity"
        elif v >= .67:
            name = "Balance Oriented"
        elif v <= .34 and a <= .34:
            name = "Lower Activity"
        else:
            name = "Balanced"
        names[cid] = name

    result["segment_name"] = result["cluster_id"].map(names).fillna("Inactive / No Successful Transactions")
    result["model_k"] = best_k
    return result, evaluation_df, profile
