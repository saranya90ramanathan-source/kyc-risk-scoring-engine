import streamlit as st
from inference import predict

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="KYC Risk Scoring", layout="wide")

st.title("🏦 KYC Risk Scoring System")
st.markdown("**Enter customer details below**")

# -------------------------
# Label helper
# -------------------------
def label(text):
    st.markdown(
        f"<span style='font-size:18px; font-weight:bold;'>{text}</span>",
        unsafe_allow_html=True
    )

# -------------------------
# Create 2 columns
# -------------------------
col1, col2 = st.columns(2)

# -------------------------
# LEFT COLUMN
# -------------------------
with col1:
    st.subheader("👤 Personal Details")

    label("Age")
    AGE_YR_CT = st.number_input("", 18, 100, 30, key="age")

    label("Gender")
    CUST_GNDR_CD = st.selectbox("", ["M", "F", "O"], key="gender")

    label("Customer Type")
    CUST_TYPE_CD = st.selectbox("", ["IND", "CORP"], key="cust_type")

    label("Citizenship Country 1")
    CTZSHP_CNTRY1_CD = st.text_input("", "IN", key="citizenship1")

    label("Country of Incorporation")
    COUNTRY_OF_INC = st.text_input("", "IN", key="country_inc")

    label("PEP Flag")
    PEP_FL = st.selectbox("", ["Y", "N"], key="pep")

    label("Occupation")
    OCPTN_NM = st.text_input("", "Engineer", key="occupation")

    label("Dependents")
    DPNDT_QT = st.number_input("", value=2, key="dependents")


# -------------------------
# RIGHT COLUMN
# -------------------------
with col2:
    st.subheader("💰 Financial & Risk Details")

    label("Citizenship Country 2")
    CTZSHP_CNTRY2_CD = st.text_input("", "IN", key="citizenship2")

    label("Residence Country")
    RES_CNTRY_CD = st.text_input("", "IN", key="res_country")

    label("Foreign Assets")
    FRGN_ASSETS_FL = st.selectbox("", ["Y", "N"], key="foreign_assets")

    label("Annual Income")
    ANNL_INCM_BASE_AM = st.number_input("", value=500000.0, key="income")

    label("Net Worth")
    NET_WRTH_BASE_AM = st.number_input("", value=1000000.0, key="net_worth")

    label("Liquid Net Worth")
    LQD_NET_WRTH_BASE_AM = st.number_input("", value=500000.0, key="liquid_net_worth")

    label("Wealth Source")
    WLTH_SRC_DSCR_TX = st.text_input("", "Salary", key="wealth_source")


# -------------------------
# Predict Button
# -------------------------
st.markdown("---")

if st.button("🚀 Predict Risk"):

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

        st.markdown("## 🔍 Risk Assessment Result")

        if result == "high":
            st.error("🔴 High Risk Customer")
        elif result == "medium":
            st.warning("🟡 Medium Risk Customer")
        else:
            st.success("🟢 Low Risk Customer")

    except Exception as e:
        st.error(f"Error: {e}")
