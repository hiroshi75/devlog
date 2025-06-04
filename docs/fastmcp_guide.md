# FastMCP 基本ガイド

## FastMCP とは

FastMCP（Fast Model Context Protocol）は、LLM（大規模言語モデル）と MCP サーバーを構築するための Python フレームワークです。MCP プロトコルの複雑な実装詳細を抽象化し、シンプルで直感的な API を提供することで、開発者が機能の実装に集中できるようにします。

### 主な特徴

- 🚀 **高速開発**: 高レベルのインターフェースにより、少ないコードで素早く開発
- 🍀 **シンプル**: 最小限のボイラープレートで MCP サーバーを構築
- 🐍 **Pythonic**: Python 開発者にとって自然で直感的な設計
- 🔍 **包括的**: 開発から本番環境まで、すべての MCP ユースケースに対応

## インストール

### 推奨: uv を使用したインストール

```bash
# uvのインストール（macOS）
brew install uv

# uvのインストール（Windows）
powershell -c "irm https://install.python-uv.org | iex"

# FastMCPのインストール
uv add fastmcp
```

### pip を使用したインストール

```bash
pip install fastmcp
```

### インストールの確認

```bash
fastmcp version
```

## 基本概念

FastMCP サーバーは 3 つの主要コンポーネントで構成されます：

1. **Tools（ツール）**: LLM が呼び出して実行できる関数（モデル制御）
2. **Resources（リソース）**: LLM に提供できるデータソース（アプリケーション制御）
3. **Prompts（プロンプト）**: UI を通じてユーザーが呼び出せるテンプレート（ユーザー制御）

## クイックスタート

### 1. シンプルなサーバーの作成

```python
# server.py
from fastmcp import FastMCP

# MCPサーバーインスタンスの作成
mcp = FastMCP("My First MCP Server")

# ツールの追加
@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数値を加算します"""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """挨拶を返します"""
    return f"こんにちは、{name}さん！"

# リソースの追加
@mcp.resource("config://version")
def get_version() -> str:
    """アプリケーションのバージョンを返します"""
    return "1.0.0"

# 動的リソーステンプレート
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """ユーザープロファイルを取得します"""
    # 実際のアプリケーションではデータベースから取得
    return {
        "id": user_id,
        "name": f"ユーザー {user_id}",
        "status": "active"
    }

# プロンプトの追加
@mcp.prompt()
def summarize_prompt(text: str) -> str:
    """要約用のプロンプトを生成します"""
    return f"以下のテキストを簡潔に要約してください：\n\n{text}"

# サーバーの実行
if __name__ == "__main__":
    mcp.run()
```

### 2. サーバーの実行

#### 標準的な実行方法

```bash
python server.py
```

#### FastMCP CLI を使用した実行

```bash
# STDIOトランスポート（デフォルト）
fastmcp run server.py:mcp

# SSEトランスポート（Web対応）
fastmcp run server.py:mcp --transport sse --port 8080

# デバッグモード
fastmcp run server.py:mcp --log-level DEBUG
```

### 3. デバッグとテスト

#### MCP インスペクターの使用

```bash
mcp dev server.py
```

これにより、ブラウザでインスペクターが開き、以下のことができます：

- ツールの一覧表示とテスト実行
- リソースの確認とアクセス
- プロンプトのテスト

#### クライアントを使用したテスト

```python
# test_client.py
from fastmcp import Client
import asyncio

async def test_server():
    # サーバーに接続
    async with Client("server.py") as client:
        # ツールの呼び出し
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"加算結果: {result}")

        # リソースの読み取り
        version = await client.read_resource("config://version")
        print(f"バージョン: {version}")

        # 動的リソースの読み取り
        profile = await client.read_resource("users://123/profile")
        print(f"プロファイル: {profile}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

## 高度な機能

### コンテキストの使用

コンテキストを使用して、MCP セッションの機能にアクセスできます：

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("Advanced Server")

@mcp.tool()
async def process_with_context(data: str, ctx: Context) -> str:
    """コンテキストを使用したデータ処理"""
    # クライアントにログを送信
    await ctx.info(f"データを処理中: {data}")

    # LLMにサンプリングを要求
    response = await ctx.sample(f"次のデータを分析してください: {data}")

    # 進捗を報告
    await ctx.report_progress(0.5, "処理が半分完了しました")

    return response.text
```

### 認証の実装

```python
from fastmcp import FastMCP
from fastmcp.auth import APIKeyAuth

# APIキー認証の設定
auth = APIKeyAuth(api_key="your-secret-key")
mcp = FastMCP("Secure Server", auth=auth)

# 以降、通常通りツールやリソースを定義
```

### サーバーの合成

複数の MCP サーバーを組み合わせることができます：

```python
from fastmcp import FastMCP

# メインサーバー
main_mcp = FastMCP("Main Server")

# サブサーバー
sub_mcp = FastMCP("Sub Server")

@sub_mcp.tool()
def sub_tool():
    return "サブサーバーのツール"

# サブサーバーをマウント
main_mcp.mount("sub", sub_mcp)
```

## Claude Desktop や Cursor での使用

### Claude Desktop へのインストール

```bash
fastmcp install server.py
```

これにより、自動的に Claude Desktop の設定ファイルに追加されます。

### Cursor での設定

`~/.cursor/mcp.json`ファイルに以下を追加：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/server/directory", "run", "server.py"]
    }
  }
}
```

## ベストプラクティス

1. **エラーハンドリング**: 常に適切なエラーハンドリングを実装

   ```python
   @mcp.tool()
   def safe_divide(a: float, b: float) -> float:
       """安全な除算"""
       try:
           if b == 0:
               return "エラー: ゼロで除算することはできません"
           return a / b
       except Exception as e:
           return f"エラーが発生しました: {str(e)}"
   ```

2. **型ヒントとドキュメント**: 明確な型ヒントと docstring を提供

   ```python
   @mcp.tool()
   def process_data(
       data: list[dict[str, Any]],
       filter_key: str
   ) -> list[dict[str, Any]]:
       """
       データをフィルタリングします。

       Args:
           data: 処理するデータのリスト
           filter_key: フィルタリングに使用するキー

       Returns:
           フィルタリングされたデータのリスト
       """
       return [item for item in data if filter_key in item]
   ```

3. **リソース URI の設計**: 論理的で階層的な構造を使用

   ```python
   # 良い例
   @mcp.resource("api://users/{user_id}/posts/{post_id}")
   @mcp.resource("db://products/{category}/{product_id}")

   # 避けるべき例
   @mcp.resource("get-user-post")
   @mcp.resource("product-data")
   ```

## トラブルシューティング

### よくある問題と解決方法

1. **サーバーが起動しない**

   - Python バージョンが 3.10 以上であることを確認
   - 必要な依存関係がインストールされているか確認
   - ポートが既に使用されていないか確認（SSE トランスポート使用時）

2. **ツールが認識されない**

   - `@mcp.tool()`デコレータが正しく適用されているか確認
   - 関数に適切な型ヒントと docstring があるか確認
   - サーバーを再起動してみる

3. **クライアントが接続できない**
   - サーバーが実行中であることを確認
   - 正しいトランスポートタイプを使用しているか確認
   - ファイアウォールやセキュリティソフトが接続をブロックしていないか確認

## 参考リンク

- [FastMCP 公式ドキュメント](https://gofastmcp.com)
- [FastMCP GitHub リポジトリ](https://github.com/jlowin/fastmcp)
- [Model Context Protocol 仕様](https://modelcontextprotocol.io)
- [MCP サーバーディレクトリ](https://mcp.so)

## まとめ

FastMCP は、MCP サーバーを構築するための強力で使いやすいフレームワークです。シンプルなデコレータベースの API により、複雑なプロトコルの詳細を意識することなく、機能の実装に集中できます。このガイドで紹介した基本的な使い方を理解すれば、独自の MCP サーバーを構築し、LLM アプリケーションの機能を拡張できるようになります。
