# DevStatusAPI

Slack 風の開発状況共有サービスのためのバックエンド API です。  
複数人が複数プロジェクトで複数タスクを進める状況において、開発進捗やコメントなどをメッセージ形式で一元管理することを目的としています。

## 📦 機能概要

- プロジェクトの作成・取得・更新・削除
- タスクの作成・取得・更新・削除
- ユーザー管理（追加・一覧取得）
- メッセージ投稿・取得（ステータス更新、スレッド対応）

## 🚀 使用技術

- Python 3.12+
- FastMCP
- SQLAlchemy
- PostgreSQL（または SQLite for development）
- Uvicorn（開発サーバ）
- Alembic（マイグレーション）

---

## 🛠️ セットアップ手順

### 1. .env ファイルの作成

`.env` ファイルに以下のような内容を記述してください：

```env
DATABASE_URL=postgresql://user:password@localhost/devstatus
```

※ SQLite を使う場合は：

```env
DATABASE_URL=sqlite:///./devstatus.db
```

### 4. データベース初期化

```bash
alembic upgrade head
```

---

## ▶️ 実行方法

```bash
uvicorn main:app --reload
```

API ドキュメントは以下の URL で確認できます：

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📘 エンドポイント例

### プロジェクト

| メソッド | パス             | 説明                 |
| -------- | ---------------- | -------------------- |
| `GET`    | `/projects/`     | プロジェクト一覧取得 |
| `POST`   | `/projects/`     | プロジェクト作成     |
| `GET`    | `/projects/{id}` | プロジェクト詳細取得 |
| `PUT`    | `/projects/{id}` | プロジェクト更新     |
| `DELETE` | `/projects/{id}` | プロジェクト削除     |

### タスク

| メソッド | パス          | 説明           |
| -------- | ------------- | -------------- |
| `GET`    | `/tasks/`     | タスク一覧取得 |
| `POST`   | `/tasks/`     | タスク作成     |
| `GET`    | `/tasks/{id}` | タスク詳細取得 |
| `PUT`    | `/tasks/{id}` | タスク更新     |
| `DELETE` | `/tasks/{id}` | タスク削除     |

### ユーザー

| メソッド | パス          | 説明             |
| -------- | ------------- | ---------------- |
| `GET`    | `/users/`     | ユーザー一覧取得 |
| `POST`   | `/users/`     | ユーザー登録     |
| `GET`    | `/users/{id}` | ユーザー詳細取得 |

### メッセージ

| メソッド | パス             | 説明                                 |
| -------- | ---------------- | ------------------------------------ |
| `GET`    | `/messages/`     | メッセージ一覧取得（フィルター対応） |
| `POST`   | `/messages/`     | メッセージ投稿                       |
| `GET`    | `/messages/{id}` | メッセージ詳細取得                   |

---

## 📂 ディレクトリ構成（例）

```
dev-status-api/
├── app/
│   ├── main.py
│   ├── models/           # SQLAlchemyモデル
│   ├── schemas/          # Pydanticスキーマ
│   ├── crud/             # CRUD操作ロジック
│   ├── api/              # ルーティング
│   └── db/               # DB接続・初期化
├── alembic/              # マイグレーション管理
├── requirements.txt
└── README.md
```

---

## 🧪 テスト（未実装）

後日 `pytest` による自動テストを追加予定です。

---

## 📝 ライセンス

MIT License
