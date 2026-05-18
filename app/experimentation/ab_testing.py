import hashlib


def assign_experiment_group(user_id: str, experiment_name: str) -> str:
    key = f"{experiment_name}:{user_id}"
    hash_value = int(hashlib.sha256(key.encode()).hexdigest(), 16)

    bucket = hash_value % 100

    if bucket < 50:
        return "control"

    return "treatment"