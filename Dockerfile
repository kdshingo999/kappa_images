# Python 3.11-slimをベースイメージに使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要な依存関係のインストール
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# Streamlitのポートを公開
EXPOSE 8501

# Streamlitの設定（ブラウザ自動起動を無効化、外部アクセスを許可）
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Streamlitアプリを起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
