# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# 依存インストール
uv sync

# サーバー起動 (stdio トランスポート)
OPENAI_API_KEY=sk-... uv run server.py

# MCP Inspector で対話的にテスト
OPENAI_API_KEY=sk-... uv run mcp dev server.py
```

## Architecture

`server.py` 1ファイルのみで完結する極小 MCP サーバー。

- **FastMCP** (`mcp.server.fastmcp`) をフレームワークに使用。`mcp.run()` が stdio トランスポートでループする。
- 公開ツールは `generate_image` のみ。`@mcp.tool()` デコレータで登録。
- OpenAI `client.images.generate()` を呼び、返ってきた base64 を PNG としてディスクに保存し、絶対パスを返す。base64 を MCP レスポンスに直接含めないのはコンテキスト肥大化を避けるため。
- モデル名・出力先は環境変数 (`OPENAI_IMAGE_MODEL`, `MCP_GPT_IMAGE_OUTPUT_DIR`) で上書き可能。デフォルトはそれぞれ `gpt-image-2`、`./generated`。
- `OPENAI_API_KEY` 未設定の場合は起動時に `sys.exit(1)`。

## 環境変数

| 変数 | デフォルト |
|------|-----------|
| `OPENAI_API_KEY` | (必須) |
| `OPENAI_IMAGE_MODEL` | `gpt-image-2` |
| `MCP_GPT_IMAGE_OUTPUT_DIR` | `./generated` |
