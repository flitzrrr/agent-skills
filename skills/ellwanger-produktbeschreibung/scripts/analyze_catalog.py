#!/usr/bin/env python3
"""Analyze the Ellwanger catalog for thin/missing product descriptions.

Usage:
    python analyze_catalog.py <path-to-index.json> [--category <name>] [--min-words 200]

Outputs a report showing:
- Per-category stats (product count, avg word count, products below threshold)
- The thinnest descriptions that need attention first
- Products with no description at all
"""

import json
import sys
import argparse
from collections import defaultdict


def count_words(text: str) -> int:
    """Count words in a text string."""
    if not text or not text.strip():
        return 0
    return len(text.split())


def analyze(catalog_path: str, category_filter: str | None = None, min_words: int = 200):
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])

    # Filter to active products only
    products = [p for p in products if p.get("status", "aktiv") == "aktiv"]

    if category_filter:
        cf = category_filter.lower()
        products = [p for p in products if cf in p.get("kategorie", "").lower()
                    or cf in p.get("kategorieName", "").lower()
                    or p.get("kategorie", "").lower() == cf
                    or p.get("kategorieName", "").lower() == cf]

    if not products:
        print("Keine Produkte gefunden.")
        return

    # Per-category analysis
    categories = defaultdict(list)
    for p in products:
        cat = p.get("kategorieName", p.get("kategorie", "Unbekannt"))
        wc = count_words(p.get("beschreibung", ""))
        categories[cat].append({
            "sku": p.get("sku", ""),
            "name": p.get("name", ""),
            "word_count": wc,
            "beschreibung": p.get("beschreibung", ""),
        })

    # Summary
    total = len(products)
    below_threshold = sum(1 for p in products if count_words(p.get("beschreibung", "")) < min_words)

    print(f"{'=' * 70}")
    print(f"ELLWANGER KATALOG — BESCHREIBUNGS-ANALYSE")
    print(f"{'=' * 70}")
    print(f"Produkte gesamt (aktiv): {total}")
    print(f"Unter {min_words} Wörter:        {below_threshold} ({below_threshold * 100 // total}%)")
    print(f"Über {min_words} Wörter:         {total - below_threshold} ({(total - below_threshold) * 100 // total}%)")
    print()

    # Category breakdown
    print(f"{'Kategorie':<45} {'Prod':>5} {'Ø Wörter':>9} {'< {}'.format(min_words):>7}")
    print(f"{'-' * 45} {'-' * 5} {'-' * 9} {'-' * 7}")

    sorted_cats = sorted(categories.items(), key=lambda x: sum(p["word_count"] for p in x[1]) / len(x[1]))

    for cat_name, prods in sorted_cats:
        avg_wc = sum(p["word_count"] for p in prods) / len(prods)
        below = sum(1 for p in prods if p["word_count"] < min_words)
        print(f"{cat_name:<45} {len(prods):>5} {avg_wc:>9.1f} {below:>7}")

    # Thinnest descriptions
    print(f"\n{'=' * 70}")
    print(f"DÜNNSTE BESCHREIBUNGEN (Top 20)")
    print(f"{'=' * 70}")

    all_products = []
    for cat_name, prods in categories.items():
        for p in prods:
            p["kategorie"] = cat_name
            all_products.append(p)

    all_products.sort(key=lambda x: x["word_count"])

    for i, p in enumerate(all_products[:20]):
        print(f"\n{i + 1}. {p['name']} (SKU {p['sku']}) — {p['kategorie']}")
        print(f"   Wörter: {p['word_count']}")
        desc = p['beschreibung'][:120] + "..." if len(p.get('beschreibung', '')) > 120 else p.get('beschreibung', '(leer)')
        print(f"   Text: \"{desc}\"")

    # Export format for batch processing
    if category_filter:
        print(f"\n{'=' * 70}")
        print(f"JSON FÜR BATCH-PROMPT (Kategorie: {category_filter})")
        print(f"{'=' * 70}")
        export = []
        for p in all_products:
            export.append({
                "sku": p["sku"],
                "name": p["name"],
                "beschreibung": p["beschreibung"],
                "word_count": p["word_count"],
            })
        print(json.dumps(export, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Analyze Ellwanger catalog descriptions")
    parser.add_argument("catalog_path", help="Path to index.json")
    parser.add_argument("--category", "-c", help="Filter by category name")
    parser.add_argument("--min-words", "-m", type=int, default=200, help="Minimum word count threshold (default: 200)")
    args = parser.parse_args()
    analyze(args.catalog_path, args.category, args.min_words)


if __name__ == "__main__":
    main()
