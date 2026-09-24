from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def exists(path):
    return (ROOT / path.lstrip("/")).exists()

def image_card(name, image, type_name):
    slug = slugify(name)
    return f"""
      <a class="product-card" href="./{slug}/">
        <div class="product-image">
          <img src="/{escape(image)}" alt="{escape(name)} - JSS Brothers" loading="lazy">
        </div>
        <div class="product-info">
          <small>{escape(type_name)}</small>
          <strong>{escape(name)}</strong>
        </div>
      </a>
    """

def plain_card(name, image, type_name):
    return f"""
      <div class="product-card">
        <div class="product-image">
          <img src="/{escape(image)}" alt="{escape(name)} - JSS Brothers" loading="lazy">
        </div>
        <div class="product-info">
          <small>{escape(type_name)}</small>
          <strong>{escape(name)}</strong>
        </div>
      </div>
    """

BASE_STYLE = """
:root{
  --ink:#0d2530;
  --muted:#64757c;
  --line:#dfe7e9;
  --paper:#f7f9f8;
  --white:#fff;
  --accent:#005f73;
}
*{box-sizing:border-box}
body{
  margin:0;
  font-family:Arial,Helvetica,sans-serif;
  background:var(--paper);
  color:var(--ink);
}
.topbar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:20px;
  padding:22px 5vw;
  background:#fff;
  border-bottom:1px solid var(--line);
  position:sticky;
  top:0;
  z-index:10;
}
.brand{
  font-weight:900;
  letter-spacing:.12em;
  text-decoration:none;
  color:var(--ink);
}
.back{
  text-decoration:none;
  color:var(--accent);
  font-weight:700;
}
.hero{
  padding:72px 5vw 42px;
  max-width:1450px;
  margin:auto;
}
.kicker{
  color:var(--accent);
  font-size:12px;
  font-weight:800;
  letter-spacing:.18em;
  text-transform:uppercase;
}
h1{
  font-size:clamp(42px,7vw,92px);
  line-height:.92;
  margin:14px 0 20px;
  letter-spacing:-.05em;
}
.hero p{
  max-width:720px;
  font-size:18px;
  line-height:1.65;
  color:var(--muted);
}
.grid{
  max-width:1450px;
  margin:auto;
  padding:12px 5vw 80px;
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  gap:22px;
}
.product-card{
  text-decoration:none;
  color:inherit;
  background:#fff;
  border:1px solid var(--line);
  border-radius:18px;
  overflow:hidden;
  transition:transform .18s ease,box-shadow .18s ease;
}
a.product-card:hover{
  transform:translateY(-4px);
  box-shadow:0 14px 36px rgba(15,40,50,.10);
}
.product-image{
  aspect-ratio:4/3;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#eef2f2;
  overflow:hidden;
}
.product-image img{
  width:100%;
  height:100%;
  object-fit:cover;
}
.product-info{
  padding:18px 18px 20px;
}
.product-info small{
  display:block;
  color:var(--accent);
  font-weight:800;
  letter-spacing:.12em;
  margin-bottom:7px;
  text-transform:uppercase;
}
.product-info strong{
  font-size:18px;
}
.coming{
  max-width:1450px;
  margin:auto;
  padding:20px 5vw 100px;
}
.coming-box{
  min-height:330px;
  background:#fff;
  border:1px solid var(--line);
  border-radius:24px;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:40px;
}
.coming-box strong{
  font-size:36px;
  margin-bottom:12px;
}
.coming-box p{
  color:var(--muted);
  max-width:560px;
  line-height:1.6;
}
footer{
  border-top:1px solid var(--line);
  padding:30px 5vw;
  color:var(--muted);
  background:#fff;
}
@media(max-width:1050px){
  .grid{grid-template-columns:repeat(3,minmax(0,1fr))}
}
@media(max-width:760px){
  .grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
  .hero{padding-top:50px}
}
@media(max-width:520px){
  .grid{grid-template-columns:1fr}
}
"""

def page_html(title, kicker, description, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | JSS Brothers</title>
<style>{BASE_STYLE}</style>
</head>
<body>
<header class="topbar">
  <a class="brand" href="/">JSS BROTHERS</a>
  <a class="back" href="/#catalogue">← Back to catalogue</a>
</header>

<section class="hero">
  <div class="kicker">{escape(kicker)}</div>
  <h1>{escape(title)}</h1>
  <p>{escape(description)}</p>
</section>

{body}

<footer>
  © 2026 JSS Brothers · Since 2010 · 17 Years
</footer>

<script src="/branding-loader.js?v=1"></script>
</body>
</html>
"""

def product_page(title, type_name, image, family_url):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | JSS Brothers</title>
<style>
{BASE_STYLE}
.detail{{
  max-width:1200px;
  margin:auto;
  padding:55px 5vw 100px;
  display:grid;
  grid-template-columns:1.15fr .85fr;
  gap:50px;
  align-items:center;
}}
.detail img{{
  width:100%;
  border-radius:22px;
  border:1px solid var(--line);
  background:#fff;
}}
.detail h1{{font-size:clamp(42px,6vw,76px)}}
.detail p{{color:var(--muted);line-height:1.7}}
@media(max-width:800px){{
  .detail{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<header class="topbar">
  <a class="brand" href="/">JSS BROTHERS</a>
  <a class="back" href="{family_url}">← Back</a>
</header>
<section class="detail">
  <div><img src="/{escape(image)}" alt="{escape(title)} - JSS Brothers"></div>
  <div>
    <div class="kicker">{escape(type_name)}</div>
    <h1>{escape(title)}</h1>
    <p>Available from JSS Brothers. Contact one of our branches for availability, pricing and further product information.</p>
  </div>
</section>
<footer>© 2026 JSS Brothers · Since 2010 · 17 Years</footer>
<script src="/branding-loader.js?v=1"></script>
</body>
</html>
"""

catalogues = {
    "shamuk": {
        "title":"Shamuk Metallic Yarn",
        "kicker":"SHAMUK",
        "description":"Explore Shamuk Metallic Yarn / Tilla shades available from JSS Brothers.",
        "type":"Metallic Yarn / Tilla",
        "items":[
            ("1509 Copper","images/products/metallic-yarn/shamuk/1509-copper.webp"),
            ("Champion","images/products/metallic-yarn/shamuk/champion.webp"),
            ("Copper Zebra","images/products/metallic-yarn/shamuk/copper-zebra.webp"),
            ("Light Copper","images/products/metallic-yarn/shamuk/light-copper.webp"),
            ("LL Copper","images/products/metallic-yarn/shamuk/ll-copper.webp"),
        ]
    },

    "bobbin": {
        "title":"Bobin",
        "kicker":"BOBIN",
        "description":"White and colored Bobin products available from JSS Brothers.",
        "type":"Bobin",
        "items":[]
    },

    "needles": {
        "title":"Needles",
        "kicker":"NEEDLES",
        "description":"Embroidery machine needles available from JSS Brothers.",
        "type":"Needles",
        "items":[
            ("Orange Needle #11","images/products/needles/orange-11.png"),
            ("Orange Needle #14","images/products/needles/orange-14.png"),
            ("Groz-Beckert #14","images/products/needles/groz-beckert-14.png"),
        ]
    },

    "panni": {
        "title":"Panni",
        "kicker":"PANNI",
        "description":"Available Panni finishes and colours from JSS Brothers.",
        "type":"Panni",
        "items":[
            ("Light Golden","images/products/panni/light-golden-panni.webp"),
            ("Dark Golden","images/products/panni/dark-golden-panni.webp"),
            ("Silver","images/products/panni/silver-panni.webp"),
        ]
    },

    "spare-parts": {
        "title":"Spare Parts",
        "kicker":"SPARE PARTS",
        "description":"Machinery-use essentials, sprays and White Oil supplied by JSS Brothers.",
        "type":"Spare Parts",
        "items":[
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

# Bobin: exact three white products + all current 30PP shades.
bobin_items = [
    ("30 PP Small","images/products/bobbin/white/30pp-small.png"),
    ("30 PP Big","images/products/bobbin/white/30pp-big.png"),
    ("20 PP Big","images/products/bobbin/white/20pp-big.png"),
]

bobin_dir = ROOT / "images/products/bobbin/30pp"
if bobin_dir.exists():
    for f in sorted(bobin_dir.glob("*.webp")):
        if f.stem.lower() == "cover":
            continue
        bobin_items.append(
            (f"30PP {f.stem}", f"images/products/bobbin/30pp/{f.name}")
        )

catalogues["bobbin"]["items"] = bobin_items

coming_soon = {
    "stylo":("Stylo Metallic Yarn","STYLO","Stylo Metallic Yarn catalogue is being prepared."),
    "markfil":("Markfil Metallic Yarn","MARKFIL","Markfil Metallic Yarn catalogue is being prepared."),
    "solving":("Solving","SOLVING","Solving product information and images are being added."),
    "dissolving":("Dissolving","DISSOLVING","Dissolving product information and images are being added."),
    "sequence":("Sequence / CD","SEQUENCE / CD","The updated Sequence / CD catalogue is being prepared."),
    "polyester":("Polyester","POLYESTER","Polyester shades and product images are being added."),
    "fusing":("Fusing","FUSING","Fusing specifications and product images are being added."),
    "nylon":("Nylon","NYLON","Nylon product information and images are being added."),
}

for slug, data in catalogues.items():
    folder = PRODUCTS / slug
    folder.mkdir(parents=True, exist_ok=True)

    cards = []
    for name, image in data["items"]:
        if not exists(image):
            print(f"WARNING missing image: {image}")
            continue

        product_slug = slugify(name)
        product_folder = folder / product_slug
        product_folder.mkdir(parents=True, exist_ok=True)

        # Do not overwrite existing hand-built product pages.
        detail_file = product_folder / "index.html"
        if not detail_file.exists():
            detail_file.write_text(
                product_page(
                    name,
                    data["type"],
                    image,
                    f"/products/{slug}/"
                ),
                encoding="utf-8"
            )

        cards.append(image_card(name, image, data["type"]))

    body = '<main class="grid">' + "".join(cards) + "</main>"

    target = folder / "index.html"

    # Colored is the approved master and Crystal may already be hand-built.
    # Never overwrite them here.
    if slug not in ("colored","crystal"):
        target.write_text(
            page_html(
                data["title"],
                data["kicker"],
                data["description"],
                body
            ),
            encoding="utf-8"
        )

for slug,(title,kicker,desc) in coming_soon.items():
    folder = PRODUCTS / slug
    folder.mkdir(parents=True, exist_ok=True)

    body = """
<main class="coming">
  <div class="coming-box">
    <strong>Coming Soon</strong>
    <p>Products and specifications are currently being added to this catalogue.</p>
  </div>
</main>
"""

    (folder / "index.html").write_text(
        page_html(title,kicker,desc,body),
        encoding="utf-8"
    )

print("✓ Separate catalogue pages generated")
print("✓ Existing Colored page preserved")
print("✓ Existing Crystal page preserved")
print("✓ Existing product originals preserved")
