# 每日出版印刷行业动态自动收集项目

## 项目介绍
这是一个零代码、零编程基础的自动化项目，每天自动收集出版和印刷行业的最新动态，并生成结构化日报。

## 已配置文件清单
✅ `sources.json` - RSS数据源配置
✅ `generate_report.py` - 日报生成脚本
✅ `run_collector.sh` - 一键收集脚本
✅ `daily-news-collector/` - 数据收集工具包

## 如何使用

### 本地测试（验证功能）
1. 打开终端/命令行
2. 进入项目目录
3. 运行：
   ```bash
   bash run_collector.sh
   ```
4. 查看 `daily-reports/` 目录生成的日报

### 部署到GitHub（实现每天自动运行）
[待补充详细步骤]

## 输出说明
- 日报文件位置：`daily-reports/daily-news-report-YYYY-MM-DD.md`
- 包含内容：出版行业5条 + 印刷行业5条最新动态
