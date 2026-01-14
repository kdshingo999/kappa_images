# かっぱキャラクター画像生成ツール

OpenAI GPT Image 1.5を使用して、かっぱのキャラクター画像を生成するPythonスクリプトです。

## GPT Image 1.5について

GPT Image 1.5は2025年12月にリリースされたOpenAIの最新画像生成モデルです：

- **高速生成**: 従来のDALL-E 3より最大4倍速い生成速度
- **高精度**: より正確な指示追従と画像編集が可能
- **自然な結果**: より自然で高品質な画像を生成
- **テキスト描画**: 画像内のテキストレンダリングが改善
- **コスト効率**: DALL-E 3と比較して20%安いAPIクレジット

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

## プロンプト管理システム

このツールは**ベースプロンプト**と**パターン**を分離して管理する仕組みを採用しています。

### ディレクトリ構造

```
prompts/
├── base_prompt.txt    # 共通のかっぱの特徴（ベースプロンプト）
└── patterns.txt       # パターン一覧（スタイル、ポーズ、シチュエーション等）
```

### base_prompt.txt

かっぱの基本的な特徴を記述します（すべてのパターンで共通）：
- 頭の上の水が入った皿
- 背中の亀のような甲羅
- 水かきのある手足
- 緑色のウロコのある体
- など

### patterns.txt

様々なバリエーションを1行ずつ記述します：
- スタイル（マスコット風、アニメ風、リアル風、ピクセルアート等）
- ポーズ（手を振る、座る、泳ぐ、ジャンプする等）
- シチュエーション（川辺、都市公園、レストラン等）
- 季節や天候（春の桜、夏の太陽、秋の紅葉、冬の雪等）

## 使い方

### 1. パターン一覧を表示

```bash
python generate_kappa.py --list
```

利用可能なすべてのパターンが番号付きで表示されます。

### 2. デフォルト実行（パターン#1を使用）

```bash
python generate_kappa.py
```

### 3. パターン番号を指定して生成

```bash
# パターン3を使用
python generate_kappa.py --pattern 3

# 短縮形も使用可能
python generate_kappa.py -p 5
```

### 4. カスタムプロンプトで生成

```bash
# ベースプロンプト + カスタムプロンプト
python generate_kappa.py --custom "かわいいかっぱが泳いでいる"

# 短縮形も使用可能
python generate_kappa.py -c "The kappa is reading a book under a tree."
```

### 5. 画質やサイズを指定

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

## パターンのカスタマイズ

### 新しいパターンの追加

`prompts/patterns.txt` に新しい行を追加するだけです：

```
# あなたの新しいパターン
The kappa is wearing a samurai armor and holding a katana.
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
