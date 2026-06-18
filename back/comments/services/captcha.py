import random
import string
import uuid
from base64 import b64encode
from io import BytesIO

from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAPTCHA_CHARS = string.ascii_uppercase + string.digits
CAPTCHA_LENGTH = 6
CAPTCHA_TTL = 300  # seconds — captcha expires after 5 minutes
CACHE_PREFIX = "captcha:"


def _cache_key(key: str) -> str:
    return f"{CACHE_PREFIX}{key}"


def generate_captcha() -> tuple[str, str]:
    """Creates a new captcha. Returns (key, base64_png_image)."""
    key = str(uuid.uuid4())
    text = "".join(random.choices(CAPTCHA_CHARS, k=CAPTCHA_LENGTH))
    cache.set(_cache_key(key), text, timeout=CAPTCHA_TTL)
    return key, _render_image(text)


def verify_captcha(key: str, value: str) -> bool:
    """Checks user answer against stored value. Deletes the key (one-time use)."""
    stored = cache.get(_cache_key(key))
    if stored is None:
        return False
    cache.delete(_cache_key(key))
    return stored.upper() == value.strip().upper()


def _render_image(text: str) -> str:
    """Renders captcha text to a noisy PNG and returns it as a base64 data-URI."""
    width, height = 200, 60
    bg_color = (245, 245, 245)

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Background noise dots
    for _ in range(120):
        draw.point(
            (random.randint(0, width), random.randint(0, height)),
            fill=(
                random.randint(150, 220),
                random.randint(150, 220),
                random.randint(150, 220),
            ),
        )

    # Load font — Pillow 10+ supports load_default(size=N)
    try:
        font = ImageFont.load_default(size=36)
    except TypeError:
        font = ImageFont.load_default()

    # Draw each character with slight random vertical jitter
    x = 15
    for char in text:
        y = random.randint(5, 18)
        color = (
            random.randint(10, 80),
            random.randint(10, 80),
            random.randint(10, 80),
        )
        draw.text((x, y), char, fill=color, font=font)
        x += 28

    # Noise lines across the image
    for _ in range(4):
        draw.line(
            [
                (random.randint(0, width), random.randint(0, height)),
                (random.randint(0, width), random.randint(0, height)),
            ],
            fill=(random.randint(100, 180), random.randint(100, 180), random.randint(100, 180)),
            width=1,
        )

    img = img.filter(ImageFilter.SMOOTH)

    buf = BytesIO()
    img.save(buf, format="PNG")
    encoded = b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"