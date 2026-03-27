from fastapi import FastAPI
from pydantic import BaseModel
from inference import predict

app = FastAPI(title="KYC Risk Scoring API")

class CustomerInput(BaseModel):
    AGE_YR_CT: float
    CUST_GNDR_CD: str
    CUST_TYPE_CD: str
    CTZSHP_CNTRY1_CD: str
    COUNTRY_OF_INC: str
    RES_CNTRY_CD: str
    PEP_FL: str
    ANNL_INCM_BASE_AM: float

@app.post("/predict")
def predict_risk(data: CustomerInput):
    result = predict(data.dict())
    return {"risk_class": result}
