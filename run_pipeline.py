from pipeline.stage_01_ingest import run as ingest
from pipeline.stage_02_validate import run as validate
from pipeline.stage_03_preprocess import run as preprocess
from pipeline.stage_04_train     import run as train
from pipeline.stage_05_evaluate  import run as evaluate

import sys

if __name__ == "__main__":
    print("=" * 50)
    print("HOUSE PRICE DEMO — PIPELINE")
    print("=" * 50)

    steps = [
        ("Ingestion",     ingest),
        ("Validation",    validate),
        ("Preprocessing", preprocess),
        ("Training",      train),
        ("Evaluation",    evaluate),
    ]

    for name, step in steps:
        print(f"\nRunning {name}...")
        if step() is False:
            print(f"Pipeline stopped at {name}")
            sys.exit(1)

    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    print("=" * 50)