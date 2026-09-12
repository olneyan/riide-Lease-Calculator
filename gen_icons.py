from PIL import Image, ImageDraw
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "icons")

BG = (44, 62, 80, 255)      # #2c3e50 navy
ACCENT = (52, 152, 219, 255)  # #3498db blue
WHITE = (255, 255, 255, 255)


def draw_car(d, size, cx, cy, scale, color):
    """Simple flat side-view car silhouette centered at (cx, cy)."""
    body_w = size * 0.60 * scale
    body_h = size * 0.15 * scale
    body_top = cy - body_h * 0.2
    body_left = cx - body_w / 2

    cabin_w = size * 0.32 * scale
    cabin_h = size * 0.15 * scale
    cabin_left = cx - cabin_w / 2
    cabin_top = body_top - cabin_h * 0.85

    # cabin (roof + windows)
    d.rounded_rectangle(
        [cabin_left, cabin_top, cabin_left + cabin_w, cabin_top + cabin_h * 1.2],
        radius=cabin_h * 0.55, fill=color
    )
    # body
    d.rounded_rectangle(
        [body_left, body_top, body_left + body_w, body_top + body_h],
        radius=body_h * 0.5, fill=color
    )
    # wheels
    wheel_r = size * 0.075 * scale
    wheel_y = body_top + body_h
    for wx in (body_left + body_w * 0.24, body_left + body_w * 0.76):
        d.ellipse([wx - wheel_r, wheel_y - wheel_r, wx + wheel_r, wheel_y + wheel_r], fill=BG if color == WHITE else color)
        d.ellipse([wx - wheel_r * 0.45, wheel_y - wheel_r * 0.45, wx + wheel_r * 0.45, wheel_y + wheel_r * 0.45], fill=color)

    # motion lines (speed) to the left of the car — scaled with the car itself
    line_y_offsets = [-0.02, 0.05, 0.12]
    line_lengths = [0.14, 0.20, 0.10]
    line_x_end = body_left - size * 0.03 * scale
    for dy, ll in zip(line_y_offsets, line_lengths):
        ly = cy + size * dy * scale
        d.line(
            [(line_x_end - size * ll * scale, ly), (line_x_end, ly)],
            fill=color, width=max(2, int(size * 0.018 * scale))
        )


def make_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if maskable:
        d.rectangle([0, 0, size, size], fill=BG)
        scale = 0.60  # keep content inside the maskable safe zone
    else:
        radius = int(size * 0.20)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)
        scale = 0.85

    # the motion lines sit left of the car, so nudge the car right to
    # keep the whole composition (car + lines) visually centered
    cx = size / 2 + size * scale * 0.115
    draw_car(d, size, cx, size * 0.56, scale, WHITE)

    # accent underline suggesting a road
    road_w = size * 0.66 * scale
    road_h = max(2, int(size * 0.028))
    d.rounded_rectangle(
        [size / 2 - road_w / 2, size * 0.78, size / 2 + road_w / 2, size * 0.78 + road_h],
        radius=road_h / 2, fill=ACCENT
    )

    return img


os.makedirs(OUT, exist_ok=True)

make_icon(192).save(os.path.join(OUT, "icon-192.png"))
make_icon(512).save(os.path.join(OUT, "icon-512.png"))
make_icon(192, maskable=True).save(os.path.join(OUT, "icon-maskable-192.png"))
make_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"))

print("icons written to", OUT)
