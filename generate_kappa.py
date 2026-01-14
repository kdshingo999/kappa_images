#!/usr/bin/env python3
"""
かっぱのキャラクター画像を生成するスクリプト
OpenAI GPT Image 1.5を使用
"""

import os
import sys
import base64
from datetime import datetime
from pathlib import Path
from openai import OpenAI


def generate_kappa_image(prompt: str = None, size: str = "1024x1024", quality: str = "standard"):
    """
    かっぱのキャラクター画像を生成する

    Args:
        prompt: カスタムプロンプト（指定しない場合はデフォルトのかっぱプロンプトを使用）
        size: 画像サイズ ("1024x1024", "1024x1792", "1792x1024")
        quality: 画質 ("standard" or "hd")
    """
    # OpenAI APIキーの確認
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        sys.exit(1)

    # OpenAIクライアントの初期化
    client = OpenAI(api_key=api_key)

    # デフォルトのかっぱキャラクタープロンプト
    if prompt is None:
        prompt = """
        A cute and friendly kappa (Japanese water yokai) character design.
        The kappa has a distinctive water-filled dish on top of its head,
        a turtle-like shell on its back, webbed hands and feet, and a green scaly body.
        The character has big expressive eyes and a friendly smile.
        The style should be charming and suitable for a mascot or children's character.
        The background is simple and clean.
        """

    print(f"画像生成中...")
    print(f"プロンプト: {prompt.strip()}")
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
        image_filename = f"kappa_{timestamp}.png"
        image_filepath = output_dir / image_filename

        # 画像を保存
        with open(image_filepath, "wb") as f:
            f.write(image_bytes)

        print(f"画像を保存しました: {image_filepath}")

        # プロンプト情報をテキストファイルに保存
        info_filename = f"kappa_{timestamp}_info.txt"
        info_filepath = output_dir / info_filename

        with open(info_filepath, "w", encoding="utf-8") as f:
            f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"モデル: gpt-image-1.5\n")
            f.write(f"画像ファイル: {image_filename}\n")
            f.write(f"サイズ: {size}\n")
            f.write(f"画質: {quality}\n")
            f.write(f"\nプロンプト:\n{prompt}\n")

        print(f"画像情報を保存しました: {info_filepath}")

        return image_filepath, prompt

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)


def main():
    """メイン関数"""
    print("=" * 60)
    print("かっぱキャラクター画像生成スクリプト (GPT Image 1.5)")
    print("=" * 60)
    print()

    # カスタムプロンプトの例
    # custom_prompt = "かわいいかっぱのキャラクター。頭にお皿、甲羅を背負い、緑色の体。漫画風のイラスト"

    # デフォルトプロンプトで生成
    generate_kappa_image()

    # カスタムプロンプトで生成したい場合
    # generate_kappa_image(prompt=custom_prompt, size="1024x1024", quality="hd")


if __name__ == "__main__":
    main()
