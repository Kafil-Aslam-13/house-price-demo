import pandas as pd
import yaml

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)
    
def run():
    config = load_config()
    df     = pd.read_csv(f"{config['data']['artifact_dir']}/raw.csv")

    print(f"[Stage 02] Validating data...")

    errors=[]

    # check rows 
    if len(df) < 100:
        errors.append(f"Too few rows : {len(df)}")

        if config["target_column"] not in df.columns:
            errors.append(f"Target column '{config['target_column']}' missing")

    empty_cols =[col for col in df.columns if df[col].isnull().all()]
    if empty_cols:
        errors.append(f"fully empty column exists: {empty_cols}")

    
    for col in config["binary_columns"]:
        if col in df.columns:
            unique_vals=df[col].unique().tolist()
            invalid = [v for v in unique_vals if v not in ["yes","no"]]
            if invalid:
                print(f"[Stage 02] WARNING — '{col}' has unexpected values: {invalid}")
    
    if errors:
        for err in errors:
            print (f"stage 2 has Errors - {err}")
        return False
    
    print(f"[Stage 02] Validation passed — {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"[Stage 02] Nulls: {df.isnull().sum().sum()}")
    print(f"[Stage 02] Price range: {df['price'].min()} - {df['price'].max()}")
    return True

if __name__ == "__main__":
    run()