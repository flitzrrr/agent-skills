#!/usr/bin/env node

/**
 * Update the GitHub Wiki with current catalog data.
 * Clones the wiki repo, regenerates the Skills-Catalog page, and pushes.
 *
 * Run: node bin/update-wiki.js
 * Requires: git, SSH access to the wiki repo
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const CATALOG = path.join(ROOT, "docs", "catalog.json");
const WIKI_DIR = "/tmp/agent-skills-wiki";
const WIKI_REPO = "git@github.com:flitzrrr/agent-skills.wiki.git";

function run(cmd, opts) {
  return execSync(cmd, { encoding: "utf8", ...opts }).trim();
}

function groupBy(arr, key) {
  const map = {};
  for (const item of arr) {
    const k = item[key];
    (map[k] = map[k] || []).push(item);
  }
  return map;
}

function main() {
  if (!fs.existsSync(CATALOG)) {
    console.error("catalog.json not found. Run build-catalog.js first.");
    process.exit(1);
  }

  const catalog = JSON.parse(fs.readFileSync(CATALOG, "utf8"));
  const grouped = groupBy(catalog.skills, "source");
  const sourceEntries = Object.entries(grouped).sort((a, b) => b[1].length - a[1].length);

  // Clone wiki
  try {
    if (fs.existsSync(WIKI_DIR)) {
      run(`rm -rf ${WIKI_DIR}`);
    }
    run(`git clone ${WIKI_REPO} ${WIKI_DIR}`);
  } catch (e) {
    console.error("Failed to clone wiki repo:", e.message);
    process.exit(1);
  }

  // Generate Skills-Catalog.md
  let md = `# Skills Catalog\n\n`;
  md += `> Last updated: ${catalog.generated.split("T")[0]} | **${catalog.total} skills** across **${sourceEntries.length} sources**\n\n`;
  md += `The full searchable catalog with copy-to-clipboard is on the [GitHub Pages site](https://flitzrrr.github.io/agent-skills/#catalog).\n\n`;
  md += `## Skills by Source\n\n`;

  for (const [source, skills] of sourceEntries) {
    md += `### ${source} (${skills.length} skills)\n\n`;
    md += `| Skill | Description |\n`;
    md += `|-------|-------------|\n`;
    for (const s of skills) {
      const desc = s.description || "--";
      md += `| \`${s.name}\` | ${desc} |\n`;
    }
    md += `\n`;
  }

  fs.writeFileSync(path.join(WIKI_DIR, "Skills-Catalog.md"), md);

  // Update Home page stats
  const homePath = path.join(WIKI_DIR, "Home.md");
  if (fs.existsSync(homePath)) {
    let home = fs.readFileSync(homePath, "utf8");
    // Update skill count references
    home = home.replace(/\b\d{2,4}\+?\s+skills\b/gi, `${catalog.total}+ skills`);
    fs.writeFileSync(homePath, home);
  }

  // Commit and push
  try {
    run("git add -A", { cwd: WIKI_DIR });
    const diff = run("git diff --cached --stat", { cwd: WIKI_DIR });
    if (!diff) {
      console.log("Wiki is already up to date.");
      return;
    }

    run(`git config user.name "github-actions[bot]"`, { cwd: WIKI_DIR });
    run(`git config user.email "github-actions[bot]@users.noreply.github.com"`, { cwd: WIKI_DIR });
    run(`git commit -m "docs: update skill catalog [${catalog.generated.split("T")[0]}]"`, { cwd: WIKI_DIR });
    run("git push origin master", { cwd: WIKI_DIR });
    console.log("Wiki updated and pushed.");
  } catch (e) {
    console.error("Failed to push wiki:", e.message);
    process.exit(1);
  }
}

main();
