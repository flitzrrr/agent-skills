#!/usr/bin/env python3
"""Validate catalog JSON structure after description updates.

Usage:
    python validate_json.py <catalog.json>

Checks: valid JSON, required fields, no duplicate SKUs,
no HTML in descriptions, valid slug format.
"""

import json
import sys
import re
from collections import Counter

REQUIRED_FIELDS = ["sku", "name", "slug"]


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <catalog.json>")
        sys.exit(1)

    path = sys.argv[1]
    errors = []
    warnings = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[-] FATAL: Invalid JSON: {e}")
        sys.exit(1)

    products = data.get("products", [])
    print(f"Validating {len(products)} products in {path}...")

    # Required fields
    for i, p in enumerate(products):
        for field in REQUIRED_FIELDS:
            if field not in p:
                errors.append(f"Product #{i} (SKU {p.get('sku', '?')}): missing field '{field}'")

    # Duplicate SKUs
    skus = [p.get("sku", "") for p in products]
    dupes = [sku for sku, count in Counter(skus).items() if count > 1]
    if dupes:
        errors.append(f"Duplicate SKUs: {', '.join(dupes)}")

    # Empty descriptions
    desc_field = "beschreibung" if any("beschreibung" in p for p in products[:5]) else "description"
    for p in products:
        if not p.get(desc_field, "").strip():
            warnings.append(f"SKU {p.get('sku', '?')}: empty description")

    # HTML in descriptions
    for p in products:
        desc = p.get(desc_field, "")
        if re.search(r'<[^>]+>', desc):
            errors.append(f"SKU {p.get('sku', '?')}: HTML tags found in description")

    # Slug format
    for p in products:
        slug = p.get("slug", "")
        if slug and not re.match(r'^[a-z0-9\-_\.]+$', slug):
            warnings.append(f"SKU {p.get('sku', '?')}: slug '{slug}' contains invalid characters")

    # Report
    print(f"\n{'=' * 50}")
    if errors:
        print(f"[-] {len(errors)} errors found:")
        for e in errors:
            print(f"  [-] {e}")
    if warnings:
        print(f"[!] {len(warnings)} warnings:")
        for w in warnings:
            print(f"  [!] {w}")
    if not errors and not warnings:
        print("[+] All validations passed!")
    elif not errors:
        print(f"\n[+] No critical errors. {len(warnings)} warnings.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
