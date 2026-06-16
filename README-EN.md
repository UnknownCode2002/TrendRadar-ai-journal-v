<div align="center" id="trendradar">

<a href="https://github.com/UnknownCode2002/TrendRadar-ai-journal-v" title="TrendRadar AI Journal">
  <img src="/_image/banner.webp" alt="TrendRadar Banner" width="80%">
</a>

Deploy in <strong>30 seconds</strong> — AI trend tracker with newspaper-style daily reports

[![GitHub Stars](https://img.shields.io/github/stars/UnknownCode2002/TrendRadar-ai-journal-v?style=flat-square&logo=github&color=yellow)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/UnknownCode2002/TrendRadar-ai-journal-v?style=flat-square&logo=github&color=blue)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v/network/members)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-v6.9.1-blue.svg)](https://github.com/UnknownCode2002/TrendRadar-ai-journal-v)

</div>

<div align="center">

**[中文](README.md)** | **English**

</div>

> This is a deep-customized fork of [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar), focused on **AI vertical trend tracking** with **newspaper-style daily reports**.

<br>

---

## 🎯 Core Features

### 📰 **Newspaper-Style Report** (Fork Feature)

- **Masthead**: Date, issue number, data sources, version
- **AI Trends Column**: Dedicated section for AI industry news
- **GitHub Trending**: Standalone block for trending AI open-source projects
- **Dark Mode**: One-click toggle, auto-saves preference
- **Keyboard Shortcuts**: `W` wide mode, `D` dark mode, `/` search, `?` help
- **One-Click Copy**: Hover news number to copy title + link

### **Multi-Platform Aggregation**

Monitors 19 platforms by default: Zhihu, Douyin, Bilibili, WallStreetCN, Tieba, Baidu, CLS, ThePaper, Ifeng, Toutiao, Weibo, GitHub Trending, Hacker News, Juejin, 36Kr, ITHome, V2EX, SSPai, Product Hunt, Xueqiu.

### **RSS Support**

RSS/Atom feed fetching with keyword grouping, unified format with hotlist.

### **Smart Push Strategy**

| Mode | Use Case | Behavior |
|------|----------|----------|
| **daily** | Managers / General users | Push all matched news on schedule |
| **current** | Content creators | Push current trending list |
| **incremental** | Investors / Traders | Push new items only, zero duplicates |

### **AI Smart Filtering** (v6.5.0)

Describe interests in natural language, AI auto-classifies and scores news.

### **AI Analysis Push** (v5.0.0)

AI generates deep insight reports for each push.

### **AI Translation** (v5.2.0)

Translate content to any language (English, Japanese, Korean, etc.).

### **Multi-Channel Push**

WeWork, Feishu, DingTalk, Telegram, Email, ntfy, Bark, Slack, Generic Webhook.

### **Flexible Storage**

Local SQLite / Remote S3-compatible cloud storage, auto-switch.

### **Multi-Platform Deployment**

GitHub Actions / Docker / Local.

<br>

---

## 🚀 Quick Start

### 1️⃣ Clone & Configure

```bash
git clone https://github.com/UnknownCode2002/TrendRadar-ai-journal-v.git
cd TrendRadar-ai-journal-v
```

### 2️⃣ Configure Secrets

```bash
copy config\config.yaml.example config\config.yaml
# Edit config.yaml with your API Key, email credentials, etc.
```

> ⚠️ `config/config.yaml` contains secrets and is excluded by `.gitignore`.

### 3️⃣ Configure Notification Channels

Edit `config/config.yaml` to set up your push channels (Email, Feishu, DingTalk, etc.).

### 4️⃣ Set Keywords

Edit `config/frequency_words.txt` with topics you care about.

### 5️⃣ Run

```bash
# Windows
run.bat
```

### 6️⃣ Docker

```bash
docker compose pull
docker compose up -d
```

<br>

---

## 📝 Changelog

### 2026/06/16 - v6.9.1 (Fork Customized)

**📰 Newspaper-Style Report**
- Added `html_newspaper.py` — newspaper-style HTML report template
- Masthead with date, issue number, data sources, version
- AI Trends Column for AI industry news
- GitHub Trending standalone block

**🔧 Fixes & Optimizations**
- Fixed GBK encoding for Chinese environment
- Fixed RSS unpacking errors
- Cleaned git conflict markers
- Adjusted morning briefing to 08:35-09:35

**🤖 AI Vertical Focus**
- AI interests focused on LLM, AI applications, AI infrastructure
- Custom AI analysis/translation prompts
- Keyword config optimized for AI industry

**📦 Deployment**
- Added `run.bat`, `run_hidden.bat`, `run_hidden.vbs`
- Added `config/config.yaml.example` template
- Secrets protected via `git rm --cached` + `.gitignore`

<details>
<summary>👉 Click to expand: <strong>Upstream Changelog</strong></summary>

### 2026/05/23 - v6.8.0
HTML report enhancements, CDN multi-source fallback

### 2026/03/28 - v6.6.0
Browser enhancements: wide mode, tabs, dark mode, shortcuts

### 2026/03/12 - v6.5.0
AI smart filtering, per-period filtering, independent AI analysis scope

### 2026/02/09 - v6.0.0
Unified scheduling, 5 presets, visual config editor

### 2026/01/19 - v5.3.0
AI module migrated to LiteLLM, 100+ AI providers

### 2026/01/10 - v5.0.0
5-section push restructure, AI analysis push, standalone display

### 2025/10/20 - v3.0.0
AI analysis feature launch, MCP protocol with 17 tools

</details>

<br>

---

## License

GPL-3.0 License — Deep fork of [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)

---

<div align="center">

[🔝 Back to Top](#trendradar)

</div>
