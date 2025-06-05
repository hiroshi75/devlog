# DevLog 設定ガイド

**DevLog** を各種 MCP クライアントで使用するための設定手順です。

> **🎯 重要: DevLog は標準的な MCP サーバーです**  
> Claude Desktop、Cline、その他の MCP 対応クライアントから利用できます。

## 📋 目次

- [🚀 MCP クライアント対応状況](#-mcp-クライアント対応状況)
- [事前準備](#事前準備)
- [環境変数の設定](#環境変数の設定)
- [データベースの初期化](#データベースの初期化)
- [🤖 Claude Desktop での設定](#-claude-desktop-での設定)
- [🖥️ Cline (VS Code 拡張) での設定](#️-cline-vs-code拡張-での設定)
- [🔧 その他の MCP クライアントでの設定](#-その他の-mcp-クライアントでの設定)
- [動作確認](#動作確認)
- [トラブルシューティング](#トラブルシューティング)

---

## 🚀 MCP クライアント対応状況

DevLog は **標準的な MCP サーバー** として実装されており、以下のクライアントで利用可能です：

| クライアント              | 対応状況    | 設定の簡単さ | 推奨度    |
| ------------------------- | ----------- | ------------ | --------- |
| **Claude Desktop**        | ✅ 完全対応 | ⭐⭐⭐⭐⭐   | 🥇 最推奨 |
| **Cline (VS Code 拡張)**  | ✅ 完全対応 | ⭐⭐⭐⭐     | 🥈 推奨   |
| **Continue.dev**          | ✅ 対応     | ⭐⭐⭐       | 良好      |
| **その他 MCP 対応ツール** | ✅ 対応     | ⭐⭐         | 使用可能  |

---

## 🔧 事前準備

### 必要なソフトウェア

1. **Python 3.12+**

   ```bash
   python --version  # 3.12以上であることを確認
   ```

2. **uv** (Python パッケージマネージャー)

   ```bash
   # uvのインストール（未インストールの場合）
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # または
   pip install uv
   ```

3. **PostgreSQL** または **SQLite**
   - PostgreSQL 推奨（本番環境）
   - SQLite 可（開発環境）

### DevLog プロジェクトのセットアップ

1. **リポジトリのクローンまたはダウンロード**

   ```bash
   # プロジェクトディレクトリに移動
   cd /path/to/devlog
   ```

2. **依存関係のインストール**
   ```bash
   # 必要なライブラリをインストール
   uv sync
   ```

---

## 🌍 環境変数の設定

### .env ファイルの作成

プロジェクトルートに `.env` ファイルを作成します：

```bash
# .env ファイルの作成
touch .env
```

### 環境変数の設定例

```env
# データベース設定
DEVLOG_DATABASE_URL=postgresql://username:password@localhost:5432/devlog

# または SQLite を使用する場合
# DEVLOG_DATABASE_URL=sqlite:///./devlog.db

# デバッグモード（開発時のみ）
DEVLOG_DEBUG=true

# ログレベル
DEVLOG_LOG_LEVEL=INFO
```

### PostgreSQL の設定例

1. **PostgreSQL サーバーの起動**

   ```bash
   # macOS (Homebrew)
   brew services start postgresql

   # Ubuntu/Debian
   sudo systemctl start postgresql
   ```

2. **データベースとユーザーの作成**

   ```bash
   # PostgreSQL に接続
   psql postgres

   # データベースの作成
   CREATE DATABASE devlog;

   # ユーザーの作成（オプション）
   CREATE USER devuser WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE devlog TO devuser;

   # 接続テスト
   \q
   ```

### SQLite の設定例

開発環境で SQLite を使用する場合：

```env
# .env ファイル
DEVLOG_DATABASE_URL=sqlite:///./devlog.db
DEVLOG_DEBUG=true
DEVLOG_LOG_LEVEL=DEBUG
```

---

## 🗄️ データベースの初期化

### マイグレーションの実行

```bash
# Alembic マイグレーションを実行
alembic upgrade head
```

### データベースの確認

```bash
# PostgreSQL の場合
psql $DEVLOG_DATABASE_URL -c "\dt"

# SQLite の場合
sqlite3 devlog.db ".tables"
```

---

## 🤖 Claude Desktop での設定

> **💡 最も簡単で推奨される方法**

### 1. Claude Desktop の設定ファイルを開く

**macOS:**

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**

```cmd
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**

```bash
nano ~/.config/Claude/claude_desktop_config.json
```

### 2. DevLog サーバーの設定を追加

設定ファイルに以下の内容を追加：

```json
{
  "mcpServers": {
    "devlog": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "/path/to/your/devlog",
      "env": {
        "DEVLOG_DATABASE_URL": "postgresql://username:password@localhost:5432/devlog"
      }
    }
  }
}
```

### 3. パスの設定例

**絶対パスで指定：**

```json
{
  "mcpServers": {
    "devlog": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "/Users/username/projects/devlog",
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:///./devlog.db"
      }
    }
  }
}
```

---

## 🖥️ Cline (VS Code 拡張) での設定

> **💡 VS Code ユーザーに推奨**

### 1. Cline 拡張機能のインストール

VS Code の拡張機能マーケットプレイスで「Cline」を検索してインストール。

### 2. Cline の設定ファイルを編集

VS Code で `Ctrl+Shift+P` → "Cline: Open Settings" を選択。

### 3. MCP サーバー設定の追加

```json
{
  "mcpServers": {
    "devlog": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "/path/to/devlog",
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:///./devlog.db"
      }
    }
  }
}
```

### 4. VS Code でのワークスペース設定

**`.vscode/settings.json` に追加:**

```json
{
  "cline.mcpServers": {
    "devlog": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "${workspaceFolder}/devlog"
    }
  }
}
```

---

## 🔧 その他の MCP クライアントでの設定

### Continue.dev での設定

**`~/.continue/config.json` に追加:**

```json
{
  "mcpServers": [
    {
      "name": "devlog",
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "/path/to/devlog",
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:///./devlog.db"
      }
    }
  ]
}
```

### 汎用 MCP クライアント設定

**標準的な MCP 設定フォーマット:**

```json
{
  "servers": {
    "devlog": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.main"],
      "cwd": "/absolute/path/to/devlog",
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:///./devlog.db"
      }
    }
  }
}
```

### Docker での実行（高度な設定）

```bash
# Dockerfile の作成例
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "python", "-m", "app.main"]
```

**Docker Compose での設定:**

```yaml
version: "3.8"
services:
  devlog:
    build: .
    environment:
      - DEVLOG_DATABASE_URL=postgresql://user:pass@db:5432/devlog
    volumes:
      - ./data:/app/data
```

**MCP クライアント設定（Docker 版）:**

```json
{
  "mcpServers": {
    "devlog": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "devlog"],
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:///./data/devlog.db"
      }
    }
  }
}
```

---

## ✅ 動作確認

### 1. Claude Desktop での確認

1. **Claude Desktop を再起動**
2. **新しい会話を開始**
3. **DevLog ツールのテスト**：

```
DevLog でプロジェクトを作成してください：
- 名前: "テストプロジェクト"
- 説明: "DevLog の動作確認用プロジェクト"
```

4. **期待される応答**：
   - `create_project` ツールが自動的に呼び出される
   - プロジェクトが正常に作成される
   - プロジェクト ID と詳細が表示される

### 2. Cline での確認

VS Code で Cline を開き、以下をテスト：

```
DevLog を使ってタスクを作成してください
```

### 3. リソースのテスト

**任意のクライアントで:**

```
project://1 の情報を確認してください
```

期待される応答：

- プロジェクトリソースが取得される
- プロジェクト名と説明が表示される

### 4. 手動でのサーバー起動テスト

```bash
# プロジェクトディレクトリで実行
cd /path/to/devlog

# DevLog サーバーを手動起動
uv run python -m app.main

# 正常に起動すれば以下のようなメッセージが表示される
# DevLog server starting...
# Server running on stdio
```

---

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. モジュールが見つからないエラー

```
ModuleNotFoundError: No module named 'fastmcp'
```

**解決方法：**

```bash
# 依存関係を再インストール
uv sync
```

#### 2. データベース接続エラー

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError)
```

**解決方法：**

```bash
# PostgreSQL サービスの確認
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# データベースの存在確認
psql -c "SELECT 1" $DEVLOG_DATABASE_URL
```

#### 3. 権限エラー

```
PermissionError: [Errno 13] Permission denied
```

**解決方法：**

```bash
# ファイル権限の確認
ls -la /path/to/devlog

# 権限の修正
chmod +x /path/to/devlog
```

#### 4. MCP クライアントでツールが認識されない

**確認事項：**

1. 設定ファイルの JSON が有効か確認
2. パスが正しく設定されているか確認
3. クライアントの再起動
4. ログファイルの確認

**デバッグ方法：**

```bash
# 手動でサーバーを起動してエラーを確認
cd /path/to/devlog
uv run python -m app.main
```

#### 5. 環境変数が読み込まれない

**解決方法：**

```bash
# .env ファイルの確認
cat .env

# 環境変数の手動設定
export DEVLOG_DATABASE_URL="your_database_url"
```

### ログの確認

```bash
# アプリケーションログの確認
tail -f /path/to/devlog/app.log

# システムログの確認 (macOS)
log show --predicate 'process == "Claude"' --last 1h

# システムログの確認 (Linux)
journalctl -u claude-desktop -f
```

---

## 📚 関連ドキュメント

- [ツールガイド](tools_guide.md) - DevLog の全 16 ツール
- [リソースガイド](resources_guide.md) - DevLog の 4 リソース
- [FastMCP ガイド](fastmcp_guide.md) - 開発環境のセットアップ

---

## 🚀 次のステップ

設定が完了したら：

1. **基本的な操作を試す**

   - プロジェクトの作成・取得
   - ユーザーの登録
   - タスクの作成・管理

2. **チームでの利用を開始**

   - メンバーの登録
   - プロジェクトの共有
   - 進捗管理の運用

3. **他のツールとの連携**
   - 既存のワークフローへの統合
   - 自動化の設定
   - カスタム機能の追加

---

## 💡 DevLog 活用のヒント

- **複数環境**: 開発・テスト・本番環境で別々のデータベースを使用
- **バックアップ**: 定期的にデータベースのバックアップを取得
- **モニタリング**: サーバーのログを定期的に確認
- **セキュリティ**: 本番環境では適切なアクセス制御を実装
- **パフォーマンス**: 大量データの場合は PostgreSQL の使用を推奨
