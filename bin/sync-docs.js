#!/usr/bin/env node

/**
 * Regenerates README.md badges/counts, sources table, repo structure,
 * AGENTS.md, CLAUDE.md, and .cursorrules based on current skills/ and vendor/ state.
 *
 * Run: node bin/sync-docs.js
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const VENDOR_DIR = path.join(ROOT, "vendor");

// Count skills and sources
const skills = fs
  .readdirSync(SKILLS_DIR)
  .filter((f) => !f.startsWith("."));
const sources = fs
  .readdirSync(VENDOR_DIR)
  .filter((f) => !f.startsWith(".") && fs.statSync(path.join(VENDOR_DIR, f)).isDirectory());

const skillCount = skills.length;
const sourceCount = sources.length;

console.log(`Found ${skillCount} skills from ${sourceCount} sources`);

// --- Update README.md ---
const readmePath = path.join(ROOT, "README.md");
let readme = fs.readFileSync(readmePath, "utf8");

// Update badge counts
readme = readme.replace(
  /skills-\d+-blue/,
  `skills-${skillCount}-blue`
);
readme = readme.replace(
  /sources-\d+-green/,
  `sources-${sourceCount}-green`
);

// Update intro line
readme = readme.replace(
  /\*\*\d+ agent skills\*\* from \*\*\d+ industry-leading sources\*\*/,
  `**${skillCount} agent skills** from **${sourceCount} industry-leading sources**`
);

// Update repo structure counts
readme = readme.replace(
  /skills\/\s+\d+ symlinks/,
  `skills/          ${skillCount} symlinks`
);
readme = readme.replace(
  /vendor\/\s+\d+ Git submodules/,
  `vendor/          ${sourceCount} Git submodules`
);

fs.writeFileSync(readmePath, readme, "utf8");
console.log("Updated README.md");

// --- Update AGENTS.md ---
const agentsPath = path.join(ROOT, "AGENTS.md");
if (fs.existsSync(agentsPath)) {
  let agents = fs.readFileSync(agentsPath, "utf8");
  agents = agents.replace(/\d+ skills/g, `${skillCount} skills`);
  agents = agents.replace(/\d+ sources/g, `${sourceCount} sources`);
  fs.writeFileSync(agentsPath, agents, "utf8");
  console.log("Updated AGENTS.md");
}

// --- Update CLAUDE.md ---
const claudePath = path.join(ROOT, "CLAUDE.md");
if (fs.existsSync(claudePath)) {
  let claude = fs.readFileSync(claudePath, "utf8");
  claude = claude.replace(/\d+ skills/g, `${skillCount} skills`);
  claude = claude.replace(/\d+ sources/g, `${sourceCount} sources`);
  fs.writeFileSync(claudePath, claude, "utf8");
  console.log("Updated CLAUDE.md");
}

// --- Update .cursorrules ---
const cursorPath = path.join(ROOT, ".cursorrules");
if (fs.existsSync(cursorPath)) {
  let cursor = fs.readFileSync(cursorPath, "utf8");
  cursor = cursor.replace(/\d+ skills/g, `${skillCount} skills`);
  cursor = cursor.replace(/\d+ sources/g, `${sourceCount} sources`);
  fs.writeFileSync(cursorPath, cursor, "utf8");
  console.log("Updated .cursorrules");
}

// --- Update .lovable ---
const lovablePath = path.join(ROOT, ".lovable");
if (fs.existsSync(lovablePath)) {
  let lovable = fs.readFileSync(lovablePath, "utf8");
  lovable = lovable.replace(/\d+ curated AI agent skills/, `${skillCount} curated AI agent skills`);
  lovable = lovable.replace(/\d+ skills/g, `${skillCount} skills`);
  lovable = lovable.replace(/\d+ sources/g, `${sourceCount} sources`);
  fs.writeFileSync(lovablePath, lovable, "utf8");
  console.log("Updated .lovable");
}

// --- Update .github/copilot-instructions.md ---
const copilotPath = path.join(ROOT, ".github", "copilot-instructions.md");
if (fs.existsSync(copilotPath)) {
  let copilot = fs.readFileSync(copilotPath, "utf8");
  copilot = copilot.replace(/\d+ curated AI agent skills/, `${skillCount} curated AI agent skills`);
  fs.writeFileSync(copilotPath, copilot, "utf8");
  console.log("Updated .github/copilot-instructions.md");
}

// --- Update CHEATSHEET.md ---
const cheatsheetPath = path.join(ROOT, "CHEATSHEET.md");
if (fs.existsSync(cheatsheetPath)) {
  let cheatsheet = fs.readFileSync(cheatsheetPath, "utf8");
  cheatsheet = cheatsheet.replace(/\d+ skills/g, `${skillCount} skills`);
  cheatsheet = cheatsheet.replace(/\d+ sources/g, `${sourceCount} sources`);
  fs.writeFileSync(cheatsheetPath, cheatsheet, "utf8");
  console.log("Updated CHEATSHEET.md");
}

// --- Generate skills list for AGENTS.md / CLAUDE.md ---
const skillList = skills.sort().map((s) => `- ${s}`).join("\n");
const marker = "<!-- SKILL_LIST -->";
const endMarker = "<!-- /SKILL_LIST -->";

for (const filePath of [agentsPath, claudePath]) {
  if (!fs.existsSync(filePath)) continue;
  let content = fs.readFileSync(filePath, "utf8");
  const startIdx = content.indexOf(marker);
  const endIdx = content.indexOf(endMarker);
  if (startIdx !== -1 && endIdx !== -1) {
    content =
      content.substring(0, startIdx + marker.length) +
      "\n" +
      skillList +
      "\n" +
      content.substring(endIdx);
    fs.writeFileSync(filePath, content, "utf8");
    console.log(`Updated skill list in ${path.basename(filePath)}`);
  }
}

console.log("Done.");

