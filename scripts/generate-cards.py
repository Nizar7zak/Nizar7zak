#!/usr/bin/env python3
"""Generate bento-style project card SVGs for GitHub profile README."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cards"

W, H = 448, 104
HERO_W, HERO_H = 920, 120

PROJECTS = [
    {
        "id": "bayzat",
        "name": "Bayzat",
        "desc": "AI app builder + agentic cowork layer",
        "tag": "Enterprise AI",
        "accent": "#8b5cf6",
        "logo": "https://cdn.jsdelivr.net/gh/GLINCKER/thesvg@main/public/icons/bayzat/default.svg",
        "hero": True,
    },
    {
        "id": "evnno",
        "name": "evnno",
        "desc": "Maps link to paid landing page",
        "tag": "AI SaaS",
        "accent": "#8b5cf6",
        "logo": "https://www.evnno.com/evnno-logo.png",
    },
    {
        "id": "dozny",
        "name": "Dozny",
        "desc": "AI campaign packs for creators",
        "tag": "Creator AI",
        "accent": "#8b5cf6",
        "logo": "https://www.dozny.com/dozny-icon.svg",
    },
    {
        "id": "gaza-committee",
        "name": "Gaza Committee",
        "desc": "Universities emergency support platform",
        "tag": "Public good",
        "accent": "#3b82f6",
        "logo": "https://www.gazauniversities.org/images/site-logo.svg",
        "logo_w": 56,
        "logo_h": 36,
    },
    {
        "id": "loi",
        "name": "LOI",
        "desc": "Saudi law firm · EN/AR · admin",
        "tag": "Legal tech",
        "accent": "#3b82f6",
        "logo": "https://www.loi.sa/logo.svg",
    },
    {
        "id": "herfa",
        "name": "Herfa",
        "desc": "Scroll-driven brand storytelling",
        "tag": "Motion UX",
        "accent": "#10b981",
        "logo": "https://herfa-ymtv.vercel.app/logo-herfa.svg",
    },
    {
        "id": "4co",
        "name": "4co",
        "desc": "Events & marketing agency site",
        "tag": "EN/AR",
        "accent": "#10b981",
        "logo": "https://www.4co.sa/icon.svg",
    },
    {
        "id": "saqeefa",
        "name": "Saqeefa",
        "desc": "Festival 2026 B2B landing",
        "tag": "B2B",
        "accent": "#10b981",
        "logo": "https://saqeefa-ch26.com/icon.svg",
    },
    {
        "id": "azr",
        "name": "AZR",
        "desc": "Corporate site · maps · admin",
        "tag": "Corporate",
        "accent": "#10b981",
        "logo": "https://azr-brown.vercel.app/icon.svg",
    },
    {
        "id": "iminds",
        "name": "iMinds",
        "desc": "Saudi business site on Framer",
        "tag": "Framer",
        "accent": "#f59e0b",
        "logo": "https://framerusercontent.com/images/TbEPcTSAwkumrs7w3uC2zafho.svg",
    },
    {
        "id": "cons",
        "name": "Cons",
        "desc": "Saudi business site on Framer",
        "tag": "Framer",
        "accent": "#f59e0b",
        "logo": "https://framerusercontent.com/images/BbBeUvGeBgnKjzxe6enNChMqVtU.svg",
    },
    {
        "id": "bouncegame",
        "name": "BounceGame",
        "desc": "Interactive Three.js browser game",
        "tag": "WebGL",
        "accent": "#ef4444",
        "logo": "https://raw.githubusercontent.com/Nizar7zak/Nizar7zak/main/assets/logos/bouncegame.svg",
    },
    {
        "id": "gamehub",
        "name": "GameHub",
        "desc": "Game discovery powered by RAWG",
        "tag": "Side project",
        "accent": "#ef4444",
        "logo": "https://raw.githubusercontent.com/Nizar7zak/Nizar7zak/main/assets/logos/gamehub.webp",
    },
]


def card_svg(p: dict) -> str:
    hero = p.get("hero", False)
    w, h = (HERO_W, HERO_H) if hero else (W, H)
    lw = p.get("logo_w", 48)
    lh = p.get("logo_h", 48)
    lx = 28 if hero else 24
    ly = (h - lh) // 2
    tx = lx + lw + 22
    name = html.escape(p["name"])
    desc = html.escape(p["desc"])
    tag = html.escape(p["tag"])
    accent = p["accent"]
    logo = html.escape(p["logo"], quote=True)
    grad_id = f"g-{p['id']}"
    glow_id = f"gl-{p['id']}"

    title_size = 22 if hero else 18
    desc_size = 14 if hero else 12.5
    tag_y = 78 if hero else 68
    title_y = 46 if hero else 42
    desc_y = 68 if hero else 58

    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}" stop-opacity="0.85"/>
      <stop offset="0.55" stop-color="#8b5cf6" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#06b6d4" stop-opacity="0.75"/>
    </linearGradient>
    <filter id="{glow_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="clip-{p['id']}">
      <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="10"/>
    </clipPath>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#14141f"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="url(#{grad_id})" fill-opacity="0.08"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16.5" stroke="url(#{grad_id})" stroke-opacity="0.65"/>
  <rect x="18" y="18" width="{lw+12}" height="{lh+12}" rx="14" fill="#ffffff" fill-opacity="0.04"/>
  <image href="{logo}" x="{lx}" y="{ly}" width="{lw}" height="{lh}" clip-path="url(#clip-{p['id']})" preserveAspectRatio="xMidYMid meet"/>
  <text x="{tx}" y="{title_y}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="{title_size}" font-weight="700" fill="#f8fafc">{name}</text>
  <text x="{tx}" y="{desc_y}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="{desc_size}" fill="#94a3b8">{desc}</text>
  <rect x="{tx}" y="{tag_y}" width="{len(p['tag']) * 6.8 + 18}" height="20" rx="10" fill="{accent}" fill-opacity="0.18"/>
  <rect x="{tx}" y="{tag_y}" width="{len(p['tag']) * 6.8 + 18}" height="20" rx="10" stroke="{accent}" stroke-opacity="0.45"/>
  <text x="{tx + 9}" y="{tag_y + 14}" font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10.5" font-weight="600" fill="{accent}">{tag}</text>
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        path = OUT / f"{p['id']}.svg"
        path.write_text(card_svg(p), encoding="utf-8")
        print(f"wrote {path.name}")
    (OUT / "manifest.json").write_text(json.dumps(PROJECTS, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
