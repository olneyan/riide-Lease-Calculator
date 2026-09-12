from PIL import Image, ImageDraw
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "icons")

BG = (44, 62, 80, 255)      # #2c3e50 navy
ACCENT = (52, 152, 219, 255)  # #3498db blue
WHITE = (255, 255, 255, 255)


def draw_group(d, size, cx, cy, scale):
    """Car + motion lines + road underline, anchored at (cx, cy)."""
    body_w = size * 0.60 * scale
    body_h = size * 0.15 * scale
    body_top = cy - body_h * 0.2
    body_left = cx - body_w / 2

    cabin_w = size * 0.32 * scale
    cabin_h = size * 0.15 * scale
    cabin_left = cx - cabin_w / 2
    cabin_top = body_top - cabin_h * 0.85

    d.rounded_rectangle(
        [cabin_left, cabin_top, cabin_left + cabin_w, cabin_top + cabin_h * 1.2],
        radius=cabin_h * 0.55, fill=WHITE
    )
    d.rounded_rectangle(
        [body_left, body_top, body_left + body_w, body_top + body_h],
        radius=body_h * 0.5, fill=WHITE
    )

    wheel_r = size * 0.075 * scale
    wheel_y = body_top + body_h
    for wx in (body_left + body_w * 0.24, body_left + body_w * 0.76):
        d.ellipse([wx - wheel_r, wheel_y - wheel_r, wx + wheel_r, wheel_y + wheel_r], fill=BG)
        d.ellipse([wx - wheel_r * 0.45, wheel_y - wheel_r * 0.45, wx + wheel_r * 0.45, wheel_y + wheel_r * 0.45], fill=WHITE)

    line_y_offsets = [-0.02, 0.05, 0.12]
    line_lengths = [0.14, 0.20, 0.10]
    line_x_end = body_left - size * 0.03 * scale
    for dy, ll in zip(line_y_offsets, line_lengths):
        ly = cy + size * dy * scale
        d.line(
            [(line_x_end - size * ll * scale, ly), (line_x_end, ly)],
            fill=WHITE, width=max(2, int(size * 0.018 * scale))
        )

    road_w = size * 0.66 * scale
    road_h = max(2, int(size * 0.028 * scale))
    road_top = wheel_y + wheel_r + size * 0.09 * scale
    d.rounded_rectangle(
        [cx - road_w / 2, road_top, cx + road_w / 2, road_top + road_h],
        radius=road_h / 2, fill=ACCENT
    )


def content_bbox_center(size, scale):
    """Render the group on a transparent canvas at a neutral anchor and
    measure its actual bounding box, so we can compute the shift needed
    to make it exactly centered regardless of its internal asymmetry."""
    probe = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(probe)
    anchor = (size / 2, size / 2)
    draw_group(d, size, anchor[0], anchor[1], scale)
    bbox = probe.getbbox()
    bx0, by0, bx1, by1 = bbox
    return ((bx0 + bx1) / 2, (by0 + by1) / 2), anchor


def make_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if maskable:
        d.rectangle([0, 0, size, size], fill=BG)
        scale = 0.60
    else:
        radius = int(size * 0.20)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)
        scale = 0.85

    bbox_center, anchor = content_bbox_center(size, scale)
    shift_x = size / 2 - bbox_center[0]
    shift_y = size / 2 - bbox_center[1]
    cx = anchor[0] + shift_x
    cy = anchor[1] + shift_y

    draw_group(d, size, cx, cy, scale)
    return img


os.makedirs(OUT, exist_ok=True)

make_icon(192).save(os.path.join(OUT, "icon-192.png"))
make_icon(512).save(os.path.join(OUT, "icon-512.png"))
make_icon(192, maskable=True).save(os.path.join(OUT, "icon-maskable-192.png"))
make_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"))

print("icons written to", OUT)
