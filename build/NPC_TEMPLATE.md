# NPC/Monster JSON template

Use this to have Claude generate an NPC or monster for you. Describe the
NPC (name, species, role, rough stats, notable items/spells/abilities) and
ask Claude to fill in this shape. Then:

1. In DM mode, open **+ New NPC / Monster** (creates a blank sheet).
2. Tap **📥 Import JSON** near the top of the page.
3. Paste the JSON Claude gave you and tap **Import**.

The sheet fills in instantly — no rebuild or file editing needed, since NPCs
live only in the DM's browser (see `README.md`). Only `name` is required;
everything else is optional and defaults sensibly if left out.

## Template

```json
{
  "name": "Grix the Snitch",
  "species": "Goblin",
  "background": "Underworld informant",
  "classes": [
    { "id": "role", "name": "Scout", "level": 2, "hitDie": 6, "subclass": "" }
  ],
  "abilities": { "str": 8, "dex": 16, "con": 10, "int": 12, "wis": 10, "cha": 14 },
  "proficientSaves": ["dex", "cha"],
  "skillProficiencies": ["stealth", "deception"],
  "skillExpertise": [],
  "hp": { "max": 14, "current": 14, "temp": 0 },
  "speed": 30,
  "conditions": [],
  "inspiration": false,
  "spellSlots": { "1": { "max": 2, "used": 0 } },
  "spellsPrepared": [
    {
      "name": "Fog Cloud",
      "level": 1,
      "spellType": "conjuration",
      "castingTime": "1 Action",
      "range": "120 feet",
      "desc": "Creates a 20-foot-radius sphere of fog."
    }
  ],
  "currency": { "cp": 0, "sp": 0, "ep": 0, "gp": 12, "pp": 0 },
  "inventory": [
    {
      "id": "i1",
      "name": "Shortbow",
      "kind": "weapon",
      "quantity": 1,
      "dmg": "1d6",
      "dmgType": "Piercing",
      "rangeType": "Ranged",
      "props": ["Ammunition", "Two-Handed"],
      "equipped": true,
      "desc": "A worn hunting bow."
    },
    {
      "id": "i2",
      "name": "Leather Armor",
      "kind": "armor",
      "quantity": 1,
      "acBase": 11,
      "equipped": true
    }
  ],
  "notes": "Freelance informant. Owes the party a favor.",
  "customFeatures": [
    {
      "id": "f1",
      "name": "Nimble Escape",
      "desc": "Can take the Disengage or Hide action as a bonus action."
    }
  ]
}
```

## Field notes

- **classes**: array, supports multiple entries for multiclassing. `name`
  can be anything ("Scout", "Brute", "Cultist") — it doesn't have to be a
  real PC class, but it does drive proficiency bonus (`level` total →
  standard 5e proficiency-by-level).
- **abilities**: all six required if you include the block at all; each
  1–30. Omit the whole `abilities` key to default everything to 10.
- **proficientSaves** / **skillProficiencies** / **skillExpertise**: arrays
  of ability/skill keys — `str dex con int wis cha` for saves;
  `acrobatics animalHandling arcana athletics deception history insight
  intimidation investigation medicine nature perception performance
  persuasion religion sleightOfHand stealth survival` for skills.
- **spellsPrepared[].spellType**: one of `abjuration conjuration divination
  enchantment evocation illusion necromancy transmutation fire ice` — picks
  the spell's icon. Leave it out for the "unassigned" icon.
- **inventory[].kind**: `weapon | armor | shield | gear`. Weapons: `dmg`
  (e.g. `"1d6"`), `dmgType` (`Slashing Piercing Bludgeoning`), `rangeType`
  (`Melee Ranged`) pick the weapon icon (bow/mace/sword) automatically.
  Armor: `acBase`, optional `dexMax`. Shield: `acBonus`.
  Any item can have `desc` (markdown supported) and an `icon` override
  (`sword bow mace shield gear`).
  `skillEffects`: `[{ "skill": "stealth", "mode": "advantage" }]` for gear
  that grants advantage/disadvantage on a check while equipped.
- **customFeatures[].hasPool** / **poolMax**: give a feature a chargeable
  resource pool (like Lay on Hands) — set `"hasPool": true, "poolMax": 15`.
- A feature named exactly **"Lay on Hands"** gets this pool automatically
  if you don't set it yourself.

Anything you omit just falls back to a sensible default (0, empty, or "10"
for HP) — you never need to include every field.
