#!/usr/bin/env python3
"""
Generate creative Pinterest-optimized 1000x1500 images for ClearCents posts.
Adds branded text overlay, gradient, title, and CTA for high-conversion pins.
"""

import sys
import os
import re
import glob
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Brand colours
GOLD    = (245, 197, 24)
WHITE   = (255, 255, 255)
DARK    = (5,   8,  16)
GREEN   = (0,  208, 132)

W, H = 1000, 1500   # 2:3 Pinterest ratio

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
FONT_PATHS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + 2*radius, y0 + 2*radius], fill=fill)
    draw.ellipse([x1 - 2*radius, y0, x1, y0 + 2*radius], fill=fill)
    draw.ellipse([x0, y1 - 2*radius, x0 + 2*radius, y1], fill=fill)
    draw.ellipse([x1 - 2*radius, y1 - 2*radius, x1, y1], fill=fill)

def create_gradient_overlay(size):
    ov = Image.new("RGBA", size, (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)
    w, h = size
    for y in range(h):
        t = y / h
        # Gentle dark vignette top + heavy dark bottom for text legibility
        if t < 0.25:
            alpha = int(120 * (t / 0.25))
        elif t < 0.55:
            alpha = int(120 + 60 * ((t - 0.25) / 0.30))
        else:
            alpha = int(180 + 68 * ((t - 0.55) / 0.45))
        d.line([(0, y), (w, y)], fill=(*DARK, min(alpha, 235)))
    return ov

def create_pinterest_image(title, image_url, output_path, category=""):
    # 1 ── Download & crop background
    try:
        resp = requests.get(image_url, timeout=25)
        resp.raise_for_status()
        bg = Image.open(BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        print(f"  ✗ Could not download image: {e}")
        return False

    scale = max(W / bg.width, H / bg.height)
    nw, nh = int(bg.width * scale), int(bg.height * scale)
    bg = bg.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    bg = bg.crop((x0, y0, x0 + W, y0 + H))

    # 2 ── Overlay
    canvas = Image.alpha_composite(bg.convert("RGBA"), create_gradient_overlay((W, H))).convert("RGB")
    draw   = ImageDraw.Draw(canvas)

    # 3 ── Fonts
    f_brand   = load_font(FONT_PATHS,     46)
    f_title   = load_font(FONT_PATHS,     78)
    f_title_sm= load_font(FONT_PATHS,     66)
    f_cta     = load_font(FONT_PATHS,     38)
    f_cat     = load_font(FONT_PATHS,     34)

    # 4 ── TOP BADGE ─────────────────────────────────────────────
    badge_x, badge_y = 48, 56
    badge_text = "CLEARCENTS"
    # gold pill behind text
    bbox = draw.textbbox((0, 0), badge_text, font=f_brand)
    bw = bbox[2] - bbox[0] + 40
    bh = bbox[3] - bbox[1] + 18
    draw_rounded_rect(draw, (badge_x - 12, badge_y - 6, badge_x + bw, badge_y + bh), 10, GOLD)
    draw.text((badge_x + 8, badge_y + 2), badge_text, font=f_brand, fill=DARK)

    # category chip (if present)
    if category:
        cat_label = category.replace("-", " ").upper()
        cx = badge_x
        cy = badge_y + bh + 22
        cb = draw.textbbox((0, 0), cat_label, font=f_cat)
        cw = cb[2] - cb[0] + 36
        ch = cb[3] - cb[1] + 14
        draw_rounded_rect(draw, (cx - 10, cy - 4, cx + cw, cy + ch), 8, GREEN)
        draw.text((cx + 8, cy + 2), cat_label, font=f_cat, fill=DARK)

    # 5 ── TITLE BLOCK ────────────────────────────────────────────
    # Choose font size based on title length
    if len(title) <= 40:
        tf, line_h = f_title, 96
        wrap_w = 18
    else:
        tf, line_h = f_title_sm, 84
        wrap_w = 22

    lines = textwrap.wrap(title, width=wrap_w)
    total_h = len(lines) * line_h
    ty = H - total_h - 210

    for line in lines:
        # shadow
        draw.text((54, ty + 4), line, font=tf, fill=(0, 0, 0, 200))
        # white text
        draw.text((50, ty), line, font=tf, fill=WHITE)
        ty += line_h

    # 6 ── GOLD ACCENT LINE ───────────────────────────────────────
    draw.rectangle([(50, H - 185), (340, H - 180)], fill=GOLD)

    # 7 ── CTA STRIP ──────────────────────────────────────────────
    cta = "→  Free guide at clearcentslife.com"
    draw.text((50, H - 162), cta, font=f_cta, fill=GOLD)

    # 8 ── BOTTOM TAGLINE ─────────────────────────────────────────
    f_tag = load_font(FONT_PATHS_REG, 30)
    draw.text((50, H - 110), "Practical money advice for real people", font=f_tag, fill=(200, 200, 200))

    # 9 ── Save ───────────────────────────────────────────────────
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path, "JPEG", quality=94, optimize=True)
    print(f"  ✓ {output_path}")
    return True


def extract_front_matter(content):
    m = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        kv = line.split(":", 1)
        if len(kv) == 2:
            fm[kv[0].strip()] = kv[1].strip().strip('"').strip("'")
    return fm


def main():
    posts = sorted(glob.glob("_posts/*.md"))
    if not posts:
        print("No posts found. Run from the Jekyll root directory.")
        sys.exit(1)

    # If a specific slug is passed, only process that one
    target = sys.argv[1] if len(sys.argv) > 1 else None

    for post_path in posts:
        slug = os.path.basename(post_path).replace(".md", "")
        if target and target not in slug:
            continue

        out = f"assets/pinterest/{slug}.jpg"
        if os.path.exists(out) and not target:
            continue  # skip already generated (unless explicit target)

        with open(post_path, encoding="utf-8") as f:
            content = f.read()

        fm = extract_front_matter(content)
        title     = fm.get("title", "")
        image_url = fm.get("image", "")
        category  = fm.get("categories", "").strip("[]").split()[0] if fm.get("categories") else ""

        if not title or not image_url:
            print(f"  skip {slug} (missing title or image)")
            continue

        print(f"Generating: {slug}")
        create_pinterest_image(title, image_url, out, category)


if __name__ == "__main__":
    main()
