import joblib
import numpy as np
import pandas as pd

# -------------------------
# Load artifacts
# -------------------------
lgbm = joblib.load("lgbm_model.pkl")
encoders = joblib.load("encoders.pkl")
num_imputer = joblib.load("num_imputer.pkl")
scaler = joblib.load("scaler.pkl")
training_columns = joblib.load("training_columns.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -------------------------
# Preprocessing
# -------------------------
def preprocess(data: dict):
    df = pd.DataFrame([data])

    # -------------------------
    # Numeric processing
    # -------------------------
    df_num = df.select_dtypes(include=[np.number])
    
    if len(df_num.columns) > 0:
        df_num = pd.DataFrame(
            num_imputer.transform(df_num),
            columns=df_num.columns
        )
        df_num = pd.DataFrame(
            scaler.transform(df_num),
            columns=df_num.columns
        )
    else:
        df_num = pd.DataFrame()

    # -------------------------
    # Categorical encoding
    # -------------------------
    df_cat = pd.DataFrame()

    for col, info in encoders.items():
        val = str(data.get(col, "___MISSING___"))
        mapping = info["mapping"]
        df_cat[col] = [mapping.get(val, info["unk"])]

    # -------------------------
    # Combine
    # -------------------------
    X = pd.concat([df_num, df_cat], axis=1)

    # Ensure column order matches training
    for col in training_columns:
        if col not in X.columns:
            X[col] = 0

    X = X[training_columns]

    return X


# -------------------------
# Prediction
# -------------------------
def predict(data: dict):
    X = preprocess(data)

    # ⚠️ IMPORTANT:
    # This assumes LGBM was trained WITHOUT FAN augmentation
    pred = lgbm.predict(X)

    label = label_encoder.inverse_transform(pred)

    return label[0]
