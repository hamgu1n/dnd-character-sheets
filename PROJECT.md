# D&D Character Sheet Web App

## Overview

A lightweight character sheet tool for a 5e Dungeons & Dragons campaign (DM: Haytham, ~5-6 players). Built to replace a buggy third-party character sheet app.

## Goals

- **Phase 1 (fast, for immediate session use):** Static HTML character sheets, one file per character, viewable locally in any mobile/tablet/desktop browser. No hosting or backend required.
- **Phase 2 (follow-up):** A public, free-hosted website where each player enters their character's name to pull up their own sheet.

## Phase 1 — Static HTML Sheets

- One self-contained `.html` file per player character (no external dependencies required, so files can be opened directly from a phone/tablet without internet).
- Should be interactive where useful: e.g. clickable ability score blocks, expandable spell/inventory lists, simple JS-based dice roll buttons (e.g. roll a d20 + modifier).
- Should look clean and readable on a phone screen — this is the primary use case.
- Suggested structure per sheet:
  - Character name, race, class, level, background
  - Ability scores + modifiers
  - HP, AC, initiative, speed
  - Saving throws & skills (with proficiency indicated)
  - Attacks/weapons
  - Spells (if applicable)
  - Inventory
  - Notes/backstory section

## Phase 2 — Hosted Lookup Site

- Deploy as a static site via **GitHub Pages** or **Firebase Hosting** (both free at this scale).
- Landing page with a simple name-entry field that routes to the matching character's sheet.
- Stretch goal: basic write access so players can update HP/inventory themselves (would need a lightweight backend, e.g. Firebase free tier — evaluate once Phase 1 is working).

## File Structure (proposed)

```
/index.html          → name lookup / landing page
/characters/
  character-name.html  → one file per PC
/assets/
  style.css           → shared styling
  sheet.js            → shared interactive logic (dice rolls, toggles)
```

## Notes

- No character data has been provided yet — sheets will need each player's stats, class features, spells, and inventory filled in.
- Priority for the first pass: get something usable and mobile-friendly in front of players quickly; polish and hosting can follow.
