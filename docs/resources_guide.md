# DevLog リソースガイド

**DevLog** が提供する 4 個のリソースの詳細な使用方法とサンプルです。

DevLog は Slack 風の開発状況共有サービスとして、プロジェクト、タスク、ユーザー、メッセージの情報を効率的に取得できるリソース機能を提供します。

## 📋 目次

- [リソースとは](#リソースとは)
- [プロジェクトリソース](#プロジェクトリソース)
- [タスクリソース](#タスクリソース)
- [ユーザーリソース](#ユーザーリソース)
- [メッセージリソース](#メッセージリソース)
- [リソースの活用方法](#リソースの活用方法)

---

## 📖 リソースとは

DevLog のリソースは、読み取り専用のデータアクセス機能です。ツールとは異なり、データの変更は行わず、情報の取得のみを行います。LLM がコンテキストとして情報を参照する際に活用されます。

### DevLog リソースの特徴

- **読み取り専用**: データの変更はできません
- **高速アクセス**: 効率的な情報取得が可能
- **コンテキスト提供**: LLM との会話で背景情報として活用
- **URL 形式**: `scheme://identifier` の形式で指定
- **開発状況の可視化**: プロジェクトの進捗状況を即座に把握

---

## 📁 プロジェクトリソース

### project://{project_id}

特定のプロジェクトの詳細情報と関連タスクを取得します。

**URL 形式:**

```
project://1
project://123
```

**パラメータ:**

- `project_id` (string): プロジェクトの ID

**使用例:**

```
project://1
```

**取得できる情報:**

- プロジェクト名
- プロジェクトの説明
- 関連タスクの数

**レスポンス例:**

```
Project: 新しいWebアプリ
Description: React と Node.js を使用したWebアプリケーション

Tasks: 5 tasks
```

**開発における活用シーン:**

- プロジェクトの概要を把握したい時
- 関連タスクの総数を確認したい時
- LLM にプロジェクトコンテキストを提供したい時

---

## ✅ タスクリソース

### task://{task_id}

特定のタスクの詳細情報を取得します。

**URL 形式:**

```
task://1
task://456
```

**パラメータ:**

- `task_id` (string): タスクの ID

**使用例:**

```
task://1
```

**取得できる情報:**

- タスクのタイトル
- タスクのステータス
- タスクの詳細説明

**レスポンス例:**

```
Task: ユーザー認証機能の実装
Status: in_progress
Description: ログイン・ログアウト機能を実装する
```

**開発における活用シーン:**

- 特定のタスクの詳細を確認したい時
- タスクの現在の状況を把握したい時
- LLM にタスクコンテキストを提供したい時

---

## 👤 ユーザーリソース

### user://{user_id}

特定のユーザーの基本情報を取得します。

**URL 形式:**

```
user://1
user://789
```

**パラメータ:**

- `user_id` (string): ユーザーの ID

**使用例:**

```
user://1
```

**取得できる情報:**

- ユーザー名
- メールアドレス

**レスポンス例:**

```
User: tanaka_taro
Email: tanaka@example.com
```

**開発における活用シーン:**

- チームメンバーの情報を確認したい時
- 担当者の詳細を把握したい時
- LLM にユーザーコンテキストを提供したい時

---

## 💬 メッセージリソース

### messages://{type}

指定されたタイプのメッセージを取得します。

**URL 形式:**

```
messages://recent
```

**パラメータ:**

- `type` (string): メッセージのタイプ

**対応タイプ:**

- `recent`: 最新のメッセージ（最大 20 件）

**使用例:**

```
messages://recent
```

**取得できる情報:**

- 最新のメッセージ一覧
- メッセージの投稿日時
- 投稿者情報
- メッセージ内容

**レスポンス例:**

```
Recent Messages:

[2024-01-01T10:30:00] 1: ユーザー認証機能の実装を開始しました
[2024-01-01T09:15:00] 2: データベース設計が完了しました
[2024-01-01T08:45:00] 1: プロジェクトを開始します
```

**開発における活用シーン:**

- 最新の活動状況を確認したい時
- チーム内のコミュニケーションを把握したい時
- LLM にプロジェクトの最新状況を提供したい時

---

## �� DevLog リソースの活用方法

### 1. プロジェクト状況の把握

LLM との会話でプロジェクトやタスクの背景情報が必要な場合：

```
# プロジェクトの詳細を確認
project://1

# 関連するタスクの詳細も確認
task://5
task://8
```

### 2. 開発進捗の状況収集

現在の開発状況を把握したい場合：

```
# 最新の活動を確認
messages://recent

# 特定のプロジェクトの概要を確認
project://1
```

### 3. チーム情報の参照

チームメンバーの情報が必要な場合：

```
# 担当者の情報を確認
user://1
user://2
```

### 4. 複数リソースの組み合わせ

包括的な状況把握のために複数のリソースを活用：

```
# プロジェクト全体の状況を把握
project://1        # プロジェクト概要
messages://recent  # 最新の活動
task://5          # 重要なタスクの詳細
user://1          # キーパーソンの情報
```

---

## 💡 DevLog リソース活用のベストプラクティス

### 効果的な使用方法

1. **事前情報収集**: ツールを実行する前にリソースで情報を収集
2. **コンテキスト提供**: LLM に十分な背景情報を提供
3. **関連情報の結合**: 複数のリソースを組み合わせて全体像を把握
4. **定期的な状況確認**: `messages://recent` で活動状況を定期確認

### 注意事項

1. **読み取り専用**: リソースではデータの変更はできません
2. **リアルタイム性**: 情報は取得時点のものです
3. **ID の有効性**: 存在しない ID を指定するとエラーになります
4. **権限**: 将来的にアクセス権限が追加される可能性があります

---

## 🔗 関連ドキュメント

- [ツールガイド](tools_guide.md) - DevLog の全ツール機能
- [設定ガイド](setup_guide.md) - 各種 MCP クライアントでの設定方法
- [FastMCP ガイド](fastmcp_guide.md) - 開発環境のセットアップ

---

## 📝 DevLog 使用例シナリオ

### シナリオ 1: 新しいタスクを作成する前の情報収集

```
1. project://1 でプロジェクトの概要を確認
2. messages://recent で最新の活動状況を把握
3. 適切なタスクを create_task ツールで作成
```

### シナリオ 2: 進捗報告を行う前の状況把握

```
1. task://5 で現在のタスク状況を確認
2. user://1 で担当者情報を確認
3. create_message ツールで進捗報告を投稿
```

### シナリオ 3: プロジェクト全体の状況分析

```
1. project://1 でプロジェクト概要を取得
2. messages://recent で最新の活動を確認
3. task://重要なタスクID で重要タスクの詳細を確認
4. 分析結果に基づいて適切なアクションを実行
```
