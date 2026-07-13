# SMART LEAD SCORING FUNCTION
def calculate_lead_score(message, service):

    text = message.lower()

    hot_keywords = [
        "urgent",
        "asap",
        "price",
        "pricing",
        "cost",
        "budget",
        "start",
        "today",
        "this week",
        "call me",
        "call back",
        "callback",
        "request a call",
        "request call",
        "book a call",
        "schedule a call",
        "talk to me",
        "contact me",
        "ready",
        "proposal",
        "quote"
    ]

    warm_keywords = [
        "interested",
        "consultation",
        "demo",
        "more details",
        "discuss",
        "meeting"
    ]

    cold_keywords = [
        "just checking",
        "exploring",
        "research",
        "maybe later",
        "not sure",
        "information only"
    ]

    if any(word in text for word in hot_keywords):
        return "Hot Lead"

    elif any(word in text for word in warm_keywords):
        return "Warm Lead"

    elif any(word in text for word in cold_keywords):
        return "Cold Lead"

    else:
        return "Warm Lead"