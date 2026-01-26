# Foundry エージェント統合 要件定義書

## 1. プロジェクト概要

### 1.1 目的
既存の Azure OpenAI チャットアプリケーションに、Palantir Foundry エージェントとの対話機能を追加し、ユーザーが Azure OpenAI と Foundry エージェントのいずれかを選択して利用できるようにする。

### 1.2 背景
- 現在、アプリケーションは Azure OpenAI のみをサポート
- Foundry で構築されたカスタムエージェントを活用したい
- 両方のバックエンドをシームレスに切り替えられる柔軟性が必要

### 1.3 スコープ
**対象範囲：**
- Foundry エージェント API との統合
- Bearer Token 認証の実装
- バックエンドの選択機能（Azure OpenAI / Foundry）
- 既存機能の互換性維持

**対象外：**
- Foundry エージェントの新規作成
- フロントエンドの大幅なUI変更
- 既存の Azure OpenAI 機能の変更

---

## 2. 機能要件

### 2.1 Foundry エージェント統合

#### FR-001: Foundry API 接続
- **優先度:** 高
- **説明:** Foundry エンドポイントに対して HTTP リクエストを送信し、レスポンスを受信する
- **受入基準:**
  - Bearer Token を使用した認証が成功する
  - POST リクエストでメッセージを送信できる
  - JSON レスポンスを正常に受信できる

#### FR-002: 環境変数による設定
- **優先度:** 高
- **説明:** `.env` ファイルで Foundry の設定を管理
- **設定項目:**
  ```
  FOUNDRY_ENABLED=True/False
  FOUNDRY_ENDPOINT=https://demo-kddi-resource.servic...
  FOUNDRY_BEARER_TOKEN=<token>
  FOUNDRY_REGION=eastus2
  FOUNDRY_AGENT_ID=<optional>
  ```
- **受入基準:**
  - 環境変数から設定を読み込める
  - 設定が不正な場合、適切なエラーメッセージを表示

#### FR-003: バックエンド選択機能
- **優先度:** 中
- **説明:** Azure OpenAI と Foundry を切り替えられる
- **実装方法:**
  - 環境変数 `BACKEND_TYPE=azure_openai|foundry` で制御
  - または、両方有効にして動的に選択
- **受入基準:**
  - 設定に応じて適切なバックエンドが使用される
  - 切り替え時にアプリケーションが正常動作する

#### FR-004: ストリーミングレスポンス対応
- **優先度:** 中
- **説明:** Foundry がストリーミングをサポートする場合、対応する
- **受入基準:**
  - ストリーミングレスポンスを段階的に表示
  - 非ストリーミングモードでも動作
  - Azure OpenAI と同じUXを提供

#### FR-005: エラーハンドリング
- **優先度:** 高
- **説明:** Foundry API のエラーを適切に処理
- **エラーケース:**
  - 認証失敗（401 Unauthorized）
  - エンドポイント不到達（Network Error）
  - タイムアウト
  - API レート制限
- **受入基準:**
  - ユーザーフレンドリーなエラーメッセージを表示
  - ログに詳細なエラー情報を記録
  - アプリケーションがクラッシュしない

### 2.2 既存機能の維持

#### FR-006: Azure OpenAI 機能の維持
- **優先度:** 高
- **説明:** 既存の Azure OpenAI 機能が引き続き動作する
- **受入基準:**
  - 既存のチャット機能が正常動作
  - Azure OpenAI の設定が変更されていない
  - レグレッションが発生していない

#### FR-007: UI の互換性
- **優先度:** 高
- **説明:** フロントエンドは両方のバックエンドで動作する
- **受入基準:**
  - メッセージ送信・受信が正常動作
  - チャット履歴が表示される
  - UI の表示崩れがない

---

## 3. 非機能要件

### 3.1 パフォーマンス
- **NFR-001:** レスポンスタイムは Azure OpenAI と同等（3秒以内）
- **NFR-002:** 並行リクエストを処理できる（最低10並行）
- **NFR-003:** タイムアウトは30秒に設定

### 3.2 セキュリティ
- **NFR-004:** Bearer Token は環境変数で管理し、コードにハードコードしない
- **NFR-005:** `.env` ファイルは `.gitignore` に含める
- **NFR-006:** HTTPS 通信を使用
- **NFR-007:** トークンはログに出力しない

### 3.3 保守性
- **NFR-008:** コードは既存の構造に従う
- **NFR-009:** 設定は一元管理（`backend/settings.py`）
- **NFR-010:** 適切なログ出力（DEBUG, INFO, ERROR レベル）

### 3.4 可用性
- **NFR-011:** Foundry API が利用不可の場合、適切なエラーを返す
- **NFR-012:** アプリケーション起動時に接続をテストしない（遅延起動を避ける）

---

## 4. 技術要件

### 4.1 開発環境
- Python 3.11/3.13
- Quart (非同期Webフレームワーク)
- httpx (HTTP クライアント)
- pydantic-settings (設定管理)

### 4.2 Foundry API 仕様（想定）
```python
# リクエスト例
POST {FOUNDRY_ENDPOINT}/chat
Headers:
  Authorization: Bearer {FOUNDRY_BEARER_TOKEN}
  Content-Type: application/json
Body:
  {
    "message": "ユーザーのメッセージ",
    "conversation_id": "optional-session-id",
    "stream": true/false
  }

# レスポンス例
{
  "response": "エージェントの応答",
  "conversation_id": "session-id",
  "metadata": {...}
}
```

**注意:** 実際のAPI仕様は実装時に確認・調整する

### 4.3 依存ライブラリ
- 既存: `httpx==*` (requirements.txt に含まれる可能性あり)
- 必要に応じて追加

---

## 5. 実装方針

### 5.1 アーキテクチャ

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend       │
│   (Quart)       │
├─────────────────┤
│  ┌──────────┐   │
│  │ Router   │   │  ← 既存の app.py
│  └────┬─────┘   │
│       │         │
│  ┌────▼──────────────┐
│  │ Backend Factory   │  ← 新規追加
│  └────┬──────────────┘
│       │
│  ┌────▼─────┐  ┌────▼─────┐
│  │ Azure    │  │ Foundry  │  ← 新規追加
│  │ OpenAI   │  │ Client   │
│  └──────────┘  └──────────┘
└─────────────────┘
```

### 5.2 ファイル構成

```
sample-app-aoai-chatGPT-main/
├── backend/
│   ├── settings.py              # 設定管理（Foundry設定追加）
│   ├── foundry/                 # 新規ディレクトリ
│   │   ├── __init__.py
│   │   ├── client.py            # Foundry API クライアント
│   │   └── models.py            # データモデル
│   └── backends/                # 新規ディレクトリ（任意）
│       ├── __init__.py
│       ├── base.py              # 抽象ベースクラス
│       ├── azure_openai.py      # Azure OpenAI ラッパー
│       └── foundry.py           # Foundry ラッパー
├── app.py                       # ルーティング（最小限の変更）
├── .env                         # 環境変数（Foundry設定追加）
└── requirements.txt             # 依存関係（必要に応じて追加）
```

### 5.3 実装ステップ

#### Phase 1: 基盤実装
1. **設定の追加** (`backend/settings.py`)
   - Foundry 設定クラスを追加
   - 環境変数の読み込み

2. **Foundry クライアントの実装** (`backend/foundry/client.py`)
   - Bearer Token 認証
   - POST リクエストの実装
   - エラーハンドリング

3. **ユニットテストの作成**
   - 設定の読み込みテスト
   - API クライアントのモックテスト

#### Phase 2: 統合
4. **バックエンド抽象化** (任意)
   - 共通インターフェースの定義
   - Azure OpenAI と Foundry の統一

5. **ルーティングの更新** (`app.py`)
   - バックエンド選択ロジック
   - 既存エンドポイントの更新

6. **統合テスト**
   - E2E テスト
   - レグレッションテスト

#### Phase 3: 最適化
7. **ストリーミング対応**（Foundry がサポートする場合）
8. **ログ・監視の追加**
9. **ドキュメント更新**

---

## 6. 前提条件

### 6.1 Foundry 側
- [ ] Foundry エージェントが作成済み
- [ ] API エンドポイントが公開されている
- [ ] Bearer Token が発行可能
- [ ] API ドキュメントが利用可能

### 6.2 開発環境
- [ ] Python 3.11+ がインストール済み
- [ ] 既存アプリケーションが動作している
- [ ] Git リポジトリが設定済み

---

## 7. 制約事項

### 7.1 技術的制約
- Foundry API の仕様が不明な部分は実装時に調整
- APIキー認証が無効のため、Bearer Token を使用
- ストリーミング対応は Foundry API の仕様次第

### 7.2 スコープ外
- Foundry エージェントの作成・設定
- 複数エージェントの同時利用
- チャット履歴の永続化（CosmosDB）への Foundry 対応

---

## 8. 成果物

### 8.1 コード
- [ ] `backend/settings.py` の更新
- [ ] `backend/foundry/client.py` の実装
- [ ] `app.py` の更新
- [ ] `.env.sample` の更新

### 8.2 ドキュメント
- [ ] README.md の更新（Foundry 設定手順）
- [ ] API 設計ドキュメント
- [ ] テスト計画書

### 8.3 テスト
- [ ] ユニットテスト
- [ ] 統合テスト
- [ ] 動作確認手順書

---

## 9. スケジュール（概算）

| フェーズ | タスク | 所要時間 |
|---------|--------|---------|
| Phase 1 | 設定・クライアント実装 | 2-3時間 |
| Phase 2 | 統合・テスト | 2-3時間 |
| Phase 3 | 最適化・ドキュメント | 1-2時間 |
| **合計** | | **5-8時間** |

---

## 10. リスクと対策

| リスク | 影響度 | 対策 |
|-------|--------|-----|
| Foundry API 仕様が不明 | 高 | 事前にAPI ドキュメントを確認。モック実装で先行開発 |
| Bearer Token の有効期限切れ | 中 | トークンリフレッシュ機能を検討。エラーハンドリングを強化 |
| ストリーミング未対応 | 低 | 非ストリーミングモードで実装。後で拡張可能に設計 |
| 既存機能のレグレッション | 中 | 十分なテストを実施。バックエンド選択を環境変数で制御 |

---

## 11. 承認

| 役割 | 氏名 | 承認日 |
|-----|------|--------|
| 要件定義者 | - | - |
| 開発者 | - | - |
| レビュアー | - | - |

---

## 12. 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|-----|----------|---------|--------|
| 2025-01-XX | 1.0 | 初版作成 | - |

---

## 13. 補足資料

### 13.1 Foundry エージェント情報
- **エンドポイント:** `https://demo-kddi-resource.servic...`
- **リージョン:** `eastus2`
- **認証:** Bearer Token

### 13.2 参考リンク
- [Palantir Foundry Documentation](https://www.palantir.com/docs/foundry/)
- [Quart Documentation](https://quart.palletsprojects.com/)
- [httpx Documentation](https://www.python-httpx.org/)
