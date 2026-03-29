---
name: product-description-seo
description: "End-to-end skill for SEO-optimized product descriptions: inventory analysis, generation, quality assurance, catalog update, and deployment. Use whenever the user wants to analyze, write, check, update, or deploy product descriptions — whether for a single product, a category, or an entire catalog. Triggers on: 'product description', 'Produktbeschreibung', 'SEO text', 'catalog text', 'update descriptions', 'which descriptions are missing', 'thin content', 'QA check', 'description quality', or when the user names a product category and wants texts for it. Also triggers on 'deploy' or 'commit' in the context of product descriptions."
---

# Product Description SEO — End-to-End Workflow

A complete pipeline for turning thin or missing product descriptions into SEO-optimized, structured content. Works with any JSON-based product catalog, any language, any industry.

## Quick Reference

| Phase | Task | Tool |
|-------|------|------|
| 1. Inventory | Analyze catalog, find thin descriptions | `scripts/analyze_catalog.py` |
| 2. Progress | Check current completion status | `scripts/track_progress.py` |
| 3. Extraction | Pull category products as batch-ready JSON | `scripts/extract_category.py` |
| 4. Generation | Write descriptions using 4-paragraph structure | See structure below |
| 5. QA | Automated quality check (8 criteria) | `scripts/check_quality.py` |
| 6. Update | Write descriptions back to catalog JSON | `scripts/update_catalog.py` |
| 7. Validation | Verify JSON structure after update | `scripts/validate_json.py` |
| 8. Rendering | Adapt frontend for multi-paragraph text | Code guidance below |
| 9. Deploy | Feature branch, PR, merge | Git workflow |

## Setup

Before first use, create a `product-seo-config.json` in the working directory to configure the skill for a specific catalog. This is optional — all scripts work without it using sensible defaults.

```json
{
  "catalog_path": "path/to/catalog/index.json",
  "company": {
    "name": "Company Name",
    "founded": "1990",
    "location": "City, Country",
    "expertise": "short description of domain expertise",
    "usp": "key selling points for the closing paragraph"
  },
  "fields": {
    "description": "beschreibung",
    "category": "kategorieName",
    "sku": "sku",
    "name": "name",
    "status": "status",
    "status_active_value": "aktiv"
  },
  "seo": {
    "min_words": 200,
    "max_words": 350,
    "language": "de",
    "primary_keyword_pattern": "{product_name} + {industry_term}",
    "banned_words": ["best-in-class", "unparalleled", "revolutionary", "world-leading"]
  },
  "target_audience": "procurement managers, facility managers, technical buyers",
  "tone": "professional, expert, trustworthy — like an experienced technical consultant",
  "priorities": {
    "1": ["Core Category A", "Core Category B"],
    "2": ["Secondary Category C"],
    "3": []
  }
}
```

## Catalog Format

The catalog must be a JSON file with a `products` array. Field names are configurable via `product-seo-config.json`:

```json
{
  "products": [
    {
      "sku": "401",
      "name": "Product Name",
      "beschreibung": "Current description text...",
      "kategorie": "category-slug",
      "kategorieName": "Category Display Name",
      "preis": 29.99,
      "einheit": "piece",
      "status": "aktiv",
      "slug": "product-name-401"
    }
  ]
}
```

Only the description field is updated. Everything else stays untouched.

---

## Phase 1: Inventory

Understand the current state of the catalog — which descriptions are too thin, which categories need work.

```bash
# Full catalog overview
python scripts/analyze_catalog.py <catalog.json>

# Single category (fuzzy match — "Tools" finds "Power Tools" etc.)
python scripts/analyze_catalog.py <catalog.json> --category "Tools"

# Custom word threshold
python scripts/analyze_catalog.py <catalog.json> --min-words 150
```

Output: per-category statistics (avg word count, products below threshold), top-20 thinnest descriptions, and when filtering by category a JSON export ready for batch prompting.

---

## Phase 2: Progress

Track the completion status of the description update campaign.

```bash
python scripts/track_progress.py <catalog.json>

# With priority configuration
python scripts/track_progress.py <catalog.json> --config product-seo-config.json
```

Output: progress bar, per-priority breakdown, next-action queue showing which categories and products to tackle next.

---

## Phase 3: Extraction

Pull products from a category as prompt-ready JSON.

```bash
# First 8 products
python scripts/extract_category.py <catalog.json> "Power Tools" --limit 8

# Thinnest descriptions first (most urgent)
python scripts/extract_category.py <catalog.json> "Power Tools" --thin-first

# Pagination for large categories
python scripts/extract_category.py <catalog.json> "Accessories" --offset 8 --limit 8
```

Category matching is fuzzy — partial matches work. If no match is found, available categories are listed.

---

## Phase 4: Generation

Write descriptions following the **4-paragraph structure**. Process **5-8 products per batch** maximum to maintain quality.

### 4-Paragraph Structure

**Paragraph 1 — Introduction and Value (50-80 words)**
Focus keyword (product name + industry/category term) in the **first sentence**. What is the product? What problem does it solve? Why does the target audience need it?

The first 155 characters must work standalone as a meta description — complete thought, ending with a period.

**Paragraph 2 — Technical Specifications (60-100 words)**
Materials, dimensions, weight, capacity, special features. **Every** technical fact from the existing description must be preserved 1:1. Never omit data, never fabricate specs. If source data is vague, keep it vague.

**Paragraph 3 — Application and Practice (40-60 words)**
Typical use cases, ideal conditions, when to deploy. Mention 1-2 complementary products from the same catalog (cross-sell). Use CROSS-SELL.md as reference if available.

**Paragraph 4 — Quality and Service (30-50 words)**
Company expertise, personal consultation, delivery/support promise. Soft CTA: "Contact us for personalized advice." No aggressive sales pressure. Adapt to the company info from config.

### Variant Rule

Products with color, size, or material variants **must get unique texts**. The variant attribute must be mentioned and contextualized — never copy the same text across variants. Example: a red variant could mention visibility advantages; a compact variant could highlight space efficiency.

### Tone

- Professional, expert, trustworthy — like an experienced technical consultant
- Formal address (German: "Sie"; English: naturally formal; adapt to language)
- **Banned words:** best-in-class, unparalleled, revolutionary, sensational, unmatched, premium (without proof), world-leading, perfect, unique (without proof)
- Superlatives only with concrete evidence (e.g., "proven for over 10 years")
- Adapt to `target_audience` and `tone` from config

### SEO Keywords

- **Primary:** [Product Name] + industry/category term
- **Secondary:** [Category Name], industry-standard terms
- **Longtail:** "[Product Name] buy/purchase", "[Product Name] for [use case]"
- Maximum 3x focus keyword per text — no keyword stuffing
- Use KEYWORDS.md for category-specific targets if available

### Output Format

Save descriptions as a JSON array:

```json
[
  {
    "sku": "401",
    "name": "Product Name",
    "beschreibung": "Paragraph 1...\n\nParagraph 2...\n\nParagraph 3...\n\nParagraph 4..."
  }
]
```

Save as `updates-<category-slug>.json`.

---

## Phase 5: Quality Assurance

Automated check against all requirements:

```bash
# Standard check
python scripts/check_quality.py updates-tools.json

# Strict mode (warnings become failures)
python scripts/check_quality.py updates-tools.json --strict

# Custom word range
python scripts/check_quality.py updates-tools.json --min-words 150 --max-words 400
```

Checks per description:

1. Word count within configured range (default 200-350)
2. 4-paragraph structure (exactly 3x `\n\n` separator)
3. Focus keyword (product name) in first sentence
4. No banned superlatives
5. Cross-sell reference present (company name or "combination with")
6. Formal address (no informal pronouns in German texts)
7. Meta-description-ready first 155 characters
8. Plain text only (no HTML, no Markdown, no bullet points)

Fix any failures, re-check. Proceed to Phase 6 only when all checks pass.

---

## Phase 6: Update

Write QA-approved descriptions back to the catalog:

```bash
python scripts/update_catalog.py <catalog.json> updates-tools.json
```

The script:
1. Creates an automatic backup (`catalog.json.backup_YYYYMMDD_HHMMSS`)
2. Matches updates by SKU
3. Reports word count before -> after per product
4. Flags SKUs not found in catalog

---

## Phase 7: Validation

Verify JSON integrity after the update:

```bash
python scripts/validate_json.py <catalog.json>
```

Checks: valid JSON parse, required fields on every product, no duplicate SKUs, no HTML tags in descriptions, valid slug format.

---

## Phase 8: Rendering

If the frontend renders descriptions as a single element, adapt it for multi-paragraph text. Paragraphs are separated by `\n\n` in the JSON.

**Svelte:**
```svelte
{#each description.split('\n\n') as paragraph}
  <p class="description">{paragraph}</p>
{/each}
```

**React:**
```jsx
{description.split('\n\n').map((p, i) => (
  <p key={i} className="description">{p}</p>
))}
```

**Vue:**
```vue
<p v-for="(p, i) in description.split('\n\n')" :key="i" class="description">{{ p }}</p>
```

**Meta description** — use the first paragraph, truncated:
```javascript
const metaDescription = description.split('\n\n')[0].slice(0, 155);
```

This change only needs to happen once and applies to all products.

---

## Phase 9: Deploy

Standard git workflow — never push directly to main.

```bash
git checkout -b product-descriptions/<category-slug>
git add path/to/catalog.json
git commit -m "content: Update product descriptions for <Category>"
gh pr create --title "Content: Product descriptions <Category>"
```

One PR per category or batch to keep reviews manageable.

---

## Example: Full Run

```bash
# 1. Where do we stand?
python scripts/track_progress.py catalog.json

# 2. Next category
python scripts/extract_category.py catalog.json "Tools" --thin-first

# 3. Generate descriptions (4-paragraph structure)
#    -> save as updates-tools.json

# 4. Quality check
python scripts/check_quality.py updates-tools.json

# 5. Write to catalog
python scripts/update_catalog.py catalog.json updates-tools.json

# 6. Validate JSON
python scripts/validate_json.py catalog.json

# 7. Commit and PR
git checkout -b product-descriptions/tools
git add catalog.json
git commit -m "content: Update product descriptions Tools (8 products)"
gh pr create --title "Content: Product descriptions Tools"
```

---

## Optional Reference Files

Not required, but improve output quality when present alongside the skill:

| File | Purpose |
|------|---------|
| KEYWORDS.md | Category-specific keyword targets (primary, secondary, longtail) |
| CROSS-SELL.md | Cross-sell matrix defining which categories reference each other |
| product-seo-config.json | Company context, field mappings, priorities |

Templates for KEYWORDS.md and CROSS-SELL.md are included — fill them in for your catalog.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/analyze_catalog.py` | Catalog analysis (thinnest descriptions, word counts) |
| `scripts/track_progress.py` | Progress tracking with priority support |
| `scripts/extract_category.py` | Category extraction for batch prompting (fuzzy match) |
| `scripts/check_quality.py` | Automated QA with 8 configurable checks |
| `scripts/update_catalog.py` | Write descriptions to catalog with automatic backup |
| `scripts/validate_json.py` | JSON structure validation |

## Dependencies

- **Python 3.10+** for all scripts
- **gh CLI** (optional) for PR creation in Phase 9
