import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
PERSONA_FOLDER = PROJECT_DIR / "data" / "personas"


def load_personas() -> list[dict]:
    """
    Load and combine personas from all JSON files
    inside the data/personas folder.
    """

    if not PERSONA_FOLDER.exists():
        raise FileNotFoundError(
            f"Persona folder not found: {PERSONA_FOLDER}"
        )

    all_personas = []

    for file_path in sorted(PERSONA_FOLDER.glob("*.json")):
        with file_path.open("r", encoding="utf-8") as file:
            personas = json.load(file)

        if not isinstance(personas, list):
            raise ValueError(
                f"{file_path.name} must contain a JSON list."
            )

        all_personas.extend(personas)

    if not all_personas:
        raise ValueError(
            "No buyer personas were found."
        )

    return all_personas