import json, re, os, glob

# Paths are relative to this script's location (build/), not hardcoded, so
# the project can be moved/renamed without breaking the generator.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "Character Sheets")
OUT_DIR = os.path.join(PROJECT_ROOT, "characters")
NPC_SRC_DIR = os.path.join(PROJECT_ROOT, "NPCs")
NPC_OUT_DIR = os.path.join(OUT_DIR, "npcs")

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

TEMPLATE = open(os.path.join(os.path.dirname(__file__), "sheet_template.html")).read()

characters = []
os.makedirs(OUT_DIR, exist_ok=True)

# Every *.json file in Character Sheets/ is one player character. The DM's
# in-browser "Save to folder" feature writes back to these same filenames
# (<slug>.json), so this glob picks up edits automatically - no manual list
# to maintain.
source_files = sorted(glob.glob(os.path.join(SRC_DIR, "*.json")))

for path in source_files:
    fname = os.path.basename(path)
    with open(path) as f:
        data = json.load(f)
    slug = slugify(data["name"])
    data_json = json.dumps(data)
    html = TEMPLATE.replace("__CHARACTER_DATA__", data_json)
    html = html.replace("__CHARACTER_NAME__", data["name"])
    html = html.replace("__SOURCE_FILENAME__", fname)
    out_path = os.path.join(OUT_DIR, f"{slug}.html")
    with open(out_path, "w") as f:
        f.write(html)
    characters.append({"name": data["name"], "slug": slug, "species": data["species"],
                        "cls": data["classes"][0]["name"], "level": data["classes"][0]["level"],
                        "subclass": data["classes"][0].get("subclass", ""),
                        "id": data["id"], "fname": fname})
    print("wrote", out_path)

# Build "pushed" NPC/monster pages - any *.json in NPCs/ becomes a real generated
# page at characters/npcs/<slug>.html, same as a player page, but DM-gated (never
# linked from index.html) - see build_npc_page_template.py.
import subprocess
subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "build_npc_page_template.py")], check=True)
NPC_PAGE_TEMPLATE = open(os.path.join(os.path.dirname(__file__), "npc_page_template.html")).read()

npcs = []
os.makedirs(NPC_OUT_DIR, exist_ok=True)
npc_source_files = sorted(glob.glob(os.path.join(NPC_SRC_DIR, "*.json")))

for path in npc_source_files:
    fname = os.path.basename(path)
    with open(path) as f:
        data = json.load(f)
    slug = slugify(data["name"])
    html = NPC_PAGE_TEMPLATE.replace("__CHARACTER_DATA__", json.dumps(data))
    html = html.replace("__CHARACTER_NAME__", data["name"])
    html = html.replace("__SOURCE_FILENAME__", fname)
    out_path = os.path.join(NPC_OUT_DIR, f"{slug}.html")
    with open(out_path, "w") as f:
        f.write(html)
    npcs.append({"name": data["name"], "slug": slug, "id": data["id"], "fname": fname,
                 "species": data.get("species", ""),
                 "cls": (data.get("classes") or [{}])[0].get("name", "")})
    print("wrote", out_path)

# Build index.html
index_items = "\n".join(
    f'''      <a class="char-card" href="characters/{c['slug']}.html">
        <div class="char-card-name">{c['name']}</div>
        <div class="char-card-sub">{c['species']} {c['cls']} {c['level']}{' &middot; ' + c['subclass'] if c['subclass'] else ''}</div>
      </a>'''
    for c in characters
)

INDEX_TEMPLATE = open(os.path.join(os.path.dirname(__file__), "index_template.html")).read()
index_html = INDEX_TEMPLATE.replace("__CHAR_CARDS__", index_items)
with open(os.path.join(PROJECT_ROOT, "index.html"), "w") as f:
    f.write(index_html)
print("wrote index.html")

# Build compare.html
char_list_json = json.dumps([{"name": c["name"], "slug": c["slug"]} for c in characters])
COMPARE_TEMPLATE = open(os.path.join(os.path.dirname(__file__), "compare_template.html")).read()
compare_html = COMPARE_TEMPLATE.replace("__CHAR_LIST__", char_list_json)
with open(os.path.join(PROJECT_ROOT, "compare.html"), "w") as f:
    f.write(compare_html)
print("wrote compare.html")

# Build dm.html
DM_PASSCODE = "dmaccess1"  # change this (and re-run) to set your own DM passcode
dm_char_list = [{
    "name": c["name"], "slug": c["slug"], "id": c["id"], "fname": c["fname"],
    "sub": f"{c['species']} {c['cls']} {c['level']}" + (f" · {c['subclass']}" if c["subclass"] else "")
} for c in characters]
dm_npc_list = [{
    "name": n["name"], "slug": n["slug"], "id": n["id"], "fname": n["fname"],
    "sub": " ".join(filter(None, [n["species"], n["cls"]]))
} for n in npcs]
DM_TEMPLATE = open(os.path.join(os.path.dirname(__file__), "dm_template.html")).read()
dm_html = (DM_TEMPLATE
    .replace("__CHAR_LIST__", json.dumps(dm_char_list))
    .replace("__PUSHED_NPC_LIST__", json.dumps(dm_npc_list))
    .replace("__DM_PASSCODE__", DM_PASSCODE))
with open(os.path.join(PROJECT_ROOT, "dm.html"), "w") as f:
    f.write(dm_html)
print("wrote dm.html  (DM passcode:", DM_PASSCODE, ")")

# Build characters/npc.html (generic, ad-hoc NPC/monster sheet)
import subprocess
subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "build_npc_template.py")], check=True)
NPC_TEMPLATE = open(os.path.join(os.path.dirname(__file__), "npc_template.html")).read()
with open(os.path.join(OUT_DIR, "npc.html"), "w") as f:
    f.write(NPC_TEMPLATE)
print("wrote characters/npc.html")
