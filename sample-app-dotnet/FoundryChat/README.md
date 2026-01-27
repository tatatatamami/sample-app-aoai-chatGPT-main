# .NET版 Azure AI Foundry エージェントチャットアプリ

このプロジェクトは、Azure AI Foundryエージェントと連携する.NET 8.0 ベースのチャットアプリケーションです。

## 概要

- ASP.NET Core 8.0 Web API
- Azure AI Foundryエージェントとの統合
- リアルタイムストリーミングチャット
- Azure Identity (DefaultAzureCredential) による認証
- React/TypeScript フロントエンド（既存UIを使用）

## 必要な環境

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) 以上
- Azure AI Foundry プロジェクトとアプリケーション
- Azure サブスクリプション（Azure Identity認証を使用する場合）

## プロジェクト構造

```
FoundryChat/
├── Program.cs                      # アプリケーションエントリポイント
├── appsettings.json               # 本番環境設定
├── appsettings.Development.json   # 開発環境設定
├── Controllers/
│   └── ConversationController.cs  # 会話APIコントローラー
├── Services/
│   ├── IFoundryClient.cs         # Foundryクライアントインターフェース
│   └── FoundryClient.cs          # Foundryクライアント実装
├── Models/
│   ├── ChatMessage.cs            # チャットメッセージモデル
│   ├── ConversationRequest.cs    # リクエストモデル
│   └── FoundrySettings.cs        # Foundry設定モデル
└── wwwroot/                       # 静的ファイル（React UI）
    ├── index.html
    ├── assets/
    └── favicon.ico
```

## セットアップ手順

### 1. プロジェクトのクローン

```bash
cd sample-app-dotnet/FoundryChat
```

### 2. 設定ファイルの編集

`appsettings.Development.json` を編集して、Azure AI Foundry の情報を設定します：

```json
{
  "Foundry": {
    "Enabled": true,
    "Project": "your-project-id",
    "Application": "your-app-id",
    "Endpoint": "https://your-foundry-endpoint",
    "UseAzureIdentity": true,
    "ResponseTimeout": 30
  }
}
```

#### 設定項目の説明

| 項目 | 必須 | 説明 |
|------|------|------|
| `Enabled` | はい | Foundryエージェントを有効にするか |
| `Project` | はい | Foundry プロジェクトID |
| `Application` | はい | Foundry アプリケーションID |
| `Endpoint` | はい | Foundry エンドポイントURL |
| `BearerToken` | 条件付き | Bearer認証トークン（UseAzureIdentityがfalseの場合） |
| `UseAzureIdentity` | いいえ | Azure Identity認証を使用するか（デフォルト: true） |
| `ApiVersion` | いいえ | APIバージョン（デフォルト: 2025-11-15-preview） |
| `ResponseTimeout` | いいえ | タイムアウト秒数（デフォルト: 30） |

### 3. 環境変数での設定（オプション）

環境変数で設定を上書きすることもできます：

```bash
export Foundry__Enabled=true
export Foundry__Project=your-project-id
export Foundry__Application=your-app-id
export Foundry__Endpoint=https://your-foundry-endpoint
export Foundry__UseAzureIdentity=true
```

### 4. Azure認証の設定

Azure Identity (DefaultAzureCredential) を使用する場合、以下のいずれかの方法で認証します：

**開発環境:**
```bash
# Azure CLI でログイン
az login

# または環境変数で指定
export AZURE_TENANT_ID=your-tenant-id
export AZURE_CLIENT_ID=your-client-id
export AZURE_CLIENT_SECRET=your-client-secret
```

**本番環境:**
- Azure Managed Identity を使用
- App Service、Azure Functions、Azure Container Instances などで自動的に利用可能

### 5. アプリケーションの実行

```bash
# ビルド
dotnet build

# 実行
dotnet run
```

アプリケーションは `https://localhost:5001` (HTTPS) または `http://localhost:5000` (HTTP) で起動します。

### 6. アプリケーションへのアクセス

ブラウザで以下のURLにアクセスします：

- **Web UI**: https://localhost:5001
- **API ドキュメント (Swagger)**: https://localhost:5001/swagger

## API仕様

### POST /api/conversation

Foundryエージェントとの会話を処理します。

**リクエスト:**

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

data: {"content": "こんにちは..."}

data: [DONE]
```

**レスポンス（非ストリーミング）:**

```json
{
  "response": "こんにちは、お手伝いできることはありますか？"
}
```

## 認証フロー

1. **Azure Identity認証**
   - `DefaultAzureCredential` を使用して自動的に認証
   - スコープ: `https://ai.azure.com/.default`
   - 取得したトークンをFoundry APIに送信

2. **Bearer Token認証**
   - 設定ファイルまたは環境変数で指定
   - 直接Foundry APIに送信

## トラブルシューティング

### "Foundry is not enabled" エラー

設定ファイルで `Foundry.Enabled` が `true` に設定されているか確認してください。

### 認証エラー

- Azure CLI でログインしているか確認: `az account show`
- 正しいテナントにログインしているか確認
- Managed Identity が有効化されているか確認（本番環境）

### タイムアウトエラー

`Foundry.ResponseTimeout` の値を増やしてください（デフォルト: 30秒）。

## 開発

### デバッグ実行

Visual Studio または Visual Studio Code でデバッグ実行できます：

```bash
# Visual Studio Code
code .

# F5 でデバッグ開始
```

### ログレベルの変更

`appsettings.Development.json` でログレベルを調整：

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft.AspNetCore": "Information",
      "FoundryChat": "Debug"
    }
  }
}
```

## デプロイ

### Azure App Service へのデプロイ

```bash
# 発行
dotnet publish -c Release -o ./publish

# Azure へデプロイ
az webapp up --name your-app-name --resource-group your-rg
```

### Docker でのデプロイ

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["FoundryChat.csproj", "./"]
RUN dotnet restore
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "FoundryChat.dll"]
```

## ライセンス

このプロジェクトはサンプルアプリケーションです。

## 参考資料

- [ASP.NET Core ドキュメント](https://learn.microsoft.com/aspnet/core/)
- [Azure Identity ドキュメント](https://learn.microsoft.com/dotnet/api/azure.identity)
- [Azure AI Foundry](https://azure.microsoft.com/products/ai-services/)
