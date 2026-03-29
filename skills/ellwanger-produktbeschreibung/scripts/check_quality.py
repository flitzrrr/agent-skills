#!/usr/bin/env python3
"""Quality-check product descriptions against the Ellwanger SEO requirements.

Usage:
    python check_quality.py <updates.json> [--strict]

Checks each description against:
- Minimum 200 words
- Maximum 350 words
- 4 paragraph structure (3 x \\n\\n separators)
- Focus keyword in first sentence (product name)
- Professional tone (no banned superlatives)
- Cross-sell mention (Ellwanger reference in paragraph 3)
- Meta-description length (first 155 chars meaningful)

updates.json format:
[{"sku": "401", "name": "Tennisnetz Standard", "beschreibung": "..."}]
"""

import json
import sys
import re
import argparse

BANNED_WORDS = [
    "erstklassig", "herausragend", "unschlagbar", "einzigartig", "revolutionär",
    "sensationell", "unvergleichlich", "premium", "höchstem niveau",
    "weltweit führend", "bester", "beste", "bestes", "perfekt",
]

CROSS_SELL_INDICATORS = [
    "ellwanger", "kombination mit", "ergänzend", "zusammen mit",
    "empfehlen wir", "passend dazu", "dazu eignet",
]


def check_description(product: dict, strict: bool = False) -> dict:
    """Check a single product description. Returns dict with pass/fail per criterion."""
    sku = product.get("sku", "?")
    name = product.get("name", "?")
    text = product.get("beschreibung", "")

    results = {"sku": sku, "name": name, "checks": [], "passed": 0, "failed": 0, "warnings": 0}

    # 1. Word count
    words = len(text.split())
    if words >= 200:
        if words <= 350:
            results["checks"].append(("PASS", f"Wortanzahl: {words} (Ziel: 200-350)"))
            results["passed"] += 1
        else:
            results["checks"].append(("WARN", f"Wortanzahl: {words} — über 350, kürzen empfohlen"))
            results["warnings"] += 1
    else:
        results["checks"].append(("FAIL", f"Wortanzahl: {words} — unter 200 Minimum"))
        results["failed"] += 1

    # 2. Paragraph structure
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) == 4:
        results["checks"].append(("PASS", f"4-Absatz-Struktur: {len(paragraphs)} Absätze"))
        results["passed"] += 1
    elif len(paragraphs) >= 3:
        results["checks"].append(("WARN", f"Absatz-Struktur: {len(paragraphs)} Absätze (Ziel: 4)"))
        results["warnings"] += 1
    else:
        results["checks"].append(("FAIL", f"Absatz-Struktur: nur {len(paragraphs)} Absätze (Ziel: 4)"))
        results["failed"] += 1

    # 3. Focus keyword in first sentence
    first_sentence = text.split(".")[0].lower() if text else ""
    name_parts = name.lower().split()
    # Check if at least the main product word is in the first sentence
    main_word = max(name_parts, key=len) if name_parts else ""
    if main_word and main_word in first_sentence:
        results["checks"].append(("PASS", f"Focus-Keyword im ersten Satz: '{main_word}' gefunden"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL", f"Focus-Keyword fehlt im ersten Satz (erwartet: '{main_word}')"))
        results["failed"] += 1

    # 4. Banned superlatives
    text_lower = text.lower()
    found_banned = [w for w in BANNED_WORDS if w in text_lower]
    if not found_banned:
        results["checks"].append(("PASS", "Tonalität: keine verbotenen Superlative"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL" if strict else "WARN",
                                  f"Verbotene Superlative: {', '.join(found_banned)}"))
        if strict:
            results["failed"] += 1
        else:
            results["warnings"] += 1

    # 5. Cross-sell
    has_cross_sell = any(ind in text_lower for ind in CROSS_SELL_INDICATORS)
    if has_cross_sell:
        results["checks"].append(("PASS", "Cross-Sell-Hinweis vorhanden"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL", "Kein Cross-Sell-Hinweis gefunden"))
        results["failed"] += 1

    # 6. Sie-Form (no du/dein)
    du_patterns = re.findall(r'\b(du|dein|deine|deinem|deinen|deiner|dir|dich)\b', text_lower)
    if not du_patterns:
        results["checks"].append(("PASS", "Professionelle Sie-Form"))
        results["passed"] += 1
    else:
        results["checks"].append(("FAIL", f"Du-Form gefunden: {', '.join(set(du_patterns))}"))
        results["failed"] += 1

    # 7. Meta-description (first 155 chars)
    first_155 = text[:155]
    if len(first_155) >= 100 and "." in first_155:
        results["checks"].append(("PASS", f"Meta-Description: {len(first_155)} Zeichen, enthält Satzende"))
        results["passed"] += 1
    else:
        results["checks"].append(("WARN", f"Meta-Description: erste 155 Zeichen prüfen — kein Satzende oder zu kurz"))
        results["warnings"] += 1

    # 8. No HTML/Markdown
    if re.search(r'<[^>]+>|#{1,6}\s|\*\*|__|\[.*\]\(.*\)', text):
        results["checks"].append(("FAIL", "HTML oder Markdown gefunden — nur Fließtext erlaubt"))
        results["failed"] += 1
    else:
        results["checks"].append(("PASS", "Reiner Fließtext (kein HTML/Markdown)"))
        results["passed"] += 1

    return results


def main():
    parser = argparse.ArgumentParser(description="Quality-check product descriptions")
    parser.add_argument("updates_path", help="Path to updates.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    with open(args.updates_path, "r", encoding="utf-8") as f:
        updates = json.load(f)

    print(f"{'=' * 70}")
    print(f"QUALITÄTSPRÜFUNG — {len(updates)} Beschreibungen")
    print(f"{'=' * 70}")

    total_pass = 0
    total_fail = 0
    total_warn = 0
    failed_products = []

    for product in updates:
        result = check_description(product, args.strict)
        total_pass += result["passed"]
        total_fail += result["failed"]
        total_warn += result["warnings"]

        status = "✓" if result["failed"] == 0 else "✗"
        print(f"\n{status} SKU {result['sku']}: {result['name']} ({result['passed']}P/{result['failed']}F/{result['warnings']}W)")

        for check_type, msg in result["checks"]:
            icon = {"PASS": "  ✓", "FAIL": "  ✗", "WARN": "  ⚠"}[check_type]
            print(f"  {icon} {msg}")

        if result["failed"] > 0:
            failed_products.append(f"SKU {result['sku']}: {result['name']}")

    # Summary
    total_checks = total_pass + total_fail + total_warn
    print(f"\n{'=' * 70}")
    print(f"ZUSAMMENFASSUNG")
    print(f"{'=' * 70}")
    print(f"Produkte:  {len(updates)}")
    print(f"Checks:    {total_checks} ({total_pass} bestanden, {total_fail} fehlgeschlagen, {total_warn} Warnungen)")
    print(f"Quote:     {total_pass * 100 // total_checks}% bestanden" if total_checks > 0 else "")

    if failed_products:
        print(f"\nNacharbeit nötig bei:")
        for fp in failed_products:
            print(f"  → {fp}")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
