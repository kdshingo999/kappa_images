#!/bin/bash

echo "========================================="
echo "かっぱキャラクター画像生成 Web版"
echo "========================================="
echo ""

# OPENAI_API_KEYの確認
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  エラー: OPENAI_API_KEY環境変数が設定されていません"
    echo "以下のコマンドで設定してください:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

echo "✓ OPENAI_API_KEY が設定されています"
echo ""

# Docker Composeでコンテナを起動
echo "🐳 Dockerコンテナを起動中..."
docker compose up -d --build

if [ $? -ne 0 ]; then
    echo "❌ コンテナの起動に失敗しました"
    exit 1
fi

echo "✓ コンテナ起動完了"
echo ""

# コンテナが完全に起動するまで待機
echo "⏳ Streamlitの起動を待機中..."
sleep 5

# 割り当てられたポート番号を取得
PORT=$(docker compose port app 8501 2>/dev/null | cut -d: -f2)

if [ -z "$PORT" ]; then
    echo "⚠️  ポート番号の取得に失敗しました"
    echo "コンテナのログを確認してください:"
    echo "  docker compose logs app"
    exit 1
fi

echo "✓ Streamlitが起動しました"
echo ""
echo "========================================="
echo "🎨 Webアプリが利用可能です"
echo "========================================="
echo "URL: http://localhost:${PORT}"
echo ""
echo "ブラウザを自動的に開きます..."
echo ""
echo "停止する場合は以下を実行:"
echo "  ./stop.sh"
echo "========================================="

# ブラウザを開く
sleep 1
open "http://localhost:${PORT}"
