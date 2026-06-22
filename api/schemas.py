from pydantic import BaseModel , Field , ConfigDict
from typing import Literal

class HouseInput(BaseModel):
    model_config=ConfigDict(
        json_schema_extra={"example": {
            "area": 7500, "bedrooms": 4, "bathrooms": 2,
            "stories": 2, "mainroad": "yes", "guestroom": "no",
            "basement": "yes", "hotwaterheating": "no",
            "airconditioning": "yes", "parking": 2,
            "prefarea": "yes", "furnishingstatus": "furnished"
        }}
    )

    area:             int  = Field(..., ge=100, le=20000)
    bedrooms:         int  = Field(..., ge=1,   le=10)
    bathrooms:        int  = Field(..., ge=1,   le=10)
    stories:          int  = Field(..., ge=1,   le=5)
    mainroad:         Literal["yes", "no"]
    guestroom:        Literal["yes", "no"]
    basement:         Literal["yes", "no"]
    hotwaterheating:  Literal["yes", "no"]
    airconditioning:  Literal["yes", "no"]
    parking:          int  = Field(..., ge=0,   le=5)
    prefarea:         Literal["yes", "no"]
    furnishingstatus: Literal["furnished", "semi-furnished", "unfurnished"]


class PredictionOutput(BaseModel):
    predicted_price:  float
    price_range_low:  float
    price_range_high: float