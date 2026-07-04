#!/usr/bin/env python3
"""Generate native HTML timeline block for GitHub profile README."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "timeline.html"

STOPS = [
    {
        "year": "2025",
        "company": "Bayzat",
        "flag": "🇦🇪",
        "desc": "Full-stack product work · AI builder · agentic cowork",
        "tags": ["Next.js", "TypeScript", "AI"],
        "accent": "8b5cf6",
        "line": "6366f1",
        "current": True,
    },
    {
        "year": "2024",
        "company": "Metachain",
        "flag": "",
        "desc": "Built evnno + Dozny · AI generation · Stripe · AWS",
        "tags": ["SaaS", "OpenAI", "AWS"],
        "accent": "6366f1",
        "line": "3b82f6",
    },
    {
        "year": "2023",
        "company": "A-LL Creative Technology",
        "flag": "🇨🇭",
        "desc": "Web AR for Swiss museums · 8thWall · R3F · Swift App Clips",
        "tags": ["Web AR", "Three.js", "Swift"],
        "accent": "3b82f6",
        "line": "10b981",
    },
    {
        "year": "2022",
        "company": "Gaza Sky Geeks",
        "flag": "🇵🇸",
        "desc": "AWS Instructor · React/Express mentor · 200+ students",
        "tags": ["AWS", "React", "Teaching"],
        "accent": "10b981",
        "line": None,
    },
]


def year_shield(year: str, color: str) -> str:
    return (
        f'<img src="https://img.shields.io/badge/{year}-{year}-{color}'
        f'?style=flat-square&labelColor={color}&color=ffffff" alt="{year}"/>'
    )


def tag_shield(tag: str, color: str) -> str:
    slug = tag.replace(" ", "%20").replace(".", "%2E")
    return (
        f'<img src="https://img.shields.io/badge/{slug}-ffffff?style=flat-square'
        f'&labelColor={color}&color=ffffff" alt="{tag}"/>'
    )


from typing import Optional


def dot_cell(accent: str, current: bool, line: Optional[str]) -> str:
    glow = ""
    if current:
        glow = (
            f'<span style="color:#{accent};font-size:28px;line-height:1;opacity:0.35">◉</span><br/>'
        )
    dot = f'<span style="color:#{accent};font-size:18px;line-height:1">●</span>'
    spine = ""
    if line:
        spine = (
            f'<table cellpadding="0" cellspacing="0" align="center" style="margin-top:2px">'
            f'<tr><td width="3" height="58" bgcolor="#{line}"></td></tr></table>'
        )
    return (
        f'<td width="56" align="center" valign="top" style="padding-top:2px">'
        f"{glow}{dot}{spine}</td>"
    )


def entry_row(stop: dict, last: bool) -> str:
    flag = f" {stop['flag']}" if stop.get("flag") else ""
    accent = stop["accent"]
    line = None if last else stop.get("line")
    tags = " ".join(tag_shield(t, accent) for t in stop["tags"])
    year = year_shield(stop["year"], accent)
    return f"""<tr>
{dot_cell(accent, stop.get("current", False), line)}
<td valign="top" style="padding-bottom:14px">
{year} <strong>{stop['company']}{flag}</strong><br/>
<sub>{stop['desc']}</sub><br/>
{tags}
</td>
</tr>"""


def main() -> None:
    rows = "\n".join(
        entry_row(s, i == len(STOPS) - 1) for i, s in enumerate(STOPS)
    )
    html = f"""<div align="center">

<table width="920" cellpadding="0" cellspacing="0" style="table-layout:fixed;">
<tr><td bgcolor="#14141f" style="border:2px solid #6366f1;border-radius:16px;padding:10px 16px 6px">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td colspan="2" align="right"><sub>2022 → NOW</sub></td></tr>
{rows}
</table>
</td></tr>
</table>

</div>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
