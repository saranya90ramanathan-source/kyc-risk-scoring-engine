from fastapi import FastAPI
from pydantic import BaseModel
from inference import predict

app = FastAPI(title="KYC Risk Scoring API")

# -------------------------
# Health Check (ADD HERE)
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

class CustomerInput(BaseModel):
    AGE_YR_CT : int
    CUST_GNDR_CD : str
    CUST_TYPE_CD : str
    CTZSHP_CNTRY1_CD : str
    CTZSHP_CNTRY2_CD : str
    COUNTRY_OF_INC : str
    RES_CNTRY_CD : str
    PEP_FL : str
    FRGN_ASSETS_FL : str
    ANNL_INCM_BASE_AM : float
    NET_WRTH_BASE_AM : float
    LQD_NET_WRTH_BASE_AM : float
    OCPTN_NM : str
    DPNDT_QT : int
    WLTH_SRC_DSCR_TX : str

@app.post("/predict")
def predict_risk(data: CustomerInput):
    result = predict(data.dict())
    return {"risk_class": result}
