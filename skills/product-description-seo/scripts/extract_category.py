#!/usr/bin/env python3
"""Extract products of a category as JSON for batch prompting.

Usage:
    python extract_category.py <catalog.json> <category-name> [--limit 8]

Supports fuzzy category matching and pagination.
"""

import json
import sys
import argparse

DESC_FIELD = "beschreibung"
CAT_FIELD = "kategorieName"
CAT_FIELD_ALT = "kategorie"
SKU_FIELD = "sku"
NAME_FIELD = "name"
STATUS_FIELD = "status"
STATUS_ACTIVE = "aktiv"


def main():
    parser = argparse.ArgumentParser(description="Extract category products for batch prompting")
    parser.add_argument("catalog_path", help="Path to catalog JSON file")
    parser.add_argument("category", help="Category name (fuzzy match)")
    parser.add_argument("--limit", "-l", type=int, default=8,
                        help="Max products per batch (default: 8)")
    parser.add_argument("--offset", "-o", type=int, default=0,
                        help="Skip first N products for pagination")
    parser.add_argument("--thin-first", "-t", action="store_true",
                        help="Sort thinnest descriptions first")
    args = parser.parse_args()

    with open(args.catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    search = args.category.lower()
    products = [
        p for p in data.get("products", [])
        if p.get(STATUS_FIELD, STATUS_ACTIVE) == STATUS_ACTIVE
        and (search in p.get(CAT_FIELD_ALT, "").lower()
             or search in p.get(CAT_FIELD, "").lower()
             or p.get(CAT_FIELD_ALT, "").lower() == search
             or p.get(CAT_FIELD, "").lower() == search)
    ]

    if not products:
        all_cats = sorted(set(
            p.get(CAT_FIELD, p.get(CAT_FIELD_ALT, "?"))
            for p in data.get("products", [])
        ))
        print(f"No active products found for '{args.category}'.", file=sys.stderr)
        print("Available categories:", file=sys.stderr)
        for c in all_cats:
            print(f"  - {c}", file=sys.stderr)
        sys.exit(1)

    if args.thin_first:
        products.sort(key=lambda p: len(p.get(DESC_FIELD, "").split()))

    batch = products[args.offset:args.offset + args.limit]

    output = []
    for p in batch:
        entry = {
            SKU_FIELD: p.get(SKU_FIELD, ""),
            NAME_FIELD: p.get(NAME_FIELD, ""),
            DESC_FIELD: p.get(DESC_FIELD, ""),
        }
        # Include optional fields if present
        for field in ["variante", "preis", "preisAufAnfrage", "einheit"]:
            if field in p:
                entry[field] = p[field]
        output.append(entry)

    total = len(products)
    shown = len(batch)
    remaining = total - args.offset - shown

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n// Category: {args.category} | Shown: {shown}/{total}"
          f" | Offset: {args.offset} | Remaining: {max(0, remaining)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
