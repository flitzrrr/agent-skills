#!/usr/bin/env python3
"""Write updated product descriptions back to a catalog JSON file.

Usage:
    python update_catalog.py <catalog.json> <updates.json>

updates.json format:
[
  {"sku": "401", "beschreibung": "New description text..."},
  {"sku": "402", "beschreibung": "Another description..."}
]

Creates an automatic backup before writing.
"""

import json
import sys
import shutil
from datetime import datetime

DESC_FIELD = "beschreibung"
SKU_FIELD = "sku"
NAME_FIELD = "name"


def main():
    if len(sys.argv) < 3:
        print("Usage: python update_catalog.py <catalog.json> <updates.json>")
        sys.exit(1)

    catalog_path = sys.argv[1]
    updates_path = sys.argv[2]

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    with open(updates_path, "r", encoding="utf-8") as f:
        updates = json.load(f)

    # Support both "beschreibung" and "description" field names in updates
    update_map = {}
    for u in updates:
        desc = u.get(DESC_FIELD, u.get("description", ""))
        update_map[u[SKU_FIELD]] = desc

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{catalog_path}.backup_{timestamp}"
    shutil.copy2(catalog_path, backup_path)
    print(f"Backup created: {backup_path}")

    updated = 0
    not_found = []

    for product in catalog.get("products", []):
        sku = product.get(SKU_FIELD, "")
        if sku in update_map:
            old_wc = len(product.get(DESC_FIELD, "").split())
            product[DESC_FIELD] = update_map[sku]
            new_wc = len(update_map[sku].split())
            print(f"  [+] SKU {sku}: {product.get(NAME_FIELD, '?')} ({old_wc} -> {new_wc} words)")
            updated += 1
            del update_map[sku]

    for sku in update_map:
        not_found.append(sku)
        print(f"  [-] SKU {sku}: Not found in catalog")

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent="\t")

    print(f"\n{updated} descriptions updated.")
    if not_found:
        print(f"{len(not_found)} SKUs not found: {', '.join(not_found)}")


if __name__ == "__main__":
    main()
