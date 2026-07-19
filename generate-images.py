#!/usr/bin/env python3
"""
Generates the blog + treatment images via Replicate (Flux) and saves them
straight into the project's public/images folder.

Usage:
    REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py
or:
    python3 generate-images.py r8_xxx
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ.get("REPLICATE_API_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else None)
if not TOKEN:
    print("Usage: REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# nano-banana (Google) tends to render more photorealistic, less "AI glossy" results.
MODEL = "google/nano-banana"
API_URL = f"https://api.replicate.com/v1/models/{MODEL}/predictions"

STYLE = (
    "candid documentary-style photograph, shot on a Canon EOS R5 with an 85mm "
    "f/1.4 lens, natural soft window light, real skin texture with visible "
    "pores and fine detail, unretouched, warm neutral beige and cream color "
    "grade, subtle gold accent details, shallow depth of field, film-like "
    "grain, photojournalistic, not airbrushed, not smoothed, not CGI, not "
    "3D render, not digital illustration, not plastic looking, no visible "
    "text, no logos, no readable labels, ultra realistic"
)

IMAGES = [
    (
        "public/images/blog/generated/huidverbeterende-gezichtsbehandeling-uitgelegd.jpg",
        f"A real esthetician's hands applying a clay facial mask to a client "
        f"lying back in a boutique skincare salon chair, {STYLE}",
    ),
    (
        "public/images/blog/generated/chemische-peeling-vs-microdermabrasie.jpg",
        f"Still life of two skincare treatment concepts side by side, glass "
        f"skincare bottles with completely blank unlabeled surfaces and a "
        f"diamond-tip microdermabrasion device on a marble surface, {STYLE}",
    ),
    (
        "public/images/blog/generated/skincare-routine-vanaf-je-dertigste.jpg",
        f"Skincare routine flatlay, serums and moisturizer bottles with "
        f"completely blank unlabeled surfaces, arranged on a soft cream "
        f"surface, soft morning light, {STYLE}",
    ),
    (
        "public/images/blog/generated/hoe-vaak-wenkbrauwen-epileren.jpg",
        f"Close-up of a real eyebrow shaping treatment in progress, tweezers "
        f"held near a client's brow, clean white towel beneath, minimal salon "
        f"setting, {STYLE}",
    ),
    (
        "public/images/blog/generated/waxen-vs-scheren-vs-ipl.jpg",
        f"Still life representing smooth skin hair removal, soft cotton pads, "
        f"a warm oil bottle with a completely blank unlabeled surface, and a "
        f"clean folded towel on a light beige surface, {STYLE}",
    ),
    (
        "public/images/blog/generated/paulas-choice-of-skeyndor.jpg",
        f"Flatlay of premium skincare bottles and jars with completely blank "
        f"unlabeled surfaces, neutral white and amber glass packaging, minimal "
        f"luxury skincare aesthetic, {STYLE}",
    ),
    (
        "public/images/blog/generated/wat-helpt-tegen-pigmentvlekken.jpg",
        f"Extreme close-up of real human skin on a cheek, natural texture, "
        f"visible pores, even glowing tone, soft focus background, gold "
        f"accent light reflection, {STYLE}",
    ),
    (
        "public/images/blog/generated/huidverzorging-winter-vs-zomer.jpg",
        f"Still life of a rich cream jar with a completely blank unlabeled "
        f"surface nestled in a warm cozy knit blanket, soft directional "
        f"sunlight, {STYLE}",
    ),
    (
        "public/images/treatments/microdermabrasie.jpg",
        f"A real esthetician wearing gloves using a diamond-tip "
        f"microdermabrasion device on a client's cheek, client lying back "
        f"eyes closed in a clean boutique salon, {STYLE}",
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
        if os.path.exists(full_path):
            print(f"Skipping {rel_path} (already exists)")
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
