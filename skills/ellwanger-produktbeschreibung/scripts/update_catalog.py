#!/usr/bin/env python3
"""Update product descriptions in the Ellwanger catalog index.json.

Usage:
    python update_catalog.py <index.json> <updates.json>

updates.json format:
[
  {"sku": "401", "beschreibung": "New description text..."},
  {"sku": "402", "beschreibung": "Another new description..."}
]

The script:
1. Reads the catalog index.json
2. Matches updates by SKU
3. Replaces the beschreibung field
4. Writes back to the same file (with backup)
5. Reports what was updated
"""

import json
import sys
import shutil
from datetime import datetime


def main():
    if len(sys.argv) < 3:
        print("Usage: python update_catalog.py <index.json> <updates.json>")
        sys.exit(1)

    catalog_path = sys.argv[1]
    updates_path = sys.argv[2]

    # Read catalog
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Read updates
    with open(updates_path, "r", encoding="utf-8") as f:
        updates = json.load(f)

    # Index updates by SKU
    update_map = {u["sku"]: u["beschreibung"] for u in updates}

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{catalog_path}.backup_{timestamp}"
    shutil.copy2(catalog_path, backup_path)
    print(f"Backup erstellt: {backup_path}")

    # Apply updates
    updated = 0
    not_found = []

    for product in catalog.get("products", []):
        sku = product.get("sku", "")
        if sku in update_map:
            old_wc = len(product.get("beschreibung", "").split())
            product["beschreibung"] = update_map[sku]
            new_wc = len(update_map[sku].split())
            print(f"  ✓ SKU {sku}: {product['name']} ({old_wc} → {new_wc} Wörter)")
            updated += 1
            del update_map[sku]

    # Check for SKUs not found in catalog
    for sku in update_map:
        not_found.append(sku)
        print(f"  ✗ SKU {sku}: Nicht im Katalog gefunden!")

    # Write updated catalog
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent="\t")

    print(f"\n{updated} Beschreibungen aktualisiert.")
    if not_found:
        print(f"{len(not_found)} SKUs nicht gefunden: {', '.join(not_found)}")


if __name__ == "__main__":
    main()
