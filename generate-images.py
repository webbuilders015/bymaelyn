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
import urllib.request

TOKEN = os.environ.get("REPLICATE_API_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else None)
if not TOKEN:
    print("Usage: REPLICATE_API_TOKEN=r8_xxx python3 generate-images.py")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = "black-forest-labs/flux-schnell"
API_URL = f"https://api.replicate.com/v1/models/{MODEL}/predictions"

STYLE = (
    "editorial beauty photography, soft natural light, warm neutral beige and "
    "cream tones, subtle gold accent details, minimal clean aesthetic, shallow "
    "depth of field, no visible text or logos, realistic photography style"
)

IMAGES = [
    (
        "public/images/blog/generated/huidverbeterende-gezichtsbehandeling-uitgelegd.jpg",
        f"Facial treatment in a boutique skincare salon, esthetician applying a "
        f"calming mask to a client's skin, {STYLE}",
    ),
    (
        "public/images/blog/generated/chemische-peeling-vs-microdermabrasie.jpg",
        f"Still life of two skincare treatment concepts side by side, glass "
        f"skincare bottles with completely blank unlabeled surfaces and a "
        f"diamond-tip microdermabrasion device on a marble surface, {STYLE}",
    ),
    (
        "public/images/blog/generated/skincare-routine-vanaf-je-dertigste.jpg",
        f"Elegant skincare routine flatlay, serums and moisturizer bottles with "
        f"completely blank unlabeled surfaces, arranged on a soft cream "
        f"surface, soft morning light, {STYLE}",
    ),
    (
        "public/images/blog/generated/hoe-vaak-wenkbrauwen-epileren.jpg",
        f"Close-up of eyebrow shaping treatment, tweezers and brow tools on a "
        f"clean white towel, minimal salon setting, {STYLE}",
    ),
    (
        "public/images/blog/generated/waxen-vs-scheren-vs-ipl.jpg",
        f"Still life representing smooth skin hair removal, soft cotton pads, "
        f"warm oil bottle and clean towel on a light beige surface, {STYLE}",
    ),
    (
        "public/images/blog/generated/paulas-choice-of-skeyndor.jpg",
        f"Flatlay of premium skincare bottles and jars with completely blank "
        f"unlabeled surfaces, neutral white and amber glass packaging, minimal "
        f"luxury skincare aesthetic, {STYLE}",
    ),
    (
        "public/images/blog/generated/wat-helpt-tegen-pigmentvlekken.jpg",
        f"Close-up beauty photography of glowing even skin texture, soft focus, "
        f"gold accent light reflection, {STYLE}",
    ),
    (
        "public/images/blog/generated/huidverzorging-winter-vs-zomer.jpg",
        f"Split-mood still life representing seasonal skincare, on one side a "
        f"warm cozy knit texture and rich cream jar with a completely blank "
        f"unlabeled surface, on the other soft daylight and a light serum "
        f"bottle with a completely blank unlabeled surface, {STYLE}",
    ),
    (
        "public/images/treatments/microdermabrasie.jpg",
        f"Microdermabrasion facial treatment, esthetician using a diamond-tip "
        f"device on a client's cheek in a clean boutique salon, {STYLE}",
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

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.load(resp)

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
        time.sleep(1)

    print("Done. Let Claude know the images are in place so it can wire them into the site.")


if __name__ == "__main__":
    main()
