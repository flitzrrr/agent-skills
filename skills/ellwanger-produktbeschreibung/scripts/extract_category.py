#!/usr/bin/env python3
"""Extract products of a specific category as JSON for batch prompting.

Usage:
    python extract_category.py <index.json> <category-name> [--limit 8]

Outputs a clean JSON array with only the fields needed for the prompt.
"""

import json
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Extract category products for batch prompting")
    parser.add_argument("catalog_path", help="Path to index.json")
    parser.add_argument("category", help="Category name (e.g., 'Tennisnetze')")
    parser.add_argument("--limit", "-l", type=int, default=8, help="Max products per batch (default: 8)")
    parser.add_argument("--offset", "-o", type=int, default=0, help="Skip first N products (for pagination)")
    parser.add_argument("--thin-first", "-t", action="store_true", help="Sort thinnest descriptions first")
    args = parser.parse_args()

    with open(args.catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    search = args.category.lower()
    products = [
        p for p in data.get("products", [])
        if p.get("status", "aktiv") == "aktiv"
        and (search in p.get("kategorie", "").lower()
             or search in p.get("kategorieName", "").lower()
             or p.get("kategorie", "").lower() == search
             or p.get("kategorieName", "").lower() == search)
    ]

    if not products:
        # Show available categories as help
        all_cats = sorted(set(p.get("kategorieName", p.get("kategorie", "?")) for p in data.get("products", [])))
        print(f"Keine aktiven Produkte für '{args.category}' gefunden.", file=sys.stderr)
        print(f"Verfügbare Kategorien:", file=sys.stderr)
        for c in all_cats:
            print(f"  - {c}", file=sys.stderr)
        sys.exit(1)

    if args.thin_first:
        products.sort(key=lambda p: len(p.get("beschreibung", "").split()))

    batch = products[args.offset:args.offset + args.limit]

    output = []
    for p in batch:
        output.append({
            "sku": p.get("sku", ""),
            "name": p.get("name", ""),
            "beschreibung": p.get("beschreibung", ""),
            "variante": p.get("variante", ""),
            "preis": p.get("preis"),
            "preisAufAnfrage": p.get("preisAufAnfrage", False),
            "einheit": p.get("einheit", "Stück"),
        })

    total = len(products)
    shown = len(batch)
    remaining = total - args.offset - shown

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n// Kategorie: {args.category} | Gezeigt: {shown}/{total} | Offset: {args.offset} | Verbleibend: {max(0, remaining)}", file=sys.stderr)


if __name__ == "__main__":
    main()
