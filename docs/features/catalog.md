---
type: documentation
entity: feature
feature: "catalog"
version: 1.0
---

# Feature: Catalog

> Part of [Agent Skills Hub](../overview.md)

## Summary

A searchable skill catalog published as a GitHub Pages site and mirrored to the GitHub Wiki. Built automatically from SKILL.md frontmatter across all skills.

## How It Works

### User Flow

1. User visits https://flitzrrr.github.io/agent-skills/
2. Searchable HTML page shows all skills with name, source, and description
3. Alternatively, the GitHub Wiki at https://github.com/flitzrrr/agent-skills/wiki provides a markdown-formatted catalog grouped by source

### Technical Flow

1. `build-catalog.js` iterates all entries in `skills/`
2. For each skill, resolves symlinks to find the real directory
3. Searches recursively (max depth 4) for `SKILL.md`
4. Extracts description from YAML frontmatter (quoted, multi-line, or single-line) or first paragraph
5. Falls back to a hardcoded map or auto-generated description from the skill name
6. Writes `docs/catalog.json` with skill name, source prefix, and description
7. `docs/index.html` reads `catalog.json` client-side and renders the searchable UI
8. `update-wiki.js` clones the wiki repo, generates `Skills-Catalog.md` grouped by source, pushes

## Implementation

| Module                           | Symbols               | Role                                          |
| -------------------------------- | --------------------- | --------------------------------------------- |
| [build](../modules/build.md)    | `findSkillMd`         | Recursively locates SKILL.md in skill dirs    |
| [build](../modules/build.md)    | `extractDescription`  | Parses frontmatter for description            |
| [build](../modules/build.md)    | `descFromName`        | Generates fallback description from skill name|
| [build](../modules/build.md)    | `update-wiki.js`      | Generates wiki markdown from catalog.json     |

## Configuration

- **Output path**: `docs/catalog.json` (hardcoded)
- **Wiki repo**: `git@github.com:flitzrrr/agent-skills.wiki.git` (hardcoded in `update-wiki.js`)
- **GitHub Pages**: Served from `docs/` directory on the `main` branch

## Edge Cases & Limitations

- **Description extraction**: Skills with non-standard frontmatter or no first paragraph get an auto-generated description like "Foo Bar tooling and automation." — these are low quality
- **Hardcoded fallback map**: `descFromName()` has a manual map for ~15 skills whose YAML doesn't parse cleanly — this needs maintenance when those skills change
- **Wiki push failures**: Requires SSH access; CI uses `x-access-token` via GITHUB_TOKEN

## Related Features

- [Auto-Discovery](auto-discovery.md) — triggers catalog rebuild after adding new sources
- [Vendor Sync](vendor-sync.md) — upstream changes may add/change SKILL.md frontmatter
