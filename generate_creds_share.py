"""
Generates a client-facing Creds page as a plain, static, standalone HTML document, meant to be
run inside a GitHub Actions workflow (see .github/workflows/publish-share.yml) and published via
GitHub Pages -- this is the CI-facing counterpart of the version that runs inside a Claude
conversation. No window.claude / Claude Artifact capabilities are used or needed here.

Usage (from repo root):
    python3 generate_creds_share.py --name "Client Name" --ids "ihg,reddit,meta" --out docs/client-slug/index.html
"""
import json, base64, io, argparse, re, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(HERE, "assets.json")


def slugify(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return s or 'set'


with open(ASSETS_PATH) as f:
    A = json.load(f)


def img_ratio(data_uri):
    raw = base64.b64decode(data_uri.split(",", 1)[1])
    im = Image.open(io.BytesIO(raw))
    return round(im.width / im.height, 4)


def photo(id, key):
    return {"id": id, "url": A[key], "ratio": img_ratio(A[key])}


NOTHING_PHOTOS = [photo("n_hero", "n_hero")] + [photo("n_%02d" % i, "n_%02d" % i) for i in range(1, 32)]
AUDI_PHOTOS = [photo("audi_%d" % i, "audi_e%02d" % i) for i in range(1, 26)]
IHG_PHOTOS = [photo("ihg_%d" % i, "ihg_e%02d" % i) for i in range(1, 30)]
REDDIT_PHOTOS = [photo("reddit_%d" % i, "reddit_e%02d" % i) for i in range(1, 15)]
META_PHOTOS = [photo("meta_%d" % i, "meta_e%02d" % i) for i in range(1, 18)]
NETFLIX_PHOTOS = [photo("netflix_%d" % i, "netflix_e%02d" % i) for i in range(1, 9)]

# Same catalog as the Work Library (generate_unified.py) -- kept in sync by hand. Real content
# only, verified against wearefamilylondon.com project pages and the recovered master-deck images.
PROJECTS = [
    {
        "id": "nothing", "client": "Nothing",
        "title": "House of Nothing — Phone (3) & Headphones (1) Launch",
        "sector": "Technology", "type": "Product Launch", "year": 2025, "region": "London",
        "photos": NOTHING_PHOTOS,
        "tags": ["Experiential Activation", "Set Design & Build", "Content Creation", "Talent & Entertainment"],
        "challenge": "Create a global launch that delivers at the intersection of technology and style. Launch two new products — Phone (3) and Headphones (1) — to 300 journalists from around the world by day, then 1,000 guests by night. The goal: make tech fun again.",
        "experience": "“House of Nothing” ran as two connected events. By day, an immersive entrance and kinesis rigging let the products literally drop into the room. By night, the space split into two rooms built around different sides of Nothing's personality, anchored by a 20-metre bespoke pétanque court, plus photobooths, a DJ record table, a zoom lab and live performances from London artists — the whole thing livestreamed globally.",
        "impact": "The launch became a trending topic on Instagram, exceeded expected influencer engagement, drew thousands to the livestream and held press coverage in the days that followed — smashing brand awareness and trust goals, particularly in the UK.",
        "stats": [
            ("20.5k", "Concurrent livestream views"),
            ("234k", "Total livestream views, 24hrs"),
            ("32.7k", "nothing.tech DTC sessions during livestream"),
            ("2,440", "Traditional articles, 24hrs post-embargo"),
        ],
        "press": ["CNET", "Wallpaper*", "9to5Google", "Cybernews"],
        "quote": "", "quote_by": "",
    },
    {
        "id": "audi", "client": "Audi", "title": "Audi | Wilderness",
        "sector": "Automotive", "type": "Festival Brand Activation", "year": 2024, "region": "Oxfordshire",
        "photos": AUDI_PHOTOS,
        "tags": ["Event Production", "Set Design & Build", "Talent & Speaker Management", "Creative Concepting"],
        "challenge": "Create a distinctive 100-person lounge and dining activation for Audi's debut as headline sponsor at Wilderness Festival — enhancing product perception and connecting with target audiences through a cultural experience, not just a campaign.",
        "experience": "The Audi Haven deconstructed the Audi Q6 e-tron's design language, weaving in the animal motifs — moths, owls, fish — from the wider campaign, with interior curves that mirrored the car's sleek aesthetic. The space offered crafts, face painting, interactive AR filters and signature cocktails by day, with dining curated by Michelin-starred Chef Rohit Ghai, building to the Audi Wonder Parade and DJ performances after dark.",
        "impact": "The activation received high praise for its sophisticated blend of luxury and interactive elements, driving significant engagement and enhancing Audi's brand perception at the festival.",
        "stats": [("100", "Guest capacity, Audi Haven lounge & dining")],
        "press": [],
        "quote": "The activation perfectly captured the festival's spirit, driving significant engagement and enhancing Audi's brand perception.",
        "quote_by": "Client feedback",
    },
    {
        "id": "reddit", "client": "Reddit", "title": "Cannes Executive Dinner",
        "sector": "Technology", "type": "Executive Dinner", "year": 2025, "region": "Cannes",
        "photos": REDDIT_PHOTOS,
        "tags": ["Experiential Activation", "Creative Concepting", "Talent & Speaker Management", "Set Design & Build"],
        "challenge": "Create an elevated, immersive experience at the Cannes Lions Festival of Creativity that put Reddit's authentic, community-driven conversation at the centre of the room — manifesting what makes Reddit distinct as a platform where real dialogue shapes culture and inspires bold thinking.",
        "experience": "Conversation-starters were woven into seating, content, entertainment and design at Villa Belle Plage. The evening introduced Reddit's new ‘Community Intelligence’ product by demonstrating its real-world value — how community conversations reveal insight and creative potential for agencies — closing with intimate performances from Rick Astley and James Blake under the night sky.",
        "impact": "An intimate gathering that fostered meaningful, net-new relationships with senior agency leadership.",
        "stats": [], "press": [],
        "quote": "Every detail was beautifully thought through and flawlessly executed.",
        "quote_by": "Client feedback",
    },
    {
        "id": "ihg", "client": "IHG Hotels & Resorts", "title": "IHG | Wilderness — English Eccentrics",
        "sector": "Hospitality", "type": "Festival Brand Activation", "year": 2025, "region": "Oxfordshire",
        "photos": IHG_PHOTOS,
        "tags": ["Experiential Activation", "Set Design & Build", "Creative Concepting", "Talent & Speaker Management"],
        "challenge": "Bring IHG's vision for a ‘Hotel in the Wild’ to life at festival scale — blending luxury with nature to elevate brand presence, drive One Rewards sign-ups and build masterbrand visibility.",
        "experience": "We designed a boutique camping experience inspired by the English countryside, using sustainable materials and whimsical, Wes Anderson-inspired styling: a ‘Forgot it? We've Got it!’ concierge service, vintage luggage trolleys, pamper parlours, in-tent welcome amenities, and a piano lounge with cocktails and live entertainment from beatboxers and roaming performers, framed by bronze lanterns and floral displays.",
        "impact": "The activation demonstrated IHG's innovative hospitality approach through creative execution, cementing it as a must-visit festival destination.",
        "stats": [("8bn", "Media impressions"), ("17.3m", "Social impressions")],
        "press": [],
        "quote": "", "quote_by": "",
    },
    {
        "id": "meta", "client": "Meta", "title": "Multi-Market Marketing Summit",
        "sector": "Technology", "type": "Summit / Conference", "year": 2025, "region": "London · Berlin · EMEA",
        "photos": META_PHOTOS,
        "tags": ["Event Production", "Content Creation", "Talent & Speaker Management", "Creative Concepting"],
        "challenge": "Meta engaged us to deliver its flagship Marketing Summit across the UK, Germany and online — a multi-market programme designed to showcase innovation, highlight the power of AI and creativity, and reinforce Meta's position as a trusted growth partner.",
        "experience": "We delivered a multi-format Summit programme across regions: in the UK, a two-day event at Meta's London headquarters combining an Executive Breakfast with a full Practitioner Summit; in Germany, a reimagined one-day Summit in Berlin adapting the global playbook into a distinctive local experience; and across EMEA, a large-scale online edition reaching practitioners at scale.",
        "impact": "A consistent Summit experience delivered across three formats and multiple markets, extending Meta's reach deep into its practitioner and agency community.",
        "stats": [("15k", "Practitioners reached, EMEA online edition"), ("2", "Days, UK Executive Breakfast + Practitioner Summit")],
        "press": [],
        "quote": "", "quote_by": "",
    },
    {
        "id": "netflix", "client": "Netflix", "title": "See What's Next",
        "sector": "Entertainment", "type": "Creator & Influencer Experience", "year": 2025, "region": "London",
        "photos": NETFLIX_PHOTOS,
        "tags": ["Experiential Activation", "Content Creation", "Set Design & Build", "Talent & Entertainment"],
        "challenge": "Host an exclusive event at Netflix HQ designed to engage the UK's top social creators and build relationships with potential social media partners through an inspiring evening of exclusive content and shareable experiences.",
        "experience": "‘See What's Next’ gave influencers first looks at upcoming Netflix titles while immersing them in interactive, themed entertainment — screenings, themed food and drink, and photo-ready moments built around the new slate, staged with live entertainment throughout the night.",
        "impact": "Over 130 influencers attended an unforgettable evening that reinforced Netflix as the number one entertainment brand.",
        "stats": [("130+", "Influencers in attendance")],
        "press": [],
        "quote": "", "quote_by": "",
    },
]
BY_ID = {p["id"]: p for p in PROJECTS}

# ---------- Tiling algorithm (ported/shared with the Work Library's JS version) ----------
_TEMPLATES = [
    [("tile--square", 1, 1), ("tile--portrait", 1, 1), ("tile--landscape", 1, 1)],
    [("tile--wide", 2, 1), ("tile--square", 1, 1)],
    [("tile--tall", 1, 2), ("tile--landscape", 1, 1), ("tile--portrait", 1, 1),
     ("tile--square", 1, 1), ("tile--landscape", 1, 1)],
]


def decompose_exact(n):
    for a in range(n // 5, -1, -1):
        rem1 = n - 5 * a
        for b in range(rem1 // 3, -1, -1):
            rem2 = rem1 - 3 * b
            if rem2 % 2 == 0:
                return a, b, rem2 // 2
    raise ValueError(f"no exact 5/3/2 decomposition for n={n}")


def assign_tiles(photos):
    portrait_q = [p for p in photos if p["ratio"] < 0.85]
    landscape_q = [p for p in photos if p["ratio"] > 1.3]
    square_q = [p for p in photos if 0.85 <= p["ratio"] <= 1.3]
    queues = {"tile--portrait": portrait_q, "tile--tall": portrait_q,
              "tile--landscape": landscape_q, "tile--wide": landscape_q,
              "tile--square": square_q}
    all_qs = [portrait_q, landscape_q, square_q]

    def take(tile_cls):
        for q in [queues[tile_cls]] + all_qs:
            if q:
                return q.pop(0)
        return None

    a5, b3, c2 = decompose_exact(len(photos))
    from collections import deque
    idx_by_size = {5: 2, 3: 0, 2: 1}
    buckets = {5: deque([5] * a5), 3: deque([3] * b3), 2: deque([2] * c2)}
    sizes_cycle = [s for s in (5, 3, 2) if buckets[s]]
    template_seq = []
    while any(buckets.values()):
        for s in list(sizes_cycle):
            if buckets[s]:
                buckets[s].popleft()
                template_seq.append(_TEMPLATES[idx_by_size[s]])
            else:
                sizes_cycle.remove(s)

    out = []
    for template in template_seq:
        for tile_cls, col, row in template:
            ph = take(tile_cls)
            out.append({**ph, "tile": tile_cls, "col": col, "row": row})
    return out


def split3(seq):
    n = len(seq)
    a = n // 3
    b = (n - a) // 2
    g1, g2, g3 = seq[:a], seq[a:a + b], seq[a + b:]
    return [g for g in (g1, g2, g3) if g]


def photo_groups(photos):
    return [assign_tiles(group) for group in split3(photos)]


def effective_photos(project):
    # CI build always uses the project's base photo list (no live "Manage Photos" edits --
    # those only exist in the Work Library artifact's own db, which this workflow has no
    # access to). Ask Claude to refresh this repo's PROJECTS data if photos change materially.
    base = project["photos"]
    return [{"id": p["id"], "url": p["url"], "ratio": p.get("ratio", 1), "x": 50, "y": 50} for p in base]


def render_creds(selected_ids, set_name):
    selected = [BY_ID[i] for i in selected_ids if i in BY_ID]
    total = len(selected)
    logo = A["logo"]

    def grid_html(photos, client, offset):
        cells = "".join(
            f'<article class="gallery-item {ph["tile"]}">'
            f'<img src="{ph["url"]}" style="object-position:{ph["x"]}% {ph["y"]}%" '
            f'alt="{client} — event photo {offset+j+1}" loading="lazy"></article>'
            for j, ph in enumerate(photos)
        )
        return f'<div class="gallery">{cells}</div>'

    sections_html = ""
    for i, p in enumerate(selected):
        num = str(i + 1).zfill(2)
        total_s = str(total).zfill(2)
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        quote_html = ""
        if p.get("quote"):
            quote_html = f'<div class="case-quote">“{p["quote"]}”<span>{p["quote_by"]}</span></div>'

        photos = effective_photos(p)
        parts = photo_groups(photos)
        stats_html = "".join(
            f'<div class="stat"><div class="stat-num">{val}</div><div class="stat-label">{label}</div></div>'
            for val, label in p["stats"]
        )
        press_html = " · ".join(p["press"])
        beats_all = [("The Challenge", p["challenge"]), ("The Experience", p["experience"]), ("The Impact", p["impact"])]
        beats = beats_all[:len(parts)]
        parts_html = ""
        offset = 0
        for (heading, copy), beat_photos in zip(beats, parts):
            extra = ""
            if heading == "The Impact" and (p["stats"] or p["press"]):
                stats_block = f'<div class="n-stats">{stats_html}</div>' if p["stats"] else ""
                press_block = f'<div class="n-press"><span>As featured in</span>{press_html}</div>' if p["press"] else ""
                extra = stats_block + press_block
            parts_html += f"""
      <div class="n-part">
        <div class="n-part-copy"><h3>{heading}</h3><p>{copy}</p>{extra}</div>
        {grid_html(beat_photos, p["client"], offset)}
      </div>"""
            offset += len(beat_photos)

        sections_html += f"""
    <section class="case" data-id="{p['id']}">
      <div class="case-eyebrow-row">
        <span class="case-num">{num} / {total_s}</span>
        <span class="case-client">{p['client']}</span>
      </div>
      <h2 class="case-title">{p['title']}</h2>
      <div class="case-meta-row">
        <div><b>Sector</b>{p['sector']}</div>
        <div><b>Event type</b>{p['type']}</div>
        <div><b>Year</b>{p['year']}</div>
        <div><b>Location</b>{p['region']}</div>
      </div>
      <div class="case-tags">{tags_html}</div>
      {parts_html}
      {quote_html}
    </section>
"""

    body = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Creds — Prepared by We Are Family London</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  :root{{
    --paper:#FAFAF8; --ink:#000000; --line:#E4E3DD; --line-strong:#CFCEC6; --muted:#6B6A64;
    --g1:#FFA05C; --g2:#FF015B; --g3:#FE730E; --g4:#F9B52E; --g5:#F5F248;
  }}
  *{{box-sizing:border-box;}}
  html,body{{background:var(--paper);}}
  body{{
    color:var(--ink); font-family:'Helvetica Neue',Helvetica,Arial,system-ui,-apple-system,sans-serif;
    margin:0; padding:0; min-height:100%; -webkit-font-smoothing:antialiased; letter-spacing:-0.01em;
  }}
  .wrap{{max-width:1040px;margin:0 auto;padding:0 24px;}}
  img{{display:block;width:100%;height:100%;object-fit:cover;}}
  a{{color:inherit;}} h1,h2,h3{{margin:0;}}
  .heading{{font-family:'DM Sans',system-ui,sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.01em;}}

  #app{{padding-bottom:80px;}}
  .cover{{padding:64px 0 52px;border-bottom:2px solid var(--ink);margin-bottom:80px;}}
  .cover img.logo{{height:24px;width:auto;display:block;margin-bottom:64px;object-fit:contain;}}
  .eyebrow{{font-family:'DM Sans',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;font-size:14px;color:var(--muted);}}
  .cover .eyebrow{{margin-bottom:20px;}}
  .cover h1{{font-size:47px;line-height:1.13;max-width:18ch;}}
  .cover p{{color:var(--muted);font-size:19.5px;max-width:75%;margin:18px 0 0;line-height:1.55;}}
  .cover .dots{{display:flex;gap:5px;margin-top:30px;}}
  .cover .dots span{{width:9px;height:9px;border-radius:50%;}}

  section.case{{margin-bottom:104px;}}
  .case-eyebrow-row{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:20px;}}
  .case-num{{font-family:'DM Sans',sans-serif;font-weight:700;font-size:14px;letter-spacing:0.09em;color:var(--muted);}}
  .case-client{{font-family:'DM Sans',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;font-size:14px;color:var(--muted);}}

  .case-title{{font-family:'DM Sans',sans-serif;font-weight:700;text-transform:uppercase;font-size:39px;line-height:1.18;max-width:22ch;margin-bottom:32px;}}

  .case-meta-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:22px 0;margin-bottom:36px;}}
  .case-meta-row div{{font-size:17.5px;}}
  .case-meta-row b{{display:block;font-family:'DM Sans',sans-serif;font-weight:700;text-transform:uppercase;font-size:13px;letter-spacing:0.07em;color:var(--muted);margin-bottom:4px;}}

  .n-part{{margin-bottom:76px;}}
  .n-part-copy{{margin-bottom:32px;max-width:75%;}}
  .n-part-copy h3{{font-size:14px;text-transform:uppercase;letter-spacing:0.09em;color:var(--muted);margin-bottom:16px;font-family:'DM Sans',sans-serif;font-weight:700;}}
  .n-part-copy p{{margin:0;font-size:19px;line-height:1.55;}}

  .gallery{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-auto-rows:minmax(120px,auto);gap:5px;align-items:stretch;justify-items:stretch;}}
  .gallery-item{{position:relative;min-width:0;overflow:hidden;background:#eee;}}
  .gallery-item img{{width:100%;height:100%;display:block;object-fit:cover;}}
  .gallery-item.tile--square{{aspect-ratio:1/1;}}
  .gallery-item.tile--portrait{{aspect-ratio:3/4;}}
  .gallery-item.tile--landscape{{aspect-ratio:4/3;}}
  .gallery-item.tile--wide{{grid-column:span 2;aspect-ratio:16/9;}}
  .gallery-item.tile--tall{{grid-row:span 2;min-height:100%;}}

  .n-stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;border-top:1px solid var(--line);padding-top:26px;margin:32px 0 22px;}}
  .stat-num{{font-family:'DM Sans',sans-serif;font-weight:900;font-size:31px;line-height:1;margin-bottom:5px;}}
  .stat-label{{font-size:15px;color:var(--muted);line-height:1.4;}}

  .n-press{{font-size:16px;color:var(--muted);display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;margin-top:6px;}}
  .n-press span{{font-family:'DM Sans',sans-serif;font-weight:700;text-transform:uppercase;font-size:14px;letter-spacing:0.07em;color:var(--ink);margin-right:4px;}}

  .case-tags{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:40px;}}
  .tag{{font-size:14px;color:var(--muted);border:1px solid var(--line);padding:4px 10px;border-radius:3px;font-family:'DM Sans',sans-serif;}}

  .case-quote{{border-left:3px solid var(--ink);padding-left:18px;font-family:'DM Sans',sans-serif;font-weight:700;font-size:25px;line-height:1.4;max-width:70ch;margin-top:8px;}}
  .case-quote span{{display:block;margin-top:10px;font-size:14px;color:var(--muted);text-transform:uppercase;letter-spacing:0.05em;font-weight:700;}}

  .closing{{border-top:2px solid var(--ink);padding-top:36px;}}
  .closing h3{{font-size:29px;max-width:28ch;line-height:1.25;}}
  .closing p{{color:var(--muted);font-size:18px;margin:14px 0 0;max-width:75%;line-height:1.55;}}
  .closing .dots{{display:flex;gap:5px;margin-top:28px;}}
  .closing .dots span{{width:9px;height:9px;border-radius:50%;}}

  @media (max-width:760px){{
    .wrap{{padding:0 16px;}}
    .cover{{padding-top:36px;}}
    .cover img.logo{{margin-bottom:40px;}}
    .cover h1{{font-size:34px;}}
    .case-title{{font-size:29px;}}
    .case-meta-row{{grid-template-columns:repeat(2,1fr);row-gap:14px;}}
  }}
  @media (max-width:900px){{
    .gallery{{grid-template-columns:repeat(2,minmax(0,1fr));}}
    .gallery-item.tile--wide{{grid-column:span 2;}}
    .gallery-item.tile--tall{{grid-row:span 1;aspect-ratio:3/4;}}
  }}
  @media (max-width:600px){{
    .gallery{{grid-template-columns:1fr;gap:5px;}}
    .gallery-item,
    .gallery-item.tile--square,
    .gallery-item.tile--portrait,
    .gallery-item.tile--landscape,
    .gallery-item.tile--wide,
    .gallery-item.tile--tall{{grid-column:span 1;grid-row:span 1;aspect-ratio:4/5;}}
  }}
</style>
</head>
<body>
<div id="app">
  <div class="wrap">
    <div class="cover">
      <img class="logo" src="{logo}" alt="waf.">
      <div class="eyebrow">{set_name}</div>
      <h1 class="heading">Work, chosen for this conversation.</h1>
      <p>The projects below were picked from our archive to speak to what we'd bring to this partnership — real briefs, real approach, real results, no template deck required.</p>
      <div class="dots"><span style="background:var(--g1)"></span><span style="background:var(--g2)"></span><span style="background:var(--g3)"></span><span style="background:var(--g4)"></span><span style="background:var(--g5)"></span></div>
    </div>

    {sections_html}

    <div class="closing">
      <div class="eyebrow">We Are Family London</div>
      <h3 class="heading">Let's talk about what we'd build for you.</h3>
      <p>This link was put together specifically for this conversation — if the shortlist changes, ask and we'll update it.</p>
      <div class="dots"><span style="background:var(--g1)"></span><span style="background:var(--g2)"></span><span style="background:var(--g3)"></span><span style="background:var(--g4)"></span><span style="background:var(--g5)"></span></div>
    </div>
  </div>
</div>
</body>
</html>
"""
    return body


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Client / pitch name")
    ap.add_argument("--ids", required=True, help="Comma-separated project ids")
    ap.add_argument("--out", required=False, help="Output file path (default: docs/<slug>/index.html)")
    args = ap.parse_args()

    ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    unknown = [i for i in ids if i not in BY_ID]
    if unknown:
        print(f"WARNING: unknown project ids ignored: {unknown}", file=sys.stderr)
    ids = [i for i in ids if i in BY_ID]
    if not ids:
        print("ERROR: no valid project ids given", file=sys.stderr)
        sys.exit(1)

    slug = slugify(args.name)
    out_path = args.out or os.path.join("docs", slug, "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    html = render_creds(ids, args.name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {out_path} ({len(html)//1024} KB) slug={slug}")
