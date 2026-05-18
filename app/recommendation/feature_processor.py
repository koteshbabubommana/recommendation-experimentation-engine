def process_features(user_features: dict) -> dict:
    normalized_features = {
        "age_score": min(user_features.get("age", 25) / 100, 1),
        "activity_score": min(user_features.get("activity_level", 5) / 10, 1),
        "purchase_score": min(user_features.get("purchase_count", 1) / 50, 1),
        "engagement_score": min(user_features.get("engagement_score", 0.5), 1)
    }

    normalized_features["combined_user_score"] = round(
        (
            normalized_features["activity_score"] * 0.35
            + normalized_features["purchase_score"] * 0.30
            + normalized_features["engagement_score"] * 0.35
        ),
        4
    )

    return normalized_features