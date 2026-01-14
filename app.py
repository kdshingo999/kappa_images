#!/usr/bin/env python3
"""
かっぱキャラクター画像生成 Streamlit Webアプリ
"""

import os
import sys
import base64
import streamlit as st
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from io import BytesIO


def load_base_prompt(base_prompt_file: str = "prompts/base_prompt.txt") -> str:
    """ベースプロンプトをファイルから読み込む"""
    try:
        with open(base_prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def load_patterns(patterns_file: str = "prompts/patterns.txt") -> list:
    """パターンファイルから有効なパターンを読み込む"""
    try:
        with open(patterns_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        patterns = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)

        return patterns
    except FileNotFoundError:
        return []


def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    api_key: str = None
) -> tuple:
    """
    かっぱのキャラクター画像を生成する

    Returns:
        tuple: (image_bytes, error_message)
    """
    if not api_key:
        return None, "エラー: OPENAI_API_KEY環境変数が設定されていません"

    try:
        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        return image_bytes, None

    except Exception as e:
        return None, f"エラーが発生しました: {e}"


def save_image_to_file(image_bytes: bytes, prompt: str, size: str, quality: str, pattern_number: int = None):
    """生成された画像をファイルに保存"""
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pattern_suffix = f"_p{pattern_number}" if pattern_number else ""
    image_filename = f"kappa_{timestamp}{pattern_suffix}.png"
    image_filepath = output_dir / image_filename

    with open(image_filepath, "wb") as f:
        f.write(image_bytes)

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

    return image_filepath


def main():
    """メイン関数"""
    st.set_page_config(
        page_title="かっぱキャラクター画像生成",
        page_icon="🥒",
        layout="wide"
    )

    st.title("🥒 かっぱキャラクター画像生成ツール")
    st.markdown("OpenAI GPT Image 1.5を使用して、かっぱのキャラクター画像を生成します")

    # サイドバー設定
    st.sidebar.header("⚙️ 設定")

    size = st.sidebar.selectbox(
        "画像サイズ",
        ["1024x1024", "1024x1792", "1792x1024"],
        index=0
    )

    quality = st.sidebar.selectbox(
        "画質",
        ["standard", "hd"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 ヒント")
    st.sidebar.markdown("- 共通プロンプトはかっぱの基本特徴を記述")
    st.sidebar.markdown("- パターンでスタイルやポーズを指定")
    st.sidebar.markdown("- カスタムプロンプトで独自の指示も可能")

    # APIキーの確認
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY環境変数が設定されていません")
        st.stop()

    # ベースプロンプトの読み込みと表示
    base_prompt = load_base_prompt()

    st.header("📝 プロンプト設定")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("共通プロンプト（ベース）")
        edited_base_prompt = st.text_area(
            "かっぱの基本的な特徴を記述",
            value=base_prompt,
            height=200,
            help="すべての生成に共通する、かっぱの基本的な特徴を記述します"
        )

    with col2:
        st.subheader("パターン選択")

        # パターンの読み込み
        patterns = load_patterns()

        pattern_mode = st.radio(
            "入力方法",
            ["パターンから選択", "カスタム入力"],
            horizontal=True
        )

        if pattern_mode == "パターンから選択":
            if patterns:
                pattern_options = [f"{i+1}. {p[:60]}..." if len(p) > 60 else f"{i+1}. {p}"
                                 for i, p in enumerate(patterns)]
                selected_index = st.selectbox(
                    "パターンを選択",
                    range(len(patterns)),
                    format_func=lambda x: pattern_options[x]
                )
                pattern_prompt = patterns[selected_index]
                pattern_number = selected_index + 1

                st.text_area(
                    "選択したパターン",
                    value=pattern_prompt,
                    height=100,
                    disabled=True
                )
            else:
                st.warning("パターンファイルが見つかりません")
                pattern_prompt = ""
                pattern_number = None
        else:
            pattern_prompt = st.text_area(
                "カスタムプロンプト",
                placeholder="例: かわいいかっぱが川で遊んでいる",
                height=100,
                help="ベースプロンプトに追加する独自の指示を入力します"
            )
            pattern_number = None

    # 生成ボタン
    st.markdown("---")

    if st.button("🎨 画像を生成", type="primary", use_container_width=True):
        if not edited_base_prompt.strip():
            st.error("共通プロンプトを入力してください")
            st.stop()

        if not pattern_prompt.strip():
            st.error("パターンを選択するか、カスタムプロンプトを入力してください")
            st.stop()

        # 最終プロンプトの構築
        final_prompt = f"{edited_base_prompt}\n{pattern_prompt}"

        # 生成中の表示
        with st.spinner("画像を生成中... ⏳"):
            image_bytes, error = generate_image(
                prompt=final_prompt,
                size=size,
                quality=quality,
                api_key=api_key
            )

        if error:
            st.error(error)
        else:
            st.success("✅ 画像生成成功!")

            # 画像の表示
            st.image(image_bytes, caption="生成されたかっぱのキャラクター", use_container_width=True)

            # ファイルに保存
            saved_path = save_image_to_file(
                image_bytes=image_bytes,
                prompt=final_prompt,
                size=size,
                quality=quality,
                pattern_number=pattern_number
            )

            st.info(f"💾 画像を保存しました: {saved_path}")

            # ダウンロードボタン
            st.download_button(
                label="📥 画像をダウンロード",
                data=image_bytes,
                file_name=f"kappa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

            # 生成情報の表示
            with st.expander("📋 生成情報"):
                st.markdown(f"**モデル:** gpt-image-1.5")
                st.markdown(f"**サイズ:** {size}")
                st.markdown(f"**画質:** {quality}")
                if pattern_number:
                    st.markdown(f"**パターン番号:** {pattern_number}")
                st.markdown(f"**プロンプト:**")
                st.code(final_prompt, language="text")

    # フッター
    st.markdown("---")
    st.markdown("Made with ❤️ using OpenAI GPT Image 1.5 and Streamlit")


if __name__ == "__main__":
    main()
