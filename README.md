# mcp-gpt-image

OpenAI の `gpt-image-2` を使った画像生成 MCP サーバー。ツールは `generate_image` のみ。

## セットアップ

```bash
# 依存インストール
uv sync

# API キーを設定
cp .env.example .env
# .env の OPENAI_API_KEY を編集
```

## 環境変数

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `OPENAI_API_KEY` | (必須) | OpenAI API キー |
| `OPENAI_IMAGE_MODEL` | `gpt-image-2` | 使用するモデル |
| `MCP_GPT_IMAGE_OUTPUT_DIR` | `./generated` | 画像の保存先ディレクトリ |

## ツール: `generate_image`

| 引数 | 型 | デフォルト | 説明 |
|------|----|-----------|------|
| `prompt` | string | (必須) | 生成する画像のテキスト説明 |
| `size` | string | `1024x1024` | `1024x1024` / `1024x1536` / `1536x1024` / `auto` |
| `quality` | string | `auto` | `low` / `medium` / `high` / `auto` |
| `background` | string | `auto` | `transparent` / `opaque` / `auto` |
| `filename` | string | (自動生成) | 拡張子なしの保存ファイル名 |

返り値: 保存された PNG ファイルの絶対パス。

## Claude Desktop への登録

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) に追加:

```json
{
  "mcpServers": {
    "gpt-image": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-gpt-image", "run", "server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

## Claude Code への登録

プロジェクトルートの `.mcp.json` または `~/.claude/mcp.json` に追加:

```json
{
  "mcpServers": {
    "gpt-image": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-gpt-image", "run", "server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

## 動作確認 (MCP Inspector)

```bash
OPENAI_API_KEY=sk-... uv run mcp dev server.py
```

ブラウザで Inspector が開くので `generate_image` ツールに `prompt` を渡して実行する。
