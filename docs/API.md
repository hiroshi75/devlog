# DevLog API リファレンス

DevLog MCP サーバーが提供する全ての API ツールの詳細なリファレンスです。

## 📚 目次

- [プロジェクト管理 API](#プロジェクト管理-api)
- [タスク管理 API](#タスク管理-api)
- [ユーザー管理 API](#ユーザー管理-api)
- [メッセージ・コミュニケーション API](#メッセージコミュニケーション-api)
- [エラーハンドリング](#エラーハンドリング)

---

## プロジェクト管理 API

### `create_project`

新しいプロジェクトを作成します。

#### パラメータ

| パラメータ    | 型     | 必須 | 説明               |
| ------------- | ------ | ---- | ------------------ |
| `name`        | string | ✅   | プロジェクト名     |
| `description` | string | ❌   | プロジェクトの説明 |

#### 戻り値

```json
{
  "id": 1,
  "name": "プロジェクト名",
  "description": "プロジェクトの説明",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
# 基本的な作成
result = create_project(name="ユーザー管理システム")

# 説明付きで作成
result = create_project(
    name="E コマースサイト",
    description="新しいオンラインショップの構築プロジェクト"
)
```

### `get_projects`

全てのプロジェクトの一覧を取得します。

#### パラメータ

なし

#### 戻り値

```json
[
  {
    "id": 1,
    "name": "プロジェクト名",
    "description": "プロジェクトの説明",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
projects = get_projects()
print(f"プロジェクト数: {len(projects)}")
```

### `get_project`

指定されたプロジェクトの詳細情報を取得します。

#### パラメータ

| パラメータ   | 型  | 必須 | 説明            |
| ------------ | --- | ---- | --------------- |
| `project_id` | int | ✅   | プロジェクト ID |

#### 戻り値

```json
{
  "id": 1,
  "name": "プロジェクト名",
  "description": "プロジェクトの説明",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
project = get_project(project_id=1)
print(f"プロジェクト: {project['name']}")
```

### `update_project`

既存のプロジェクト情報を更新します。

#### パラメータ

| パラメータ    | 型     | 必須 | 説明                 |
| ------------- | ------ | ---- | -------------------- |
| `project_id`  | int    | ✅   | プロジェクト ID      |
| `name`        | string | ❌   | 新しいプロジェクト名 |
| `description` | string | ❌   | 新しい説明           |

#### 戻り値

```json
{
  "id": 1,
  "name": "更新後のプロジェクト名",
  "description": "更新後の説明",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 使用例

```python
# 名前のみ更新
result = update_project(project_id=1, name="新しいプロジェクト名")

# 名前と説明を更新
result = update_project(
    project_id=1,
    name="新しいプロジェクト名",
    description="更新された説明"
)
```

### `delete_project`

プロジェクトを削除します。

#### パラメータ

| パラメータ   | 型  | 必須 | 説明                    |
| ------------ | --- | ---- | ----------------------- |
| `project_id` | int | ✅   | 削除するプロジェクト ID |

#### 戻り値

```json
{
  "message": "Project deleted successfully",
  "project_id": 1
}
```

#### 使用例

```python
result = delete_project(project_id=1)
```

---

## タスク管理 API

### `create_task`

新しいタスクを作成します。

#### パラメータ

| パラメータ    | 型     | 必須 | 説明                                |
| ------------- | ------ | ---- | ----------------------------------- |
| `title`       | string | ✅   | タスクのタイトル                    |
| `project_id`  | int    | ✅   | 所属するプロジェクト ID             |
| `description` | string | ❌   | タスクの説明                        |
| `status`      | string | ❌   | ステータス（デフォルト: "pending"） |
| `assignee_id` | int    | ❌   | 担当者のユーザー ID                 |

#### ステータス一覧

- `pending` - 未着手
- `in_progress` - 進行中
- `review` - レビュー中
- `completed` - 完了
- `cancelled` - キャンセル

#### 戻り値

```json
{
  "id": 1,
  "title": "ログイン機能の実装",
  "description": "JWT を使用したログイン機能",
  "status": "pending",
  "project_id": 1,
  "assignee_id": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
# 基本的なタスク作成
task = create_task(
    title="ログイン機能の実装",
    project_id=1
)

# 詳細な情報付きでタスク作成
task = create_task(
    title="ユーザー登録 API の開発",
    project_id=1,
    description="JWT 認証付きのユーザー登録エンドポイント",
    status="in_progress",
    assignee_id=2
)
```

### `get_tasks`

タスクの一覧を取得します。フィルタリング機能付き。

#### パラメータ

| パラメータ    | 型     | 必須 | 説明                       |
| ------------- | ------ | ---- | -------------------------- |
| `project_id`  | int    | ❌   | プロジェクト ID でフィルタ |
| `status`      | string | ❌   | ステータスでフィルタ       |
| `assignee_id` | int    | ❌   | 担当者 ID でフィルタ       |

#### 戻り値

```json
[
  {
    "id": 1,
    "title": "ログイン機能の実装",
    "description": "JWT を使用したログイン機能",
    "status": "pending",
    "project_id": 1,
    "assignee_id": 2,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
# 全タスクを取得
all_tasks = get_tasks()

# プロジェクト 1 のタスクのみ取得
project_tasks = get_tasks(project_id=1)

# 進行中のタスクのみ取得
active_tasks = get_tasks(status="in_progress")

# 特定ユーザーのタスクのみ取得
user_tasks = get_tasks(assignee_id=2)

# 複合条件でフィルタ
filtered_tasks = get_tasks(
    project_id=1,
    status="pending",
    assignee_id=2
)
```

### `get_task`

指定されたタスクの詳細情報を取得します。

#### パラメータ

| パラメータ | 型  | 必須 | 説明      |
| ---------- | --- | ---- | --------- |
| `task_id`  | int | ✅   | タスク ID |

#### 戻り値

```json
{
  "id": 1,
  "title": "ログイン機能の実装",
  "description": "JWT を使用したログイン機能",
  "status": "pending",
  "project_id": 1,
  "assignee_id": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
task = get_task(task_id=1)
print(f"タスク: {task['title']} - {task['status']}")
```

### `update_task`

既存のタスク情報を更新します。

#### パラメータ

| パラメータ    | 型     | 必須 | 説明             |
| ------------- | ------ | ---- | ---------------- |
| `task_id`     | int    | ✅   | タスク ID        |
| `title`       | string | ❌   | 新しいタイトル   |
| `description` | string | ❌   | 新しい説明       |
| `status`      | string | ❌   | 新しいステータス |
| `assignee_id` | int    | ❌   | 新しい担当者 ID  |

#### 戻り値

```json
{
  "id": 1,
  "title": "更新後のタイトル",
  "description": "更新後の説明",
  "status": "completed",
  "project_id": 1,
  "assignee_id": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 使用例

```python
# ステータスのみ更新
result = update_task(task_id=1, status="completed")

# 複数項目を更新
result = update_task(
    task_id=1,
    title="新しいタイトル",
    description="追加の要件を含めた実装",
    status="in_progress"
)
```

### `delete_task`

タスクを削除します。

#### パラメータ

| パラメータ | 型  | 必須 | 説明              |
| ---------- | --- | ---- | ----------------- |
| `task_id`  | int | ✅   | 削除するタスク ID |

#### 戻り値

```json
{
  "message": "Task deleted successfully",
  "task_id": 1
}
```

#### 使用例

```python
result = delete_task(task_id=1)
```

---

## ユーザー管理 API

### `create_user`

新しいユーザーを登録します。

#### パラメータ

| パラメータ | 型     | 必須 | 説明                   |
| ---------- | ------ | ---- | ---------------------- |
| `username` | string | ✅   | ユーザー名（一意）     |
| `email`    | string | ✅   | メールアドレス（一意） |

#### 戻り値

```json
{
  "id": 1,
  "username": "tanaka",
  "email": "tanaka@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
user = create_user(
    username="tanaka",
    email="tanaka@example.com"
)
```

### `get_users`

全てのユーザーの一覧を取得します。

#### パラメータ

なし

#### 戻り値

```json
[
  {
    "id": 1,
    "username": "tanaka",
    "email": "tanaka@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
users = get_users()
for user in users:
    print(f"{user['username']} ({user['email']})")
```

### `get_user`

指定されたユーザーの詳細情報を取得します。

#### パラメータ

| パラメータ | 型  | 必須 | 説明        |
| ---------- | --- | ---- | ----------- |
| `user_id`  | int | ✅   | ユーザー ID |

#### 戻り値

```json
{
  "id": 1,
  "username": "tanaka",
  "email": "tanaka@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
user = get_user(user_id=1)
print(f"ユーザー: {user['username']}")
```

---

## メッセージ・コミュニケーション API

### `create_message`

汎用的なメッセージを作成します。プロジェクト、タスク、DM、スレッドに対応。

#### パラメータ

| パラメータ     | 型     | 必須 | 説明                                      |
| -------------- | ------ | ---- | ----------------------------------------- |
| `content`      | string | ✅   | メッセージ内容                            |
| `user_id`      | int    | ✅   | 投稿者のユーザー ID                       |
| `message_type` | string | ❌   | メッセージタイプ（デフォルト: "comment"） |
| `task_id`      | int    | ❌   | 関連するタスク ID                         |
| `project_id`   | int    | ❌   | 関連するプロジェクト ID                   |
| `parent_id`    | int    | ❌   | 親メッセージ ID（スレッド返信用）         |
| `recipient_id` | int    | ❌   | 受信者 ID（ダイレクトメッセージ用）       |

#### メッセージタイプ一覧

- `comment` - 一般的なコメント
- `question` - 質問
- `answer` - 回答
- `announcement` - アナウンス
- `direct_message` - ダイレクトメッセージ
- `task_update` - タスク更新通知
- `status_update` - ステータス更新
- `status_change` - ステータス変更通知

#### 戻り値

```json
{
  "id": 1,
  "content": "メッセージ内容",
  "message_type": "comment",
  "user_id": 1,
  "recipient_id": null,
  "project_id": 1,
  "task_id": null,
  "parent_id": null,
  "is_read": false,
  "is_deleted": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
# プロジェクトメッセージ
msg = create_message(
    content="プロジェクトの進捗報告です",
    user_id=1,
    project_id=1,
    message_type="status_update"
)

# タスクコメント
task_msg = create_message(
    content="このタスクで使用する技術について相談したいです",
    user_id=1,
    task_id=5,
    message_type="question"
)

# スレッド返信
reply = create_message(
    content="了解しました！明日までに確認します",
    user_id=2,
    parent_id=1,  # 元メッセージへの返信
    project_id=1
)

# ダイレクトメッセージ
dm = create_message(
    content="個人的な相談があります",
    user_id=1,
    recipient_id=2,
    message_type="direct_message"
)
```

### `create_direct_message`

ダイレクトメッセージ専用の作成関数です。

#### パラメータ

| パラメータ     | 型     | 必須 | 説明                             |
| -------------- | ------ | ---- | -------------------------------- |
| `content`      | string | ✅   | メッセージ内容                   |
| `user_id`      | int    | ✅   | 送信者のユーザー ID              |
| `recipient_id` | int    | ✅   | 受信者のユーザー ID              |
| `parent_id`    | int    | ❌   | 親メッセージ ID（DM スレッド用） |

#### 戻り値

```json
{
  "id": 1,
  "content": "ダイレクトメッセージ内容",
  "message_type": "direct_message",
  "user_id": 1,
  "recipient_id": 2,
  "parent_id": null,
  "is_read": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
# 基本的な DM
dm = create_direct_message(
    content="プルリクエストのレビューをお願いします",
    user_id=1,
    recipient_id=2
)

# DM への返信
dm_reply = create_direct_message(
    content="もちろんです！すぐに確認します",
    user_id=2,
    recipient_id=1,
    parent_id=1  # 元の DM への返信
)
```

### `get_messages`

メッセージの一覧を取得します。多様なフィルタリング機能付き。

#### パラメータ

| パラメータ        | 型     | 必須 | 説明                                            |
| ----------------- | ------ | ---- | ----------------------------------------------- |
| `project_id`      | int    | ❌   | プロジェクト ID でフィルタ                      |
| `task_id`         | int    | ❌   | タスク ID でフィルタ                            |
| `user_id`         | int    | ❌   | ユーザー ID でフィルタ                          |
| `recipient_id`    | int    | ❌   | 受信者 ID でフィルタ                            |
| `message_type`    | string | ❌   | メッセージタイプでフィルタ                      |
| `parent_id`       | int    | ❌   | 親メッセージ ID でフィルタ                      |
| `include_deleted` | bool   | ❌   | 削除済みメッセージを含める（デフォルト: false） |
| `limit`           | int    | ❌   | 取得件数制限（デフォルト: 100）                 |

#### 戻り値

```json
[
  {
    "id": 1,
    "content": "メッセージ内容",
    "message_type": "comment",
    "user_id": 1,
    "recipient_id": null,
    "project_id": 1,
    "task_id": null,
    "parent_id": null,
    "is_read": false,
    "is_deleted": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
# 全メッセージを取得
all_messages = get_messages()

# プロジェクト 1 のメッセージのみ
project_messages = get_messages(project_id=1)

# 質問タイプのメッセージのみ
questions = get_messages(message_type="question")

# タスク 5 のコメントのみ
task_comments = get_messages(task_id=5)

# ユーザー 1 が投稿したメッセージ
user_messages = get_messages(user_id=1)

# 最新 20 件のメッセージ
recent_messages = get_messages(limit=20)
```

### `get_direct_messages`

2 ユーザー間のダイレクトメッセージ履歴を取得します。

#### パラメータ

| パラメータ      | 型  | 必須 | 説明                            |
| --------------- | --- | ---- | ------------------------------- |
| `user_id`       | int | ✅   | 現在のユーザー ID               |
| `other_user_id` | int | ✅   | 相手のユーザー ID               |
| `limit`         | int | ❌   | 取得件数制限（デフォルト: 100） |

#### 戻り値

```json
[
  {
    "id": 1,
    "content": "ダイレクトメッセージ内容",
    "user_id": 1,
    "recipient_id": 2,
    "parent_id": null,
    "is_read": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
# ユーザー 1 と 2 の DM 履歴
dm_history = get_direct_messages(user_id=1, other_user_id=2)

# 最新 50 件の DM
recent_dms = get_direct_messages(
    user_id=1,
    other_user_id=2,
    limit=50
)
```

### `get_thread_messages`

特定のメッセージへの返信（スレッド）を取得します。

#### パラメータ

| パラメータ  | 型  | 必須 | 説明                            |
| ----------- | --- | ---- | ------------------------------- |
| `parent_id` | int | ✅   | 親メッセージの ID               |
| `limit`     | int | ❌   | 取得件数制限（デフォルト: 100） |

#### 戻り値

```json
[
  {
    "id": 2,
    "content": "返信メッセージ",
    "message_type": "comment",
    "user_id": 2,
    "recipient_id": null,
    "project_id": 1,
    "task_id": null,
    "parent_id": 1,
    "is_read": false,
    "created_at": "2024-01-01T01:00:00Z"
  }
]
```

#### 使用例

```python
# メッセージ ID 1 への返信を取得
replies = get_thread_messages(parent_id=1)

# 最新 20 件の返信のみ
recent_replies = get_thread_messages(parent_id=1, limit=20)
```

### `get_unread_messages`

ユーザーの未読メッセージを取得します。

#### パラメータ

| パラメータ     | 型     | 必須 | 説明                       |
| -------------- | ------ | ---- | -------------------------- |
| `user_id`      | int    | ✅   | ユーザー ID                |
| `message_type` | string | ❌   | メッセージタイプでフィルタ |

#### 戻り値

```json
[
  {
    "id": 1,
    "content": "未読メッセージ内容",
    "message_type": "direct_message",
    "user_id": 2,
    "recipient_id": 1,
    "project_id": null,
    "task_id": null,
    "parent_id": null,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 使用例

```python
# ユーザー 1 の全未読メッセージ
unread = get_unread_messages(user_id=1)

# 未読の DM のみ
unread_dms = get_unread_messages(
    user_id=1,
    message_type="direct_message"
)
```

### `mark_message_as_read`

特定のメッセージを既読にします。

#### パラメータ

| パラメータ   | 型  | 必須 | 説明          |
| ------------ | --- | ---- | ------------- |
| `message_id` | int | ✅   | メッセージ ID |

#### 戻り値

```json
{
  "id": 1,
  "is_read": true,
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 使用例

```python
result = mark_message_as_read(message_id=1)
```

### `mark_conversation_as_read`

2 ユーザー間の会話を一括で既読にします。

#### パラメータ

| パラメータ      | 型  | 必須 | 説明              |
| --------------- | --- | ---- | ----------------- |
| `user_id`       | int | ✅   | 現在のユーザー ID |
| `other_user_id` | int | ✅   | 相手のユーザー ID |

#### 戻り値

```json
{
  "messages_marked_read": 5
}
```

#### 使用例

```python
# ユーザー 1 と 2 の会話を全て既読に
result = mark_conversation_as_read(user_id=1, other_user_id=2)
print(f"{result['messages_marked_read']} 件のメッセージを既読にしました")
```

### `delete_message`

メッセージを削除します（論理削除）。

#### パラメータ

| パラメータ   | 型  | 必須 | 説明                  |
| ------------ | --- | ---- | --------------------- |
| `message_id` | int | ✅   | 削除するメッセージ ID |

#### 戻り値

```json
{
  "id": 1,
  "is_deleted": true,
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 使用例

```python
result = delete_message(message_id=1)
```

### `get_message`

特定のメッセージの詳細情報を取得します。

#### パラメータ

| パラメータ   | 型  | 必須 | 説明          |
| ------------ | --- | ---- | ------------- |
| `message_id` | int | ✅   | メッセージ ID |

#### 戻り値

```json
{
  "id": 1,
  "content": "メッセージ内容",
  "message_type": "comment",
  "user_id": 1,
  "recipient_id": null,
  "project_id": 1,
  "task_id": null,
  "parent_id": null,
  "is_read": false,
  "is_deleted": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 使用例

```python
message = get_message(message_id=1)
print(f"メッセージ: {message['content']}")
```

---

## エラーハンドリング

DevLog API では、以下のような場合にエラーが発生します：

### 一般的なエラー

#### `ValueError`

- 必須パラメータが不足している場合
- 不正な値が指定された場合
- データが見つからない場合

```python
# 例: 存在しないプロジェクト ID を指定
try:
    project = get_project(project_id=999)
except ValueError as e:
    print(f"エラー: {e}")  # "Project not found: 999"
```

#### データ整合性エラー

- 外部キー制約違反（存在しないユーザー ID など）
- 一意制約違反（重複するユーザー名など）

### メッセージ関連の特定エラー

#### ダイレクトメッセージのエラー

```python
# 自分自身に DM を送ろうとした場合
try:
    dm = create_direct_message(
        content="自分への DM",
        user_id=1,
        recipient_id=1  # 同じユーザー ID
    )
except ValueError as e:
    print(f"エラー: {e}")  # "Cannot send direct message to yourself"
```

#### メッセージタイプの制約エラー

```python
# DM でプロジェクト ID を指定した場合
try:
    msg = create_message(
        content="DM です",
        user_id=1,
        recipient_id=2,
        message_type="direct_message",
        project_id=1  # DM はプロジェクトに属せない
    )
except ValueError as e:
    print(f"エラー: {e}")  # "Direct messages cannot belong to projects or tasks"
```

### エラー対策のベストプラクティス

1. **存在確認**: ID 指定前にリソースの存在を確認
2. **適切な try-catch**: 予想されるエラーを適切にハンドリング
3. **パラメータ検証**: 送信前にパラメータの妥当性を確認

```python
# 良い例: エラーハンドリング付きの実装
def safe_create_task(title, project_id, **kwargs):
    try:
        # プロジェクトの存在確認
        project = get_project(project_id=project_id)

        # タスク作成
        task = create_task(
            title=title,
            project_id=project_id,
            **kwargs
        )
        return task
    except ValueError as e:
        print(f"タスク作成に失敗しました: {e}")
        return None
```

---

## 📱 実用的な組み合わせパターン

### パターン 1: プロジェクト開始フロー

```python
# 1. プロジェクト作成
project = create_project(
    name="新サービス開発",
    description="次世代 Web アプリケーション"
)

# 2. チームメンバーの確認
team_members = get_users()

# 3. 初期タスクの作成
tasks = [
    create_task(
        title="要件定義",
        project_id=project["id"],
        assignee_id=team_members[0]["id"]
    ),
    create_task(
        title="UI/UX デザイン",
        project_id=project["id"],
        assignee_id=team_members[1]["id"]
    )
]

# 4. キックオフメッセージの投稿
create_message(
    content="プロジェクトがスタートしました！よろしくお願いします",
    user_id=team_members[0]["id"],
    project_id=project["id"],
    message_type="announcement"
)
```

### パターン 2: 日次進捗確認フロー

```python
# 1. 進行中のタスクを取得
active_tasks = get_tasks(status="in_progress")

# 2. 各タスクの最新コメントを確認
for task in active_tasks:
    comments = get_messages(task_id=task["id"], limit=5)
    print(f"タスク: {task['title']}")
    print(f"最新コメント数: {len(comments)}")

# 3. 未読メッセージの確認
for member in team_members:
    unread = get_unread_messages(user_id=member["id"])
    if unread:
        print(f"{member['username']}: {len(unread)} 件の未読")
```

### パターン 3: 質問・回答フロー

```python
# 1. 質問の投稿
question = create_message(
    content="API の認証方式はどうしますか？JWT でいいでしょうか？",
    user_id=junior_dev_id,
    project_id=project_id,
    message_type="question"
)

# 2. 回答の投稿（スレッド返信）
answer = create_message(
    content="JWT で進めましょう。セキュリティ要件も満たせます。",
    user_id=senior_dev_id,
    parent_id=question["id"],  # 質問への返信
    project_id=project_id,
    message_type="answer"
)

# 3. お礼の返信
thanks = create_message(
    content="ありがとうございます！実装を進めます",
    user_id=junior_dev_id,
    parent_id=question["id"],
    project_id=project_id
)
```

### パターン 4: DM でのコードレビュー依頼

```python
# 1. DM でレビュー依頼
review_request = create_direct_message(
    content="PR #123 のレビューをお願いできますか？ユーザー認証機能です。",
    user_id=developer_id,
    recipient_id=reviewer_id
)

# 2. レビュー完了の通知
review_done = create_direct_message(
    content="レビュー完了しました。2 点修正をお願いします。",
    user_id=reviewer_id,
    recipient_id=developer_id,
    parent_id=review_request["id"]
)

# 3. 修正完了の報告
fix_done = create_direct_message(
    content="修正しました。再度確認をお願いします。",
    user_id=developer_id,
    recipient_id=reviewer_id,
    parent_id=review_request["id"]
)
```

この API リファレンスを活用して、効率的な開発チームコミュニケーションを実現してください！
