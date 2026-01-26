# Azure AI Foundry Agent Integration Guide

## 概要

このアプリケーションでは、Azure OpenAI に加えて **Azure AI Foundry Agent** との統合がサポートされています。

## Foundry Agent の設定方法

### 1. Bearer Token の取得

Azure AI Foundry ポータルで Bearer Token を生成します：

1. Azure AI Foundry にログイン
2. プロジェクト設定に移動
3. 「認証」または「API Keys」セクションから Bearer Token を生成
4. トークンをコピーして安全に保管

### 2. 環境変数の設定

`.env` ファイルに以下の設定を追加：

```bash
# Azure AI Foundry Agent Settings
FOUNDRY_ENABLED=True
FOUNDRY_PROJECT=demo-kddi
FOUNDRY_APPLICATION=IncidentKnowledgeAgent
FOUNDRY_ENDPOINT=https://demo-kddi-resource.services.ai.azure.com
FOUNDRY_BEARER_TOKEN=<your-bearer-token-here>
FOUNDRY_API_VERSION=2025-11-15-preview
```

**設定項目の説明：**

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `FOUNDRY_ENABLED` | Foundry を有効化 (`True`/`False`) | はい |
| `FOUNDRY_PROJECT` | Foundry プロジェクト名 | はい |
| `FOUNDRY_APPLICATION` | Foundry アプリケーション名 | はい |
| `FOUNDRY_ENDPOINT` | Foundry エンドポイントURL | はい |
| `FOUNDRY_BEARER_TOKEN` | 認証用Bearer Token | はい |
| `FOUNDRY_API_VERSION` | API バージョン | いいえ (デフォルト: `2025-11-15-preview`) |

### 3. サーバーの起動

設定後、通常通りサーバーを起動：

```bash
python -m uvicorn app:app --port 50505 --reload
```

## API エンドポイント

### Foundry Conversation Endpoint

**URL:** `/foundry/conversation`  
**Method:** `POST`

#### リクエスト例（ストリーミング）

```json
{
  "messages": [
    {
      "role": "user",
      "content": "こんにちは"
    }
  ],
  "stream": true
}
```

#### リクエスト例（非ストリーミング）

```json
{
  "messages": [
    {
      "role": "user",
      "content": "こんにちは"
    }
  ],
  "stream": false
}
```

#### レスポンス（ストリーミング）

```
data: {"choices":[{"delta":{"content":"こん"}}]}

data: {"choices":[{"delta":{"content":"にちは"}}]}

data: [DONE]
```

## フロントエンドとの統合

フロントエンドで Foundry を使用するには、`/foundry/conversation` エンドポイントに POST リクエストを送信します。

既存の Azure OpenAI エンドポイントと同じメッセージフォーマット（OpenAI 互換）を使用できます。

## トラブルシューティング

### 1. "Foundry is not enabled" エラー

**原因:** `.env` ファイルで `FOUNDRY_ENABLED=True` が設定されていない

**解決策:** `.env` ファイルを確認し、`FOUNDRY_ENABLED=True` を設定

### 2. "Failed to initialize Foundry client" エラー

**原因:** Bearer Token が設定されていない、または無効

**解決策:**
- `.env` ファイルで `FOUNDRY_BEARER_TOKEN` が正しく設定されているか確認
- Azure AI Foundry ポータルで新しいトークンを生成

### 3. 401 Unauthorized エラー

**原因:** Bearer Token の有効期限切れ、または権限不足

**解決策:**
- Azure AI Foundry ポータルで新しいトークンを生成
- トークンに必要な権限があるか確認

### 4. 接続タイムアウト

**原因:** ネットワークの問題、またはエンドポイントURLの誤り

**解決策:**
- `FOUNDRY_ENDPOINT` が正しいか確認
- ネットワーク接続を確認
- ファイアウォール設定を確認

## セキュリティ上の注意

?? **重要:** Bearer Token は機密情報です！

- `.env` ファイルは `.gitignore` に含まれており、Git にコミットされません
- Bearer Token を公開リポジトリにコミットしないでください
- 本番環境では Azure Key Vault などの安全な方法でトークンを管理してください

## 既存機能との互換性

- Azure OpenAI の既存機能は影響を受けません
- `FOUNDRY_ENABLED=False` の場合、Foundry 機能は無効化されます
- 両方のバックエンドを同時に有効化できます

## アーキテクチャ

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
    /conversation   /foundry/conversation
         │              │
         ▼              ▼
┌────────────┐   ┌────────────┐
│  Azure     │   │  Foundry   │
│  OpenAI    │   │  Agent     │
└────────────┘   └────────────┘
```

## 参考リンク

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
