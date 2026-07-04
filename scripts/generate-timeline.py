#!/usr/bin/env python3
"""Generate timeline SVG for GitHub profile README."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "timeline.svg"

W, H = 920, 400

STOPS = [
    {
        "year": "2025",
        "company": "Bayzat",
        "desc": "Full-stack product work · AI builder · agentic cowork",
        "tags": ["Next.js", "TypeScript", "AI"],
        "accent": "#8b5cf6",
        "flag": "🇦🇪",
        "current": True,
    },
    {
        "year": "2024",
        "company": "Metachain",
        "desc": "Built evnno + Dozny · AI generation · Stripe · AWS",
        "tags": ["SaaS", "OpenAI", "AWS"],
        "accent": "#6366f1",
        "flag": "",
    },
    {
        "year": "2023",
        "company": "A-LL Creative Technology",
        "desc": "Web AR for Swiss museums · 8thWall · R3F · Swift App Clips",
        "tags": ["Web AR", "Three.js", "Swift"],
        "accent": "#3b82f6",
        "flag": "🇨🇭",
    },
    {
        "year": "2022",
        "company": "Gaza Sky Geeks",
        "desc": "AWS Instructor · React/Express mentor · 200+ students",
        "tags": ["AWS", "React", "Teaching"],
        "accent": "#10b981",
        "flag": "🇵🇸",
    },
]


def tag_row(tags: list[str], x: int, y: int, accent: str) -> str:
    parts = []
    cx = x
    for tag in tags:
        tw = len(tag) * 6.2 + 16
        parts.append(
            f'<rect x="{cx}" y="{y}" width="{tw}" height="18" rx="9" fill="{accent}" fill-opacity="0.22" stroke="{accent}" stroke-opacity="0.5"/>'
            f'<text x="{cx + 8}" y="{y + 13}" font-family="ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="10" font-weight="600" fill="#ffffff">{tag}</text>'
        )
        cx += tw + 6
    return "\n    ".join(parts)


def stop_row(i: int, s: dict) -> str:
    y = 72 + i * 82
    cy = y + 28
    accent = s["accent"]
    flag = f' {s["flag"]}' if s.get("flag") else ""
    pulse = ""
    if s.get("current"):
        pulse = f"""
    <circle cx="56" cy="{cy}" r="16" fill="{accent}" fill-opacity="0.15"/>
    <circle cx="56" cy="{cy}" r="11" fill="{accent}" fill-opacity="0.35"/>"""

    return f"""
  {pulse}
  <circle cx="56" cy="{cy}" r="7" fill="{accent}"/>
  <circle cx="56" cy="{cy}" r="4" fill="#ffffff"/>
  <rect x="78" y="{y}" width="96" height="24" rx="12" fill="{accent}" fill-opacity="0.2" stroke="{accent}" stroke-opacity="0.55"/>
  <text x="126" y="{y + 17}" text-anchor="middle" font-family="ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="{accent}">{s['year']}</text>
  <text x="190" y="{y + 18}" font-family="ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="17" font-weight="700" fill="#f8fafc">{s['company']}{flag}</text>
  <text x="190" y="{y + 40}" font-family="ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="13" fill="#94a3b8">{s['desc']}</text>
  {tag_row(s['tags'], 190, y + 50, accent)}"""


def main() -> None:
    rows = "\n".join(stop_row(i, s) for i, s in enumerate(STOPS))
    line_end = 72 + (len(STOPS) - 1) * 82 + 28

    svg = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8b5cf6" stop-opacity="0.75"/>
      <stop offset="0.55" stop-color="#6366f1" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#06b6d4" stop-opacity="0.65"/>
    </linearGradient>
    <linearGradient id="line-grad" x1="56" y1="72" x2="56" y2="{line_end}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8b5cf6"/>
      <stop offset="0.5" stop-color="#6366f1"/>
      <stop offset="1" stop-color="#10b981"/>
    </linearGradient>
    <style>
      @keyframes pulse {{
        0%, 100% {{ opacity: 0.35; r: 11; }}
        50% {{ opacity: 0.15; r: 18; }}
      }}
      .live {{ animation: pulse 2.4s ease-in-out infinite; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="#14141f"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#bg-grad)" fill-opacity="0.08"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16.5" stroke="url(#bg-grad)" stroke-opacity="0.65"/>
  <text x="890" y="38" text-anchor="end" font-family="ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" font-weight="600" fill="#64748b">2022 → NOW</text>
  <line x1="56" y1="72" x2="56" y2="{line_end}" stroke="url(#line-grad)" stroke-width="3" stroke-linecap="round"/>
  {rows}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
