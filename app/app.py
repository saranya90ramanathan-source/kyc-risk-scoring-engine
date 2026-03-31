import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
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
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.metric {
    font-size:18px;
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

# -------------------------
# Static / default fields
# -------------------------
input_data = {
    "AGE_YR_CT": AGE_YR_CT,
    "CUST_GNDR_CD": CUST_GNDR_CD,
    "CUST_TYPE_CD": CUST_TYPE_CD,
    "CTZSHP_CNTRY1_CD": "IN",
    "CTZSHP_CNTRY2_CD": "IN",
    "COUNTRY_OF_INC": "IN",
    "RES_CNTRY_CD": "IN",
    "PEP_FL": PEP_FL,
    "FRGN_ASSETS_FL": FRGN_ASSETS_FL,
    "ANNL_INCM_BASE_AM": ANNL_INCM_BASE_AM,
    "NET_WRTH_BASE_AM": NET_WRTH_BASE_AM,
    "LQD_NET_WRTH_BASE_AM": NET_WRTH_BASE_AM * 0.5,
    "OCPTN_NM": "Engineer",
    "DPNDT_QT": 2,
    "WLTH_SRC_DSCR_TX": "Salary"
}

# -------------------------
# Prediction
# -------------------------
result = predict(input_data)

# -------------------------
# CARDS SECTION
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><div class='metric'>Age</div><h2>{AGE_YR_CT}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><div class='metric'>Income</div><h2>₹ {ANNL_INCM_BASE_AM:,.0f}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><div class='metric'>Net Worth</div><h2>₹ {NET_WRTH_BASE_AM:,.0f}</h2></div>", unsafe_allow_html=True)

# -------------------------
# RISK RESULT CARD
# -------------------------
st.markdown("### 🔍 Risk Assessment")

if result == "high":
    st.error("🔴 High Risk Customer")
elif result == "medium":
    st.warning("🟡 Medium Risk Customer")
else:
    st.success("🟢 Low Risk Customer")

# -------------------------
# CHARTS
# -------------------------
st.markdown("### 📊 Financial Overview")

fig, ax = plt.subplots()
labels = ["Income", "Net Worth", "Liquid Net Worth"]
values = [ANNL_INCM_BASE_AM, NET_WRTH_BASE_AM, NET_WRTH_BASE_AM * 0.5]

ax.bar(labels, values)
st.pyplot(fig)

# -------------------------
# SHAP EXPLANATION (simple mock if not integrated)
# -------------------------
st.markdown("### 🧠 Model Explainability (Top Factors)")

# Dummy feature importance (replace with real SHAP later)
features = ["Income", "Net Worth", "PEP Flag", "Foreign Assets"]
importance = np.random.rand(4)

fig2, ax2 = plt.subplots()
ax2.barh(features, importance)
st.pyplot(fig2)
