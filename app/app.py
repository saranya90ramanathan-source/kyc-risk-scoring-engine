import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from inference import predict

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="KYC Risk Dashboard", layout="wide")

# -------------------------
# Custom CSS (cards)
# -------------------------
st.markdown("""
<style>
.card {
    background-color: #f9f9f9;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.metric {
    font-size:16px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏦 KYC Risk Intelligence Dashboard")

# -------------------------
# SIDEBAR INPUTS
# -------------------------
st.sidebar.header("🧾 Customer Input")

AGE_YR_CT = st.sidebar.number_input("Age", 18, 100, 30)
CUST_GNDR_CD = st.sidebar.selectbox("Gender", ["M", "F", "O"])
CUST_TYPE_CD = st.sidebar.selectbox("Customer Type", ["IND", "CORP"])

PEP_FL = st.sidebar.selectbox("PEP Flag", ["Y", "N"])
FRGN_ASSETS_FL = st.sidebar.selectbox("Foreign Assets", ["Y", "N"])

ANNL_INCM_BASE_AM = st.sidebar.number_input("Annual Income", value=500000.0)
NET_WRTH_BASE_AM = st.sidebar.number_input("Net Worth", value=1000000.0)
CTZSHP_CNTRY1_CD = st.sidebar.selectbox(
    "Citizenship Country 1",
    ["IN", "US", "UK", "AE", "SG"]
)

OCPTN_NM = st.sidebar.text_input("Occupation", "Engineer")

WLTH_SRC_DSCR_TX = st.sidebar.selectbox(
    "Wealth Source",
    ["Salary", "Business", "Investments", "Inheritance", "Other"]
)

# -------------------------
# Predict Button
# -------------------------
run = st.sidebar.button("🚀 Predict Risk")

# -------------------------
# Prepare input
# -------------------------
input_data = {
    "AGE_YR_CT": AGE_YR_CT,
    "CUST_GNDR_CD": CUST_GNDR_CD,
    "CUST_TYPE_CD": CUST_TYPE_CD,
    "CTZSHP_CNTRY1_CD": CTZSHP_CNTRY1_CD,
    "CTZSHP_CNTRY2_CD": "IN",
    "COUNTRY_OF_INC": "IN",
    "RES_CNTRY_CD": "IN",
    "PEP_FL": PEP_FL,
    "FRGN_ASSETS_FL": FRGN_ASSETS_FL,
    "ANNL_INCM_BASE_AM": ANNL_INCM_BASE_AM,
    "NET_WRTH_BASE_AM": NET_WRTH_BASE_AM,
    "LQD_NET_WRTH_BASE_AM": NET_WRTH_BASE_AM * 0.5,
    "OCPTN_NM": OCPTN_NM,
    "DPNDT_QT": 2,
    "WLTH_SRC_DSCR_TX": WLTH_SRC_DSCR_T"
}

# -------------------------
# Run Prediction
# -------------------------
if run:

    with st.spinner("🔍 Analyzing customer risk..."):
        result = predict(input_data)

    # -------------------------
    # CARDS
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"<div class='card'><div class='metric'>Age</div><h3>{AGE_YR_CT}</h3></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<div class='card'><div class='metric'>Income</div><h3>₹ {ANNL_INCM_BASE_AM:,.0f}</h3></div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<div class='card'><div class='metric'>Net Worth</div><h3>₹ {NET_WRTH_BASE_AM:,.0f}</h3></div>",
            unsafe_allow_html=True
        )

    # -------------------------
    # RESULT
    # -------------------------
    st.markdown("### 🔍 Risk Assessment")

    if result == "high":
        st.error("🔴 High Risk Customer")
    elif result == "medium":
        st.warning("🟡 Medium Risk Customer")
    else:
        st.success("🟢 Low Risk Customer")

    # -------------------------
    # CHARTS (4x4)
    # -------------------------
    st.markdown("### 📊 Financial Overview")

    fig, ax = plt.subplots(figsize=(4, 4))
    labels = ["Income", "Net Worth", "Liquid Net Worth"]
    values = [ANNL_INCM_BASE_AM, NET_WRTH_BASE_AM, NET_WRTH_BASE_AM * 0.5]

    ax.bar(labels, values)
    ax.set_title("Financial Distribution")
    st.pyplot(fig)

    # -------------------------
    # SHAP (mock)
    # -------------------------
    st.markdown("### 🧠 Model Explainability")

    features = ["Income", "Net Worth", "PEP Flag", "Foreign Assets"]
    importance = np.random.rand(4)

    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.barh(features, importance)
    ax2.set_title("Top Risk Factors")
    st.pyplot(fig2)
