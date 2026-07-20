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
    print("Usage: REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py [--force]")
    sys.exit(1)

FORCE = "--force" in sys.argv or os.environ.get("FORCE") == "1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# nano-banana (Google) tends to render more photorealistic, less "AI glossy" results.
MODEL = "google/nano-banana"
API_URL = f"https://api.replicate.com/v1/models/{MODEL}/predictions"

# Things that reliably make an image read as "AI-generated" to the eye: perfect
# symmetry, glassy/plastic skin, over-saturated colors, centered/staged
# composition, and a suspiciously clean environment. This suffix pushes hard
# against all of that. Per-image prompts below also vary lens/light/angle so
# every shot doesn't come out with the identical "look".
ANTI_AI = (
    "authentic editorial photography for a boutique skincare salon website, "
    "in the style of a real magazine feature (Kinfolk / Cereal magazine "
    "aesthetic), shot handheld with slight natural imperfection, asymmetrical "
    "off-center composition, real imperfect environment with authentic small "
    "clutter, true-to-life muted color grading (not oversaturated, not "
    "teal-and-orange), accurate white balance, visible natural film grain, "
    "realistic uneven ambient light with soft shadows, skin has visible pores "
    "texture and natural blemishes and is not airbrushed or smoothed, "
    "imperfect natural hair flyaways, no perfect symmetry, no plastic or "
    "glossy CGI look, no waxy skin, no uncanny valley, no beauty-filter "
    "smoothing, no readable text or logos anywhere, not a 3D render, not "
    "digital illustration, not a stock-photo studio setup"
)

IMAGES = [
    (
        "public/images/blog/generated/huidverbeterende-gezichtsbehandeling-uitgelegd.jpg",
        "Candid over-the-shoulder photo in a small boutique beauty salon "
        "treatment room: an esthetician's hand gently spreading a clay mask "
        "along a client's jawline with a soft spatula, client reclined with "
        "eyes closed, a rolled white towel around her hairline, warm late "
        "afternoon window light from the side, shallow depth of field on a "
        "50mm lens, realistic imperfect skin texture, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/chemische-peeling-vs-microdermabrasie.jpg",
        "Overhead flatlay on a raw linen cloth: a small unlabeled amber "
        "glass dropper bottle catching soft window light next to a "
        "diamond-tip microdermabrasion wand resting on its side, a folded "
        "muslin cloth beside it, natural uneven shadows, slightly imperfect "
        "asymmetrical arrangement (not centered, not perfectly aligned), "
        "shot on 35mm with natural daylight, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/skincare-routine-vanaf-je-dertigste.jpg",
        "Morning bathroom counter flatlay, slightly from above at an angle: "
        "a few unlabeled matte glass skincare bottles and a jar of cream "
        "with the lid off and a small texture visible, a damp washcloth "
        "nearby, soft directional morning sunlight casting long natural "
        "shadows, realistic uneven arrangement, faint water droplets on the "
        "counter, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/hoe-vaak-wenkbrauwen-epileren.jpg",
        "Close side-profile photo of an eyebrow shaping treatment: tweezers "
        "held just above a client's brow by an out-of-focus hand in the "
        "foreground, focus on the natural brow hair and skin texture, "
        "client's eyes closed, soft diffused salon lighting, shot on a "
        "85mm macro lens with shallow depth of field, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/waxen-vs-scheren-vs-ipl.jpg",
        "Simple still life on a light oak table: a small stack of folded "
        "waffle-weave cotton towels, a wooden bowl with cotton pads, and an "
        "unlabeled amber oil bottle catching a sliver of window light, "
        "natural soft shadows, slightly imperfect casual arrangement, shot "
        "on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/paulas-choice-of-skeyndor.jpg",
        "Flatlay of a small skincare collection on a warm cream stone "
        "surface: two or three unlabeled frosted glass bottles of varying "
        "heights and a low ceramic jar, arranged with realistic uneven "
        "spacing (not symmetrical), soft raking window light creating long "
        "natural shadows, subtle dust visible in the light, shot on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/wat-helpt-tegen-pigmentvlekken.jpg",
        "Natural close-up portrait crop of a woman's cheek and jaw turned "
        "slightly away from camera, soft window light from one side, real "
        "visible skin texture with faint natural pigmentation and pores, "
        "a few loose flyaway hairs, shot on an 85mm portrait lens with "
        "shallow depth of field, background softly blurred, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/blog/generated/huidverzorging-winter-vs-zomer.jpg",
        "Cozy still life: an unlabeled matte ceramic cream jar with the lid "
        "resting beside it, sitting on a rumpled chunky knit blanket near a "
        "window, soft cool daylight mixed with a warm interior light source, "
        "realistic fabric texture and creases, shot on 35mm, "
        f"{ANTI_AI}",
    ),
    (
        "public/images/treatments/microdermabrasie.jpg",
        "Candid three-quarter angle photo in a boutique salon treatment "
        "room: an esthetician's gloved hand guiding a diamond-tip "
        "microdermabrasion device along a client's cheekbone, client "
        "reclined with eyes closed and a headband holding her hair back, "
        "soft window light from the side, realistic skin texture, shot on "
        "a 50mm lens with shallow depth of field, "
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
