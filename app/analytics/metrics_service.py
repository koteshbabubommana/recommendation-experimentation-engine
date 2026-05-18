def summarize_recommendations(logs):
    total_requests = len(logs)

    if total_requests == 0:
        return {
            "total_recommendation_requests": 0,
            "average_top_score": 0,
            "control_count": 0,
            "treatment_count": 0,
            "cache_hit_rate": 0
        }

    average_top_score = sum(log.top_score for log in logs) / total_requests
    control_count = sum(1 for log in logs if log.experiment_group == "control")
    treatment_count = sum(1 for log in logs if log.experiment_group == "treatment")
    cached_count = sum(1 for log in logs if log.cached)

    return {
        "total_recommendation_requests": total_requests,
        "average_top_score": round(average_top_score, 4),
        "control_count": control_count,
        "treatment_count": treatment_count,
        "cache_hit_rate": round(cached_count / total_requests, 4)
    }


def summarize_events(events):
    total_events = len(events)

    event_counts = {}

    for event in events:
        event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1

    return {
        "total_events": total_events,
        "event_breakdown": event_counts
    }