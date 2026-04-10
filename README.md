# 🎯 チャーン予測MLパイプライン

B2B SaaS顧客の60日以内の解約リスクを予測する、**バックエンド主導設計**のMLシステム。

**🔗 Live Demo**: [churn-frontend-git-main-re-lu.vercel.app](https://churn-frontend-git-main-re-lu.vercel.app)

---

## 🎯 プロジェクト概要

「精度の高いモデルを作る」だけでは実務では使えない。

本プロジェクトでは、**「まず予測の意味を作る、見た目は後からいくらでも盛れる」**という設計思想のもと、以下の優先順位で開発しました。

1. Notebookでモデルを完成させ、APIレスポンスまで一気に作る
2. JSONを正式化してフロントのモックとして使う
3. 仕様ブレをなくしてからUIを作る

この順番により、**フロントエンドとバックエンドの仕様が一切ずれない**一気通貫の設計を実現しています。

---

## 🧩 解決した課題

### 1. バックエンド主導設計で仕様ブレをゼロにする

#### 課題
フロントとバックを並行開発すると、APIのレスポンス形式が途中で変わり、手戻りが大量発生する。

#### 対応
Notebookの最終セルで、入力1件を渡すと以下のJSONを返す関数まで作ってから、フロント開発に着手。

```json
{
  "company_id": "C-1042",
  "churn_probability": 0.8922,
  "risk_level": "High",
  "top_factors": [
    {"feature": "active_users_ratio", "impact": 0.7226},
    {"feature": "nps_score", "impact": 0.6827},
    {"feature": "login_freq_per_week", "impact": 0.4442}
  ],
  "recommended_actions": [
    "CSチームによる緊急フォローアップ実施",
    "オンボーディング再実施・活用支援",
    "請求担当者へエスカレーション"
  ]
}
```

このJSONがそのままZodスキーマ定義の元データとなり、フロントのモックとして機能した。

#### 学び
「先に予測の意味を作る」ことで、フロントエンジニアとの連携コストをゼロにできる。

---

### 2. 3段階のQAゲートで「動くゴミ」を作らない

#### 課題
モデルの精度が低いまま本番デプロイしても意味がない。かといってGreat Expectationsを最初から入れると完成しない。

#### 対応
まず完成させることを優先しつつ、以下の3つのQAゲートをNotebook内に実装。

| ゲート | チェック内容 | 基準 |
|------|------|------|
| QA Gate 1 | スキーマ・欠損値 | 全カラム存在・欠損なし |
| QA Gate 2 | 特徴量分布・leakage | 学習/テストの分布乖離なし |
| QA Gate 3 | モデル精度 | AUC ≥ 0.75 |

**結果: AUC 0.7615でGate 3クリア。**

#### 学び
「失敗しても代替案がある」設計にするには、品質基準を数値で定義しておくことが前提になる。

---

### 3. 段階的デプロイで確実に「完成」を積み上げる

#### 課題
最初からGreat ExpectationsやONNX化を入れようとすると、完成しないまま終わるリスクがある。

#### 対応
以下の順番で段階的に完成させた。

```
Logistic Regression で完成
→ FastAPI でAPI化
→ Next.js + Vercel で公開
→ （余裕があれば）LightGBM換装
→ （余裕があれば）ONNX化
→ （余裕があれば）Great Expectations追加
```

VercelとRenderの無料枠で本番稼働まで到達。

---

## 🛠 技術スタック

| レイヤー | 技術 |
|------|------|
| ML | Python, Scikit-learn, Logistic Regression |
| API | FastAPI, Pydantic |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Deploy | Vercel (Frontend), Render (Backend) |
| 管理 | GitHub |

## 📊 モデル性能

| 指標 | スコア |
|------|------|
| AUC | 0.7615 |
| Accuracy | 0.70 |
| 学習データ | 4,000件 |
| テストデータ | 1,000件 |

---

## 🚀 ローカル起動

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