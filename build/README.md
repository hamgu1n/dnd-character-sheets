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

## NPCs/monsters created in DM mode

These are **not** part of this build — they live only in the DM's own browser
storage (see the note on the DM dashboard). There's nothing to "save" for them
in this pipeline; they just persist in that browser until deleted.

**Creating one with Claude:** see `NPC_TEMPLATE.md` for the JSON shape. Describe
the NPC to Claude, ask it to fill in that template, then on the NPC's page tap
**📥 Import JSON** and paste the result — it fills in the sheet instantly, no
rebuild needed. (An import that fails validation — bad JSON, or no `name` — shows
an error in the modal instead of silently doing nothing.)

**Deleting one** requires: an initial confirm, then typing the NPC's exact name
into a prompt, then a final confirm — deliberately hard to do by accident, since
it's permanent and there's no undo.

## Files in this folder

- `gen_sheets.py` — the build script (run this)
- `sheet_template.html` — the template used for every player character page
- `index_template.html` — the player-facing character picker
- `compare_template.html` — the DM's side-by-side compare tool
- `dm_template.html` — the DM dashboard (passcode is set near the top of `gen_sheets.py`)
- `npc_template.html` / `build_npc_template.py` — generates `characters/npc.html`,
  the generic ad-hoc NPC/monster sheet
