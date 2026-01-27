# .NET版 Azure AI Foundry エージェントチャットアプリケーション

このディレクトリには、Azure AI Foundryエージェントと連携する.NET 8.0ベースのチャットアプリケーションが含まれています。

## 🎯 概要

既存のPython版チャットアプリケーションを参考に、Azure AI Foundryエージェントと連携する最小構成の.NETアプリケーションとして実装されています。

### 主な特徴

- ✅ **ASP.NET Core 8.0 Web API** - モダンで高性能なWebフレームワーク
- ✅ **Azure AI Foundry統合** - OpenAI互換のエンドポイントを使用
- ✅ **リアルタイムストリーミング** - Server-Sent Events (SSE) によるストリーミングチャット
- ✅ **Azure Identity認証** - DefaultAzureCredentialによる安全な認証
- ✅ **React/TypeScript UI** - 既存のフロントエンドをそのまま使用
- ✅ **Swagger/OpenAPI** - APIドキュメントの自動生成

## 📁 プロジェクト構造

```
sample-app-dotnet/
├── README.md                    # このファイル
└── FoundryChat/                 # メインプロジェクト
    ├── Controllers/
    │   └── ConversationController.cs
    ├── Services/
    │   ├── IFoundryClient.cs
    │   └── FoundryClient.cs
    ├── Models/
    │   ├── ChatMessage.cs
    │   ├── ConversationRequest.cs
    │   └── FoundrySettings.cs
    ├── wwwroot/                 # 静的ファイル（React UI）
    ├── Program.cs
    ├── appsettings.json
    ├── appsettings.Development.json
    ├── .env.sample
    └── README.md               # 詳細なセットアップ手順
```

## 🚀 クイックスタート

### 前提条件

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) 以上
- Azure AI Foundryプロジェクトとアプリケーション
- Azure認証情報（Azure CLI または環境変数）

### セットアップ

1. **プロジェクトディレクトリに移動**
   ```bash
   cd sample-app-dotnet/FoundryChat
   ```

2. **設定ファイルを編集**
   
   `appsettings.Development.json` を編集してFoundry情報を設定：
   ```json
   {
     "Foundry": {
       "Enabled": true,
       "Project": "your-project-id",
       "Application": "your-app-id",
       "Endpoint": "https://your-foundry-endpoint",
       "UseAzureIdentity": true
     }
   }
   ```

3. **Azure認証の設定**
   ```bash
   az login
   ```

4. **アプリケーションの実行**
   ```bash
   dotnet run
   ```

5. **ブラウザでアクセス**
   - UI: https://localhost:5001
   - API Docs: https://localhost:5001/swagger

詳細なセットアップ手順は [FoundryChat/README.md](./FoundryChat/README.md) を参照してください。

## 📚 API仕様

### POST /api/conversation

Foundryエージェントとの会話を処理するエンドポイント

**リクエスト例:**
```json
{
  "messages": [
    {"role": "user", "content": "こんにちは"}
  ],
  "stream": true
}
```

**レスポンス（ストリーミング）:**
```
Content-Type: text/event-stream

data: {"content": "応答テキスト..."}
data: [DONE]
```

**レスポンス（非ストリーミング）:**
```json
{
  "response": "こんにちは、お手伝いできることはありますか？"
}
```

## 🔧 技術スタック

### バックエンド
- ASP.NET Core 8.0 Web API
- Azure.Identity (v1.13.1)
- System.Text.Json

### フロントエンド
- React + TypeScript
- Vite
- 既存のUIをそのまま使用

### 認証
- DefaultAzureCredential
- スコープ: `https://ai.azure.com/.default`

## 🏗️ アーキテクチャ

```
┌─────────────┐
│   Browser   │
│  (React UI) │
└──────┬──────┘
       │ HTTP/SSE
       ▼
┌─────────────────────────┐
│  ASP.NET Core Web API   │
│  ┌──────────────────┐   │
│  │ Conversation     │   │
│  │ Controller       │   │
│  └────────┬─────────┘   │
│           │             │
│  ┌────────▼─────────┐   │
│  │ FoundryClient    │   │
│  │ Service          │   │
│  └────────┬─────────┘   │
└───────────┼─────────────┘
            │ HTTPS + Bearer Token
            ▼
┌─────────────────────────┐
│  Azure AI Foundry       │
│  Agent API              │
└─────────────────────────┘
```

## 🔒 セキュリティ

### 認証方法

1. **Azure Identity (推奨)**
   - DefaultAzureCredentialを使用
   - 開発環境: Azure CLI認証
   - 本番環境: Managed Identity

2. **Bearer Token**
   - 直接トークンを指定
   - 開発・テスト用途のみ推奨

### 環境変数

機密情報は環境変数で管理：
```bash
export Foundry__BearerToken=your-token
export AZURE_TENANT_ID=your-tenant-id
export AZURE_CLIENT_ID=your-client-id
export AZURE_CLIENT_SECRET=your-client-secret
```

## 📊 実装状況

### ✅ 実装済み機能

- Azure AI Foundryエージェント統合
- ストリーミング/非ストリーミング対応
- Azure Identity認証
- OpenAI互換メッセージフォーマット
- Server-Sent Events (SSE)
- エラーハンドリング
- 静的ファイル配信（React UI）
- SPAルーティング対応
- Swagger/OpenAPI ドキュメント
- 設定管理（appsettings.json）

### ❌ 実装対象外

- Azure OpenAI統合
- CosmosDB履歴保存
- ユーザー認証機能
- フィードバック機能
- Azure AI Search統合

## 🧪 テスト

### ビルドテスト
```bash
cd FoundryChat
dotnet build
```

### 実行テスト
```bash
dotnet run
```

### APIテスト
```bash
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}], "stream": false}'
```

## 📦 デプロイ

### Azure App Service

```bash
# 発行
dotnet publish -c Release -o ./publish

# Azureへデプロイ
az webapp up --name your-app-name --resource-group your-rg
```

### Docker

```bash
docker build -t foundry-chat .
docker run -p 5000:80 foundry-chat
```

## 🐛 トラブルシューティング

### "Foundry is not enabled" エラー
→ `appsettings.json` で `Foundry.Enabled` を `true` に設定

### 認証エラー
→ Azure CLI でログイン: `az login`

### タイムアウトエラー
→ `Foundry.ResponseTimeout` の値を増やす

詳細は [FoundryChat/README.md](./FoundryChat/README.md) を参照してください。

## 📖 参考資料

- [詳細なREADME](./FoundryChat/README.md)
- [ASP.NET Core ドキュメント](https://learn.microsoft.com/aspnet/core/)
- [Azure Identity ドキュメント](https://learn.microsoft.com/dotnet/api/azure.identity)
- [Azure AI Foundry](https://azure.microsoft.com/products/ai-services/)
- [Python版実装](../backend/foundry/)

## 📝 ライセンス

このプロジェクトはサンプルアプリケーションです。

## 🤝 貢献

既存のPython版実装との一貫性を保つため、機能追加の際は以下を参照してください：
- `backend/foundry/client.py` - Foundryクライアント実装
- `app.py` (1200-1291行) - エンドポイント実装
- `FOUNDRY.md` - Foundry統合ドキュメント
