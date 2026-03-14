#!/usr/bin/env node

/**
 * Build catalog.json from all SKILL.md frontmatter.
 * Searches recursively for SKILL.md and generates descriptions
 * for skills that lack frontmatter descriptions.
 *
 * Run: node bin/build-catalog.js
 * Output: docs/catalog.json
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const OUT = path.join(ROOT, "docs", "catalog.json");

function findSkillMd(dir, maxDepth) {
  if (maxDepth <= 0) return null;
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    // Check current directory first
    for (const e of entries) {
      if (e.isFile() && e.name.toLowerCase() === "skill.md") {
        return path.join(dir, e.name);
      }
    }
    // Then recurse into subdirectories
    for (const e of entries) {
      if (e.isDirectory() && e.name !== ".git" && e.name !== "node_modules") {
        const found = findSkillMd(path.join(dir, e.name), maxDepth - 1);
        if (found) return found;
      }
    }
  } catch {}
  return null;
}

function extractDescription(skillMdPath) {
  const content = fs.readFileSync(skillMdPath, "utf8");
  const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
  if (fmMatch) {
    // Multi-line description in quotes
    let descMatch = fmMatch[1].match(/description:\s*"([\s\S]*?)"/);
    if (!descMatch) {
      // Single-line description
      descMatch = fmMatch[1].match(/description:\s*(.+?)(?:\n|$)/);
    }
    if (descMatch) {
      let desc = descMatch[1].replace(/\s+/g, " ").trim();
      // First sentence
      const sentEnd = desc.match(/[.!?]\s/);
      if (sentEnd) desc = desc.substring(0, sentEnd.index + 1);
      if (desc.length > 150) desc = desc.substring(0, 147) + "...";
      return desc;
    }
  }
  // Fallback: first real paragraph
  const noFm = content.replace(/^---[\s\S]*?---\s*/, "");
  const lines = noFm
    .split("\n")
    .filter((l) => l.trim() && !l.startsWith("#") && !l.startsWith("```"));
  if (lines.length > 0) {
    let desc = lines[0].trim();
    const sentEnd = desc.match(/[.!?]\s/);
    if (sentEnd) desc = desc.substring(0, sentEnd.index + 1);
    if (desc.length > 150) desc = desc.substring(0, 147) + "...";
    return desc;
  }
  return null;
}

// Generate a human-readable description from the skill name
function descFromName(name) {
  const map = {
    "expo": "Expo SDK integration for React Native mobile app development.",
    "scientific": "Scientific computing and research automation toolkit.",
    // finance
    "finance-equity-research": "Equity research analysis and investment recommendations.",
    "finance-financial-analysis": "Financial modeling, valuation, and quantitative analysis.",
    "finance-investment-banking": "Investment banking deal execution and M&A advisory.",
    "finance-lseg": "LSEG (London Stock Exchange Group) data integration.",
    "finance-private-equity": "Private equity deal sourcing and portfolio management.",
    "finance-spglobal": "S&P Global market intelligence data integration.",
    "finance-wealth-management": "Wealth management and financial planning advisory.",
    // terraform
    "terraform-code-generation": "Generate Terraform HCL code from infrastructure requirements.",
    "terraform-module-generation": "Create reusable Terraform modules following best practices.",
    "terraform-provider-development": "Build custom Terraform providers for new infrastructure APIs.",
  };
  if (map[name]) return map[name];

  // Auto-generate from name
  const parts = name.replace(/^(tob|anthropic|agents|cloudflare|sentry)-/, "").split("-");
  const readable = parts.map((p) => p.charAt(0).toUpperCase() + p.slice(1)).join(" ");
  return `${readable}.`;
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
    let realDir;

    try {
      const stats = fs.lstatSync(entryPath);
      if (stats.isSymbolicLink()) {
        const linkTarget = fs.readlinkSync(entryPath);
        const normalized = linkTarget.replace(/^\.\.\/\.\.\//, "");
        realDir = path.join(ROOT, normalized);
      } else if (stats.isDirectory()) {
        realDir = entryPath;
      } else {
        continue;
      }
    } catch {
      continue;
    }

    const prefix = entry.split("-")[0];
    let description = null;

    if (fs.existsSync(realDir) && fs.statSync(realDir).isDirectory()) {
      // Search recursively for SKILL.md (max depth 4)
      const skillMd = findSkillMd(realDir, 4);
      if (skillMd) {
        description = extractDescription(skillMd);
      }
    }

    // Fallback: generate from name
    if (!description) {
      description = descFromName(entry);
    }

    catalog.push({
      name: entry,
      source: prefix,
      description,
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
