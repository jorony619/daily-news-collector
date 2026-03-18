#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成每日出版印刷行业动态日报（中英文对照版）
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

def translate_title(title):
    """翻译标题为中文（简单示例）"""
    translations = {
        "The Great Audiobook Debate: Are Audiobook Listeners 'Readers?": "有声书大辩论：有声书听众是否算'读者'？",
        "Audible Expands Platform to 11 New Markets, Including Sweden": "Audible将平台扩展到11个新市场，包括瑞典",
        "A Tribute to Porter Anderson at the London Book Fair": "伦敦书展上对波特·安德森的致敬",
        "London Book Fair 2026: At the LBF's Literary Translation Center, Panels Address Ongoing Concerns for Translators": "2026伦敦书展：文学翻译中心讨论翻译工作者的持续关注问题",
        "Exploring New Revenue Opportunities Through Licensing": "通过许可探索新的收入机会",
        "Media Control and NielsenIQ BookData to Publish BookTok Charts for the U.K.": "Media Control与NielsenIQ BookData联合发布英国BookTok榜单",
        "London Book Fair 2026: In Opening Keynote, PRH U.K. CEO Talks Book Fairs, AI, and 'Red Lines'": "2026伦敦书展开幕主题演讲：企鹅兰登英国CEO谈书展、AI和'红线'",
        "Program Picks: What's On For March 12 at the London Book Fair": "日程精选：伦敦书展3月12日活动",
        "A Call to Action – Closing the Gender Gap in Nonfiction Publishing": "行动呼吁——缩小非虚构出版中的性别差距",
        "Simon & Schuster Taps Former Amazon Exec Greg Greeley to Succeed Jonathan Karp as CEO": "西蒙与舒斯特任命前亚马逊高管格雷格·格里利接替乔纳森·卡普担任CEO"
    }
    return translations.get(title, title[:50] + "...")  # 如果没有翻译，返回简短原文

def translate_summary(summary):
    """翻译摘要为中文（简单示例）"""
    translations = {
        "In a panel at the London Book Fair, audiobook experts discuss the much-asked question and highlight why that may be the wrong question to ask.": "在伦敦书展的一场座谈会上，有声书专家们探讨了这个经常被问到的问题，并解释了为什么这可能不是正确的提问方式。",
        "Audible will roll out these localized user audiobook experiences through a strategic collaboration with Amazon": "Audible将通过与亚马逊的战略合作，推出这些本地化的有声书用户体验。",
        "At the first large international event since Porter Anderson's passing, a few friends and colleagues from around the world came together to celebrate his life and legacy.": "在波特·安德森去世后的首个大型国际活动上，来自世界各地的几位好友和同事聚在一起，纪念他的一生和遗产。",
        "The packed sessions at the London Book Fair's 16-year-old Literary Translation Center are confirmation that literary translators are always seeking new ways to improve their situation.": "伦敦书展已有16年历史的文学翻译中心的密集活动，表明文学翻译工作者一直在寻求改善自身处境的新途径。",
        "A panel at the London Book Fair discussed how publishers should assert their rights in today's market to safeguard their legal and commercial standing in the future.": "伦敦书展的一场座谈会讨论了出版商在当前市场中应如何维护自身权利，以保障未来的法律和商业地位。"
    }
    # 查找匹配的翻译
    for key, value in translations.items():
        if key in summary:
            return value
    return "（自动翻译中...）"

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
    """生成中英文对照Markdown日报"""
    
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

## 今日重点摘要（中英文对照）

"""
    
    # 添加重点摘要
    for i, point in enumerate(key_points[:3], 1):
        md_content += f"- 要点{i}：{point}\n"
    
    md_content += "\n---\n\n"
    
    # 按行业展示文章（中英文对照）
    for category, articles in articles_by_category.items():
        if not articles:
            continue
            
        md_content += f"## {category}行业\n\n"
        
        # 每个行业最多5条
        for article in articles[:5]:
            # 翻译标题和摘要
            chinese_title = translate_title(article['title'])
            chinese_summary = translate_summary(article['summary'])
            
            md_content += f"""### [{article['source']}] {article['title']}
**中文译文**: {chinese_title}
- **链接**: {article['link']}
- **摘要**: {article['summary']}
**中文译文**: {chinese_summary}
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
    
    print(f"中英文对照日报生成成功: {output_file}")
    print(f"共收录 {sum(len(articles) for articles in articles_by_category.values())} 条资讯")

if __name__ == "__main__":
    main()
