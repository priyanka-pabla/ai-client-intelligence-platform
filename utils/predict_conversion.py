from pathlib import Path
import joblib
import pandas as pd

from utils.feature_extractor import extract_message_features


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "conversion_model.pkl"
)


def load_conversion_model():
    """
    Load the trained conversion prediction pipeline.
    """

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Conversion model not found: {MODEL_FILE}"
        )

    return joblib.load(MODEL_FILE)


def determine_lead_score(
    conversion_probability: float
) -> str:
    """
    Convert conversion probability into a CRM lead score.
    """

    if conversion_probability >= 0.70:
        return "Hot"

    if conversion_probability >= 0.40:
        return "Warm"

    return "Cold"


def build_model_input(
    service: str,
    industry: str,
    company_size: int,
    budget: float | None,
    timeline: str,
    message: str
) -> pd.DataFrame:
    """
    Combine direct form inputs and message-derived features
    into the exact structure expected by the model.
    """

    message_features = extract_message_features(
        message=message
    )

    model_input = {
        "service": service,
        "industry": industry,
        "company_size": company_size,

        "message_length":
            message_features["message_length"],

        "proposal_requested":
            message_features["proposal_requested"],

        "pricing_requested":
            message_features["pricing_requested"],

        "callback_requested":
            message_features["callback_requested"],

        "budget": budget,
        "timeline": timeline,

        "communication_preference":
            message_features[
                "communication_preference"
            ],

        "lead_intent":
            message_features["lead_intent"]
    }

    return pd.DataFrame(
        [model_input]
    )


def predict_conversion(
    service: str,
    industry: str,
    company_size: int,
    budget: float | None,
    timeline: str,
    message: str
) -> dict:
    """
    Predict conversion probability and lead score
    for one customer enquiry.
    """

    model = load_conversion_model()

    model_input = build_model_input(
        service=service,
        industry=industry,
        company_size=company_size,
        budget=budget,
        timeline=timeline,
        message=message
    )
    

    # print("\nMODEL EXPECTED FEATURES")
    # print(model.feature_names_in_.tolist())

    # print("\nPREDICTION INPUT FEATURES")
    # print(model_input.columns.tolist())

    predicted_class = int(
    model.predict(model_input)[0]
    )





    predicted_class = int(
        model.predict(model_input)[0]
    )

    conversion_probability = float(
        model.predict_proba(model_input)[0][1]
    )

    lead_score = determine_lead_score(
        conversion_probability
    )

    return {
        "predicted_conversion": predicted_class,
        "conversion_probability":
            conversion_probability,
        "conversion_percentage":
            round(conversion_probability * 100, 2),
        "lead_score": lead_score
    }



if __name__ == "__main__":

    prediction = predict_conversion(
        service="AI Chatbots",
        industry="Healthcare",
        company_size=25,
        budget=None,
        timeline="Within 2 weeks",
        message=(
            "We are ready to start and need a WhatsApp "
            "chatbot. Please send a quotation and call me."
        )
    )

    print("\nCONVERSION PREDICTION")
    print("=" * 50)

    for key, value in prediction.items():
        print(f"{key}: {value}")