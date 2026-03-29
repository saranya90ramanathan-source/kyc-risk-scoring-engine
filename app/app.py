import streamlit as st
from inference import predict

st.set_page_config(page_title="KYC Risk Scoring Engine", layout="centered")

st.title("🏦 KYC Risk Scoring System")
st.markdown("Enter customer details below")

# -------------------------
# Inputs
# -------------------------

AGE_YR_CT = st.number_input("Age", 18, 100, 30)

CUST_GNDR_CD = st.selectbox("Gender", ["M", "F", "O"])
CUST_TYPE_CD = st.selectbox("Customer Type", ["IND", "CORP"])

CTZSHP_CNTRY1_CD = st.text_input("Citizenship Country 1", "IN")
CTZSHP_CNTRY2_CD = st.text_input("Citizenship Country 2", "IN")

COUNTRY_OF_INC = st.text_input("Country of Incorporation", "IN")
RES_CNTRY_CD = st.text_input("Residence Country", "IN")

PEP_FL = st.selectbox("PEP Flag", ["Y", "N"])
FRGN_ASSETS_FL = st.selectbox("Foreign Assets", ["Y", "N"])

ANNL_INCM_BASE_AM = st.number_input("Annual Income", value=500000.0)
NET_WRTH_BASE_AM = st.number_input("Net Worth", value=1000000.0)
LQD_NET_WRTH_BASE_AM = st.number_input("Liquid Net Worth", value=500000.0)

OCPTN_NM = st.text_input("Occupation", "Engineer")
DPNDT_QT = st.number_input("Dependents", value=2)

WLTH_SRC_DSCR_TX = st.text_input("Wealth Source", "Salary")

# -------------------------
# Prediction
# -------------------------

if st.button("Predict Risk"):
    input_data = {
        "AGE_YR_CT": AGE_YR_CT,
        "CUST_GNDR_CD": CUST_GNDR_CD,
        "CUST_TYPE_CD": CUST_TYPE_CD,
        "CTZSHP_CNTRY1_CD": CTZSHP_CNTRY1_CD,
        "CTZSHP_CNTRY2_CD": CTZSHP_CNTRY2_CD,
        "COUNTRY_OF_INC": COUNTRY_OF_INC,
        "RES_CNTRY_CD": RES_CNTRY_CD,
        "PEP_FL": PEP_FL,
        "FRGN_ASSETS_FL": FRGN_ASSETS_FL,
        "ANNL_INCM_BASE_AM": ANNL_INCM_BASE_AM,
        "NET_WRTH_BASE_AM": NET_WRTH_BASE_AM,
        "LQD_NET_WRTH_BASE_AM": LQD_NET_WRTH_BASE_AM,
        "OCPTN_NM": OCPTN_NM,
        "DPNDT_QT": DPNDT_QT,
        "WLTH_SRC_DSCR_TX": WLTH_SRC_DSCR_TX
    }

    try:
        result = predict(input_data)
        st.success(f"Risk Level: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
