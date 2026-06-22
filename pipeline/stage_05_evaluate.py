import pandas as pd
import yaml
import joblib
import json
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)


def run():
    config = load_config()
    out = config["data"]["artifact_dir"]

    print("[Stage 05] Evaluating pipeline on test set...")

    test_df = pd.read_csv(f"{out}/raw.csv")

    # same preprocessing as training
    for col in config["binary_columns"]:
        test_df[col] = test_df[col].map({"yes": 1, "no": 0})

    X = test_df.drop(columns=[config["target_column"]])
    y = test_df[config["target_column"]]

    pipeline = joblib.load(f"{out}/house_price_pipeline.joblib")

    y_pred = pipeline.predict(X)

    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
    mae = float(mean_absolute_error(y, y_pred))
    r2 = float(r2_score(y, y_pred))

    print(f"[Stage 05] RMSE : {rmse:.2f}")
    print(f"[Stage 05] MAE  : {mae:.2f}")
    print(f"[Stage 05] R2   : {r2:.4f}")

    report = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "status": "PASSED" if r2 >= 0.6 else "REVIEW"
    }

    with open(f"{out}/evaluation_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("[Stage 05] Evaluation complete")
    return True


if __name__ == "__main__":
    run()