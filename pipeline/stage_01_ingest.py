import pandas as pd
import yaml 
import os
from pathlib import Path


def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)
    

def run():
    config = load_config()
    source=config["data"]["source_path"]
    out=config["data"]["artifact_dir"]

    print(f"[stage 1] Reading data from {source}")

    if not os.path.exists(source):
        print(f"Error - file not found{source}")
        return False
    
    df=pd.read_csv(source)

    print(f" Data Loaded {df.shape[0]} rows and {df.shape[1]} columns")
    Path(out).mkdir(parents=True,exist_ok=True)
    df.to_csv(f"{out}/raw.csv",index=False)
    print("[Stage 01] Data Ingestion complete")
    return True

if __name__=="__main__":
    run()
