#!/usr/bin/env python3
"""Generate bento-style project card SVGs for GitHub profile README."""

import base64
import html
import json
import mimetypes
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cards"
LOGOS = ROOT / "assets" / "logos"

CARD_W = 920
CARD_H = 120
HERO_H = 156

RAW = "https://raw.githubusercontent.com/Nizar7zak/Nizar7zak/main/assets/logos"

PROJECTS = [
    {
        "id": "bayzat",
        "name": "Bayzat",
        "desc": "AI app builder + agentic cowork layer on Bayzat's work-life platform",
        "desc2": "Next.js · TypeScript · v0-style builder · agentic tools shipped to production",
        "tags": ["Enterprise AI", "Full-stack @ Bayzat"],
        "accent": "#8b5cf6",
        "logo_url": "https://cdn.jsdelivr.net/gh/GLINCKER/thesvg@main/public/icons/bayzat/default.svg",
        "logo_file": "bayzat.svg",
        "hero": True,
    },
    {
        "id": "evnno",
        "name": "evnno",
        "desc": "Maps link to paid landing page for freelancers",
        "tags": ["AI SaaS", "Stripe"],
        "accent": "#8b5cf6",
        "logo_url": "https://www.evnno.com/evnno-logo.png",
        "logo_file": "evnno.png",
    },
    {
        "id": "dozny",
        "name": "Dozny",
        "desc": "AI campaign and creative packs for creators",
        "tags": ["Creator AI", "AWS"],
        "accent": "#8b5cf6",
        "logo_url": "https://www.dozny.com/dozny-icon.svg",
        "logo_file": "dozny.svg",
    },
    {
        "id": "gaza-committee",
        "name": "Gaza Committee",
        "desc": "Universities emergency support and coordination platform",
        "tags": ["Public good", "Next.js"],
        "accent": "#3b82f6",
        "logo_url": "https://www.gazauniversities.org/images/site-logo.svg",
        "logo_file": "gaza-committee.svg",
        "logo_w": 56,
        "logo_h": 36,
    },
    {
        "id": "loi",
        "name": "LOI",
        "desc": "Saudi law firm site with EN/AR and admin dashboard",
        "tags": ["Legal tech", "EN/AR"],
        "accent": "#3b82f6",
        "logo_url": "https://www.loi.sa/logo.svg",
        "logo_file": "loi.svg",
    },
    {
        "id": "herfa",
        "name": "Herfa",
        "desc": "Scroll-driven brand storytelling for the Saudi market",
        "tags": ["Motion UX", "Next.js"],
        "accent": "#10b981",
        "logo_url": "https://herfa-ymtv.vercel.app/logo-herfa.svg",
        "logo_file": "herfa.svg",
    },
    {
        "id": "4co",
        "name": "4co",
        "desc": "Events and marketing agency site · bilingual EN/AR",
        "tags": ["Agency", "EN/AR"],
        "accent": "#10b981",
        "logo_url": "https://www.4co.sa/icon.svg",
        "logo_file": "4co.svg",
    },
    {
        "id": "saqeefa",
        "name": "Saqeefa",
        "desc": "Festival 2026 B2B landing and lead capture",
        "tags": ["B2B", "Next.js"],
        "accent": "#10b981",
        "logo_url": "https://saqeefa-ch26.com/icon.svg",
        "logo_file": "saqeefa.svg",
    },
    {
        "id": "azr",
        "name": "AZR",
        "desc": "Corporate site with maps integration and admin panel",
        "tags": ["Corporate", "Admin"],
        "accent": "#10b981",
        "logo_url": "https://azr-brown.vercel.app/icon.svg",
        "logo_file": "azr.svg",
    },
    {
        "id": "iminds",
        "name": "iMinds",
        "desc": "Saudi business marketing site built on Framer",
        "tags": ["Framer", "Saudi"],
        "accent": "#f59e0b",
        "logo_url": "https://framerusercontent.com/images/TbEPcTSAwkumrs7w3uC2zafho.svg",
        "logo_file": "iminds.svg",
    },
    {
        "id": "cons",
        "name": "Cons",
        "desc": "Saudi business marketing site built on Framer",
        "tags": ["Framer", "Saudi"],
        "accent": "#f59e0b",
        "logo_url": "https://framerusercontent.com/images/BbBeUvGeBgnKjzxe6enNChMqVtU.svg",
        "logo_file": "cons.svg",
    },
    {
        "id": "bouncegame",
        "name": "BounceGame",
        "desc": "Interactive Three.js browser game experiment",
        "tags": ["WebGL", "Three.js"],
        "accent": "#ef4444",
        "logo_file": "bouncegame.svg",
    },
    {
        "id": "gamehub",
        "name": "GameHub",
        "desc": "Game discovery app powered by the RAWG API",
        "tags": ["Side project", "TypeScript"],
        "accent": "#ef4444",
        "logo_file": "gamehub.webp",
    },
]


def fetch_logos() -> None:
    LOGOS.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        if "logo_url" not in p:
            continue
        dest = LOGOS / p["logo_file"]
        if dest.exists() and dest.stat().st_size > 0:
            continue
        print(f"fetching {p['logo_file']}...")
        req = urllib.request.Request(p["logo_url"], headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        dest.write_bytes(data)


def logo_data_uri(logo_file: str) -> str:
    path = LOGOS / logo_file
    data = path.read_bytes()
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        mime = "image/svg+xml" if path.suffix == ".svg" else "application/octet-stream"
    if path.suffix == ".svg" and mime != "image/svg+xml":
        mime = "image/svg+xml"
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def tag_pills(tags: list[str], accent: str, x: int, y: int) -> str:
    parts = []
    cx = x
    for tag in tags:
        w = len(tag) * 6.8 + 18
        t = html.escape(tag)
        parts.append(
            f'<rect x="{cx}" y="{y}" width="{w}" height="20" rx="10" fill="{accent}" fill-opacity="0.18"/>'
            f'<rect x="{cx}" y="{y}" width="{w}" height="20" rx="10" stroke="{accent}" stroke-opacity="0.45"/>'
            f'<text x="{cx + 9}" y="{y + 14}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10.5" font-weight="600" fill="{accent}">{t}</text>'
        )
        cx += w + 8
    return "\n  ".join(parts)


def card_svg(p: dict) -> str:
    hero = p.get("hero", False)
    w, h = CARD_W, (HERO_H if hero else CARD_H)
    lw = p.get("logo_w", 48)
    lh = p.get("logo_h", 48)
    lx, ly = 28, (h - lh) // 2
    tx = lx + lw + 24
    name = html.escape(p["name"])
    desc = html.escape(p["desc"])
    desc2 = html.escape(p.get("desc2", ""))
    accent = p["accent"]
    logo = logo_data_uri(p["logo_file"])
    grad_id = f"g-{p['id']}"

    title_y = 50 if hero else 46
    desc_y = 74 if hero else 66
    desc2_y = 94 if hero else 0
    tag_y = 118 if hero else 88

    desc2_line = ""
    if desc2:
        desc2_line = f'\n  <text x="{tx}" y="{desc2_y}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="12.5" fill="#64748b">{desc2}</text>'

    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}" stop-opacity="0.85"/>
      <stop offset="0.55" stop-color="#8b5cf6" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#06b6d4" stop-opacity="0.75"/>
    </linearGradient>
    <clipPath id="clip-{p['id']}">
      <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="10"/>
    </clipPath>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#14141f"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="url(#{grad_id})" fill-opacity="0.08"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16.5" stroke="url(#{grad_id})" stroke-opacity="0.65"/>
  <rect x="18" y="18" width="{lw+12}" height="{lh+12}" rx="14" fill="#ffffff" fill-opacity="0.04"/>
  <image href="{logo}" x="{lx}" y="{ly}" width="{lw}" height="{lh}" clip-path="url(#clip-{p['id']})" preserveAspectRatio="xMidYMid meet"/>
  <text x="{tx}" y="{title_y}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="{'22' if hero else '19'}" font-weight="700" fill="#f8fafc">{name}</text>
  <text x="{tx}" y="{desc_y}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="{'14' if hero else '13'}" fill="#94a3b8">{desc}</text>{desc2_line}
  {tag_pills(p["tags"], accent, tx, tag_y)}
</svg>
"""


def main() -> None:
    fetch_logos()
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        path = OUT / f"{p['id']}.svg"
        path.write_text(card_svg(p), encoding="utf-8")
        print(f"wrote {path.name}")
    (OUT / "manifest.json").write_text(json.dumps(PROJECTS, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
