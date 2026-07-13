import pandas as pd

def parse_submitted_at(value):
    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    # Old format: 6/12/2026 22:22
    if "/" in value:
        return pd.to_datetime(value, format="%m/%d/%Y %H:%M", errors="coerce")

    # New format: 12-06-2026 10:22 PM
    if "-" in value:
        return pd.to_datetime(value, format="%d-%m-%Y %I:%M %p", errors="coerce")

    return pd.to_datetime(value, errors="coerce")


def calculate_reply_deadline(row):
    submitted_time = row["Submitted DateTime"]
    now = pd.Timestamp.now()

    if pd.isna(submitted_time):
        return "Unknown"

    if row["Lead Status"] in ["Won", "Lost"]:
        return "Closed"

    if row["Lead Score"] == "Hot Lead":
        deadline = submitted_time + pd.Timedelta(hours=1)

    elif row["Lead Score"] == "Warm Lead":
        deadline = submitted_time + pd.Timedelta(hours=24)

    else:
        return "No urgent deadline"

    time_left = deadline - now

    if time_left.total_seconds() <= 0:
        return "Overdue"

    hours = int(time_left.total_seconds() // 3600)
    minutes = int((time_left.total_seconds() % 3600) // 60)

    return f"{hours}h {minutes}m left"


