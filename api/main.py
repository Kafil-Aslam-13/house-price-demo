import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from api.schemas import HouseInput, PredictionOutput

app = FastAPI(title="House Price Demo App", version="1.0.0")

# LOAD PIPELINE ONLY
try:
    pipeline = joblib.load("artifacts/house_price_pipeline.joblib")
except Exception as e:
    pipeline = None
    print(f"Warning: {e}")


@app.get("/")
def health():
    return {
        "status": "running",
        "model_loaded": pipeline is not None
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(house: HouseInput):

    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    bmap = {"yes": 1, "no": 0}

    try:
        df = pd.DataFrame([{
            "area": house.area,
            "bedrooms": house.bedrooms,
            "bathrooms": house.bathrooms,
            "stories": house.stories,
            "parking": house.parking,
            "furnishingstatus": house.furnishingstatus,

            "mainroad": bmap[house.mainroad],
            "guestroom": bmap[house.guestroom],
            "basement": bmap[house.basement],
            "hotwaterheating": bmap[house.hotwaterheating],
            "airconditioning": bmap[house.airconditioning],
            "prefarea": bmap[house.prefarea],
}])

        price = float(pipeline.predict(df)[0])

        return PredictionOutput(
            predicted_price=round(price, 2),
            price_range_low=round(price * 0.90, 2),
            price_range_high=round(price * 1.10, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))