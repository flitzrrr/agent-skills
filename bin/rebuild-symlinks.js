#!/usr/bin/env node

/**
 * Rebuilds all skill symlinks from vendor/ submodules.
 *
 * Each SKILL.md found in vendor/<source>/ gets a symlink in skills/ with the
 * naming convention: <prefix>-<skill_name>
 *
 * Prefix mapping is defined explicitly for known sources, with a fallback
 * to the first segment of the vendor directory name.
 *
 * Run: node bin/rebuild-symlinks.js
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const VENDOR_DIR = path.join(ROOT, "vendor");

// Explicit prefix mapping: vendor directory name → skill prefix
const PREFIX_MAP = {
  "trailofbits-skills": "tob",
  "anthropic-skills": "anthropic",
  "anthropic-finance": "finance",
  "vercel-agent-skills": "vercel",
  "getsentry-skills": "sentry",
  "google-stitch-skills": "google",
  "cloudflare-skills": "cloudflare",
  "stripe-skills": "stripe",
  "expo-skills": "expo",
  "hashicorp-skills": "hashicorp",
  "supabase-skills": "supabase",
  "callstack-skills": "callstack",
  "scientific-skills": "scientific",
  "opencode-processing-skills": "opencode",
  "agentic-seo-skill": "seo",
  "marketingskills": null, // no prefix, use skill name directly
  "addyosmani-agent-skills": "addyosmani",
  "itsmostafa-aws-agent-skills": "aws",
  "MoizIbnYousaf-Ai-Agent-Skills": "MoizIbnYousaf",
  "JackyST0-awesome-agent-skills": "JackyST0",
};

function getPrefix(vendorName) {
  if (vendorName in PREFIX_MAP) return PREFIX_MAP[vendorName];
  // Fallback: first segment before first hyphen
  return vendorName.split("-")[0];
}

function findSkillMds(dir, maxDepth, results) {
  if (maxDepth <= 0) return;
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    if (e.name === ".git" || e.name === "node_modules") continue;
    const full = path.join(dir, e.name);
    if (e.isFile() && e.name.toLowerCase() === "skill.md") {
      results.push(path.dirname(full));
    } else if (e.isDirectory()) {
      findSkillMds(full, maxDepth - 1, results);
    }
  }
}

function main() {
  // Preserve manually-created skill directories (non-symlinks)
  const manualSkills = new Set();
  if (fs.existsSync(SKILLS_DIR)) {
    for (const entry of fs.readdirSync(SKILLS_DIR)) {
      const entryPath = path.join(SKILLS_DIR, entry);
      const stat = fs.lstatSync(entryPath);
      if (stat.isDirectory() && !stat.isSymbolicLink()) {
        manualSkills.add(entry);
      }
    }
  }

  // Remove all existing symlinks
  if (fs.existsSync(SKILLS_DIR)) {
    for (const entry of fs.readdirSync(SKILLS_DIR)) {
      const entryPath = path.join(SKILLS_DIR, entry);
      if (fs.lstatSync(entryPath).isSymbolicLink()) {
        fs.unlinkSync(entryPath);
      }
    }
  } else {
    fs.mkdirSync(SKILLS_DIR);
  }

  let created = 0;
  let skipped = 0;
  const vendors = fs.readdirSync(VENDOR_DIR).filter((d) => {
    const p = path.join(VENDOR_DIR, d);
    return !d.startsWith(".") && fs.statSync(p).isDirectory();
  });

  for (const vendor of vendors) {
    const vendorPath = path.join(VENDOR_DIR, vendor);
    const prefix = getPrefix(vendor);
    const skillDirs = [];
    findSkillMds(vendorPath, 5, skillDirs);

    // Special case: seo skill — single top-level link
    if (vendor === "agentic-seo-skill") {
      const linkName = "seo";
      const target = `../vendor/${vendor}`;
      if (!manualSkills.has(linkName)) {
        fs.symlinkSync(target, path.join(SKILLS_DIR, linkName));
        created++;
      }
      continue;
    }

    for (const skillDir of skillDirs) {
      const skillName = path.basename(skillDir);
      const linkName = prefix ? `${prefix}-${skillName}` : skillName;

      // Don't overwrite manual skills
      if (manualSkills.has(linkName)) {
        skipped++;
        continue;
      }

      // Relative path from skills/ to the skill directory
      const relPath = path.relative(SKILLS_DIR, skillDir);
      const target = `../vendor/${path.relative(VENDOR_DIR, skillDir)}`;

      try {
        // Check for name collisions
        const linkPath = path.join(SKILLS_DIR, linkName);
        if (fs.existsSync(linkPath) || fs.lstatSync(linkPath).isSymbolicLink()) {
          // Already exists, skip
          skipped++;
          continue;
        }
      } catch {
        // lstatSync throws if path doesn't exist — that's what we want
      }

      try {
        fs.symlinkSync(target, path.join(SKILLS_DIR, linkName));
        created++;
      } catch (err) {
        // Name collision from a different vendor
        skipped++;
      }
    }
  }

  console.log(`Rebuilt symlinks: ${created} created, ${skipped} skipped (manual or collision)`);
  console.log(`Manual skill dirs preserved: ${[...manualSkills].join(", ") || "(none)"}`);
  console.log(`Total skills/ entries: ${fs.readdirSync(SKILLS_DIR).length}`);
}

main();
