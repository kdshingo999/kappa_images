#!/usr/bin/env python3
"""
かっぱのキャラクター画像を生成するスクリプト
OpenAI GPT Image 1.5を使用
"""

import os
import sys
import base64
import argparse
from datetime import datetime
from pathlib import Path
from openai import OpenAI


def load_base_prompt(base_prompt_file: str = "prompts/base_prompt.txt") -> str:
    """
    ベースプロンプトをファイルから読み込む

    Args:
        base_prompt_file: ベースプロンプトファイルのパス

    Returns:
        ベースプロンプトの文字列
    """
    try:
        with open(base_prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"エラー: ベースプロンプトファイルが見つかりません: {base_prompt_file}")
        sys.exit(1)


def load_patterns(patterns_file: str = "prompts/patterns.txt") -> list:
    """
    パターンファイルから有効なパターンを読み込む
    空白行で区切られた複数行のパターンに対応

    Args:
        patterns_file: パターンファイルのパス

    Returns:
        パターンのリスト（空白行で区切られた複数行パターン）
    """
    try:
        with open(patterns_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        patterns = []
        current_pattern = []

        for line in lines:
            line_stripped = line.strip()

            # コメント行をスキップ
            if line_stripped.startswith("#"):
                continue

            # 空行でパターン区切り
            if not line_stripped:
                if current_pattern:
                    patterns.append("\n".join(current_pattern))
                    current_pattern = []
            else:
                current_pattern.append(line_stripped)

        # 最後のパターンを追加
        if current_pattern:
            patterns.append("\n".join(current_pattern))

        return patterns
    except FileNotFoundError:
        print(f"エラー: パターンファイルが見つかりません: {patterns_file}")
        sys.exit(1)


def list_patterns(patterns: list):
    """
    利用可能なパターン一覧を表示する（複数行対応）

    Args:
        patterns: パターンのリスト
    """
    print("\n利用可能なパターン一覧:")
    print("=" * 60)
    for i, pattern in enumerate(patterns, 1):
        # 複数行パターンの最初の行のみ表示
        first_line = pattern.split('\n')[0]
        preview = first_line[:70] + "..." if len(first_line) > 70 else first_line
        print(f"{i:2d}. {preview}")
    print("=" * 60)


def generate_kappa_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    pattern_number: int = None
):
    """
    かっぱのキャラクター画像を生成する

    Args:
        prompt: プロンプト
        size: 画像サイズ ("1024x1024", "1024x1792", "1792x1024")
        quality: 画質 ("standard" or "hd")
        pattern_number: 使用したパターン番号（記録用、Noneの場合は記録しない）
    """
    # OpenAI APIキーの確認
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        sys.exit(1)

    # OpenAIクライアントの初期化
    client = OpenAI(api_key=api_key)

    print(f"\n画像生成中...")
    print(f"プロンプト: {prompt[:100]}..." if len(prompt) > 100 else f"プロンプト: {prompt}")
    print(f"サイズ: {size}, 画質: {quality}")

    try:
        # GPT Image 1.5で画像生成
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        # 生成された画像データ（base64形式）
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        print(f"\n✓ 画像生成成功!")

        # 画像を保存するディレクトリを作成
        output_dir = Path("generated_images")
        output_dir.mkdir(exist_ok=True)

        # タイムスタンプ付きのファイル名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pattern_suffix = f"_p{pattern_number}" if pattern_number else ""
        image_filename = f"kappa_{timestamp}{pattern_suffix}.png"
        image_filepath = output_dir / image_filename

        # 画像を保存
        with open(image_filepath, "wb") as f:
            f.write(image_bytes)

        print(f"画像を保存しました: {image_filepath}")

        # プロンプト情報をテキストファイルに保存
        info_filename = f"kappa_{timestamp}{pattern_suffix}_info.txt"
        info_filepath = output_dir / info_filename

        with open(info_filepath, "w", encoding="utf-8") as f:
            f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"モデル: gpt-image-1.5\n")
            f.write(f"画像ファイル: {image_filename}\n")
            f.write(f"サイズ: {size}\n")
            f.write(f"画質: {quality}\n")
            if pattern_number:
                f.write(f"パターン番号: {pattern_number}\n")
            f.write(f"\nプロンプト:\n{prompt}\n")

        print(f"画像情報を保存しました: {info_filepath}")

        return image_filepath, prompt

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="かっぱのキャラクター画像を生成するツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # パターン一覧を表示
  python generate_kappa.py --list

  # すべてのパターンで一括生成
  python generate_kappa.py --all

  # パターン番号3を使って生成
  python generate_kappa.py --pattern 3

  # カスタムプロンプトで生成
  python generate_kappa.py --custom "かわいいかっぱが泳いでいる"

  # 高画質で一括生成
  python generate_kappa.py --all --quality hd

  # カスタムサイズで生成
  python generate_kappa.py --pattern 1 --size 1024x1792
        """
    )

    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="利用可能なパターン一覧を表示"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="すべてのパターンで画像を一括生成"
    )
    parser.add_argument(
        "--pattern", "-p",
        type=int,
        help="使用するパターン番号（1から始まる）"
    )
    parser.add_argument(
        "--custom", "-c",
        type=str,
        help="カスタムプロンプト（ベースプロンプトと結合される）"
    )
    parser.add_argument(
        "--size", "-s",
        type=str,
        default="1024x1024",
        choices=["1024x1024", "1024x1792", "1792x1024"],
        help="画像サイズ（デフォルト: 1024x1024）"
    )
    parser.add_argument(
        "--quality", "-q",
        type=str,
        default="standard",
        choices=["standard", "hd"],
        help="画質（デフォルト: standard）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("かっぱキャラクター画像生成スクリプト (GPT Image 1.5)")
    print("=" * 60)

    # ベースプロンプトを読み込む
    base_prompt = load_base_prompt()

    # パターンを読み込む
    patterns = load_patterns()

    # パターン一覧表示
    if args.list:
        list_patterns(patterns)
        return

    # すべてのパターンで一括生成
    if args.all:
        print(f"\n全{len(patterns)}パターンの画像を一括生成します...")
        print(f"サイズ: {args.size}, 画質: {args.quality}")
        print("=" * 60)

        success_count = 0
        failed_patterns = []

        for i, pattern in enumerate(patterns, 1):
            print(f"\n[{i}/{len(patterns)}] パターン#{i}: {pattern[:60]}...")
            prompt = f"{base_prompt}\n{pattern}"

            try:
                generate_kappa_image(
                    prompt=prompt,
                    size=args.size,
                    quality=args.quality,
                    pattern_number=i
                )
                success_count += 1
            except Exception as e:
                print(f"⚠️  パターン#{i}の生成に失敗しました: {e}")
                failed_patterns.append((i, pattern[:30]))

        # 結果サマリー
        print("\n" + "=" * 60)
        print(f"一括生成完了!")
        print(f"成功: {success_count}/{len(patterns)}")
        if failed_patterns:
            print(f"失敗: {len(failed_patterns)}/{len(patterns)}")
            print("\n失敗したパターン:")
            for num, desc in failed_patterns:
                print(f"  - パターン#{num}: {desc}...")
        print("=" * 60)
        return

    # プロンプトを構築
    pattern_number = None
    if args.pattern:
        # パターン番号チェック
        if args.pattern < 1 or args.pattern > len(patterns):
            print(f"エラー: パターン番号は 1 から {len(patterns)} の範囲で指定してください")
            sys.exit(1)

        selected_pattern = patterns[args.pattern - 1]
        prompt = f"{base_prompt}\n{selected_pattern}"
        pattern_number = args.pattern
        print(f"\n使用パターン: #{args.pattern}")
        print(f"  {selected_pattern}")
    elif args.custom:
        # カスタムプロンプト
        prompt = f"{base_prompt}\n{args.custom}"
        print(f"\nカスタムプロンプト: {args.custom}")
    else:
        # デフォルト（パターン1を使用）
        prompt = f"{base_prompt}\n{patterns[0]}"
        pattern_number = 1
        print(f"\nデフォルトパターン（#1）を使用")
        print(f"  {patterns[0]}")

    # 画像生成
    generate_kappa_image(
        prompt=prompt,
        size=args.size,
        quality=args.quality,
        pattern_number=pattern_number
    )


if __name__ == "__main__":
    main()
