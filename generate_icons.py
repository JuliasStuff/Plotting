#!/usr/bin/env python3
"""
Generate Plotting PWA icons (icon-192.png and icon-512.png).
Requires Pillow:  pip install Pillow
"""
import math

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Pillow not found. Install it with:  pip install Pillow")


def star_points(cx, cy, outer, inner, n=4):
    """Return vertex list for an n-pointed star."""
    pts = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        angle = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def make_icon(size: int) -> None:
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s    = size

    # ── Rounded-square background ────────────────────────────────────
    radius = s // 5
    draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill="#1c1131")

    # Subtle inner gradient ring (simulate with concentric ellipses)
    ring_pad = s // 10
    draw.ellipse(
        [ring_pad, ring_pad, s - ring_pad, s - ring_pad],
        outline="#a855f7", width=max(2, s // 60),
    )

    cx, cy = s / 2, s / 2

    # ── Large gold 4-pointed sparkle star ───────────────────────────
    outer4 = s * 0.30
    inner4 = s * 0.08
    draw.polygon(star_points(cx, cy, outer4, inner4, n=4), fill="#f59e0b")

    # ── Smaller pink accent stars at the corners ─────────────────────
    accents = [
        (-0.25, -0.26, 0.10),
        ( 0.26, -0.25, 0.09),
        (-0.24,  0.27, 0.08),
        ( 0.25,  0.26, 0.10),
    ]
    for ox, oy, scale in accents:
        px, py  = cx + ox * s, cy + oy * s
        s_out   = s * scale
        s_in    = s_out * 0.35
        draw.polygon(star_points(px, py, s_out, s_in, n=4), fill="#ec4899")

    # ── Tiny purple dot in centre ────────────────────────────────────
    r_dot = max(2, s // 28)
    draw.ellipse(
        [cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot],
        fill="#f0e6ff",
    )

    path = f"icon-{size}.png"
    img.save(path)
    print(f"  Created {path}  ({size}×{size})")


if __name__ == "__main__":
    print("Generating Plotting icons…")
    make_icon(192)
    make_icon(512)
    print("Done!")
