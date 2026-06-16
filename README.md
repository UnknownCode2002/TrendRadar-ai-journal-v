<div align="center" id="trendradar">

<a href="https://github.com/UnknownCode2002/TrendRadar-ai-journal-v" title="TrendRadar AI Journal">
  <img src="/_image/banner.webp" alt="TrendRadar Banner" width="80%">
</a>

最快<strong>30秒</strong>部署的 AI 趋势热点助手 —— 纸质报刊风格，专注 AI 垂直赛道

[![GitHub Stars](https://img.shields.io/github/stars/UnknownCode2002/TrendRadar-ai-journal-v?style=flat-square&logo=github&color=yellow)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/UnknownCode2002/TrendRadar-ai-journal-v?style=flat-square&logo=github&color=blue)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v/network/members)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-v6.9.1-blue.svg)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)
[![MCP](https://img.shields.io/badge/MCP-v4.0.4-green.svg)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)
[![RSS](https://img.shields.io/badge/RSS-订阅源支持-orange.svg?style=flat-square&logo=rss&logoColor=white)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)
[![AI翻译](https://img.shields.io/badge/AI-多语言推送-purple.svg?style=flat-square)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)

[![企业微信通知](https://img.shields.io/badge/企业微信-通知-00D4AA?style=flat-square)](https://work.weixin.qq.com/)
[![个人微信通知](https://img.shields.io/badge/个人微信-通知-00D4AA?style=flat-square)](https://weixin.qq.com/)
[![Telegram通知](https://img.shields.io/badge/Telegram-通知-00D4AA?style=flat-square)](https://telegram.org/)
[![dingtalk通知](https://img.shields.io/badge/钉钉-通知-00D4AA?style=flat-square)](#)
[![飞书通知](https://img.shields.io/badge/飞书-通知-00D4AA?style=flat-square)](https://www.feishu.cn/)
[![邮件通知](https://img.shields.io/badge/Email-通知-00D4AA?style=flat-square)](#)
[![ntfy通知](https://img.shields.io/badge/ntfy-通知-00D4AA?style=flat-square)](https://github.com/binwiederhier/ntfy)
[![Bark通知](https://img.shields.io/badge/Bark-通知-00D4AA?style=flat-square)](https://github.com/Finb/Bark)
[![Slack通知](https://img.shields.io/badge/Slack-通知-00D4AA?style=flat-square)](https://slack.com/)
[![通用Webhook](https://img.shields.io/badge/通用-Webhook-607D8B?style=flat-square&logo=webhook&logoColor=white)](#)


[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-自动化-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)
[![Docker](https://img.shields.io/badge/Docker-部署-2496ED?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/wantcat/trendradar)
[![MCP Support](https://img.shields.io/badge/MCP-AI分析支持-FF6B6B?style=flat-square&logo=ai&logoColor=white)](https://modelcontextprotocol.io/)
[![AI分析推送](https://img.shields.io/badge/AI-分析推送-FF6B6B?style=flat-square&logo=openai&logoColor=white)](#)
[![AI智能筛选](https://img.shields.io/badge/AI-智能筛选新闻-9B59B6?style=flat-square&logo=openai&logoColor=white)](#)

</div>

<div align="center">

**中文** | **[English](README-EN.md)**

</div>

> 本项目基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) 深度定制，聚焦 **AI 垂直赛道趋势追踪**，以 **纸质报刊风格** 呈现日报。

<br>

---

## 🎯 核心功能

### 📰 **报刊风格日报**（本 fork 特色）

告别枯燥的列表式推送，以 **纸质报刊风格** 呈现每日 AI 趋势报告：

- **报头设计**：日期、期号、数据来源、版本号一应俱全
- **AI 趋势专栏**：独立板块展示 AI 行业重大动态
- **GitHub Trending**：独立区块展示当日 AI 相关热门开源项目
- **版面式布局**：头条加粗突出，次条清晰分层
- **暗色模式**：一键切换深色主题，自动记住偏好
- **快捷键系统**：`W` 宽屏、`D` 暗色、`/` 搜索、`?` 查看所有快捷键
- **一键复制**：悬停新闻序号即可复制标题和链接

### **全网热点聚合**

默认监控 19 个平台（知乎、抖音、B站、华尔街见闻、贴吧、百度、财联社、澎湃、凤凰网、今日头条、微博、GitHub Trending、Hacker News、掘金、36氪、IT之家、V2EX、少数派、Product Hunt、雪球），也可自行增减。

### **RSS 订阅源支持**

支持 RSS/Atom 订阅源抓取，按关键词分组统计，与热榜统一格式推送。

### **智能推送策略**

| 模式 | 适用场景 | 推送特点 |
|------|---------|---------|
| **当日汇总** (daily) | 企业管理者/普通用户 | 按时推送当日所有匹配新闻 |
| **当前榜单** (current) | 自媒体人/内容创作者 | 按时推送当前榜单匹配新闻 |
| **增量监控** (incremental) | 投资者/交易员 | 仅推送新增内容，零重复 |

### **AI 智能筛选**（v6.5.0）

用自然语言描述兴趣，AI 自动分类新闻并打分，替代传统关键词匹配。

### **AI 分析推送**（v5.0.0）

AI 大模型对推送内容深度分析，自动生成热点洞察报告。

### **AI 多语言翻译**（v5.2.0）

将推送内容翻译为任意语言，支持 English、Japanese、Korean 等。

### **多渠道推送**

企业微信、飞书、钉钉、Telegram、邮件、ntfy、Bark、Slack、通用 Webhook。

### **灵活存储架构**

本地 SQLite / 远程云存储（S3 兼容），自动切换。

### **多端部署**

GitHub Actions / Docker / 本地直接运行。

<br>

---

## 🚀 快速开始

### 1️⃣ 克隆并配置

```bash
git clone https://github.com/UnknownCode2002/TrendRadar-ai-journal-v.git
cd TrendRadar-ai-journal-v
```

### 2️⃣ 配置敏感信息

```bash
# 复制配置模板并填入真实信息
copy config\config.yaml.example config\config.yaml
# 编辑 config.yaml，填入 API Key、邮箱密码等
```

> ⚠️ `config/config.yaml` 含敏感信息，已在 `.gitignore` 中排除，不会被 git 追踪。

### 3️⃣ 配置通知渠道

在 `config/config.yaml` 中配置需要的推送渠道（邮件、飞书、钉钉等）。

### 4️⃣ 配置关注内容

编辑 `config/frequency_words.txt` 设置关心的关键词。

### 5️⃣ 运行

```bash
# Windows
run.bat
```

### 6️⃣ Docker 部署

```bash
docker compose pull
docker compose up -d
```

<br>

---

## 📝 更新日志

### 2026/06/16 - v6.9.1（本 fork 深度定制版）

**📰 报刊风格日报系统**
- 新增 `html_newspaper.py` — 纸质报刊风格的 HTML 报告模板
- 报头设计：日期、期号、数据来源、版本号完整展示
- AI 趋势专栏：独立板块展示 AI 行业重大动态
- GitHub Trending 独立区块：展示当日 AI 相关热门开源项目

**🔧 核心修复与优化**
- 修复 GBK 编码问题，确保中文环境兼容性
- 修复 RSS 解包错误
- 清理所有 git 冲突标记
- 到岗速览时间调整为 08:35-09:35

**🤖 AI 垂直赛道聚焦**
- AI 兴趣方向聚焦：大模型、AI 应用、AI 基础设施
- 自定义 AI 分析/翻译提示词
- 关键词配置优化：聚焦 AI 行业动态

**📦 部署增强**
- 新增 `run.bat`、`run_hidden.bat`、`run_hidden.vbs` 运行脚本
- 新增 `config/config.yaml.example` 配置模板
- 敏感信息通过 `git rm --cached` + `.gitignore` 双重保障

<details>
<summary>👉 点击展开：<strong>上游更新日志</strong></summary>

### 2026/05/23 - v6.8.0
HTML 报告增强、版本检查 CDN 多源回退、展示区域开关生效

### 2026/03/28 - v6.6.0
HTML 报告浏览器增强：宽屏、Tab 切换、暗色模式、快捷键

### 2026/03/12 - v6.5.0
AI 智能筛选系统、分时段筛选、AI 分析范围独立控制

### 2026/02/09 - v6.0.0
统一调度系统、5 种预设模板、可视化配置编辑器

### 2026/01/19 - v5.3.0
AI 模块迁移至 LiteLLM，支持 100+ AI 提供商

### 2026/01/17 - v5.2.0
AI 翻译功能、配置架构优化、AI 分析增强

### 2026/01/10 - v5.0.0
推送内容五大板块重构、AI 分析推送、独立展示区

### 2025/10/20 - v3.0.0
AI 分析功能上线，基于 MCP 协议的 17 种智能分析工具

</details>

<br>

---

## ☕ 支持项目

本项目基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) 深度定制。如果觉得有用：

- ⭐ 给 [原项目](https://github.com/sansan0/TrendRadar) 点 Star
- ⭐ 给 [本 fork](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v) 点 Star
- 🐛 发现 bug → 开 Issue

---

## 📄 许可证

GPL-3.0 License — 基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) 深度定制

---

<div align="center">

[🔝 回到顶部](#trendradar)

</div>
