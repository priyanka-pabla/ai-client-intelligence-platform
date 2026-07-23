from pathlib import Path
import pandas as pd
import joblib
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "synthetic_leads.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "conversion_model.pkl"
)


def load_dataset(
    data_file: Path
) -> pd.DataFrame:
    """
    Load the synthetic lead dataset from a CSV file.
    """

    if not data_file.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_file}"
        )

    dataset = pd.read_csv(
        data_file
    )

    return dataset

def inspect_dataset(
    dataset: pd.DataFrame
) -> None:
    """
    Display basic information about the dataset.
    """

    print("\n" + "=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)

    print(f"Rows: {dataset.shape[0]}")
    print(f"Columns: {dataset.shape[1]}")

    print("\nFirst 5 rows:")
    print(dataset.head())

    print("\nColumn Information:")
    dataset.info()

    print("\nSummary Statistics:")
    print(dataset.describe())

    print("\nTarget Distribution:")
    print(dataset["converted"].value_counts())

    print("=" * 70)


def prepare_features_and_target(dataset):

    X = dataset.drop(
        columns=[
            "persona_id",
            "persona_name",
            "company",
            "name",
            "decision_maker",
            "message",
            "technical_maturity",
            "base_conversion_probability",
            "conversion_probability",
            "lead_category",
            "converted"
        ]
    )

    y = dataset["converted"]

    return X, y


from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


def create_preprocessor(X):

    categorical_columns = X.select_dtypes(
        include=["object", "str"]
    ).columns.tolist()

    numerical_columns = X.select_dtypes(
        exclude=["object", "str"]
    ).columns.tolist()

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore")
            )
        ]
    )

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            ),
            (
                "numerical",
                numerical_pipeline,
                numerical_columns
            )
        ]
    )

    return preprocessor

def create_model_pipeline(
    preprocessor,
    classifier
):

    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "classifier",
                classifier
            )
        ]
    )

    return model_pipeline


def evaluate_model(
    model_name,
    model_pipeline,
    X_test,
    y_test
) -> None:
    """
    Evaluate the trained model using unseen testing data.
    """

    y_pred = model_pipeline.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print("\n" + "=" * 70)
    print(f"{model_name.upper()} EVALUATION")
    print("=" * 70)

    print(
        f"\nAccuracy: {accuracy:.2%}"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("=" * 70)


def display_feature_importance(
    model_pipeline,
    top_n=15
) -> None:
    """
    Display the features that have the strongest influence
    on Logistic Regression predictions.
    """

    fitted_preprocessor = model_pipeline.named_steps[
        "preprocessor"
    ]

    trained_classifier = model_pipeline.named_steps[
        "classifier"
    ]

    feature_names = fitted_preprocessor.get_feature_names_out()

    coefficients = trained_classifier.coef_[0]

    feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "importance": abs(coefficients)
        }
    )

    feature_importance = feature_importance.sort_values(
        by="importance",
        ascending=False
    )

    print("\n" + "=" * 70)
    print("LOGISTIC REGRESSION FEATURE IMPACT")
    print("=" * 70)

    print(
        feature_importance[
            [
                "feature",
                "coefficient"
            ]
        ].head(top_n).to_string(
            index=False
        )
    )

    print("=" * 70)





if __name__ == "__main__":

    # ==============================================================
    # Load Dataset
    # ==============================================================

    dataset = load_dataset(
        data_file=DATA_FILE
    )

    inspect_dataset(
        dataset=dataset
    )
    
    # print("\nIndustry values:")
    # print(dataset["industry"].unique())

    # print("\nTimeline values:")
    # print(dataset["timeline"].unique())

    # print("\nCompany size dtype:")
    # print(dataset["company_size"].dtype)

    # print("\nBudget dtype:")
    # print(dataset["budget"].dtype)

    # print("\nMissing budget values:")
    # print(dataset["budget"].isna().sum())





    X, y = prepare_features_and_target(
        dataset=dataset
    )

    print("\nMODEL FEATURES")
    print("=" * 70)
    print(X.columns.tolist())

    # ==============================================================
    # Train-Test Split
    # ==============================================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTRAIN-TEST SPLIT")
    print("=" * 70)

    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}")

    print("\nTraining target distribution:")
    print(y_train.value_counts())

    print("\nTesting target distribution:")
    print(y_test.value_counts())

    # ==============================================================
    # Logistic Regression Model
    # ==============================================================

    logistic_preprocessor = create_preprocessor(
        X=X_train
    )

    logistic_regression = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    logistic_pipeline = create_model_pipeline(
        preprocessor=logistic_preprocessor,
        classifier=logistic_regression
    )

    logistic_pipeline.fit(
        X_train,
        y_train
    )

    evaluate_model(
        model_name="Logistic Regression",
        model_pipeline=logistic_pipeline,
        X_test=X_test,
        y_test=y_test
    )

    display_feature_importance(
        model_pipeline=logistic_pipeline,
        top_n=15
    )

    # ==============================================================
    # Random Forest Model
    # ==============================================================

    random_forest_preprocessor = create_preprocessor(
        X=X_train
    )

    random_forest = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    random_forest_pipeline = create_model_pipeline(
        preprocessor=random_forest_preprocessor,
        classifier=random_forest
    )

    random_forest_pipeline.fit(
        X_train,
        y_train
    )

    evaluate_model(
        model_name="Random Forest",
        model_pipeline=random_forest_pipeline,
        X_test=X_test,
        y_test=y_test
    )

    # ==============================================================
    # Save Best Model (Logistic Regression)
    # Logistic Regression achieved better performance
    # and is selected as the production model.
    # ==============================================================

    MODEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        logistic_pipeline,
        MODEL_FILE
    )

    print("\n" + "=" * 70)
    print("MODEL SAVED")
    print("=" * 70)
    print(f"Best model saved successfully:\n{MODEL_FILE}")
    print("=" * 70)