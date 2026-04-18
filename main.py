from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import json
import numpy as np
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.joblib")
with open("feature_columns.json") as f:
    feature_cols = json.load(f)

class CustomerInput(BaseModel):
    company_id: str
    contract_months: int
    monthly_fee: int
    active_users_ratio: float
    login_freq_per_week: float
    feature_usage_score: float
    support_tickets_90d: int
    nps_score: int
    payment_delays_count: int

@app.post("/predict")
def predict(data: CustomerInput):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])[feature_cols]

    prob = model.predict_proba(input_df)[0][1]

    if prob >= 0.7:
        risk_level = "High"
    elif prob >= 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    importance = model.feature_importances_
    factors = sorted(
        zip(feature_cols, importance),
        key=lambda x: x[1],
        reverse=True
    )
    top_factors = [
        {"feature": f, "impact": round(float(v), 4)}
        for f, v in factors[:3]
    ]

    actions = []
    if input_dict["nps_score"] <= 3:
        actions.append("CSチームによる緊急フォローアップ実施")
    if input_dict["login_freq_per_week"] < 2.0:
        actions.append("オンボーディング再実施・活用支援")
    if input_dict["payment_delays_count"] >= 2:
        actions.append("請求担当者へエスカレーション")
    if not actions:
        actions.append("定期チェックイン継続")

    return {
        "company_id": data.company_id,
        "churn_probability": round(float(prob), 4),
        "risk_level": risk_level,
        "top_factors": top_factors,
        "recommended_actions": actions
    }

@app.get("/health")
def health():
    return {"status": "ok"}