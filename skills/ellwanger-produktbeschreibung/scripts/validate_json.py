#!/usr/bin/env python3
"""Validate that the catalog JSON is structurally correct after updates.

Usage:
    python validate_json.py <index.json>

Checks:
- Valid JSON
- All required fields present on each product
- No duplicate SKUs
- No empty beschreibung fields
- Paragraph separators are \\n\\n (not <br>, <p>, etc.)
"""

import json
import sys
from collections import Counter

REQUIRED_FIELDS = ["sku", "name", "beschreibung", "kategorie", "kategorieName",
                   "preis", "einheit", "status", "slug"]


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <index.json>")
        sys.exit(1)

    path = sys.argv[1]
    errors = []
    warnings = []

    # 1. Valid JSON
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"✗ FATAL: Ungültiges JSON: {e}")
        sys.exit(1)

    products = data.get("products", [])
    print(f"Validiere {len(products)} Produkte in {path}...")

    # 2. Required fields
    for i, p in enumerate(products):
        for field in REQUIRED_FIELDS:
            if field not in p:
                errors.append(f"Produkt #{i} (SKU {p.get('sku', '?')}): Feld '{field}' fehlt")

    # 3. Duplicate SKUs
    skus = [p.get("sku", "") for p in products]
    dupes = [sku for sku, count in Counter(skus).items() if count > 1]
    if dupes:
        errors.append(f"Doppelte SKUs: {', '.join(dupes)}")

    # 4. Empty descriptions
    for p in products:
        if not p.get("beschreibung", "").strip():
            warnings.append(f"SKU {p.get('sku', '?')}: Leere Beschreibung")

    # 5. HTML in descriptions
    import re
    for p in products:
        desc = p.get("beschreibung", "")
        if re.search(r'<[^>]+>', desc):
            errors.append(f"SKU {p.get('sku', '?')}: HTML in Beschreibung gefunden")
        if "<br>" in desc or "<p>" in desc:
            errors.append(f"SKU {p.get('sku', '?')}: HTML-Tags statt \\n\\n für Absätze")

    # 6. Slug format
    for p in products:
        slug = p.get("slug", "")
        if slug and not re.match(r'^[a-z0-9\-]+$', slug):
            warnings.append(f"SKU {p.get('sku', '?')}: Slug '{slug}' enthält ungültige Zeichen")

    # Report
    print(f"\n{'=' * 50}")
    if errors:
        print(f"✗ {len(errors)} Fehler gefunden:")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print(f"⚠ {len(warnings)} Warnungen:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print("✓ Alle Validierungen bestanden!")
    elif not errors:
        print(f"\n✓ Keine kritischen Fehler. {len(warnings)} Warnungen.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
