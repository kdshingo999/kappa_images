#!/usr/bin/env python3
"""
かっぱキャラクター画像生成 Streamlit Webアプリ
Responses API + 画像入力対応版
"""

import os
import base64
import streamlit as st
from datetime import datetime
from pathlib import Path
from openai import OpenAI


def load_base_prompt(base_prompt_file: str = "prompts/base_prompt.txt") -> str:
    """ベースプロンプトをファイルから読み込む"""
    try:
        with open(base_prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def load_patterns(patterns_file: str = "prompts/patterns.txt") -> list:
    """
    パターンファイルから有効なパターンを読み込む
    空白行で区切られた複数行のパターンに対応
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
        return []


def image_to_data_uri(image_bytes: bytes) -> str:
    """画像バイトをdata URIに変換"""
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/png;base64,{b64}"


def generate_image_with_responses_api(
    prompt: str,
    base_images: list = None,
    api_key: str = None
) -> tuple:
    """
    Responses APIを使って画像生成（ベース画像対応）

    Args:
        prompt: プロンプトテキスト
        base_images: ベース画像のdata URIリスト（任意）
        api_key: OpenAI APIキー

    Returns:
        tuple: (image_bytes, error_message)
    """
    if not api_key:
        return None, "エラー: OPENAI_API_KEY環境変数が設定されていません"

    try:
        client = OpenAI(api_key=api_key)

        # contentを構築
        content = [{"type": "input_text", "text": prompt}]

        # ベース画像があれば追加（最大5枚）
        if base_images:
            for img_uri in base_images[:5]:
                content.append({
                    "type": "input_image",
                    "image_url": img_uri
                })

        # Responses APIで画像生成（gpt-4.1を使用）
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            tools=[{
                "type": "image_generation",
                "input_fidelity": "high" if base_images else "low"
            }]
        )

        # 生成画像を取得
        for output in response.output:
            if output.type == "image_generation_call":
                image_bytes = base64.b64decode(output.result)
                return image_bytes, None

        return None, "画像が生成されませんでした"

    except Exception as e:
        return None, f"エラーが発生しました: {e}"


def save_image_to_file(image_bytes: bytes, prompt: str, pattern_number: int = None):
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
        f.write(f"モデル: gpt-4.1 (Responses API with image_generation tool)\n")
        f.write(f"画像ファイル: {image_filename}\n")
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

    st.title("🥒 かっぱキャラクター画像生成ツール（改良版）")
    st.markdown("✨ ベース画像をアップロード可能。プロンプトに画像サイズ・画質を記述。")

    # サイドバー設定
    st.sidebar.header("⚙️ 設定")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 ヒント")
    st.sidebar.markdown("- ベース画像は任意でアップロード（最大5枚）")
    st.sidebar.markdown("- プロンプトに画像サイズや画質を記述")
    st.sidebar.markdown("- パターンは空白行で区切る（複数行OK）")
    st.sidebar.markdown("- 例: `画像サイズ: 1024x1024, 画質: HD`")

    # APIキーの確認
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY環境変数が設定されていません")
        st.stop()

    # ベース画像アップロード
    st.header("📤 ベース画像（任意）")
    uploaded_files = st.file_uploader(
        "ベース画像をアップロード（最大5枚、任意）",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="ベース画像を使うと、その画像を参考に新しい画像を生成します"
    )

    base_image_uris = []
    if uploaded_files:
        if len(uploaded_files) > 5:
            st.warning("⚠️ ベース画像は最大5枚までです。最初の5枚を使用します。")
            uploaded_files = uploaded_files[:5]

        st.markdown(f"**アップロード済み: {len(uploaded_files)}枚**")
        cols = st.columns(min(len(uploaded_files), 5))
        for i, file in enumerate(uploaded_files):
            image_bytes = file.read()
            base_image_uris.append(image_to_data_uri(image_bytes))
            with cols[i]:
                st.image(image_bytes, caption=f"画像{i+1}", use_container_width=True)

    # ベースプロンプトの読み込みと表示
    base_prompt = load_base_prompt()

    st.header("📝 プロンプト設定")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("共通プロンプト（ベース）")
        edited_base_prompt = st.text_area(
            "かっぱの基本的な特徴を記述",
            value=base_prompt,
            height=250,
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
                # パターンのプレビュー表示
                pattern_options = []
                for i, p in enumerate(patterns):
                    first_line = p.split('\n')[0]
                    preview = first_line[:40] + "..." if len(first_line) > 40 else first_line
                    pattern_options.append(f"{i+1}. {preview}")

                selected_index = st.selectbox(
                    "パターンを選択",
                    range(len(patterns)),
                    format_func=lambda x: pattern_options[x]
                )
                pattern_prompt = patterns[selected_index]
                pattern_number = selected_index + 1

                st.text_area(
                    "選択したパターン（複数行対応）",
                    value=pattern_prompt,
                    height=150,
                    disabled=True
                )
            else:
                st.warning("パターンファイルが見つかりません")
                pattern_prompt = ""
                pattern_number = None
        else:
            pattern_prompt = st.text_area(
                "カスタムプロンプト（複数行OK）",
                placeholder="例:\nかわいいかっぱが川で遊んでいる\n画像サイズ: 1024x1024\n画質: HD",
                height=150,
                help="ベースプロンプトに追加する独自の指示を入力します（複数行OK）"
            )
            pattern_number = None

    # 生成ボタン（2種類）
    st.markdown("---")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        single_generate = st.button("🎨 1枚生成", type="primary", use_container_width=True)

    with col_btn2:
        if patterns and pattern_mode == "パターンから選択":
            batch_generate = st.button(
                f"🎨🎨 全パターン生成（{len(patterns)}枚）",
                use_container_width=True,
                help="全てのパターンで画像を一括生成します"
            )
        else:
            batch_generate = False
            st.button(
                "🎨🎨 全パターン生成（パターン選択時のみ）",
                disabled=True,
                use_container_width=True
            )

    # 1枚生成
    if single_generate:
        if not edited_base_prompt.strip():
            st.error("共通プロンプトを入力してください")
            st.stop()

        if not pattern_prompt.strip():
            st.error("パターンを選択するか、カスタムプロンプトを入力してください")
            st.stop()

        # 最終プロンプトの構築
        final_prompt = f"{edited_base_prompt}\n\n{pattern_prompt}"

        # 生成中の表示
        with st.spinner("画像を生成中... ⏳"):
            image_bytes, error = generate_image_with_responses_api(
                prompt=final_prompt,
                base_images=base_image_uris if base_image_uris else None,
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
                st.markdown(f"**モデル:** gpt-4.1 (Responses API)")
                if base_image_uris:
                    st.markdown(f"**ベース画像:** {len(base_image_uris)}枚（高精度モード）")
                else:
                    st.markdown(f"**ベース画像:** なし")
                if pattern_number:
                    st.markdown(f"**パターン番号:** {pattern_number}")
                st.markdown(f"**プロンプト:**")
                st.code(final_prompt, language="text")

    # 全パターン一括生成
    if batch_generate:
        if not edited_base_prompt.strip():
            st.error("共通プロンプトを入力してください")
            st.stop()

        st.markdown("---")
        st.header(f"🎨🎨 全パターン一括生成（{len(patterns)}枚）")

        progress_bar = st.progress(0)
        status_text = st.empty()

        success_count = 0
        failed_patterns = []

        results_container = st.container()

        for i, pattern in enumerate(patterns):
            progress = (i + 1) / len(patterns)
            progress_bar.progress(progress)
            status_text.text(f"生成中... [{i+1}/{len(patterns)}] パターン#{i+1}")

            final_prompt = f"{edited_base_prompt}\n\n{pattern}"

            image_bytes, error = generate_image_with_responses_api(
                prompt=final_prompt,
                base_images=base_image_uris if base_image_uris else None,
                api_key=api_key
            )

            if error:
                first_line = pattern.split('\n')[0]
                failed_patterns.append((i+1, first_line[:30]))
            else:
                success_count += 1
                saved_path = save_image_to_file(
                    image_bytes=image_bytes,
                    prompt=final_prompt,
                    pattern_number=i+1
                )

                with results_container:
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        st.image(image_bytes, caption=f"パターン#{i+1}", use_container_width=True)
                    with col_info:
                        st.markdown(f"**パターン #{i+1}**")
                        preview_text = pattern[:100] + "..." if len(pattern) > 100 else pattern
                        st.code(preview_text, language="text")
                        st.markdown(f"✅ 保存: `{saved_path.name}`")

        # 結果サマリー
        progress_bar.progress(1.0)
        status_text.text("完了!")

        st.markdown("---")
        st.success(f"✅ 一括生成完了! 成功: {success_count}/{len(patterns)}")

        if failed_patterns:
            with st.expander("❌ 失敗したパターン"):
                for num, desc in failed_patterns:
                    st.markdown(f"- パターン#{num}: {desc}...")

    # フッター
    st.markdown("---")
    st.markdown("Made with ❤️ using OpenAI GPT-4.1 (Responses API) and Streamlit")


if __name__ == "__main__":
    main()
