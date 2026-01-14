# かっぱキャラクター画像生成ツール

OpenAI Responses API (GPT-4.1)を使用して、かっぱのキャラクター画像を生成するツールです。

## 画像生成APIについて

このツールは**OpenAI Responses API**を使用し、GPT-4.1モデルで画像生成を行います：

- **ベース画像対応**: 最大5枚の参考画像をアップロード可能
- **高精度生成**: input_fidelity="high"で詳細を保持
- **柔軟なプロンプト**: テキストと画像を組み合わせた指示が可能
- **最新技術**: OpenAIの最新Responses APIを使用

## 必要な環境

- Python 3.8以上
- OpenAI APIキー

## セットアップ

1. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

2. OpenAI APIキーの設定（既に設定済みの場合はスキップ）:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 2つの使い方

このツールは2つの方法で利用できます：

### 1. CLI版（コマンドライン）
Pythonスクリプトを直接実行して画像を生成します。バッチ処理や自動化に適しています。

### 2. Web版（ブラウザ）
Docker Composeで起動するWebインターフェース。視覚的な操作で画像を生成・プレビューできます。

---

## プロンプト管理システム

このツールは**ベースプロンプト**と**パターン**を分離して管理する仕組みを採用しています。

### ディレクトリ構造

```
prompts/
├── base_prompt.txt    # 共通のかっぱの特徴（ベースプロンプト）
└── patterns.txt       # パターン一覧（空白行区切り、複数行記述可能）
```

### base_prompt.txt

かっぱの基本的な特徴を記述します（すべてのパターンで共通）：
- 頭の上の水が入った皿
- 背中の亀のような甲羅
- 水かきのある手足
- 緑色のウロコのある体
- など

### patterns.txt

様々なバリエーションを**空白行で区切って**記述します（複数行記述可能）：

**記述例**：
```
# パターン1の説明
The style is charming and suitable for a mascot.
The kappa is waving cheerfully.
The scene is set in spring with cherry blossoms.

# パターン2の説明（空白行で区切る）
The style is anime-inspired with bold outlines.
The kappa is sitting peacefully.
```

**パターンの要素**：
- スタイル（マスコット風、アニメ風、リアル風、ピクセルアート等）
- ポーズ・アクション（手を振る、座る、泳ぐ、ジャンプする等）
- シチュエーション（川辺、都市公園、レストラン等）
- 季節や天候（春の桜、夏の太陽、秋の紅葉、冬の雪等）
- 画像サイズや画質の指定（任意）

---

## CLI版の使い方

### 1. パターン一覧を表示

```bash
python generate_kappa.py --list
```

利用可能なすべてのパターンが番号付きで表示されます。

### 2. すべてのパターンで一括生成

```bash
# すべてのパターン（25種類）の画像を一括生成
python generate_kappa.py --all

# 短縮形も使用可能
python generate_kappa.py -a

# 高画質で一括生成
python generate_kappa.py --all --quality hd
```

**注意**: 一括生成は25枚の画像を生成するため、APIクレジットを多く消費します（standard品質で約$1.00、hd品質で約$2.00）。

### 3. デフォルト実行（パターン#1を使用）

```bash
python generate_kappa.py
```

### 4. パターン番号を指定して生成

```bash
# パターン3を使用
python generate_kappa.py --pattern 3

# 短縮形も使用可能
python generate_kappa.py -p 5
```

### 5. カスタムプロンプトで生成

```bash
# ベースプロンプト + カスタムプロンプト
python generate_kappa.py --custom "かわいいかっぱが泳いでいる"

# 短縮形も使用可能
python generate_kappa.py -c "The kappa is reading a book under a tree."
```

### 6. 画質やサイズを指定

```bash
# 高画質で生成
python generate_kappa.py --pattern 5 --quality hd

# カスタムサイズで生成（縦長）
python generate_kappa.py --pattern 1 --size 1024x1792

# 複合例
python generate_kappa.py -p 10 -q hd -s 1792x1024
```

### コマンドライン引数一覧

| 引数 | 短縮形 | 説明 | デフォルト |
|------|--------|------|-----------|
| `--list` | `-l` | パターン一覧を表示 | - |
| `--all` | `-a` | すべてのパターンで画像を一括生成 | - |
| `--pattern N` | `-p N` | パターン番号を指定（1から始まる） | 1 |
| `--custom "text"` | `-c "text"` | カスタムプロンプトを指定 | - |
| `--size SIZE` | `-s SIZE` | 画像サイズ（1024x1024, 1024x1792, 1792x1024） | 1024x1024 |
| `--quality Q` | `-q Q` | 画質（standard, hd） | standard |

### ヘルプ表示

```bash
python generate_kappa.py --help
```

## 出力ファイル

生成された画像は `generated_images/` ディレクトリに保存されます：

```
generated_images/
├── kappa_20260115_143022_p3.png        # 画像ファイル（パターン3を使用）
└── kappa_20260115_143022_p3_info.txt  # 生成情報（プロンプト等）
```

ファイル名の形式：
- `kappa_YYYYMMDD_HHMMSS_pN.png` - パターン番号Nを使用した場合
- `kappa_YYYYMMDD_HHMMSS.png` - カスタムプロンプトを使用した場合

---

## Web版の使い方（Docker Compose）

Web版はDockerを使用してローカル環境を汚さずに実行できます。ブラウザから簡単に画像生成が可能です。

### 必要な環境

- Docker Desktop for Mac
- Docker Compose（Docker Desktopに含まれています）
- OpenAI APIキー（環境変数に設定済み）

### セットアップ

1. **OpenAI APIキーの確認**

既にMacのシェルに設定されているか確認：

```bash
echo $OPENAI_API_KEY
```

設定されていない場合は以下で設定：

```bash
export OPENAI_API_KEY='your-api-key-here'
```

永続化する場合は `~/.zshrc` に追加：

```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

2. **起動スクリプトに実行権限を付与**

```bash
chmod +x start.sh stop.sh
```

### 起動方法

```bash
./start.sh
```

起動スクリプトが以下を自動的に実行します：
- Dockerコンテナのビルドと起動
- 動的なポート割り当て
- ブラウザの自動起動

コンソールに表示されるURL（例：`http://localhost:52341`）からアクセスできます。

### Web版の機能

- **ベース画像アップロード**: 最大5枚の参考画像をアップロード可能（任意）
- **共通プロンプト編集**: かっぱの基本的な特徴を記述
- **パターン選択**: 複数行対応のパターンから選択、またはカスタム入力
- **プロンプト内設定**: 画像サイズや画質をプロンプト内で柔軟に指定
- **1枚生成**: 選択したパターンで画像を1枚生成
- **全パターン一括生成**: 全てのパターンで画像を一括生成（進捗表示付き）
- **リアルタイムプレビュー**: 生成された画像をブラウザで即座に確認
- **ダウンロード**: 生成した画像を直接ダウンロード

**技術詳細**：
- OpenAI Responses API (GPT-4.1)を使用
- ベース画像アップロード時は `input_fidelity: "high"` で高精度生成
- 複数行パターン対応で、より詳細な指示が可能
- 全パターン一括生成で、複数バリエーションを効率的に作成

### 停止方法

```bash
./stop.sh
```

### Web版のトラブルシューティング

#### ポートが取得できない

```bash
# コンテナのログを確認
docker compose logs app

# コンテナを再起動
./stop.sh
./start.sh
```

#### APIキーのエラー

```bash
# 環境変数を確認
echo $OPENAI_API_KEY

# 設定し直す
export OPENAI_API_KEY='your-api-key-here'

# コンテナを再起動
./stop.sh
./start.sh
```

#### コンテナが起動しない

```bash
# Dockerが起動しているか確認
docker ps

# イメージを再ビルド
docker compose build --no-cache
./start.sh
```

---

## パターンのカスタマイズ

### 新しいパターンの追加

`prompts/patterns.txt` に**空白行で区切って**新しいパターンを追加します（複数行OK）：

```
# あなたの新しいパターン（複数行記述可能）
The style is traditional Japanese art.
The kappa is wearing a samurai armor and holding a katana.
The scene is set in an ancient Japanese castle.
Image size: 1024x1792, Quality: HD

# 別のパターン（空白行で区切る）
The style is modern digital art.
The kappa is coding on a laptop.
```

### ベースプロンプトの編集

`prompts/base_prompt.txt` を編集することで、すべてのパターンに共通する特徴を変更できます。

## 注意事項

- GPT Image 1.5は1回の実行につきAPIクレジットを消費します
- 画像のサイズや画質によってAPIクレジットの消費量が変わります
  - `standard` 品質: 約$0.04 per image
  - `hd` 品質: 約$0.08 per image

## トラブルシューティング

### エラー: ベースプロンプトファイルが見つかりません

`prompts/base_prompt.txt` が存在することを確認してください。

### エラー: パターンファイルが見つかりません

`prompts/patterns.txt` が存在することを確認してください。

### エラー: OPENAI_API_KEY環境変数が設定されていません

OpenAI APIキーを環境変数に設定してください：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 生成例

### かっぱの基本的な特徴（ベースプロンプト）
- 頭の上に水が入った皿
- 背中に亀のような甲羅
- 水かきのある手足
- 緑色のウロコのある体
- 大きくて表情豊かな目
- フレンドリーな笑顔

### パターン例
- マスコット風の可愛らしいスタイル
- アニメ風のイラスト
- 手を振っているポーズ
- 川辺で遊んでいるシチュエーション
- 春の桜の季節設定
- など（`prompts/patterns.txt` に多数のパターンを用意）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
