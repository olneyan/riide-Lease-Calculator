from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "icons")

def draw_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    bg = (44, 62, 80, 255)   # #2c3e50
    accent = (52, 152, 219, 255)  # #3498db

    if maskable:
        # fill the full square (safe-zone padding handled by OS), no rounded corners
        d.rectangle([0, 0, size, size], fill=bg)
        pad = int(size * 0.22)
    else:
        radius = int(size * 0.18)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=bg)
        pad = int(size * 0.16)

    # accent circle
    d.ellipse([pad, pad, size - pad, size - pad], fill=accent)

    # dollar sign
    label = "$"
    font = None
    for fname in ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]:
        try:
            font = ImageFont.truetype(fname, int(size * 0.42))
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = d.textbbox((0, 0), label, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), label, fill=(255, 255, 255, 255), font=font)

    return img

os.makedirs(OUT, exist_ok=True)

draw_icon(192).save(os.path.join(OUT, "icon-192.png"))
draw_icon(512).save(os.path.join(OUT, "icon-512.png"))
draw_icon(192, maskable=True).save(os.path.join(OUT, "icon-maskable-192.png"))
draw_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"))

print("icons written to", OUT)
