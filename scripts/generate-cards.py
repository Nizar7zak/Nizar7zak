#!/usr/bin/env python3
"""Generate bento-style project card PNGs for GitHub profile README."""

import json
import subprocess
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cards"
LOGOS = ROOT / "assets" / "logos"

CARD_W = 920
CARD_H = 120
HERO_H = 156

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

PROJECTS = [
    {
        "id": "bayzat",
        "name": "Bayzat",
        "desc": "Core team on Bayzat's AI app builder, shipping prompt-to-product tooling integrated with the platform",
        "desc2": "Built a lean agentic cowork layer embedded in Bayzat's system for in-platform workflows",
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


def hex_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def flatten_logo(logo: Image.Image) -> Image.Image:
    """Turn near-black pixels transparent so logos sit cleanly on dark wells."""
    logo = logo.convert("RGBA")
    pixels = logo.load()
    for y in range(logo.height):
        for x in range(logo.width):
            r, g, b, a = pixels[x, y]
            if r < 40 and g < 40 and b < 40:
                pixels[x, y] = (0, 0, 0, 0)
    return logo


def load_logo(path: Path, size: tuple[int, int]) -> Image.Image:
    if path.suffix.lower() == ".svg":
        result = subprocess.run(
            ["rsvg-convert", "-w", str(size[0]), "-h", str(size[1]), str(path)],
            capture_output=True,
            check=True,
        )
        logo = Image.open(BytesIO(result.stdout)).convert("RGBA")
    else:
        logo = Image.open(path).convert("RGBA")
        logo.thumbnail(size, Image.Resampling.LANCZOS)
    logo = flatten_logo(logo)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    ox = (size[0] - logo.width) // 2
    oy = (size[1] - logo.height) // 2
    canvas.paste(logo, (ox, oy), logo)
    return canvas


def rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill=None, outline=None, width: int = 1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_tag(draw: ImageDraw.ImageDraw, font, text: str, x: int, y: int, accent: str) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    pad_x = 10
    w = tw + pad_x * 2
    h = 22
    rounded_rect(draw, (x, y, x + w, y + h), 10, fill=accent, outline=accent, width=1)
    draw.text((x + pad_x, y + 4), text, fill=(255, 255, 255), font=font)
    return w + 8


def render_card(p: dict) -> Image.Image:
    hero = p.get("hero", False)
    w, h = CARD_W, HERO_H if hero else CARD_H
    img = Image.new("RGB", (w, h), (20, 20, 31))
    draw = ImageDraw.Draw(img)

    accent = p["accent"]
    accent_rgb = hex_rgb(accent)

    # subtle horizontal gradient wash
    for i in range(w):
        t = i / max(w - 1, 1)
        r = int(accent_rgb[0] * (1 - t) * 0.07 + 20 * (1 - 0.07))
        g = int(accent_rgb[1] * (1 - t) * 0.07 + 20 * (1 - 0.07))
        b = int(accent_rgb[2] * (1 - t) * 0.07 + 31 * (1 - 0.07))
        draw.line([(i, 0), (i, h)], fill=(r, g, b))

    # border
    rounded_rect(draw, (0, 0, w - 1, h - 1), 16, outline=accent, width=2)

    lw = p.get("logo_w", 48)
    lh = p.get("logo_h", 48)
    lx, ly = 24, (h - lh) // 2
    tx = lx + lw + 22

    # dark logo well (works for light and dark logos)
    rounded_rect(draw, (lx - 8, ly - 8, lx + lw + 8, ly + lh + 8), 12, fill=(37, 37, 54))

    logo = load_logo(LOGOS / p["logo_file"], (lw, lh))
    if logo.mode == "RGBA":
        img.paste(logo, (lx, ly), logo)
    else:
        img.paste(logo, (lx, ly))
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_BOLD, 22 if hero else 19)
    desc_font = ImageFont.truetype(FONT_REG, 14 if hero else 13)
    desc2_font = ImageFont.truetype(FONT_REG, 12)
    tag_font = ImageFont.truetype(FONT_BOLD, 12)

    title_y = 38 if hero else 34
    desc_y = 66 if hero else 58
    tag_y = 118 if hero else 86

    draw.text((tx, title_y), p["name"], fill="#f8fafc", font=title_font)
    draw.text((tx, desc_y), p["desc"], fill="#94a3b8", font=desc_font)

    if p.get("desc2"):
        draw.text((tx, desc_y + 22), p["desc2"], fill="#64748b", font=desc2_font)

    cx = tx
    for tag in p["tags"]:
        cx += draw_tag(draw, tag_font, tag, cx, tag_y, accent)

    return img


def main() -> None:
    fetch_logos()
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        png_path = OUT / f"{p['id']}.png"
        render_card(p).save(png_path, "PNG", optimize=True)
        print(f"wrote {png_path.name}")
    (OUT / "manifest.json").write_text(json.dumps(PROJECTS, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
