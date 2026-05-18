from app.experimentation.ab_testing import assign_experiment_group


def get_experiment_assignment(user_id: str, experiment_name: str):
    group = assign_experiment_group(user_id, experiment_name)

    return {
        "user_id": user_id,
        "experiment_name": experiment_name,
        "experiment_group": group,
        "allocation_strategy": "hash_based_50_50_split"
    }