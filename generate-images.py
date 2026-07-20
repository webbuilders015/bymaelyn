#!/usr/bin/env python3
"""
Generates the blog + treatment images via Replicate (nano-banana) and saves
them straight into the project's public/images folder.

Usage:
    REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py
or:
    python3 generate-images.py r8_xxx

Add --force (or FORCE=1) to regenerate images that already exist on disk,
e.g. after improving the prompts:
    REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py --force

Add --only=<tekst> to regenerate just one image whose path/filename contains
that text, instead of all 9, e.g. to redo only the wenkbrauwen image:
    REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py --force --only=wenkbrauwen
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ.get("REPLICATE_API_TOKEN") or next(
    (a for a in sys.argv[1:] if not a.startswith("-")), None
)
if not TOKEN:
    print("Usage: REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py [--force] [--only=tekst]")
    sys.exit(1)

FORCE = "--force" in sys.argv or os.environ.get("FORCE") == "1"
ONLY = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None) or os.environ.get("ONLY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# nano-banana (Google) tends to render more photorealistic, less "AI glossy" results.
MODEL = "google/nano-banana"
API_URL = f"https://api.replicate.com/v1/models/{MODEL}/predictions"

# Things that reliably make an image read as "AI-generated" to the eye: perfect
# symmetry, glassy/plastic skin, over-saturated colors, centered/staged
# composition, and a suspiciously clean environment. The previous version of
# this suffix also pushed toward a cool, muted, slightly grey "Kinfolk"
# editorial look, which read as dull/drab rather than luxurious. This version
# keeps the realism cues but shifts the color direction to warm, golden and
# rich instead - closer to a five-star spa than a moody lifestyle blog.
# Per-image prompts below also vary lens/light/angle so every shot doesn't
# come out with the identical "look".
ANTI_AI = (
    "luxurious spa and wellness photography for a high-end boutique beauty "
    "salon website, warm golden-hour light, rich warm color grading in "
    "warm ivory, champagne, honey and soft gold tones (never grey, never "
    "cool, never desaturated, never dull or flat), glowing warm skin tones, "
    "shot handheld with slight natural imperfection, asymmetrical off-center "
    "composition, real environment with authentic small tasteful details, "
    "accurate warm white balance, visible natural film grain, soft warm "
    "directional light with gentle warm shadows, skin has visible pores "
    "texture and natural blemishes and is not airbrushed or smoothed, "
    "imperfect natural hair flyaways, an inviting relaxed calm atmosphere, "
    "no perfect symmetry, no plastic or glossy CGI look, no waxy skin, no "
    "uncanny valley, no beauty-filter smoothing, no readable text or logos "
    "anywhere, not a 3D render, not digital illustration, not a flat grey "
    "stock-photo look, not a cold clinical look"
)

IMAGES = [
    (
        "public/images/blog/generated/huidverbeterende-gezichtsbehandeling-uitgelegd.jpg",
        "Candid over-the-shoulder photo in a luxurious boutique beauty salon "
        "treatment room: an esthetician's hand gently spreading a clay mask "
        "along a client's jawline with a soft spatula, client reclined with "
        "eyes closed looking utterly relaxed, a plush warm ivory towel "
        "wrapped around her hairline, a small gold-rimmed dish and a sprig "
        "of fresh eucalyptus on the side table, warm golden-hour sunlight "
        "streaming through a sheer curtain, shallow depth of field on a "
        "50mm lens, realistic imperfect skin texture with a healthy glow, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/chemische-peeling-vs-microdermabrasie.jpg",
        "Overhead flatlay on a warm honey-toned linen cloth: a small "
        "unlabeled amber glass dropper bottle glowing in warm golden "
        "afternoon light next to a diamond-tip microdermabrasion wand "
        "resting on its side, a small gold dish and a sprig of dried "
        "flowers beside it, natural warm shadows, slightly imperfect "
        "asymmetrical arrangement (not centered, not perfectly aligned), "
        "shot on 35mm with warm natural daylight, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/skincare-routine-vanaf-je-dertigste.jpg",
        "Morning flatlay on a warm cream marble counter with soft brass "
        "fixtures visible at the edge, slightly from above at an angle: a "
        "few unlabeled frosted glass skincare bottles and a jar of cream "
        "with the lid off and a small texture visible, a small sprig of "
        "fresh eucalyptus, soft golden morning sunlight casting long warm "
        "shadows, realistic uneven arrangement, faint water droplets "
        "catching the light, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/hoe-vaak-wenkbrauwen-epileren.jpg",
        "Extreme close-up macro photo of an eyebrow shaping treatment in a "
        "luxurious salon, tightly cropped on just the eyebrow and upper eye "
        "area: a simple plain steel tweezer tip precisely gripping a single "
        "hair exactly at the natural lower edge of a well-groomed eyebrow, "
        "the tweezer tip is in sharp focus touching the eyebrow hairs "
        "themselves (not the forehead, not the hairline, not empty skin), "
        "anatomically correct hand with only two fingertips holding the "
        "tweezer visible at the very edge of frame and mostly cropped out, "
        "client's eye closed looking relaxed, warm golden salon lighting, "
        "shot on a 100mm macro lens with shallow depth of field, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/waxen-vs-scheren-vs-ipl.jpg",
        "Simple luxurious still life on a warm honey-toned wood table: a "
        "small stack of folded waffle-weave ivory towels, a wooden bowl "
        "with cotton pads, a small unlit candle, and an unlabeled amber oil "
        "bottle glowing in warm afternoon sunlight, natural warm shadows, "
        "slightly imperfect casual arrangement, shot on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/paulas-choice-of-skeyndor.jpg",
        "Flatlay of a small premium skincare collection on warm travertine "
        "marble: two or three unlabeled frosted glass bottles of varying "
        "heights and a low ceramic jar, a small gold tray edge visible in "
        "frame, arranged with realistic uneven spacing (not symmetrical), "
        "warm golden raking light creating long natural shadows, subtle "
        "dust visible in the light, shot on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/wat-helpt-tegen-pigmentvlekken.jpg",
        "Natural close-up portrait crop of a woman's cheek and jaw turned "
        "slightly away from camera, warm golden-hour window light from one "
        "side giving her skin a healthy warm glow, real visible skin "
        "texture with faint natural pigmentation and pores, a few loose "
        "flyaway hairs, warm cozy interior softly blurred in the "
        "background, shot on an 85mm portrait lens with shallow depth of "
        "field, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/huidverzorging-winter-vs-zomer.jpg",
        "Cozy luxurious still life: an unlabeled matte ceramic cream jar "
        "with the lid resting beside it, sitting on a rumpled honey-toned "
        "chunky knit blanket near a window, warm golden lamp light mixing "
        "with soft daylight, a small steaming cup of tea nearby, realistic "
        "fabric texture and creases, shot on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/treatments/microdermabrasie.jpg",
        "Candid three-quarter angle photo in a luxurious boutique salon "
        "treatment room: an esthetician's gloved hand guiding a "
        "diamond-tip microdermabrasion device along a client's cheekbone, "
        "client reclined with eyes closed and a headband holding her hair "
        "back, looking utterly relaxed, warm golden window light from the "
        "side giving her skin a healthy glow, realistic skin texture, shot "
        "on a 50mm lens with shallow depth of field, "
        f"{ANTI_AI}",
    ),
]


def generate(prompt: str):
    payload = json.dumps(
        {
            "input": {
                "prompt": prompt,
                "aspect_ratio": "4:3",
                "output_format": "jpg",
            }
        }
    ).encode()

    req = urllib.request.Request(API_URL, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "wait")

    max_retries = 6
    backoff = 8
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < max_retries:
                print(f"  rate limited, waiting {backoff}s before retry {attempt}/{max_retries} ...")
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
                continue
            raise
    else:
        raise RuntimeError("Gave up after repeated 429 responses")

    if result.get("error"):
        raise RuntimeError(result["error"])

    output = result.get("output")
    if isinstance(output, list):
        return output[0] if output else None
    return output


def download(url: str, rel_path: str) -> None:
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    urllib.request.urlretrieve(url, full_path)


def main() -> None:
    for rel_path, prompt in IMAGES:
        if ONLY and ONLY.lower() not in rel_path.lower():
            continue
        full_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(full_path) and not FORCE:
            print(f"Skipping {rel_path} (already exists, use --force to regenerate)")
            continue
        print(f"Generating {rel_path} ...")
        try:
            url = generate(prompt)
            if not url:
                print(f"  ! no output returned for {rel_path}")
                continue
            download(url, rel_path)
            print(f"  saved -> {rel_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ! error: {exc}")
        time.sleep(6)

    print("Done. Let Claude know the images are in place so it can wire them into the site.")


if __name__ == "__main__":
    main()
