---
name: produktbeschreibung
description: "End-to-End Skill für Ellwanger Produktbeschreibungen: Bestandsaufnahme, Generierung, Qualitätsprüfung, JSON-Update und Deployment. Verwende diesen Skill immer wenn der User Produktbeschreibungen analysieren, schreiben, prüfen, aktualisieren oder deployen möchte — egal ob Einzelprodukt, Kategorie oder ganzer Katalog. Trigger bei: 'Beschreibung', 'Produkttext', 'SEO-Text', 'Katalogtext', 'beschreibung updaten', 'Fortschritt', 'Status Beschreibungen', 'welche fehlen noch', 'QA', 'Qualität prüfen', oder wenn der User eine Kategorie nennt und Texte dafür haben will. Trigger auch bei 'deploy', 'commit', 'PR erstellen' im Kontext von Produktbeschreibungen."
---

# Produktbeschreibung — End-to-End Workflow

Ellwanger Tennisplatz-Bau & Ausstattung (seit 1975, Oberschleißheim bei München) — ~271 Produkte in 26 Kategorien. Viele Beschreibungen sind OCR-Extrakte mit wenigen Wörtern. Ziel: Jedes Produkt bekommt 200–350 Wörter SEO-optimierten Fließtext.

## Quick Reference

| Phase | Aufgabe | Tool |
|-------|---------|------|
| 1. Bestandsaufnahme | Katalog analysieren, dünnste Texte finden | `scripts/analyze_catalog.py` |
| 2. Fortschritt | Aktuellen Status prüfen | `scripts/track_progress.py` |
| 3. Extraktion | Kategorie als JSON für Batch holen | `scripts/extract_category.py` |
| 4. Generierung | Beschreibungen schreiben | 4-Absatz-Struktur (siehe unten) |
| 5. Qualitätsprüfung | Automatischer QA-Check | `scripts/check_quality.py` |
| 6. JSON-Update | Beschreibungen zurückschreiben | `scripts/update_catalog.py` |
| 7. Validierung | JSON-Struktur prüfen | `scripts/validate_json.py` |
| 8. Rendering-Fix | Produktseite für Mehrabsatz-Texte anpassen | Code-Änderung (siehe Phase 8) |
| 9. Deploy | Feature-Branch, PR, Merge | Git-Workflow |

## Datenquelle

```
apps/web/src/content/catalog/index.json
```

Felder pro Produkt: `sku`, `name`, `beschreibung`, `kategorie`, `kategorieName`, `preis`, `preisAufAnfrage`, `einheit`, `status`, `slug`, `bilder`, `variante`. Nur `beschreibung` wird aktualisiert.

---

## Phase 1: Bestandsaufnahme

Überblick über den Katalogzustand — welche Beschreibungen sind zu dünn, welche Kategorien brauchen Arbeit.

```bash
# Gesamter Katalog
python scripts/analyze_catalog.py <index.json>

# Nur eine Kategorie
python scripts/analyze_catalog.py <index.json> --category "Tennisnetze"

# Mit anderem Threshold
python scripts/analyze_catalog.py <index.json> --min-words 150
```

Output: Per-Kategorie-Statistik (Ø Wörter, Anzahl unter Threshold), Top-20 dünnste Beschreibungen, JSON-Export für Batch-Prompt.

---

## Phase 2: Fortschritt prüfen

Zeigt den aktuellen Stand der Update-Kampagne mit Fortschrittsbalken und Priorisierung.

```bash
python scripts/track_progress.py <index.json>
```

Output: Fortschrittsbalken, Per-Priorität-Breakdown, nächste Aktionen. Priorisierung:

| Prio | Kategorien | Begründung |
|------|-----------|------------|
| 1 | Tennisnetze, Netzpfosten, Linien, Walzen, Pflegegeräte Sand | Kernprodukte, hohes Suchvolumen |
| 2 | Schleppnetze, Abziehgeräte, Besen, Kehrer, Trocknung, Regner | Platzpflege-Cluster, Longtail |
| 3 | Rest (Bänke, Stühle, Ranglisten, Training, etc.) | Ergänzungssortiment |

---

## Phase 3: Extraktion

Produkte einer Kategorie als JSON holen — bereit für den Generierungs-Prompt.

```bash
# Erste 8 Produkte einer Kategorie
python scripts/extract_category.py <index.json> "Tennisnetze" --limit 8

# Dünnste Beschreibungen zuerst
python scripts/extract_category.py <index.json> "Walzen" --thin-first

# Pagination (für große Kategorien)
python scripts/extract_category.py <index.json> "Ranglisten" --offset 8 --limit 8
```

---

## Phase 4: Generierung

Maximal **5–8 Produkte pro Durchgang** um Qualitätsverlust zu vermeiden.

### 4-Absatz-Struktur

**Absatz 1 — Einleitung & Nutzen (50–80 Wörter)**
Focus-Keyword (Produktname + „Tennisplatz" oder Kategorie) im **ersten Satz**. Was ist das Produkt? Welches Problem löst es? Warum braucht ein Verein/Betreiber es?

Die ersten 155 Zeichen müssen als Meta-Description funktionieren — eigenständig sinnvoll, mit Punkt abgeschlossen.

**Absatz 2 — Technische Details (60–100 Wörter)**
Material, Maße, Gewicht, Belastbarkeit, Besonderheiten. **Alle** technischen Daten aus der bestehenden Beschreibung 1:1 übernehmen — nichts weglassen, nichts hinzuerfinden. Wenn die Quelldaten vage sind, entsprechend vage formulieren.

**Absatz 3 — Anwendung & Praxis (40–60 Wörter)**
Belag (Sand/Ziegelmehl, Kunstrasen, Hartplatz), Einsatzzeitpunkt (Saisonstart, tägliche Pflege, nach Regen). 1–2 ergänzende Ellwanger-Produkte nennen — Cross-Sell gemäß CROSS-SELL.md.

**Absatz 4 — Qualität & Service (30–50 Wörter)**
Ellwanger seit 1975, persönliche Beratung, deutschlandweite Lieferung. Sanfter CTA: „Gerne beraten wir Sie bei der Auswahl." Kein aggressiver Verkaufsdruck.

### Varianten-Regel

Produkte mit Farbvarianten (z.B. SKU 401 schwarz / 401a grün) oder Größenvarianten **müssen einzigartige Texte** bekommen. Die Variante (Farbe, Größe, Material) muss im Text erwähnt und kontextualisiert werden — nicht denselben Text kopieren. Beispiel: Bei der grünen Variante kann man erwähnen, dass Grün sich optisch in die Platzumgebung einfügt.

### Tonalität

- Sachlich, fachkompetent, vertrauenswürdig — wie ein erfahrener Fachberater
- Professionelles „Sie" — niemals duzen
- **Verbotene Wörter:** erstklassig, herausragend, unschlagbar, einzigartig, revolutionär, sensationell, unvergleichlich, Premium, „höchstem Niveau", weltweit führend, perfekt
- Superlative nur mit konkretem Beleg (z.B. „seit mehr als 10 Jahren bewährt" ✓)
- Zielgruppe: Platzwarte, Vereinsvorstände, kommunale Sportamtsleiter, Facility Manager

### SEO-Keywords

- **Primary:** [Produktname] + „Tennisplatz" oder „für Tennisplätze"
- **Secondary:** [Kategoriename], „Tennisplatz-Zubehör", „Platzpflege"
- **Longtail:** „[Produktname] kaufen", „[Produktname] für Tennisverein"
- Max. 3× Focus-Keyword pro Text. Für kategorie-spezifische Keywords: KEYWORDS.md

### Output-Format

Beschreibungen als JSON-Array ausgeben:

```json
[
  {
    "sku": "401",
    "name": "Tennisnetz Standard",
    "beschreibung": "Absatz 1...\n\nAbsatz 2...\n\nAbsatz 3...\n\nAbsatz 4..."
  }
]
```

Speichern als `updates-<kategorie>.json` (z.B. `updates-tennisnetze.json`).

---

## Phase 5: Qualitätsprüfung

Automatische Prüfung gegen alle Anforderungen:

```bash
# Standard-Check
python scripts/check_quality.py updates-tennisnetze.json

# Strict Mode (Warnungen = Fehler)
python scripts/check_quality.py updates-tennisnetze.json --strict
```

Prüft pro Beschreibung:
- ☐ 200–350 Wörter
- ☐ 4-Absatz-Struktur (3× `\n\n`)
- ☐ Focus-Keyword im ersten Satz
- ☐ Keine verbotenen Superlative
- ☐ Cross-Sell-Hinweis vorhanden
- ☐ Professionelle Sie-Form
- ☐ Meta-Description-taugliche erste 155 Zeichen
- ☐ Reiner Fließtext (kein HTML/Markdown)

Bei Fehlern: Betroffene Beschreibungen korrigieren, dann erneut prüfen. Erst wenn alle Checks bestanden → weiter zu Phase 6.

---

## Phase 6: JSON-Update

Geprüfte Beschreibungen in den Katalog zurückschreiben:

```bash
python scripts/update_catalog.py <index.json> updates-tennisnetze.json
```

Das Script:
1. Erstellt automatisch ein Backup (`index.json.backup_YYYYMMDD_HHMMSS`)
2. Matched Updates per SKU
3. Zeigt Wortanzahl vorher → nachher
4. Meldet nicht gefundene SKUs

---

## Phase 7: Validierung

Nach dem Update die JSON-Struktur validieren:

```bash
python scripts/validate_json.py <index.json>
```

Prüft: Gültiges JSON, alle Pflichtfelder, keine doppelten SKUs, keine HTML-Tags in Beschreibungen, korrekte Slug-Formate.

---

## Phase 8: Rendering-Fix

Die Produktdetailseite (`/catalog/[slug]/+page.svelte`) rendert `beschreibung` aktuell als einzelnes `<p>`. Für mehrabsätzige Texte muss das angepasst werden.

**Änderung in `+page.svelte`:**

```svelte
<!-- Vorher -->
<p class="description-text">{productDescription}</p>

<!-- Nachher -->
{#each productDescription.split('\n\n') as paragraph}
  <p class="description-text">{paragraph}</p>
{/each}
```

Die `productDescription`-Variable existiert bereits als `$derived`:
```javascript
const productDescription = $derived(
  data.product.beschreibung || `Produktdetails zu ${data.product.name}`
);
```

Diese Änderung muss nur einmal gemacht werden und betrifft alle Produkte.

**Meta-Description anpassen** (falls noch nicht geschehen):
```javascript
// Erste 155 Zeichen des ersten Absatzes als Meta-Description
const metaDescription = $derived(
  (data.product.beschreibung || '').split('\n\n')[0].slice(0, 155)
);
```

---

## Phase 9: Deploy

Standard Git-Workflow — **niemals direkt auf main pushen**.

```bash
# 1. Feature-Branch erstellen
git checkout -b produktbeschreibungen/<kategorie>

# 2. Änderungen committen
git add apps/web/src/content/catalog/index.json
git commit -m "content: Update Produktbeschreibungen <Kategorie>"

# 3. PR erstellen
gh pr create --title "Content: Produktbeschreibungen <Kategorie>" \
  --body "SEO-optimierte Beschreibungen für <N> Produkte in <Kategorie>"

# 4. Nach Review: Merge → Deploy
```

Pro Kategorie oder Batch ein eigener PR. Nicht alles in einen riesigen PR packen — das macht Reviews unmöglich.

---

## Beispiel: Kompletter Durchlauf

```bash
# 1. Wo stehen wir?
python scripts/track_progress.py index.json

# 2. Nächste Kategorie holen
python scripts/extract_category.py index.json "Walzen" --thin-first

# 3. [Beschreibungen generieren — 4-Absatz-Struktur]
# → speichern als updates-walzen.json

# 4. Qualität prüfen
python scripts/check_quality.py updates-walzen.json

# 5. In Katalog schreiben
python scripts/update_catalog.py index.json updates-walzen.json

# 6. JSON validieren
python scripts/validate_json.py index.json

# 7. Committen & PR
git checkout -b produktbeschreibungen/walzen
git add apps/web/src/content/catalog/index.json
git commit -m "content: Update Produktbeschreibungen Walzen (4 Produkte)"
gh pr create --title "Content: Produktbeschreibungen Walzen"
```

---

## Referenzdateien

| Datei | Inhalt |
|-------|--------|
| KEYWORDS.md | Keyword-Map pro Kategorie (Primary, Secondary, Longtail) |
| CROSS-SELL.md | Cross-Sell-Matrix: welche Kategorien aufeinander verweisen |

## Scripts

| Script | Funktion |
|--------|----------|
| `scripts/analyze_catalog.py` | Katalog-Analyse (dünnste Beschreibungen, Wortanzahl) |
| `scripts/track_progress.py` | Fortschritts-Tracking mit Priorisierung |
| `scripts/extract_category.py` | Kategorie als JSON für Batch-Prompt extrahieren |
| `scripts/check_quality.py` | Automatische QA gegen alle Anforderungen |
| `scripts/update_catalog.py` | Beschreibungen in index.json zurückschreiben (mit Backup) |
| `scripts/validate_json.py` | JSON-Struktur nach Update validieren |

## Dependencies

- **Python 3.10+**: Für alle Scripts
- **gh CLI**: Für PR-Erstellung (Phase 9)
