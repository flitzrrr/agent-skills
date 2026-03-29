#!/usr/bin/env python3
"""Track progress of the product description update campaign.

Usage:
    python track_progress.py <index.json> [--min-words 200]

Shows:
- Overall progress (how many products meet the 200-word threshold)
- Per-category completion status
- Estimated remaining effort
- Priority queue (what to work on next)
"""

import json
import sys
import argparse
from collections import defaultdict


PRIO_1 = ["Tennisnetze", "Tennisnetzpfosten, Netzzubehör", "Tennislinien, Spanngeräte",
           "Tennisplatz-Walzen", "Pflegegeräte und Maschinen für Sandplätze"]
PRIO_2 = ["Schleppnetze, Abziehteppiche", "Abziehgeräte", "Abziehbesen, Abziehmatte",
           "Linienkehrer, Linienstampfer", "Platzpflege- und Instandhaltungsgeräte",
           "Platztrocknungsgeräte, Wasserschläuche", "Regner, Fächerdüsen", "Regner"]
PRIO_3 = []  # everything else


def get_priority(cat_name: str) -> int:
    if cat_name in PRIO_1:
        return 1
    elif cat_name in PRIO_2:
        return 2
    return 3


def main():
    parser = argparse.ArgumentParser(description="Track description update progress")
    parser.add_argument("catalog_path", help="Path to index.json")
    parser.add_argument("--min-words", "-m", type=int, default=200, help="Word count threshold (default: 200)")
    args = parser.parse_args()

    with open(args.catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = [p for p in data.get("products", []) if p.get("status", "aktiv") == "aktiv"]

    # Per-category stats
    categories = defaultdict(lambda: {"total": 0, "done": 0, "todo": 0, "products_todo": []})

    for p in products:
        cat = p.get("kategorieName", p.get("kategorie", "Unbekannt"))
        wc = len(p.get("beschreibung", "").split())
        categories[cat]["total"] += 1
        if wc >= args.min_words:
            categories[cat]["done"] += 1
        else:
            categories[cat]["todo"] += 1
            categories[cat]["products_todo"].append({
                "sku": p.get("sku", ""),
                "name": p.get("name", ""),
                "words": wc,
            })

    total_products = len(products)
    total_done = sum(c["done"] for c in categories.values())
    total_todo = total_products - total_done
    pct = total_done * 100 // total_products if total_products > 0 else 0

    # Progress bar
    bar_len = 40
    filled = bar_len * total_done // total_products if total_products > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"{'=' * 70}")
    print(f"FORTSCHRITT — PRODUKTBESCHREIBUNGEN")
    print(f"{'=' * 70}")
    print(f"\n  [{bar}] {pct}%")
    print(f"  {total_done}/{total_products} Produkte mit ≥{args.min_words} Wörtern")
    print(f"  {total_todo} noch zu bearbeiten")
    print(f"\n  Geschätzter Aufwand: ~{total_todo // 6 + 1} Batch-Durchläufe à 5-8 Produkte")

    # Per-priority breakdown
    for prio in [1, 2, 3]:
        prio_cats = [(name, stats) for name, stats in categories.items() if get_priority(name) == prio]
        if not prio_cats:
            continue

        prio_total = sum(s["total"] for _, s in prio_cats)
        prio_done = sum(s["done"] for _, s in prio_cats)
        prio_pct = prio_done * 100 // prio_total if prio_total > 0 else 0

        print(f"\n{'─' * 70}")
        print(f"PRIORITÄT {prio} — {prio_done}/{prio_total} erledigt ({prio_pct}%)")
        print(f"{'─' * 70}")
        print(f"{'Kategorie':<45} {'Erledigt':>10} {'Offen':>7}")

        for name, stats in sorted(prio_cats, key=lambda x: x[1]["todo"], reverse=True):
            done_str = f"{stats['done']}/{stats['total']}"
            status = "✓" if stats["todo"] == 0 else ""
            print(f"  {name:<43} {done_str:>10} {stats['todo']:>5}  {status}")

    # Next action queue
    print(f"\n{'=' * 70}")
    print(f"NÄCHSTE AKTIONEN (Prio 1 Kategorien mit offenen Produkten)")
    print(f"{'=' * 70}")

    for name, stats in sorted(categories.items(), key=lambda x: (get_priority(x[0]), -x[1]["todo"])):
        if stats["todo"] == 0:
            continue
        prio = get_priority(name)
        if prio > 2:  # Only show Prio 1 + 2 in action queue
            continue
        print(f"\n  → {name} (Prio {prio}, {stats['todo']} offen):")
        for p in sorted(stats["products_todo"], key=lambda x: x["words"])[:5]:
            print(f"    SKU {p['sku']}: {p['name']} ({p['words']} Wörter)")


if __name__ == "__main__":
    main()
