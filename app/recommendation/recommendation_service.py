from app.recommendation.feature_processor import process_features
from app.recommendation.ranking_engine import rank_items
from app.experimentation.ab_testing import assign_experiment_group


def generate_recommendations(user_id: str, candidate_items: list, user_features: dict, experiment_name: str):
    experiment_group = assign_experiment_group(user_id, experiment_name)

    processed_features = process_features(user_features)

    ranked_items = rank_items(
        candidate_items=candidate_items,
        processed_features=processed_features,
        experiment_group=experiment_group
    )

    return {
        "experiment_group": experiment_group,
        "recommendations": ranked_items[:5],
        "top_score": ranked_items[0]["ranking_score"] if ranked_items else 0
    }