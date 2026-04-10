# 🎯 チャーン予測MLパイプライン

B2B SaaS顧客の60日以内の解約リスクを予測するMLシステム。

**🔗 Live Demo**: [churn-frontend.vercel.app](https://churn-frontend-git-main-re-lu.vercel.app)

---

## 概要

単に精度の高いモデルを作るだけでなく、実務で最も重要な「データの信頼性」をシステムで担保するMLOpsの視点を取り入れたプロ仕様のポートフォリオ。

## 技術スタック

| レイヤー | 技術 |
|------|------|
| ML | Python, Scikit-learn, Logistic Regression |
| API | FastAPI, Pydantic |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Deploy | Vercel (Frontend), Render (Backend) |
| 管理 | GitHub |

## アーキテクチャ

データ生成 → QA Gate 1 → 特徴量設計 → QA Gate 2
→ モデル学習 → QA Gate 3 (AUC≥0.75) → FastAPI → Next.js

## APIレスポンス仕様

```json
{
  "company_id": "C-1042",
  "churn_probability": 0.8922,
  "risk_level": "High",
  "top_factors": [
    {"feature": "active_users_ratio", "impact": 0.7226}
  ],
  "recommended_actions": [
    "CSチームによる緊急フォローアップ実施"
  ]
}
```

## モデル性能

| 指標 | スコア |
|------|------|
| AUC | 0.7615 |
| Accuracy | 0.70 |
| 学習データ | 4,000件 |
| テストデータ | 1,000件 |

## ローカル起動

```bash
# バックエンド
cd churn-prediction
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# フロントエンド
cd churn-frontend
npm install && npm run dev
```