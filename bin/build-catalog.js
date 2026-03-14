#!/usr/bin/env node

/**
 * Build catalog.json from all SKILL.md frontmatter.
 * Handles symlinks in skills/ that are relative to the repo root.
 *
 * Run: node bin/build-catalog.js
 * Output: docs/catalog.json
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const OUT = path.join(ROOT, "docs", "catalog.json");

function extractDescription(skillDir) {
  for (const name of ["SKILL.md", "skill.md"]) {
    const file = path.join(skillDir, name);
    if (!fs.existsSync(file)) continue;

    const content = fs.readFileSync(file, "utf8");
    const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
    if (fmMatch) {
      const descMatch = fmMatch[1].match(/description:\s*(.+?)(?:\n|$)/);
      if (descMatch) {
        let desc = descMatch[1].trim();
        const sentEnd = desc.match(/[.!?]\s/);
        if (sentEnd) desc = desc.substring(0, sentEnd.index + 1);
        if (desc.length > 150) desc = desc.substring(0, 147) + "...";
        return desc;
      }
    }
    // Fallback: first real line
    const lines = content
      .split("\n")
      .filter((l) => l.trim() && !l.startsWith("#") && !l.startsWith("---"));
    if (lines.length > 0) {
      let desc = lines[0].trim();
      const sentEnd = desc.match(/[.!?]\s/);
      if (sentEnd) desc = desc.substring(0, sentEnd.index + 1);
      if (desc.length > 150) desc = desc.substring(0, 147) + "...";
      return desc;
    }
  }
  return null;
}

function main() {
  if (!fs.existsSync(SKILLS_DIR)) {
    console.error("skills/ directory not found");
    process.exit(1);
  }

  const entries = fs.readdirSync(SKILLS_DIR);
  const catalog = [];

  for (const entry of entries) {
    const entryPath = path.join(SKILLS_DIR, entry);
    const stats = fs.lstatSync(entryPath);

    let realDir;
    if (stats.isSymbolicLink()) {
      // Symlinks are relative like ../../vendor/...
      // Resolve them relative to the REPO ROOT, not the skills/ dir
      const linkTarget = fs.readlinkSync(entryPath);
      // path.resolve(SKILLS_DIR, linkTarget) would resolve ../../ from skills/
      // but that goes to the git/ parent. We need to resolve from ROOT.
      // The symlinks start with ../../vendor/ from skills/, meaning ROOT/vendor/
      const normalized = linkTarget.replace(/^\.\.\/\.\.\//, "");
      realDir = path.join(ROOT, normalized);
    } else if (stats.isDirectory()) {
      realDir = entryPath;
    } else {
      continue;
    }

    const prefix = entry.split("-")[0];

    if (!fs.existsSync(realDir) || !fs.statSync(realDir).isDirectory()) {
      catalog.push({ name: entry, source: prefix, description: null });
      continue;
    }

    catalog.push({
      name: entry,
      source: prefix,
      description: extractDescription(realDir),
    });
  }

  catalog.sort((a, b) => a.name.localeCompare(b.name));

  const output = {
    generated: new Date().toISOString(),
    total: catalog.length,
    skills: catalog,
  };

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(output, null, 2));

  const withDesc = catalog.filter((s) => s.description).length;
  console.log(`Built catalog: ${output.total} skills, ${withDesc} with descriptions`);
  console.log(`Output: ${OUT}`);
}

main();
