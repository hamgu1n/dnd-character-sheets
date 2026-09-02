# How the site is built

**Live site:** https://hamgu1n.github.io/dnd-character-sheets/
**Repo:** https://github.com/hamgu1n/dnd-character-sheets

The player-facing pages (`index.html`, `dm.html`, `compare.html`, `characters/*.html`)
are all **generated** from the templates in this folder plus the character JSON files
in `../Character Sheets/`. Don't hand-edit the generated HTML files directly — your
changes will be overwritten next time this runs.

## Regenerate the site

```
cd build
python3 gen_sheets.py
```

This rebuilds everything from the current source files. Run it any time you change
a template or a character's source JSON.

## Saving changes made in DM Edit Mode (the normal workflow)

Edits made in the browser (DM mode → Edit) only save to *that device's* local
browser storage at first — they don't touch any file on disk, and they won't show
up for players on other devices or on the hosted GitHub Pages site until you do this:

1. In DM mode, open the character, make your edits, then tap **💾 Save to Character
   Sheets folder**.
   - **First time only**: your browser will ask you to pick a folder — choose
     `Character Sheets/` in this project. It remembers your choice after that
     (stored in that browser's IndexedDB), so future saves are one tap, no picker.
   - This writes straight to `../Character Sheets/<name>.json`, replacing its
     contents — no download, no manually moving files.
   - Only works in **Chrome or Edge on desktop** (the File System Access API isn't
     supported on Safari, Firefox, or mobile browsers). On those, the button won't
     appear — use the **⬇ Export character JSON (fallback download)** button
     instead and move the file into `Character Sheets/` yourself.
2. Re-run `python3 gen_sheets.py` from this folder to regenerate the HTML.
3. Commit and push to GitHub (`git add -A && git commit -m "update characters" && git push`)
   so GitHub Pages picks up the change for everyone.

If you don't have a git repo set up yet for GitHub Pages, ask Claude to set that up —
until then, the regenerated files just update locally on your computer.

Note: character source files now live at `Character Sheets/<slug>.json` (e.g.
`patrick.json`) instead of the old `text.txt`/`text 2.txt` export names — the
generator picks up every `*.json` file in that folder automatically, so this
also just works if you add a brand new player character's JSON there by hand.

## NPCs/monsters

There are two tiers, same idea as "local edits" vs. "pushed" for players:

**Pushed NPCs** (`NPCs/*.json` → `characters/npcs/<slug>.html`) — *are* part
of this build, generated exactly like a player page but DM-gated (locked
screen unless `isDM()`) and never linked from `index.html`. They show up
under "NPCs & Monsters (on the site)" on the DM Dashboard, work from any
device once pushed, and support **💾 Save to Character Sheets folder** the
same as a player page (writes back into `NPCs/`). See `NPC_TEMPLATE.md`.

**Local drafts** (created via **+ New NPC / Monster**) — **not** part of this
build, live only in that DM's own browser storage. Nothing to "save" in this
pipeline for these; they just persist in that browser until deleted.

**Creating either with Claude:** see `NPC_TEMPLATE.md` for the JSON shape and
both workflows. For local drafts specifically: on the NPC's page tap
**📥 Import JSON** and paste the result — it fills in the sheet instantly, no
rebuild needed. (An import that fails validation — bad JSON, or no `name` — shows
an error in the modal instead of silently doing nothing.)

**Deleting a local draft** requires: an initial confirm, then typing the NPC's
exact name into a prompt, then a final confirm — deliberately hard to do by
accident, since it's permanent and there's no undo. (Pushed NPCs don't have an
in-browser delete — remove the `NPCs/<file>.json` and rebuild, same as you'd
retire a player.)

## Files in this folder

- `gen_sheets.py` — the build script (run this)
- `sheet_template.html` — the template used for every player character page
- `index_template.html` — the player-facing character picker
- `compare_template.html` — the DM's side-by-side compare tool
- `dm_template.html` — the DM dashboard (passcode is set near the top of `gen_sheets.py`)
- `npc_template.html` / `build_npc_template.py` — generates `characters/npc.html`,
  the generic ad-hoc NPC/monster sheet (local drafts)
- `npc_page_template.html` / `build_npc_page_template.py` — generates each
  `characters/npcs/<slug>.html` from `NPCs/*.json` (pushed NPCs)
