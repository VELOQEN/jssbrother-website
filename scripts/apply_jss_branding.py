from pathlib import Path
from PIL import Image, ImageOps
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

config = json.loads(
    (ROOT / "branding.json").read_text(encoding="utf-8")
)

SOURCE = ROOT / config["source_root"]
OUTPUT = ROOT / config["output_root"]
TEMPLATE = ROOT / config["template"]

extensions = {
    x.lower() for x in config["supported_extensions"]
}

skip = [
    Path(x).as_posix().lower().rstrip("/")
    for x in config.get("skip_watermark", [])
]

if not TEMPLATE.exists():
    raise SystemExit(
        f"ERROR: watermark template missing:\n{TEMPLATE}"
    )

overlay_original = Image.open(TEMPLATE).convert("RGBA")

processed = 0
copied = 0
failed = 0

for source in SOURCE.rglob("*"):

    if not source.is_file():
        continue

    if source.suffix.lower() not in extensions:
        continue

    rel = source.relative_to(SOURCE)
    rel_posix = rel.as_posix()
    rel_lower = rel_posix.lower()

    destination = OUTPUT / rel
    destination.parent.mkdir(parents=True, exist_ok=True)

    should_skip = any(
        rel_lower == prefix or
        rel_lower.startswith(prefix + "/")
        for prefix in skip
    )

    try:
        if should_skip:
            shutil.copy2(source, destination)
            copied += 1
            print(f"COPY EXISTING BRANDING: {rel_posix}")
            continue

        base = Image.open(source).convert("RGBA")

        # Resize the approved watermark template proportionally
        # and crop it to the exact product image dimensions.
        overlay = ImageOps.fit(
            overlay_original,
            base.size,
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )

        result = Image.alpha_composite(base, overlay)

        ext = source.suffix.lower()

        if ext == ".webp":
            result.save(
                destination,
                "WEBP",
                quality=94,
                method=6
            )

        elif ext in (".jpg", ".jpeg"):
            result.convert("RGB").save(
                destination,
                "JPEG",
                quality=95,
                optimize=True
            )

        else:
            result.save(
                destination,
                "PNG",
                optimize=True
            )

        processed += 1
        print(f"WATERMARKED: {rel_posix}")

    except Exception as e:
        failed += 1
        print(f"FAILED: {rel_posix}: {e}")

print()
print("==========================================")
print("JSS PRODUCT BRANDING COMPLETE")
print("==========================================")
print(f"Watermarked: {processed}")
print(f"Already-branded copied: {copied}")
print(f"Failed: {failed}")
print(f"Output: {OUTPUT}")
