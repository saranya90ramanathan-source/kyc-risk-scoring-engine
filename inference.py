import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

DEVICE = torch.device("cpu")

# -------------------------
# Load artifacts
# -------------------------
lgbm = joblib.load("app/lgbm_model.pkl")
encoders = joblib.load("app/encoders.pkl")
num_imputer = joblib.load("app/num_imputer.pkl")
scaler = joblib.load("app/scaler.pkl")
training_columns = joblib.load("app/training_columns.pkl")
label_encoder = joblib.load("app/label_encoder.pkl")

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
# FAN Model (same as training)
# -------------------------
class ImprovedFAN(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_classes=3, temperature=2.0):
        super().__init__()
        self.attn_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )
        self.cls_head = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes)
        )
        self.temperature = temperature

    def forward(self, x):
        logits_w = self.attn_net(x)
        w = torch.softmax(logits_w / self.temperature, dim=1)
        xw = x * w
        logits = self.cls_head(xw)
        return logits, w

fan = ImprovedFAN(input_dim=len(training_columns))
fan.load_state_dict(torch.load("app/fan_model.pt", map_location=DEVICE))
fan.eval()

# -------------------------
# Prediction
# -------------------------
def predict(data: dict):
    X = preprocess(data)

    X_tensor = torch.tensor(X.values.astype(np.float32))
    _, attn = fan(X_tensor)

    attn_np = attn.detach().numpy()

    # feature augmentation
    X_aug = np.hstack([X.values, X.values * attn_np, attn_np])
  

    pred = np.argmax(proba, axis=1)
    label = label_encoder.inverse_transform(pred)

    confidence = np.max(proba, axis=1)

    return label[0], float(confidence[0])
