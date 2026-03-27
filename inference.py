import joblib
import torch
import torch.nn as nn
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

DEVICE = torch.device("cpu")

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
fan.load_state_dict(torch.load("fan_model.pt", map_location=DEVICE))
fan.eval()

# -------------------------
# Preprocessing
# -------------------------
def preprocess(data: dict):
    df = pd.DataFrame([data])

    # numeric
    numeric_cols = [c for c in training_columns if c in df.columns]
    df_num = df.select_dtypes(include=[np.number])
    df_num = pd.DataFrame(num_imputer.transform(df_num), columns=df_num.columns)
    df_num = pd.DataFrame(scaler.transform(df_num), columns=df_num.columns)

    # categorical
    df_cat = pd.DataFrame()
    for col, info in encoders.items():
        val = str(df.get(col, "___MISSING___"))
        mapping = info["mapping"]
        df_cat[col] = [mapping.get(val, info["unk"])]

    # combine
    X = pd.concat([df_num, df_cat], axis=1)
    X = X[training_columns]

    return X

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

    pred = lgbm.predict(X_aug)
    label = label_encoder.inverse_transform(pred)

    return label[0]
