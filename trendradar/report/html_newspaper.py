# coding=utf-8
"""
报刊风格 HTML 报告渲染模块

提供报刊（纸质报纸）风格的热点新闻报告 HTML 生成功能。
专为邮件客户端兼容设计，同时支持 WEB 富交互展示。
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

from trendradar.report.helpers import html_escape, calculate_rank_trend
from trendradar.utils.time import convert_time_for_display


def render_html_content_newspaper(
    report_data: Dict,
    total_titles: int,
    mode: str = "daily",
    update_info: Optional[Dict] = None,
    *,
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[List[Dict]] = None,
    rss_new_items: Optional[List[Dict]] = None,
    display_mode: str = "keyword",
    standalone_data: Optional[Dict] = None,
    ai_analysis: Optional[Any] = None,
    show_new_section: bool = True,
) -> str:
    """生成报刊风格 HTML 报告

    Args:
        参数与 render_html_content 一致
    Returns:
        渲染后的 HTML 字符串
    """
    default_region_order = ["hotlist", "github_trending", "rss", "new_items", "standalone", "ai_analysis"]
    if region_order is None:
        region_order = default_region_order

    now = get_time_func() if get_time_func else datetime.now()

    # ── 计算统计摘要 ──
    stats = report_data.get("stats", [])
    total_matched = sum(s.get("count", 0) for s in stats)
    hot_news_count = total_titles
    new_count = report_data.get("total_new_count", 0)
    collect_count = report_data.get("collect_count", 0)
    if mode == "daily" and collect_count > 0:
        collect_html = f"""
        <div class="summary-item">
            <span class="summary-label">今日采集</span>
            <span class="summary-value">{collect_count}</span>
        </div>"""
    else:
        collect_html = ""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendRadar · 热点报刊</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* ── 纸张基础 ── */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Source Serif 4', 'Noto Sans SC', Georgia, 'Times New Roman', serif;
            background: #e8dccc;
            color: #1a1a1a;
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
            min-height: 100vh;
        }}

        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139,119,90,0.03) 2px, rgba(139,119,90,0.03) 4px),
                radial-gradient(ellipse at 20% 50%, rgba(210,180,140,0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(160,140,110,0.2) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }}

        .page-wrap {{ position: relative; z-index: 1; max-width: 800px; margin: 0 auto; padding: 32px 16px 64px; }}

        .newspaper {{
            background: #f7f2ea;
            border: 1px solid #c9b99a;
            box-shadow: 0 8px 40px rgba(60,40,20,0.12);
            position: relative;
        }}
        .newspaper::before {{
            content: '';
            position: absolute;
            inset: 8px;
            border: 1px solid #d4c5a8;
            pointer-events: none;
        }}
        .newspaper-inner {{ padding: 36px 40px 32px; position: relative; }}

        /* ── 报头 ── */
        .masthead {{ text-align: center; border-bottom: 3px double #1a1a1a; padding-bottom: 16px; margin-bottom: 24px; }}
        .masthead-ornament {{ font-size: 13px; color: #8b7a60; letter-spacing: 8px; margin-bottom: 4px; font-family: Georgia, serif; }}
        .masthead-title {{
            font-family: 'Playfair Display', 'Noto Sans SC', serif;
            font-size: clamp(36px, 7vw, 60px);
            font-weight: 900;
            letter-spacing: -0.02em;
            line-height: 1.05;
            color: #1a1a1a;
            text-transform: uppercase;
        }}
        .masthead-title .accent {{ color: #b22222; }}
        .masthead-sub {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: clamp(13px, 1.8vw, 16px); color: #6b5d4a; letter-spacing: 0.15em; margin-top: 2px; }}
        .masthead-date {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 6px 0 0; font-size: 11px; text-transform: uppercase;
            letter-spacing: 0.06em; color: #6b5d4a; border-top: 1px solid #d4c5a8; margin-top: 12px;
        }}
        .masthead-date .dot {{ display: inline-block; width: 4px; height: 4px; background: #b22222; border-radius: 50%; margin: 0 8px; vertical-align: middle; }}

        /* ── 摘要统计条 ── */
        .summary-bar {{
            display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;
            padding: 12px 20px; margin-bottom: 24px;
            background: rgba(210,190,160,0.15); border: 1px solid #d4c5a8;
            font-size: 12px;
        }}
        .summary-item {{ text-align: center; }}
        .summary-label {{ display: block; font-size: 9px; text-transform: uppercase; letter-spacing: 0.08em; color: #8b7a60; }}
        .summary-value {{ font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; color: #1a1a1a; }}

        /* ── 搜索栏 ── */
        .search-bar {{ margin-bottom: 20px; display: none; }}
        .search-input {{
            width: 100%; padding: 10px 16px; border: 1px solid #d4c5a8;
            font-size: 14px; font-family: inherit; background: rgba(247,242,234,0.6);
            outline: none; color: #1a1a1a;
        }}
        .search-input:focus {{ border-color: #b22222; }}
        .search-input::placeholder {{ color: #a89880; }}

        /* ── 区域标题 ── */
        .region-title {{
            font-family: 'Playfair Display', 'Noto Sans SC', serif;
            font-size: 18px; font-weight: 700; color: #1a1a1a;
            padding-bottom: 6px; border-bottom: 2px solid #1a1a1a;
            margin-bottom: 16px; margin-top: 28px;
        }}
        .region-title:first-child {{ margin-top: 0; }}

        /* ── 关键词区块 ── */
        .word-block {{ margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px dotted #ddd2be; }}

        /* ── GitHub Trending 区块 ── */
        .github-block {{ margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px dotted #ddd2be; }}
        .word-block:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}

        .word-header {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 12px; padding: 6px 10px; cursor: pointer;
            background: rgba(210,190,160,0.1); border-left: 3px solid #b22222;
        }}
        .word-name {{ font-family: 'Playfair Display', 'Noto Sans SC', serif; font-size: 16px; font-weight: 700; color: #1a1a1a; }}
        .word-count {{ font-size: 11px; color: #8b7a60; font-family: 'Source Serif 4', serif; }}
        .word-count.hot {{ color: #b22222; font-weight: 700; }}
        .word-count.warm {{ color: #b8860b; }}
        .collapse-icon {{ font-size: 10px; color: #8b7a60; margin-right: 6px; transition: transform 0.2s; user-select: none; }}
        .word-block.collapsed .news-item {{ display: none; }}
        .word-block.collapsed .collapse-icon {{ transform: rotate(-90deg); }}

        /* ── 新闻条目 ── */
        .news-item {{
            display: flex; gap: 12px; align-items: flex-start;
            padding: 10px 10px; border-bottom: 1px dotted #e8e0d0;
            transition: background 0.15s;
        }}
        .news-item:hover {{ background: rgba(210,190,160,0.08); }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item.new::after {{
            content: "NEW"; display: inline-block; margin-left: 6px;
            background: #b22222; color: #f7f2ea; font-size: 8px; font-weight: 700;
            padding: 2px 6px; letter-spacing: 0.08em; vertical-align: middle;
        }}

        .news-number {{
            font-family: 'Source Serif 4', serif; font-size: 11px; font-weight: 600;
            color: #8b7a60; min-width: 24px; text-align: center; flex-shrink: 0;
            padding-top: 2px; cursor: pointer; transition: color 0.15s;
        }}
        .news-item:hover .news-number {{ color: #b22222; }}

        .news-content {{ flex: 1; min-width: 0; }}
        .news-header {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 3px; }}

        .source-name {{ font-size: 9px; text-transform: uppercase; letter-spacing: 0.06em; color: #8b7a60; font-weight: 600; }}
        .keyword-tag {{ font-size: 9px; color: #b8860b; background: rgba(184,134,11,0.1); padding: 1px 6px; border: 1px solid rgba(184,134,11,0.2); }}

        .rank-num {{
            font-size: 9px; font-weight: 700; color: #f7f2ea;
            background: #8b7a60; padding: 2px 6px; border-radius: 2px;
            font-family: 'Source Serif 4', serif;
        }}
        .rank-num.top {{ background: #b22222; }}
        .rank-num.high {{ background: #b8860b; }}

        .trend-up, .trend-down {{ font-size: 10px; }}
        .time-info {{ font-size: 10px; color: #8b7a60; }}
        .count-info {{ font-size: 10px; color: #b8860b; font-weight: 600; }}
        .extra-info {{ font-size: 10px; color: #6b5d4a; font-weight: 500; letter-spacing: 0.02em; }}

        .news-title {{ font-size: 14px; line-height: 1.5; }}
        .news-desc {{ font-size: 12px; color: #6b5d4a; line-height: 1.5; margin-top: 2px; padding-left: 2px; border-left: 2px solid #d4c5a8; }}
        .news-link {{ color: #1a1a1a; text-decoration: none; font-weight: 500; }}
        .news-link:hover {{ color: #b22222; text-decoration: underline; }}

        /* ── 错误区 ── */
        .error-block {{
            padding: 12px 16px; background: rgba(178,34,34,0.06);
            border: 1px solid rgba(178,34,34,0.2); margin-bottom: 20px;
        }}
        .error-title {{ font-size: 12px; font-weight: 700; color: #b22222; margin-bottom: 6px; }}
        .error-list {{ list-style: none; }}
        .error-item {{ font-size: 12px; color: #8b1a1a; padding: 2px 0; }}

        /* ── RSS ── */
        .rss-feed-block {{ margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px dotted #ddd2be; }}
        .rss-feed-block:last-child {{ border-bottom: none; }}
        .feed-header {{ font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 700; color: #2d6a4f; padding-bottom: 4px; border-bottom: 1px solid #2d6a4f; margin-bottom: 10px; }}
        .rss-item {{ padding: 6px 0; border-bottom: 1px dotted #e8e0d0; }}
        .rss-item:last-child {{ border-bottom: none; }}
        .rss-meta {{ font-size: 10px; color: #8b7a60; margin-bottom: 2px; }}
        .rss-title {{ font-size: 13px; line-height: 1.5; }}
        .rss-link {{ color: #1a1a1a; text-decoration: none; font-weight: 500; }}
        .rss-link:hover {{ color: #2d6a4f; text-decoration: underline; }}

        /* ── 独立展示 ── */
        .standalone-block {{ margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px dotted #ddd2be; }}
        .standalone-name {{ font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 700; color: #1a1a1a; }}

        /* ── AI 分析 ── */
        .ai-region {{
            margin-top: 24px; padding: 20px; border: 1px solid #d4c5a8;
            background: rgba(210,190,160,0.1);
        }}
        .ai-section {{ margin-bottom: 0; }}
        .ai-section-header {{
            display: flex; align-items: center; gap: 8px;
            margin-bottom: 14px; padding-bottom: 8px;
            border-bottom: 1px solid #d4c5a8;
        }}
        .ai-section-title {{ font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 700; color: #1a1a1a; }}
        .ai-section-badge {{
            font-size: 9px; font-weight: 700; color: #f7f2ea;
            background: #b22222; padding: 2px 8px; letter-spacing: 0.06em;
        }}
        .ai-blocks-grid {{ display: flex; flex-direction: column; gap: 12px; }}
        .ai-block {{ padding: 12px 14px; background: rgba(247,242,234,0.6); border-left: 3px solid #b22222; }}
        .ai-block:last-child {{ margin-bottom: 0; }}
        .ai-block-title {{ font-size: 13px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }}
        .ai-block-content {{ font-size: 13px; line-height: 1.6; color: #3a3530; white-space: pre-wrap; }}
        .ai-info {{ padding: 12px; background: rgba(210,190,160,0.1); border: 1px solid #d4c5a8; color: #6b5d4a; font-size: 13px; }}
        .ai-error {{ padding: 12px; background: rgba(178,34,34,0.06); border: 1px solid rgba(178,34,34,0.15); color: #8b1a1a; font-size: 13px; }}
        .ai-warning {{ padding: 12px; background: #fffbeb; border: 1px solid #fde68a; color: #92400e; font-size: 13px; }}

        /* ── 新增热点 ── */
        .new-source-block {{ margin-bottom: 16px; }}
        .new-source-title {{ font-family: 'Playfair Display', serif; font-size: 13px; font-weight: 700; color: #1a1a1a; padding-bottom: 4px; border-bottom: 1px solid #d4c5a8; margin-bottom: 8px; }}
        .new-item {{
            display: flex; gap: 8px; align-items: flex-start;
            padding: 6px 0; border-bottom: 1px dotted #e8e0d0;
        }}
        .new-item:last-child {{ border-bottom: none; }}

        /* ── 页脚 ── */
        .footer {{ text-align: center; padding-top: 20px; border-top: 1px solid #d4c5a8; margin-top: 24px; }}
        .footer-ornament {{ font-size: 16px; color: #c9b99a; letter-spacing: 8px; margin-bottom: 8px; }}
        .footer-text {{ font-size: 11px; color: #8b7a60; line-height: 1.8; }}
        .footer-text a {{ color: #6b5d4a; text-decoration: underline; text-underline-offset: 2px; }}
        .footer-text a:hover {{ color: #b22222; }}

        /* ── 截图按钮 ── */
        .save-buttons {{
            display: flex; justify-content: center; gap: 8px; margin-bottom: 20px;
        }}
        .save-btn {{
            font-family: 'Source Serif 4', serif; font-size: 11px;
            padding: 6px 14px; background: #1a1a1a; color: #f7f2ea;
            border: none; cursor: pointer; letter-spacing: 0.04em;
            transition: background 0.15s;
        }}
        .save-btn:hover {{ background: #b22222; }}
        .save-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}

        /* ── 响应式 ── */
        @media (max-width: 600px) {{
            .newspaper-inner {{ padding: 24px 16px; }}
            .page-wrap {{ padding: 12px 8px; }}
            .summary-bar {{ gap: 12px; }}
            .masthead-date {{ flex-direction: column; gap: 4px; }}
        }}
        @media print {{
            body {{ background: white; }}
            .newspaper {{ box-shadow: none; border-color: #aaa; }}
            .page-wrap {{ padding: 0; }}
            .newspaper-inner {{ padding: 24px; }}
            .save-buttons {{ display: none; }}
        }}
    </style>
</head>
<body>
<div class="page-wrap">
<div class="newspaper">
<div class="newspaper-inner">

    <!-- ═══════ 报头 ═══════ -->
    <div class="masthead">
        <div class="masthead-ornament">✦ ✦ ✦</div>
        <div class="masthead-title">Trend<span class="accent">Radar</span></div>
        <div class="masthead-sub">— 每天 AI 热点 · 洞见先机 —</div>
        <div style="font-size:10px;color:#8b7a60;margin-top:4px;font-family:'Playfair Display',serif;font-style:italic;">Modified by UnknownCode &amp; XTang</div>
        <div class="masthead-date">
            <span>{now.strftime("%Y 年 %m 月 %d 日")}</span>
            <span><span class="dot"></span> 第 {now.strftime("%W")} 周 · {now.strftime("%A")} <span class="dot"></span></span>
            <span>{mode}</span>
        </div>
    </div>

    <!-- ═══════ 摘要统计条 ═══════ -->
    <div class="summary-bar">
        <div class="summary-item">
            <span class="summary-label">总监测</span>
            <span class="summary-value">{total_titles}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">关键词匹配</span>
            <span class="summary-value">{len(stats)}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">匹配条目</span>
            <span class="summary-value">{total_matched}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">新增热点</span>
            <span class="summary-value">{new_count}</span>
        </div>
        {collect_html}
    </div>

    <!-- ═══════ 搜索栏 ═══════ -->
    <div class="search-bar">
        <input type="text" class="search-input" placeholder="搜索新闻标题..." oninput="handleSearch(this.value)">
    </div>
"""

    # ════════════════════════════════════════════
    # 失败平台错误区
    # ════════════════════════════════════════════
    if report_data.get("failed_ids"):
        html += """            <div class="error-block">
            <div class="error-title">⚠️ 请求失败的平台</div>
            <ul class="error-list">"""
        for id_val in report_data["failed_ids"]:
            html += f'<li class="error-item">{html_escape(id_val)}</li>'
        html += """            </ul>
        </div>"""

    # ════════════════════════════════════════════
    # 构建区域内容
    # ════════════════════════════════════════════
    region_contents = {}

    # ─── 热榜区域 ───
    stats_html = ""
    if stats:
        stats_html += """            <div class="region-title">📰 热点新闻</div>"""
        for i, stat in enumerate(stats):
            count = stat["count"]
            if count >= 10:
                count_class = "hot"
            elif count >= 5:
                count_class = "warm"
            else:
                count_class = ""
            escaped_word = html_escape(stat["word"])

            stats_html += f"""
            <div class="word-block" data-tab-index="{i}">
                <div class="word-header" onclick="this.closest('.word-block').classList.toggle('collapsed')">
                    <span class="word-name"><span class="collapse-icon">▼</span>{escaped_word}</span>
                    <span class="word-count {count_class}">{count} 条</span>
                </div>"""

            for j, title_data in enumerate(stat.get("titles", []), 1):
                is_new = title_data.get("is_new", False)
                new_cls = " new" if is_new else ""

                stats_html += f"""
                <div class="news-item{new_cls}">
                    <div class="news-number">{j}</div>
                    <div class="news-content">
                        <div class="news-header">"""

                if display_mode == "keyword":
                    stats_html += f'<span class="source-name">{html_escape(title_data["source_name"])}</span>'
                else:
                    matched_keyword = title_data.get("matched_keyword", "")
                    if matched_keyword:
                        stats_html += f'<span class="keyword-tag">[{html_escape(matched_keyword)}]</span>'

                # 排名
                ranks = title_data.get("ranks", [])
                if ranks:
                    min_r = min(ranks)
                    max_r = max(ranks)
                    rank_th = title_data.get("rank_threshold", 10)
                    rcls = "top" if min_r <= 3 else ("high" if min_r <= rank_th else "")
                    rtxt = str(min_r) if min_r == max_r else f"{min_r}-{max_r}"
                    rank_timeline = title_data.get("rank_timeline", [])
                    trend = calculate_rank_trend(rank_timeline, ranks)
                    trend_h = ""
                    if trend == "up":
                        trend_h = '<span class="trend-up">📈</span>'
                    elif trend == "down":
                        trend_h = '<span class="trend-down">📉</span>'
                    stats_html += f'<span class="rank-num {rcls}">{rtxt}</span>{trend_h}'

                # 时间
                td = title_data.get("time_display", "")
                if td:
                    simplified = td.replace(" ~ ", "~").replace("[", "").replace("]", "")
                    stats_html += f'<span class="time-info">{html_escape(simplified)}</span>'

                # 次数
                ci = title_data.get("count", 1)
                if ci > 1:
                    stats_html += f'<span class="count-info">{ci}次</span>'

                # star/points/votes（来自 extra.info）
                extra_info = title_data.get("extra_info", "")
                if extra_info:
                    stats_html += f'<span class="extra-info">{html_escape(extra_info)}</span>'

                stats_html += """</div>"""

                # 标题
                et = html_escape(title_data["title"])
                lu = title_data.get("mobile_url") or title_data.get("url", "")
                if lu:
                    eu = html_escape(lu)
                    stats_html += f'<div class="news-title"><a href="{eu}" target="_blank" class="news-link">{et}</a></div>'
                else:
                    stats_html += f'<div class="news-title">{et}</div>'

                stats_html += """</div></div>"""

            stats_html += """</div>"""
    region_contents["hotlist"] = stats_html

    # ─── GitHub Trending 独立区块（不过 AI 筛选，展示今日 Top20）───
    github_items = report_data.get("github_trending", [])
    with open("_gh_debug3.log", "a", encoding="utf-8") as ghlog:
        ghlog.write(f"GH_SEC: len={len(github_items)}\n")
        ghlog.write(f"GH_SEC: region_order passed={'region_order' in dir()}\n")
        if github_items:
            ghlog.write(f"GH_SEC: branch ENTERED, building HTML\n")
    if github_items:
        gh_html = """            <div class="region-title">🐙 GitHub Trending</div>
            <div class="github-block">"""
        for i, item in enumerate(github_items, 1):
            title = item.get("title", "")
            url = item.get("url", "")
            stars = item.get("stars", "")
            desc = item.get("description", "")
            rank = item.get("rank", i)
            eu = html_escape(url)
            et = html_escape(title)
            ed = html_escape(desc) if desc else ""
            gh_html += f"""
                    <div class="news-item">
                        <div class="news-number">{i}</div>
                        <div class="news-content">
                            <div class="news-header">
                                <span class="source-name">GitHub</span>
                                <span class="rank-num top">{rank}</span>
                                <span class="extra-info">⭐ {html_escape(stars)}</span>
                            </div>
                            <div class="news-title"><a href="{eu}" target="_blank" class="news-link">{et}</a></div>"""
            if ed:
                gh_html += f"""                            <div class="news-desc">{ed}</div>"""
            gh_html += """                        </div>
                    </div>"""
        gh_html += """</div>"""
        region_contents["github_trending"] = gh_html
    else:
        region_contents["github_trending"] = ""

    # ─── RSS 区域 ───
    def render_rss_section(items: List[Dict], title: str) -> str:
        if not items:
            return ""
        total = sum(s.get("count", 0) for s in items)
        if total == 0:
            return ""
        rss_html = f"""            <div class="region-title">🔗 {title} <span style="font-weight:400;font-size:13px;color:#8b7a60;">（{total} 条）</span></div>"""
        for s in items:
            kw = s.get("word", "")
            titles = s.get("titles", [])
            if not titles:
                continue
            rss_html += f"""
            <div class="rss-feed-block">
                <div class="feed-header">{html_escape(kw)} <span style="font-weight:400;font-size:10px;color:#8b7a60;">{len(titles)} 条</span></div>"""
            for td in titles:
                item_title = td.get("title", "")
                url = td.get("url", "")
                time_disp = td.get("time_display", "")
                source_name = td.get("source_name", "")
                is_new = td.get("is_new", False)
                rss_html += """            <div class="rss-item"><div class="rss-meta">"""
                if time_disp:
                    rss_html += f'<span>{html_escape(time_disp)}</span>'
                if source_name:
                    rss_html += f'<span> · {html_escape(source_name)}</span>'
                if is_new:
                    rss_html += ' <span style="color:#b22222;font-weight:700;">NEW</span>'
                rss_html += "</div>"
                et = html_escape(item_title)
                if url:
                    eu = html_escape(url)
                    rss_html += f'<div class="rss-title"><a href="{eu}" target="_blank" class="rss-link">{et}</a></div>'
                else:
                    rss_html += f'<div class="rss-title">{et}</div>'
                rss_html += "</div>"
            rss_html += "</div>"
        return rss_html

    rss_stats_html = render_rss_section(rss_items, "RSS 订阅更新") if rss_items else ""
    rss_new_html = render_rss_section(rss_new_items, "RSS 新增更新") if rss_new_items else ""
    region_contents["rss"] = rss_stats_html

    # ─── 新增热点区域 ───
    new_titles_html = ""
    if show_new_section and report_data.get("new_titles"):
        total_new_count = report_data.get("total_new_count", 0)
        new_titles_html = f"""            <div class="region-title">🆕 本次新增热点（{total_new_count} 条）</div>"""
        for source_data in report_data["new_titles"]:
            esc_src = html_escape(source_data["source_name"])
            titles_cnt = len(source_data["titles"])
            new_titles_html += f"""
            <div class="new-source-block">
                <div class="new-source-title">{esc_src} · {titles_cnt}条</div>"""
            for idx, title_data in enumerate(source_data["titles"], 1):
                ranks = title_data.get("ranks", [])
                rcls = ""
                rtxt = "?"
                if ranks:
                    min_r = min(ranks)
                    rcls = "top" if min_r <= 3 else ("high" if min_r <= title_data.get("rank_threshold", 10) else "")
                    rtxt = str(min_r) if len(ranks) == 1 else f"{min_r}-{max(ranks)}"
                new_titles_html += f"""
                <div class="new-item">
                    <span class="news-number" style="min-width:20px;">{idx}</span>
                    <span class="rank-num {rcls}" style="margin-right:8px;">{rtxt}</span>
                    <div style="flex:1;">"""
                et = html_escape(title_data["title"])
                lu = title_data.get("mobile_url") or title_data.get("url", "")
                if lu:
                    eu = html_escape(lu)
                    new_titles_html += f'<a href="{eu}" target="_blank" style="color:#1a1a1a;text-decoration:none;font-size:13px;">{et}</a>'
                else:
                    new_titles_html += f'<span style="font-size:13px;">{et}</span>'
                new_titles_html += "</div></div>"
            new_titles_html += "</div>"
    region_contents["new_items"] = (new_titles_html, rss_new_html)

    # ─── 独立展示区 ───
    standalone_html = ""
    if standalone_data:
        platforms = standalone_data.get("platforms", [])
        rss_feeds = standalone_data.get("rss_feeds", [])
        if platforms or rss_feeds:
            standalone_html = """            <div class="region-title">📡 独立展示区</div>"""
            for p in platforms:
                pname = p.get("name", p.get("id", ""))
                items = p.get("items", [])
                if not items:
                    continue
                standalone_html += f"""
            <div class="standalone-block">
                <div class="standalone-name">{html_escape(pname)} <span style="font-weight:400;font-size:11px;color:#8b7a60;">{len(items)} 条</span></div>"""
                for j, item in enumerate(items, 1):
                    title = item.get("title", "")
                    url = item.get("url", "") or item.get("mobileUrl", "")
                    ranks = item.get("ranks", [])
                    rank = item.get("rank", 0)
                    ft = item.get("first_time", "")
                    lt = item.get("last_time", "")
                    cnt = item.get("count", 1)
                    standalone_html += f"""
                <div class="news-item">
                    <div class="news-number">{j}</div>
                    <div class="news-content">
                        <div class="news-header">"""
                    if ranks:
                        min_r = min(ranks)
                        max_r = max(ranks)
                        rcls = "top" if min_r <= 3 else ("high" if min_r <= 10 else "")
                        rtxt = str(min_r) if min_r == max_r else f"{min_r}-{max_r}"
                        standalone_html += f'<span class="rank-num {rcls}">{rtxt}</span>'
                    elif rank > 0:
                        rcls = "top" if rank <= 3 else ("high" if rank <= 10 else "")
                        standalone_html += f'<span class="rank-num {rcls}">{rank}</span>'
                    if ft and lt and ft != lt:
                        ft_d = convert_time_for_display(ft)
                        lt_d = convert_time_for_display(lt)
                        standalone_html += f'<span class="time-info">{html_escape(ft_d)}~{html_escape(lt_d)}</span>'
                    elif ft:
                        ft_d = convert_time_for_display(ft)
                        standalone_html += f'<span class="time-info">{html_escape(ft_d)}</span>'
                    if cnt > 1:
                        standalone_html += f'<span class="count-info">{cnt}次</span>'
                    extra_info = item.get("extra_info", "")
                    if extra_info:
                        standalone_html += f'<span class="extra-info">{html_escape(extra_info)}</span>'
                    standalone_html += """</div>"""
                    et = html_escape(title)
                    if url:
                        eu = html_escape(url)
                        standalone_html += f'<div class="news-title"><a href="{eu}" target="_blank" class="news-link">{et}</a></div>'
                    else:
                        standalone_html += f'<div class="news-title">{et}</div>'
                    standalone_html += """</div></div>"""
                standalone_html += "</div>"
            for f in rss_feeds:
                fname = f.get("name", f.get("id", ""))
                items = f.get("items", [])
                if not items:
                    continue
                standalone_html += f"""
            <div class="standalone-block">
                <div class="standalone-name">{html_escape(fname)} <span style="font-weight:400;font-size:11px;color:#8b7a60;">{len(items)} 条</span></div>"""
                for j, item in enumerate(items, 1):
                    title = item.get("title", "")
                    url = item.get("url", "")
                    published = item.get("published_at", "")
                    author = item.get("author", "")
                    standalone_html += f"""
                <div class="news-item">
                    <div class="news-number">{j}</div>
                    <div class="news-content">
                        <div class="news-header">"""
                    if published:
                        try:
                            from datetime import datetime as dt
                            tobj = dt.fromisoformat(published.replace("Z", "+00:00"))
                            td = tobj.strftime("%m-%d %H:%M")
                        except Exception:
                            td = published
                        standalone_html += f'<span class="time-info">{html_escape(td)}</span>'
                    if author:
                        standalone_html += f'<span class="source-name">{html_escape(author)}</span>'
                    standalone_html += """</div>"""
                    et = html_escape(title)
                    if url:
                        eu = html_escape(url)
                        standalone_html += f'<div class="news-title"><a href="{eu}" target="_blank" class="news-link">{et}</a></div>'
                    else:
                        standalone_html += f'<div class="news-title">{et}</div>'
                    standalone_html += """</div></div>"""
                standalone_html += "</div>"
    region_contents["standalone"] = standalone_html

    # ─── AI 分析 ───
    ai_html = ""
    if ai_analysis:
        from trendradar.ai.formatter import render_ai_analysis_html_rich
        ai_raw = render_ai_analysis_html_rich(ai_analysis)
        if ai_raw:
            ai_html = f"""            <div class="ai-region">
            {ai_raw}
        </div>"""
    region_contents["ai_analysis"] = ai_html

    # ════════════════════════════════════════════
    # 按 region_order 组装内容
    # ════════════════════════════════════════════
    for region in region_order:
        content = region_contents.get(region, "")
        if region == "new_items":
            new_h, rss_new_h = content if isinstance(content, tuple) else (content, "")
            if new_h:
                html += new_h
            if rss_new_h:
                html += rss_new_h
        elif content:
            html += content

    # ════════════════════════════════════════════
    # 截图按钮
    # ════════════════════════════════════════════
    html += """
            <div class="save-buttons" style="margin-top:24px;">
                <button class="save-btn" onclick="saveAsPNG()">📷 保存为图片</button>
            </div>
"""

    # ════════════════════════════════════════════
    # 页脚
    # ════════════════════════════════════════════
    html += """
    <div class="footer">
        <div class="footer-ornament">✦ ✦ ✦</div>
        <div class="footer-text">
            <strong>TrendRadar</strong> · 开源免费 · 自托管
            <br>
            <a href="https://github.com/sansan0/TrendRadar" target="_blank">GitHub</a>
            · 数据自动采集与分析 · 每日推送
        </div>
    </div>
"""

    # 如果有版本更新
    if update_info:
        html += f"""
    <div style="text-align:center;padding:10px;font-size:11px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;margin-top:16px;">
        发现新版本 {update_info.get('remote_version', '')}，当前版本 {update_info.get('current_version', '')}
    </div>"""

    html += """
</div><!-- /newspaper-inner -->
</div><!-- /newspaper -->
</div><!-- /page-wrap -->

<script>
    function handleSearch(query) {
        query = query.toLowerCase();
        document.querySelectorAll('.news-item').forEach(function(item) {
            var title = (item.querySelector('.news-title') || {}).textContent || '';
            item.style.display = (!query || title.toLowerCase().indexOf(query) !== -1) ? '' : 'none';
        });
    }

    function saveAsPNG() {
        var container = document.querySelector('.newspaper');
        var buttons = document.querySelector('.save-buttons');
        buttons.style.display = 'none';
        html2canvas(container, {
            backgroundColor: '#f7f2ea',
            scale: 1.5,
            useCORS: true,
            logging: false
        }).then(function(canvas) {
            buttons.style.display = '';
            var link = document.createElement('a');
            link.download = 'TrendRadar_' + new Date().toISOString().slice(0,10) + '.png';
            link.href = canvas.toDataURL('image/png');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }).catch(function() {
            buttons.style.display = '';
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        var searchBar = document.querySelector('.search-bar');
        if (searchBar) searchBar.style.display = 'block';
    });
</script>

</body>
</html>"""

    return html
