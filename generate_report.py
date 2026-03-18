#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成每日出版印刷行业动态日报
"""

import json
import os
from datetime import datetime
import re

def clean_html(text):
    """清理HTML标签"""
    if not text:
        return ""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 清理多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:200]  # 限制摘要长度

def extract_articles_by_category(raw_feeds_file, web_data_file):
    """按行业分类提取文章"""
    articles_by_category = {
        "出版": [],
        "印刷": []
    }
    
    # 读取RSS数据
    if os.path.exists(raw_feeds_file):
        with open(raw_feeds_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for article in data.get('articles', []):
            category = article.get('category', '')
            if category in articles_by_category:
                articles_by_category[category].append({
                    'title': article.get('title', ''),
                    'link': article.get('link', ''),
                    'published': article.get('published', ''),
                    'summary': clean_html(article.get('summary', '')),
                    'source': article.get('source', '')
                })
    
    # 读取网页数据（作为补充）
    if os.path.exists(web_data_file):
        with open(web_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for page in data.get('webpages', []):
            # 简单判断网页属于哪个行业
            url = page.get('url', '')
            title = page.get('title', '')
            if 'print' in url.lower() or 'printing' in url.lower():
                articles_by_category['印刷'].append({
                    'title': title,
                    'link': url,
                    'published': datetime.now().strftime('%Y-%m-%d'),
                    'summary': '印刷行业最新动态更新',
                    'source': 'Web Crawler'
                })
    
    return articles_by_category

def format_date(published_str):
    """格式化日期"""
    if not published_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    # 尝试解析各种日期格式
    try:
        from datetime import datetime as dt
        # 处理RSS常见的日期格式
        if 'GMT' in published_str or 'UTC' in published_str:
            published_str = published_str.replace('GMT', '').replace('UTC', '').strip()
        
        # 简单提取日期
        dt_obj = dt.strptime(published_str.split(' +')[0], '%a, %d %b %Y %H:%M:%S')
        return dt_obj.strftime('%Y-%m-%d')
    except:
        return published_str[:10] if len(published_str) >= 10 else published_str

def generate_markdown_report(articles_by_category, output_date):
    """生成Markdown日报"""
    
    # 提取重点摘要（取每行业前2条）
    key_points = []
    for category, articles in articles_by_category.items():
        for i, article in enumerate(articles[:2]):
            if article['title']:
                key_points.append(f"**{category}**: {article['title'][:50]}...")
    
    # 生成Markdown内容
    md_content = f"""# 出版印刷行业动态日报 - {output_date}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**资讯总数**: {sum(len(articles) for articles in articles_by_category.values())} 条
**分类数量**: {len(articles_by_category)} 个

## 今日重点摘要

"""
    
    # 添加重点摘要
    for i, point in enumerate(key_points[:3], 1):
        md_content += f"- 要点{i}：{point}\n"
    
    md_content += "\n---\n\n"
    
    # 按行业展示文章
    for category, articles in articles_by_category.items():
        if not articles:
            continue
            
        md_content += f"## {category}行业\n\n"
        
        # 每个行业最多5条
        for article in articles[:5]:
            md_content += f"""### [{article['source']}] {article['title']}
- **链接**: {article['link']}
- **摘要**: {article['summary']}
- **发布时间**: {format_date(article['published'])}

"""
    
    md_content += """---

**数据来源**: RSS订阅源、网页抓取
**生成工具**: Daily News Collector Skill
**备注**: 本报告由AI智能体自动生成
"""
    
    return md_content

def main():
    """主函数"""
    # 获取日期
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 输入文件
    raw_feeds_file = f"raw_feeds.json"
    web_data_file = f"web_data.json"
    
    # 输出文件
    output_dir = "daily-reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f"daily-news-report-{date_str}.md")
    
    # 提取文章
    articles_by_category = extract_articles_by_category(raw_feeds_file, web_data_file)
    
    # 生成报告
    markdown_content = generate_markdown_report(articles_by_category, date_str)
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"日报生成成功: {output_file}")
    print(f"共收录 {sum(len(articles) for articles in articles_by_category.values())} 条资讯")

if __name__ == "__main__":
    main()
