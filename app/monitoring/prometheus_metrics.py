from prometheus_client import Counter, Histogram

recommendation_requests_total = Counter(
    "recommendation_requests_total",
    "Total number of recommendation requests"
)

experiment_assignments_total = Counter(
    "experiment_assignments_total",
    "Total number of experiment assignment requests"
)

recommendation_latency_seconds = Histogram(
    "recommendation_latency_seconds",
    "Recommendation request latency in seconds"
)