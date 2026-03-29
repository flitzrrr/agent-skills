#!/usr/bin/env python3
"""Quality-check product descriptions against SEO requirements.

Usage:
    python check_quality.py <updates.json> [--strict] [--min-words 200] [--max-words 350]

Checks each description against 8 criteria:
1. Word count within range
2. 4-paragraph structure
3. Focus keyword in first sentence
4. No banned superlatives
5. Cross-sell reference present
6. Formal address (no informal pronouns)
7. Meta-description-ready opening
8. Plain text only (no HTML/Markdown)
"""

import json
import sys
import re
import argparse

DEFAULT_BANNED_WORDS = [
    # English
    "best-in-class", "unparalleled", "revolutionary", "sensational",
    "unmatched", "world-leading", "game-changing",
    # German
    "erstklassig", "herausragend", "unschlagbar", "einzigartig",
    "revolutionaer", "sensationell", "unvergleichlich",
    "hoechstem niveau",
]

# Indicators that a cross-sell reference is present
CROSS_SELL_INDICATORS = [
    "combination with", "kombination mit", "in combination",
    "pairs well", "complement", "together with", "zusammen mit",
    "ergaenzend", "empfehlen wir", "passend dazu",
]

# Informal pronouns that indicate wrong tone (German du-form)
INFORMAL_PRONOUNS = [
    r'\bdu\b', r'\bdein\b', r'\bdeine\b', r'\bdeinem\b',
    r'\bdeinen\b', r'\bdeiner\b', r'\bdir\b', r'\bdich\b',
]


def check_description(product: dict, min_words: int = 200, max_words: int = 350,
                       strict: bool = False) -> dict:
    sku = product.get("sku", "?")
    name = product.get("name", "?")
    text = product.get("beschreibung", product.get("description", ""))

    results = {"sku": sku, "name": name, "checks": [], "passed": 0, "failed": 0, "warnings": 0}

    # 1. Word count
    words = len(text.split())
    if min_words <= words <= max_words:
        results["checks"].append(("PASS", f"Word count: {words} (target: {min_words}-{max_words})"))
        results["passed"] += 1
    elif words > max_words:
        results["checks"].append(("WARN", f"Word count: {words} -- above {max_words}, consider trimming"))
        results["warnings"] += 1
    else:
        results["checks"].append(("FAIL", f"Word count: {words} -- below {min_words} minimum"))
        results["failed"] += 1

    # 2. Paragraph structure
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) == 4:
        results["checks"].append(("PASS", f"4-paragraph structure: {len(paragraphs)} paragraphs"))
        results["passed"] += 1
    elif len(paragraphs) >= 3:
        results["checks"].append(("WARN", f"Paragraph structure: {len(paragraphs)} paragraphs (target: 4)"))
        results["warnings"] += 1
    else:
        results["checks"].append(("FAIL", f"Paragraph structure: only {len(paragraphs)} paragraphs (target: 4)"))
        results["failed"] += 1

    # 3. Focus keyword in first sentence
    first_sentence = text.split(".")[0].lower() if text else ""
    name_parts = name.lower().split()
    main_word = max(name_parts, key=len) if name_parts else ""
    if main_word and main_word in first_sentence:
        results["checks"].append(("PASS", f"Focus keyword in first sentence: '{main_word}' found"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL", f"Focus keyword missing in first sentence (expected: '{main_word}')"))
        results["failed"] += 1

    # 4. Banned superlatives
    text_lower = text.lower()
    found_banned = [w for w in DEFAULT_BANNED_WORDS if w in text_lower]
    if not found_banned:
        results["checks"].append(("PASS", "Tone: no banned superlatives"))
        results["passed"] += 1
    else:
        level = "FAIL" if strict else "WARN"
        results["checks"].append((level, f"Banned superlatives found: {', '.join(found_banned)}"))
        if strict:
            results["failed"] += 1
        else:
            results["warnings"] += 1

    # 5. Cross-sell reference (warning only — not all products have natural cross-sells)
    has_cross_sell = any(ind in text_lower for ind in CROSS_SELL_INDICATORS)
    if has_cross_sell:
        results["checks"].append(("PASS", "Cross-sell reference present"))
        results["passed"] += 1
    else:
        level = "FAIL" if strict else "WARN"
        results["checks"].append((level, "No cross-sell reference found"))
        if strict:
            results["failed"] += 1
        else:
            results["warnings"] += 1

    # 6. Formal address
    informal_found = []
    for pattern in INFORMAL_PRONOUNS:
        matches = re.findall(pattern, text_lower)
        informal_found.extend(matches)
    if not informal_found:
        results["checks"].append(("PASS", "Formal address maintained"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL", f"Informal pronouns found: {', '.join(set(informal_found))}"))
        results["failed"] += 1

    # 7. Meta description
    first_155 = text[:155]
    if len(first_155) >= 100 and "." in first_155:
        results["checks"].append(("PASS", f"Meta description: {len(first_155)} chars, contains sentence end"))
        results["passed"] += 1
    else:
        results["checks"].append(("WARN", "Meta description: first 155 chars may need adjustment"))
        results["warnings"] += 1

    # 8. No HTML/Markdown
    if re.search(r'<[^>]+>|#{1,6}\s|\*\*|__|\[.*\]\(.*\)', text):
        results["checks"].append(("FAIL", "HTML or Markdown detected -- plain text only"))
        results["failed"] += 1
    else:
        results["checks"].append(("PASS", "Plain text format (no HTML/Markdown)"))
        results["passed"] += 1

    return results


def main():
    parser = argparse.ArgumentParser(description="Quality-check product descriptions")
    parser.add_argument("updates_path", help="Path to updates JSON file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--min-words", type=int, default=200, help="Minimum word count (default: 200)")
    parser.add_argument("--max-words", type=int, default=350, help="Maximum word count (default: 350)")
    args = parser.parse_args()

    with open(args.updates_path, "r", encoding="utf-8") as f:
        updates = json.load(f)

    print(f"{'=' * 70}")
    print(f"QUALITY CHECK -- {len(updates)} descriptions")
    print(f"{'=' * 70}")

    total_pass = 0
    total_fail = 0
    total_warn = 0
    failed_products = []

    for product in updates:
        result = check_description(product, args.min_words, args.max_words, args.strict)
        total_pass += result["passed"]
        total_fail += result["failed"]
        total_warn += result["warnings"]

        status = "OK" if result["failed"] == 0 else "FAIL"
        print(f"\n[{status}] SKU {result['sku']}: {result['name']}"
              f" ({result['passed']}P/{result['failed']}F/{result['warnings']}W)")

        for check_type, msg in result["checks"]:
            icon = {"PASS": "  [+]", "FAIL": "  [-]", "WARN": "  [!]"}[check_type]
            print(f"  {icon} {msg}")

        if result["failed"] > 0:
            failed_products.append(f"SKU {result['sku']}: {result['name']}")

    total_checks = total_pass + total_fail + total_warn
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"Products:  {len(updates)}")
    print(f"Checks:    {total_checks} ({total_pass} passed, {total_fail} failed, {total_warn} warnings)")
    if total_checks > 0:
        print(f"Pass rate: {total_pass * 100 // total_checks}%")

    if failed_products:
        print(f"\nNeeds rework:")
        for fp in failed_products:
            print(f"  -> {fp}")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
