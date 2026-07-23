import re


def calculate_message_length(message: str) -> int:
    """
    Count the number of words in the customer message.
    """

    if not message:
        return 0

    return len(message.split())


def contains_keyword(
    message: str,
    keywords: list[str]
) -> int:
    """
    Return 1 if any keyword is found in the message,
    otherwise return 0.
    """

    message_lower = message.lower()

    for keyword in keywords:
        if keyword in message_lower:
            return 1

    return 0


def extract_proposal_requested(message: str) -> int:
    """
    Detect whether the customer is requesting a proposal.
    """

    keywords = [
        "proposal",
        "send a proposal",
        "business proposal",
        "project proposal",
        "formal proposal"
    ]

    return contains_keyword(
        message=message,
        keywords=keywords
    )


def extract_pricing_requested(message: str) -> int:
    """
    Detect whether the customer is asking about pricing.
    """

    keywords = [
        "price",
        "pricing",
        "cost",
        "quotation",
        "quote",
        "how much",
        "charges",
        "package"
    ]

    return contains_keyword(
        message=message,
        keywords=keywords
    )


def extract_callback_requested(message: str) -> int:
    """
    Detect whether the customer wants to be contacted.
    """

    keywords = [
        "call me",
        "call us",
        "contact me",
        "contact us",
        "give me a call",
        "schedule a call",
        "arrange a call",
        "speak with",
        "discuss over a call"
    ]

    return contains_keyword(
        message=message,
        keywords=keywords
    )


def extract_communication_preference(message: str) -> str:
    """
    Detect the customer's preferred communication channel.
    """

    message_lower = message.lower()

    if "whatsapp" in message_lower:
        return "WhatsApp"

    if any(
        phrase in message_lower
        for phrase in [
            "video call",
            "zoom",
            "google meet"
        ]
    ):
        return "Video Call"

    if "microsoft teams" in message_lower or "teams call" in message_lower:
        return "Microsoft Teams"

    if any(
        phrase in message_lower
        for phrase in [
            "phone call",
            "call me",
            "give me a call",
            "call us"
        ]
    ):
        return "Phone Call"

    if any(
        phrase in message_lower
        for phrase in [
            "email me",
            "send me an email",
            "send details by email"
        ]
    ):
        return "Email"

    return "Email"


def extract_lead_intent(message: str) -> str:
    """
    Classify the lead as Ready to Buy,
    Considering, or Exploring.
    """

    message_lower = message.lower()

    ready_to_buy_keywords = [
        "ready to start",
        "want to proceed",
        "need immediately",
        "need this immediately",
        "start the project",
        "send a proposal",
        "send a quotation",
        "send a quote",
        "schedule a call",
        "book a call",
        "looking to hire",
        "ready to move forward"
    ]

    considering_keywords = [
        "interested in",
        "would like to know",
        "need more information",
        "can you explain",
        "looking for",
        "considering",
        "want to discuss",
        "exploring options",
        "please share details"
    ]

    if any(
        keyword in message_lower
        for keyword in ready_to_buy_keywords
    ):
        return "Ready to Buy"

    if any(
        keyword in message_lower
        for keyword in considering_keywords
    ):
        return "Considering"

    return "Exploring"


def extract_message_features(message: str) -> dict:
    """
    Convert a customer message into all message-based
    features required by the machine-learning model.
    """

    cleaned_message = re.sub(
        pattern=r"\s+",
        repl=" ",
        string=message.strip()
    )

    features = {
        "message_length": calculate_message_length(
            cleaned_message
        ),

        "proposal_requested": extract_proposal_requested(
            cleaned_message
        ),

        "pricing_requested": extract_pricing_requested(
            cleaned_message
        ),

        "callback_requested": extract_callback_requested(
            cleaned_message
        ),

        "communication_preference":
            extract_communication_preference(
                cleaned_message
            ),

        "lead_intent": extract_lead_intent(
            cleaned_message
        )
    }

    return features



if __name__ == "__main__":

    test_message = """
    Please send me a quotation.
    We are ready to start immediately.
    Contact me on WhatsApp.
    """

    extracted_features = extract_message_features(
        test_message
    )

    print("\nEXTRACTED MESSAGE FEATURES")
    print("=" * 50)

    for feature_name, feature_value in extracted_features.items():
        print(
            f"{feature_name}: {feature_value}"
        )