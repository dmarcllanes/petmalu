from app.models.weight_models import WeightLogResponse


def analyze_trend(logs: list[WeightLogResponse]) -> str:
    if len(logs) < 2:
        return "insufficient_data"

    # logs are ordered most-recent first
    recent = logs[0].weight_kg
    oldest = logs[-1].weight_kg

    if oldest == 0:
        return "insufficient_data"

    change_pct = (recent - oldest) / oldest

    if change_pct > 0.02:
        return "gaining"
    elif change_pct < -0.02:
        return "losing"
    return "stable"
