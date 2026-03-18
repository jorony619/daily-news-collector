#!/bin/bash
# 每日新闻收集脚本

DATE=$(date +%Y-%m-%d)
echo "===== 开始收集 ${DATE} 的行业动态 ====="

# 创建输出目录
mkdir -p daily-reports

# 收集RSS数据
echo "步骤1: 收集RSS数据..."
python daily-news-collector/scripts/collect_feeds.py \
    --config sources.json \
    --output raw_feeds_${DATE}.json

# 收集网页数据
echo "步骤2: 抓取网页数据..."
python daily-news-collector/scripts/collect_webpages.py \
    --url https://whattheythink.com/news/ \
    --output web_data_${DATE}.json

# 复制为最新数据（供生成脚本使用）
cp raw_feeds_${DATE}.json raw_feeds.json
cp web_data_${DATE}.json web_data.json

# 生成日报
echo "步骤3: 生成日报..."
python generate_report.py

echo "===== 任务完成 ====="
