from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"

colored_file = PRODUCTS / "colored" / "index.html"

if not colored_file.exists():
    raise SystemExit("ERROR: approved Colored page not found")

colored_html = colored_file.read_text(encoding="utf-8")

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def cards_html(items, kicker, type_name, family_slug):
    blocks = []

    for i, (name, image) in enumerate(items, 1):
        slug = slugify(name)

        blocks.append(f"""
        <a class="crystal-card" href="/products/{family_slug}/{slug}/">
          <div class="crystal-image">
            <img
              src="/{escape(image)}"
              alt="{escape(name)} {escape(type_name)} - JSS Brothers"
              loading="lazy"
              decoding="async"
            >
          </div>

          <div class="crystal-info">
            <small>{escape(kicker)} • {i:02d}</small>
            <strong>{escape(name)}</strong>
            <span>{escape(type_name)}</span>
          </div>
        </a>
        """)

    return "\n".join(blocks)

def extract_colored_grid_template(html):
    m = re.search(
        r'(<div[^>]+class=["\'][^"\']*crystal-grid[^"\']*["\'][^>]*>).*?(</div>\s*</main>|</div>\s*</section>|</div>\s*</body>)',
        html,
        flags=re.S|re.I
    )

    if not m:
        return None

    return m.group(1)

def replace_text(html, old, new):
    return html.replace(old, new)

def build_from_colored(title, description, kicker, type_name, family_slug, items):
    html = colored_html

    # Title / SEO
    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{escape(title)} | JSS Brothers</title>',
        html,
        count=1,
        flags=re.S|re.I
    )

    # Main heading
    html = re.sub(
        r'<h1[^>]*>.*?</h1>',
        f'<h1>{escape(title)}</h1>',
        html,
        count=1,
        flags=re.S|re.I
    )

    # Kicker
    html = re.sub(
        r'(<div[^>]+class=["\'][^"\']*(?:eyebrow|kicker)[^"\']*["\'][^>]*>).*?(</div>)',
        rf'\1{escape(type_name.upper())}\2',
        html,
        count=1,
        flags=re.S|re.I
    )

    # Description directly under hero title
    # This targets the first paragraph after h1.
    html = re.sub(
        r'(<h1[^>]*>.*?</h1>\s*<p[^>]*>).*?(</p>)',
        rf'\1{escape(description)}\2',
        html,
        count=1,
        flags=re.S|re.I
    )

    # Back button should always return to materials/catalogue
    html = re.sub(
        r'href=["\'][^"\']*["\']([^>]*>\s*←\s*Back to Materials\s*</a>)',
        r'href="/#catalogue"\1',
        html,
        count=1,
        flags=re.I
    )

    # Replace all existing product cards in the approved grid.
    grid_match = re.search(
        r'(<div[^>]+class=["\'][^"\']*crystal-grid[^"\']*["\'][^>]*>)(.*?)(</div>\s*(?:</main>|</section>))',
        html,
        flags=re.S|re.I
    )

    if not grid_match:
        raise RuntimeError("Could not locate product grid inside Colored master page")

    new_grid = (
        grid_match.group(1)
        + "\n"
        + cards_html(items, kicker, type_name, family_slug)
        + "\n"
        + grid_match.group(3)
    )

    html = html[:grid_match.start()] + new_grid + html[grid_match.end():]

    return html


families = {
    "crystal": {
        "title": "Crystal Metallic Yarn",
        "description": "Explore the available Crystal Metallic Yarn shades supplied by JSS Brothers.",
        "kicker": "CRYSTAL",
        "type": "Metallic Yarn / Tilla",
        "items": [
            ("1128 Zebra","images/products/metallic-yarn/crystal/1128 zebra crystal.webp"),
            ("1502 Silver","images/products/metallic-yarn/crystal/1502 SILVER CRYSTAL.webp"),
            ("1507 Copper","images/products/metallic-yarn/crystal/1507 COPPER CRYSTAL.webp"),
            ("1552","images/products/metallic-yarn/crystal/1552 CRYSTAL.webp"),
            ("15583","images/products/metallic-yarn/crystal/15583 CRYSTAL.webp"),
            ("7275","images/products/metallic-yarn/crystal/7275 CRYSTAL.webp"),
            ("Black","images/products/metallic-yarn/crystal/BLACK CRYSTAL.webp"),
            ("Copper Zebra","images/products/metallic-yarn/crystal/COPPER ZEBRA CRYSTAL.webp"),
            ("D7272","images/products/metallic-yarn/crystal/D7272 CRYSTAL.webp"),
            ("Fake Silver","images/products/metallic-yarn/crystal/FAKE SILVER CRYSTAL.webp"),
            ("Indian Gold","images/products/metallic-yarn/crystal/INDIAN GOLD CRYSTAL.webp"),
            ("KR Gold","images/products/metallic-yarn/crystal/KR GOLD CRYSTAL.webp"),
            ("MB Zebra","images/products/metallic-yarn/crystal/MB ZEBRA CRYSTAL.webp"),
            ("Pure Silver","images/products/metallic-yarn/crystal/PURE SILVER CRYSTAL.webp"),
            ("Silver Zebra","images/products/metallic-yarn/crystal/SILVER ZEBRA CRYSTAL.webp"),
            ("Sona Gold","images/products/metallic-yarn/crystal/SONA GOLD CRYSTAL.webp"),
            ("Tobacco","images/products/metallic-yarn/crystal/TOBACCO CRYSTAL.webp"),
            ("White Gold","images/products/metallic-yarn/crystal/WHITE GOLD CRYSTAL.webp"),
            ("Champion","images/products/metallic-yarn/crystal/champion crystal.webp"),
            ("Crystal White Gold","images/products/metallic-yarn/crystal/crystal white gold.webp"),
            ("L5000","images/products/metallic-yarn/crystal/l 5000 crystal.webp"),
            ("LL Copper","images/products/metallic-yarn/crystal/ll copper crystal.webp"),
        ]
    },

    "shamuk": {
        "title": "Shamuk Metallic Yarn",
        "description": "Explore the available Shamuk Metallic Yarn shades supplied by JSS Brothers.",
        "kicker": "SHAMUK",
        "type": "Metallic Yarn / Tilla",
        "items": [
            ("1509 Copper","images/products/metallic-yarn/shamuk/1509-copper.webp"),
            ("Champion","images/products/metallic-yarn/shamuk/champion.webp"),
            ("Copper Zebra","images/products/metallic-yarn/shamuk/copper-zebra.webp"),
            ("Light Copper","images/products/metallic-yarn/shamuk/light-copper.webp"),
            ("LL Copper","images/products/metallic-yarn/shamuk/ll-copper.webp"),
        ]
    },

    "needles": {
        "title": "Needles",
        "description": "Explore embroidery machine needles supplied by JSS Brothers.",
        "kicker": "NEEDLES",
        "type": "Embroidery Needles",
        "items": [
            ("Orange Needle #11","images/products/needles/orange-11.png"),
            ("Orange Needle #14","images/products/needles/orange-14.png"),
            ("Groz-Beckert #14","images/products/needles/groz-beckert-14.png"),
        ]
    },

    "panni": {
        "title": "Panni",
        "description": "Explore available Panni colours supplied by JSS Brothers.",
        "kicker": "PANNI",
        "type": "Panni",
        "items": [
            ("Dark Golden","images/products/panni/dark-golden-panni.webp"),
            ("Light Golden","images/products/panni/light-golden-panni.webp"),
            ("Silver","images/products/panni/silver-panni.webp"),
        ]
    },

    "spare-parts": {
        "title": "Spare Parts",
        "description": "Explore sprays, White Oil and machinery-use essentials supplied by JSS Brothers.",
        "kicker": "SPARE PARTS",
        "type": "Machinery Essentials",
        "items": [
            ("Spot Lifter 69","images/products/spare-parts/spot-lifter-blue-69.webp"),
            ("Spot Lifter 68","images/products/spare-parts/spot-lifter-green-68.webp"),
            ("W100","images/products/spare-parts/w100-spray.webp"),
            ("WARCO","images/products/spare-parts/warco-spray.webp"),
            ("WD40","images/products/spare-parts/wd40-spray.webp"),
            ("White Oil Bottle","images/products/spare-parts/white-oil-bottle.webp"),
            ("White Oil Can","images/products/spare-parts/white-oil-can.webp"),
        ]
    }
}

# Bobin dynamically includes all 30PP shades
bobbin_items = [
    ("30 PP Small","images/products/bobbin/white/30pp-small.png"),
    ("30 PP Big","images/products/bobbin/white/30pp-big.png"),
    ("20 PP Big","images/products/bobbin/white/20pp-big.png"),
]

for f in sorted((ROOT / "images/products/bobbin/30pp").glob("*.webp")):
    if f.stem.lower() == "cover":
        continue
    bobbin_items.append(
        (f"30PP {f.stem}", f"images/products/bobbin/30pp/{f.name}")
    )

families["bobbin"] = {
    "title": "Bobin",
    "description": "Explore White Bobin and Colored 30PP Bobin shades supplied by JSS Brothers.",
    "kicker": "BOBIN",
    "type": "Bobin",
    "items": bobbin_items
}

for slug, cfg in families.items():
    target = PRODUCTS / slug / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)

    html = build_from_colored(
        cfg["title"],
        cfg["description"],
        cfg["kicker"],
        cfg["type"],
        slug,
        cfg["items"]
    )

    target.write_text(html, encoding="utf-8")
    print(f"✓ Rebuilt /products/{slug}/ using Colored layout")

print()
print("DONE")
