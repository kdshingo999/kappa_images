#!/bin/bash

echo "========================================="
echo "かっぱキャラクター画像生成 Web版"
echo "========================================="
echo ""

echo "🛑 Dockerコンテナを停止中..."
docker compose down

if [ $? -eq 0 ]; then
    echo "✓ コンテナを停止しました"
    echo ""
    echo "再度起動する場合は以下を実行:"
    echo "  ./start.sh"
else
    echo "❌ コンテナの停止に失敗しました"
    exit 1
fi

echo "========================================="
