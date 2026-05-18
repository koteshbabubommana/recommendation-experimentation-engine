import hashlib
from typing import List


def stable_item_score(item_id: str) -> float:
    hash_value = int(hashlib.sha256(item_id.encode()).hexdigest(), 16)
    return round((hash_value % 1000) / 1000, 4)


def rank_items(candidate_items: List[str], processed_features: dict, experiment_group: str) -> list:
    user_score = processed_features["combined_user_score"]

    ranked_items = []

    for item in candidate_items:
        item_score = stable_item_score(item)

        if experiment_group == "treatment":
            final_score = (item_score * 0.55) + (user_score * 0.45)
        else:
            final_score = (item_score * 0.75) + (user_score * 0.25)

        ranked_items.append({
            "item_id": item,
            "ranking_score": round(final_score, 4)
        })

    ranked_items.sort(key=lambda x: x["ranking_score"], reverse=True)

    return ranked_items