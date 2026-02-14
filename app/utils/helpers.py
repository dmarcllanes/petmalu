from datetime import datetime

LBS_PER_KG = 2.20462


def kg_to_lbs(kg: float) -> float:
    return round(kg * LBS_PER_KG, 1)


def lbs_to_kg(lbs: float) -> float:
    return round(lbs / LBS_PER_KG, 2)


def format_date(dt: datetime) -> str:
    return dt.strftime("%b %d, %Y")


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%b %d, %Y %I:%M %p")
