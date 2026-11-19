"""Derives npc_page_template.html from sheet_template.html - used for NPCs/monsters
that have been "pushed" to the site (a real JSON file in NPCs/, generated just like
a player page). Unlike the ad-hoc npc.html (blank template, ?id= driven, browser-only
storage), this one embeds real per-NPC data at build time and is DM-gated:

- loads the NPC's real data, same as a player page (not blank)
- is gated behind DM auth (locked screen if not isDM()) - nothing renders otherwise
- links back to the DM dashboard instead of the player index
- keeps "Save to Character Sheets folder" working, pointed at NPCs/ instead
- is NEVER linked from index.html / listed anywhere a player can reach

Note: the rendered UI is locked, but on GitHub Pages the underlying HTML (with the
NPC's data baked in) is still publicly fetchable by URL or view-source, same
soft-gating tradeoff as the rest of this DM-passcode system.
"""
import os

SRC = os.path.join(os.path.dirname(__file__), "sheet_template.html")
OUT = os.path.join(os.path.dirname(__file__), "npc_page_template.html")

html = open(SRC).read()

def sub(old, new):
    """Replace exactly one occurrence, or fail the build - a silently skipped
    patch once left every pushed NPC page without its lock screen/data."""
    global html
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"build_npc_page_template: expected 1 match, found {n}:\n{old[:120]}")
    html = html.replace(old, new)

sub(
    '<body>\n',
    '''<body>

<div id="lockScreen" class="lock-screen">
  <div class="lock-card">
    <h1 style="font-size:1.3rem;">DM Access Required</h1>
    <p style="color:var(--text-dim);font-size:0.85rem;">NPC and monster sheets are hidden from players. Enter DM mode first.</p>
    <a class="reset-btn" href="../../dm.html" style="display:inline-block;width:auto;padding:9px 18px;">Go to DM Dashboard</a>
  </div>
</div>

<div id="appRoot" hidden>
'''
)

sub(
    '''<div class="toplinks">
  <a class="backlink" href="../index.html" style="margin-bottom:0;">&larr; All characters</a>
  <a class="comparelink" href="../compare.html" id="compareLink" hidden>⇄ Compare players</a>
</div>''',
    '''<div class="toplinks">
  <a class="backlink" href="../../dm.html" style="margin-bottom:0;">&larr; DM Dashboard</a>
  <a id="compareLink" hidden></a>
</div>'''
)

sub(
    '''<button class="reset-btn" onclick="resetProgress()">Reset tracked stats (HP, spell slots, notes…)</button>
<div class="footer-note">Progress and edits are saved on this device only.</div>

</div>''',
    '''<button class="reset-btn" onclick="resetProgress()">Reset tracked stats (HP, spell slots, notes…)</button>
<div class="footer-note">Progress is saved on this device only. Character edits sync via "Save to folder" like a player sheet.</div>

</div>'''
)

sub(
    "  .backlink{display:inline-block;margin-bottom:10px;color:var(--text-dim);font-size:0.8rem;text-decoration:none;}",
    """  .backlink{display:inline-block;margin-bottom:10px;color:var(--text-dim);font-size:0.8rem;text-decoration:none;}
  .lock-screen{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;}
  .lock-card{background:var(--panel);border:1px solid var(--border);border-radius:14px;
    padding:28px 24px;max-width:360px;text-align:center;}
  .lock-card h1{font-family:Georgia,"Times New Roman",serif;}
  .lock-card p{margin:10px 0 16px;}"""
)

# Gate the render behind DM auth. Firebase resolves the login asynchronously,
# so the gate re-runs from onAuthStateChanged - checking only at page load always
# saw "not DM" and never loaded the baked-in data. Firestore listeners (npcs/ is
# DM-only read) start only once authed, or the snapshot is permission-denied and
# the listener dies for good.
sub(
    """  document.getElementById("dmLogoutBtn").hidden = !dmAuthed;
  renderAll();
});""",
    """  document.getElementById("dmLogoutBtn").hidden = !dmAuthed;
  applyDMGate();
});"""
)
sub(
    """if(FS_SYNC_ENABLED){
  charRef.onSnapshot(doc => {""",
    """let fsListening = false;
function startFsSync(){
  if(fsListening || !FS_SYNC_ENABLED) return;
  fsListening = true;
  charRef.onSnapshot(doc => {"""
)
sub(
    '''charData = loadCharData();
try{ activeTab = localStorage.getItem(TAB_KEY) || "play"; }catch(e){}
setTab(activeTab);
renderAll();''',
    '''function applyDMGate(){
  const dm = isDM();
  document.getElementById("lockScreen").hidden = dm;
  document.getElementById("appRoot").hidden = !dm;
  if(!dm) return;
  if(!charData){
    charData = loadCharData();
    try{ activeTab = localStorage.getItem(TAB_KEY) || "play"; }catch(e){}
    setTab(activeTab);
  }
  startFsSync();
  renderAll();
}
applyDMGate();'''
)

# Pushed NPCs save to NPCs/, not Character Sheets/ - use a separate cached
# folder-picker handle so this doesn't silently reuse (or clobber) whatever
# folder the DM already picked for player saves.
sub(
    'const DIR_HANDLE_KEY = "characterSheetsDir"; // which cached folder-picker handle this page\'s saves use\nconst FOLDER_LABEL = "Character Sheets"; // just for the "Saved to ..." status text',
    'const DIR_HANDLE_KEY = "npcsDir";\nconst FOLDER_LABEL = "NPCs";'
)

# close the appRoot wrapper div right before </body>
sub("</body>", "</div>\n</body>")

open(OUT, "w").write(html)
print("wrote", OUT)
