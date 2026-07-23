import random
import csv
import json
from collections import Counter
from pathlib import Path
from utils.persona_loader import load_personas


PROJECT_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "synthetic_leads.csv"
)

MARKET_CONFIG_FILE = (
    PROJECT_DIR
    / "config"
    / "market_distribution.json"
)

def make_budget_optional(budget, missing_probability=0.25):
    """
    Removes the visible budget for some synthetic leads.

    A missing_probability of 0.25 means approximately
    25% of leads will have no budget information.
    """

    if random.random() < missing_probability:
        return None

    return budget


def load_market_distribution(
    config_file: Path
) -> dict:
    """
    Load the market-distribution configuration.

    The configuration controls how frequently each
    buyer persona should appear in the synthetic dataset.
    """

    if not config_file.exists():
        raise FileNotFoundError(
            f"Market configuration file not found: "
            f"{config_file}"
        )

    with config_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        market_config = json.load(file)

    if "persona_weights" not in market_config:
        raise ValueError(
            "The market configuration must contain "
            "'persona_weights'."
        )

    if not isinstance(
        market_config["persona_weights"],
        dict
    ):
        raise ValueError(
            "'persona_weights' must be a JSON object."
        )

    return market_config

    

def select_personas_for_dataset(
    personas: list[dict],
    total_leads: int,
    market_config: dict
) -> list[dict]:
    """
    Select personas for the complete synthetic dataset.

    Rules:
    1. Every persona appears at least once when enough
       leads are requested.
    2. Remaining personas are selected according to the
       centralized market-distribution configuration.
    3. Personas with higher weights appear more often.
    """

    if total_leads <= 0:
        raise ValueError(
            "total_leads must be greater than zero."
        )

    if not personas:
        raise ValueError(
            "No buyer personas were loaded."
        )

    number_of_personas = len(personas)

    # It is impossible to include every persona when
    # fewer leads than personas are requested.
    if total_leads < number_of_personas:
        return random.sample(
            personas,
            total_leads
        )

    # Guarantee one lead from every persona.
    selected_personas = personas.copy()

    remaining_leads = (
        total_leads - number_of_personas
    )

    persona_weights = market_config[
        "persona_weights"
    ]

    default_weight = market_config.get(
        "default_weight",
        1
    )

    weights = []

    for persona in personas:
        persona_id = persona["persona_id"]

        weight = persona_weights.get(
            persona_id,
            default_weight
        )

        weight = max(
            float(weight),
            0
        )

        weights.append(weight)

    # Prevent random.choices() from failing if every
    # configured weight is accidentally set to zero.
    if sum(weights) == 0:
        weights = [1] * number_of_personas

    weighted_personas = random.choices(
        population=personas,
        weights=weights,
        k=remaining_leads
    )

    selected_personas.extend(
        weighted_personas
    )

    # Mix the guaranteed and weighted leads together.
    random.shuffle(
        selected_personas
    )

    return selected_personas

def select_lead_intent(persona: dict) -> dict:
    """
    Select a lead intent using weighted probability.

    For example:
    Exploring may appear 30% of the time.
    Interested may appear 45% of the time.
    Ready to Buy may appear 25% of the time.
    """

    intents = persona["lead_intents"]

    return random.choices(
        population=intents,
        weights=[intent["weight"] for intent in intents],
        k=1
    )[0]

def add_customer_request(message):

    customer_requests = [
        "",
        "",
        "",
        "",
        " Please send us a proposal.",
        " Could you share your pricing?",
        " Please provide a quotation.",
        " Please give me a call.",
        " Could someone call me tomorrow?",
        " Could you arrange a demo?"
    ]

    return message + random.choice(customer_requests)


def generate_message(
    persona: dict,
    lead_intent: dict,
    timeline: str
) -> str:
    """
    Build a message whose wording matches the lead intent.
    """

    opening = random.choice(
        lead_intent["message_openings"]
    )

    problem = random.choice(
        persona["message_problems"]
    )

    solution = random.choice(
        persona["message_solutions"]
    )

    message = (
        f"{opening} {solution} to help with {problem}. "
        f"Our preferred timeline is {timeline.lower()}."
    )
    
    message = add_customer_request(message)
    return message


def calculate_message_length(message: str) -> int:
    """
    Count the number of words in the lead message.
    """

    return len(message.split())


def extract_proposal_requested(message: str) -> int:
    """
    Return 1 if the message asks for a proposal.
    Otherwise, return 0.
    """

    proposal_keywords = [
        "proposal",
        "send us a proposal",
        "share a proposal",
        "provide a proposal"
    ]

    message_lower = message.lower()

    return int(
        any(
            keyword in message_lower
            for keyword in proposal_keywords
        )
    )


def extract_pricing_requested(message: str) -> int:
    """
    Return 1 if the message asks about pricing or cost.
    Otherwise, return 0.
    """

    pricing_keywords = [
        "price",
        "pricing",
        "cost",
        "quotation",
        "quote",
        "budget"
    ]

    message_lower = message.lower()

    return int(
        any(
            keyword in message_lower
            for keyword in pricing_keywords
        )
    )


def extract_callback_requested(message: str) -> int:
    """
    Return 1 if the message requests a call or callback.
    Otherwise, return 0.
    """

    callback_keywords = [
        "call me",
        "call us",
        "contact me",
        "contact us",
        "give me a call",
        "give us a call",
        "callback",
        "schedule a call"
    ]

    message_lower = message.lower()

    return int(
        any(
            keyword in message_lower
            for keyword in callback_keywords
        )
    )

def calculate_conversion_probability(
    persona: dict,
    lead_intent: dict,
    timeline: str
) -> float:
    """
    Calculate a synthetic conversion probability.

    Start with the persona's base probability, then adjust it
    according to the generated lead's intent and timeline.
    """

    probability = persona["base_conversion_probability"]

    probability += lead_intent[
        "probability_adjustment"
    ]

    if timeline == "Immediately":
        probability += 0.15

    elif timeline == "Within 2 weeks":
        probability += 0.08

    elif timeline == "Within 1 month":
        probability += 0.02

    # Keep probability between 5% and 95%.
    probability = max(0.05, min(probability, 0.95))

    return round(probability, 2)


def determine_lead_category(
    conversion_probability: float
) -> str:
    """
    Convert probability into Cold, Warm or Hot.
    """

    if conversion_probability >= 0.70:
        return "Hot"

    if conversion_probability >= 0.40:
        return "Warm"

    return "Cold"


def generate_lead(persona: dict) -> dict:
    """
    Generate one synthetic lead.
    """

    # ----------------------------------------
    # Generate lead information
    # ----------------------------------------

    timeline = random.choice(
        persona["possible_timelines"]
    )

    lead_intent = select_lead_intent(persona)

    message = generate_message(
        persona=persona,
        lead_intent=lead_intent,
        timeline=timeline
    )

    # ----------------------------------------
    # Extract message features
    # ----------------------------------------

    message_length = calculate_message_length(message)

    proposal_requested = extract_proposal_requested(message)

    pricing_requested = extract_pricing_requested(message)

    callback_requested = extract_callback_requested(message)

    # ----------------------------------------
    # Calculate conversion
    # ----------------------------------------

    conversion_probability = (
        calculate_conversion_probability(
            persona=persona,
            lead_intent=lead_intent,
            timeline=timeline
        )
    )

    converted = int(
        random.random() < conversion_probability
    )

    lead_category = determine_lead_category(
        conversion_probability
    )

    employee_count = random.randint(
        persona["company_size"]["min_employees"],
        persona["company_size"]["max_employees"]
    )

    budget = random.randint(
    persona["budget"]["min"],
    persona["budget"]["max"]
    )

    visible_budget = make_budget_optional(
        budget=budget,
        missing_probability=0.25
    )



    # ----------------------------------------
    # Build lead dictionary
    # ----------------------------------------

    lead = {
        "persona_id": persona["persona_id"],
        "persona_name": persona["persona_name"],

        "company": random.choice(
            persona["sample_company_names"]
        ),

        "name": random.choice(
            persona["sample_contact_names"]
        ),

        "decision_maker": random.choice(
            persona["decision_makers"]
        ),

        "service": persona["service"],

        "industry": persona["industry"],

        "company_size": employee_count,

        "technical_maturity": persona[
            "technical_maturity"
        ],

        "message": message,

        # ---------- NEW FEATURES ----------

        "message_length": message_length,

        "proposal_requested": proposal_requested,

        "pricing_requested": pricing_requested,

        "callback_requested": callback_requested,

        # ----------------------------------

        "budget": visible_budget,

        "timeline": timeline,

        "communication_preference": random.choice(
            persona["communication_preferences"]
        ),

        "lead_intent": lead_intent["intent"],

        "base_conversion_probability": persona[
            "base_conversion_probability"
        ],

        "conversion_probability": conversion_probability,

        "lead_category": lead_category,

        "converted": converted
    }

    return lead


def generate_multiple_leads(
    personas: list[dict],
    number_of_leads: int,
    market_config: dict
) -> list[dict]:
    """
    Generate the requested number of synthetic leads.

    Persona frequency is controlled by the selected
    market-distribution configuration.
    """

    leads = []

    selected_personas = (
        select_personas_for_dataset(
            personas=personas,
            total_leads=number_of_leads,
            market_config=market_config
        )
    )

    for selected_persona in selected_personas:
        lead = generate_lead(
            selected_persona
        )

        leads.append(
            lead
        )

    return leads

def save_leads_to_csv(
    leads: list[dict],
    output_file: Path
) -> None:
    """
    Save generated synthetic leads to a CSV file.
    """

    if not leads:
        raise ValueError("There are no leads to save.")

    # Create the data folder if it doesn't exist
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Use the dictionary keys as CSV column names
    fieldnames = list(leads[0].keys())

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(leads)

    print(
        f"\n✅ Synthetic leads saved successfully!"
    )

    print(
        f"Location: {output_file}"
    )

def print_persona_distribution(
    leads: list[dict],
    market_config: dict
) -> None:
    """
    Print the number and percentage of generated leads
    for each persona.
    """

    if not leads:
        print("\nNo leads available for distribution report.")
        return

    persona_counts = Counter(
        lead["persona_id"]
        for lead in leads
    )

    total_leads = len(leads)

    configured_weights = market_config.get(
        "persona_weights",
        {}
    )

    print("\n" + "=" * 70)
    print("PERSONA DISTRIBUTION REPORT")
    print("=" * 70)

    print(
        f"{'Persona ID':<20}"
        f"{'Count':>10}"
        f"{'Percentage':>15}"
        f"{'Weight':>10}"
    )

    print("-" * 70)

    for persona_id in sorted(persona_counts):
        count = persona_counts[persona_id]

        percentage = (
            count / total_leads
        ) * 100

        configured_weight = configured_weights.get(
            persona_id,
            market_config.get("default_weight", 1)
        )

        print(
            f"{persona_id:<20}"
            f"{count:>10}"
            f"{percentage:>14.1f}%"
            f"{configured_weight:>10}"
        )

    print("-" * 70)

    print(
        f"{'TOTAL':<20}"
        f"{total_leads:>10}"
        f"{100:>14.1f}%"
    )

    missing_personas = [
        persona_id
        for persona_id in configured_weights
        if persona_id not in persona_counts
    ]

    if missing_personas:
        print("\n⚠ Missing personas:")

        for persona_id in missing_personas:
            print(f"  - {persona_id}")

    else:
        print("\n✅ Every configured persona appears in the dataset.")

    print("=" * 70)


if __name__ == "__main__":
    buyer_personas = load_personas()

    market_distribution = (
        load_market_distribution(
            MARKET_CONFIG_FILE
        )
    )

    print(
        f"\nMarket configuration: "
        f"{market_distribution.get('market_name', 'Unknown')}"
    )

    synthetic_leads = generate_multiple_leads(
        personas=buyer_personas,
        number_of_leads=1000,
        market_config=market_distribution
    )

    save_leads_to_csv(
        leads=synthetic_leads,
        output_file=OUTPUT_FILE
    )

    print_persona_distribution(
        leads=synthetic_leads,
        market_config=market_distribution
    )

    # print(
    #     f"\nGenerated {len(synthetic_leads)} "
    #     f"Synthetic Leads"
    # )

    # print("=" * 70)

    # for lead_number, lead in enumerate(
    #     synthetic_leads,
    #     start=1
    # ):
    #     print(f"\nLead {lead_number}")
    #     print("-" * 70)

    #     for field, value in lead.items():
    #         print(f"{field}: {value}")

    # print("\n" + "=" * 70)