import pandas as pd
import yaml
import joblib
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor


def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)


def run():
    config = load_config()
    out = config["data"]["artifact_dir"]

    print("[Stage 04] Training model...")

    df = pd.read_csv(f"{out}/raw.csv")

    # MUST match Stage 3 exactly
    for col in config["binary_columns"]:
        df[col] = df[col].map({"yes": 1, "no": 0})

    X = df.drop(columns=[config["target_column"]])
    y = df[config["target_column"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["model"]["test_size"],
        random_state=config["model"]["random_state"]
    )

    preprocessor = joblib.load(f"{out}/preprocessor.joblib")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBRegressor(
            n_estimators=config["model"]["n_estimators"],
            max_depth=config["model"]["max_depth"],
            learning_rate=config["model"]["learning_rate"],
            random_state=config["model"]["random_state"],
            verbosity=0
        ))
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print(f"[Stage 04] RMSE: {rmse:.2f}")
    print(f"[Stage 04] R2  : {r2:.4f}")

    # SAVE ONLY FINAL PIPELINE
    joblib.dump(pipeline, f"{out}/house_price_pipeline.joblib")

    print("[Stage 04] Saved final pipeline")


if __name__ == "__main__":
    run()