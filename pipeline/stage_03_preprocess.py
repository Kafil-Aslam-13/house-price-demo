import pandas as pd
import yaml
import joblib
from pathlib import Path

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)


def run():
    config = load_config()
    out = config["data"]["artifact_dir"]

    print("[Stage 03] Building preprocessor...")

    df = pd.read_csv(f"{out}/raw.csv")

    # binary encoding
    for col in config["binary_columns"]:
        df[col] = df[col].map({"yes": 1, "no": 0})

    X = df.drop(columns=[config["target_column"]])

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    binary_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, config["numeric_columns"]),
        ("cat", categorical_pipeline, config["categorical_columns"]),
        ("bin", binary_pipeline, config["binary_columns"])
    ])

    preprocessor.fit(X)

    Path(out).mkdir(parents=True, exist_ok=True)

    joblib.dump(preprocessor, f"{out}/preprocessor.joblib")


    print("[Stage 03] Features created:",
          preprocessor.fit(X).transform(X).shape[1])

    print("[Stage 03] Saved preprocessor")


if __name__ == "__main__":
    run()