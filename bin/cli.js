#!/usr/bin/env node

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

const REPO_URL = "https://github.com/flitzrrr/agent-skills.git";
const SKILL_DIR = path.join(os.homedir(), ".agent-skills");

const PLATFORMS = {
  claude: {
    name: "Claude Code",
    dir: null, // CLAUDE.md approach — project-level
    note: "Clone repo into your project. CLAUDE.md will be auto-discovered.",
  },
  antigravity: {
    name: "Antigravity (Gemini)",
    dir: path.join(os.homedir(), ".gemini", "antigravity", "skills"),
  },
  codex: {
    name: "Codex (OpenAI)",
    dir: path.join(os.homedir(), ".codex", "skills"),
  },
  opencode: {
    name: "OpenCode",
    dir: path.join(os.homedir(), ".config", "opencode", "skills"),
  },
  cursor: {
    name: "Cursor",
    dir: null,
    note: "Clone repo into your workspace. .cursorrules will be auto-loaded.",
  },
};

function log(msg) {
  console.log(`  ${msg}`);
}

function header(msg) {
  console.log(`\n🧠 ${msg}\n`);
}

function cloneRepo() {
  if (fs.existsSync(SKILL_DIR)) {
    log("Updating existing installation...");
    execSync(`git -C "${SKILL_DIR}" pull --quiet`, { stdio: "inherit" });
    execSync(
      `git -C "${SKILL_DIR}" submodule update --remote --merge --quiet`,
      { stdio: "inherit" }
    );
  } else {
    log("Cloning agent-skills repository...");
    execSync(
      `git clone --recurse-submodules --quiet "${REPO_URL}" "${SKILL_DIR}"`,
      { stdio: "inherit" }
    );
  }
}

function installForPlatform(platform) {
  const config = PLATFORMS[platform];
  if (!config) {
    console.error(`Unknown platform: ${platform}`);
    console.error(`Available: ${Object.keys(PLATFORMS).join(", ")}`);
    process.exit(1);
  }

  if (!config.dir) {
    log(`${config.name}: ${config.note}`);
    return;
  }

  fs.mkdirSync(config.dir, { recursive: true });

  const skillsDir = path.join(SKILL_DIR, "skills");
  const entries = fs.readdirSync(skillsDir);
  let added = 0;
  let skipped = 0;

  for (const entry of entries) {
    const target = path.join(config.dir, entry);
    const source = path.join(skillsDir, entry);

    if (fs.existsSync(target)) {
      skipped++;
      continue;
    }

    try {
      fs.symlinkSync(source, target, "junction");
      added++;
    } catch {
      // Skip if symlink fails
      skipped++;
    }
  }

  log(`${config.name}: ${added} skills added, ${skipped} skipped (existing)`);
}

function listSkills() {
  const skillsDir = path.join(SKILL_DIR, "skills");
  if (!fs.existsSync(skillsDir)) {
    console.error("Skills not installed. Run: npx @flitzrrr/agent-skills install");
    process.exit(1);
  }
  const entries = fs.readdirSync(skillsDir).sort();
  header(`${entries.length} Available Skills`);
  entries.forEach((s) => log(`  • ${s}`));
}

// Main CLI
const [, , command, ...args] = process.argv;

switch (command) {
  case "install": {
    header("Agent Skills Hub — Installation");
    cloneRepo();

    const platform = args[0];
    if (platform) {
      installForPlatform(platform);
    } else {
      log("\nInstalling for all platforms...\n");
      for (const p of Object.keys(PLATFORMS)) {
        installForPlatform(p);
      }
    }

    log("\n✅ Done! See CHEATSHEET.md for which skill to use when.");
    log(`   ${SKILL_DIR}/CHEATSHEET.md`);
    break;
  }

  case "update": {
    header("Updating Agent Skills...");
    cloneRepo();
    log("\n✅ All skills updated to latest versions.");
    break;
  }

  case "list": {
    listSkills();
    break;
  }

  default: {
    header("Agent Skills Hub — CLI");
    log("Usage:");
    log("  npx @flitzrrr/agent-skills install              # Install for all platforms");
    log("  npx @flitzrrr/agent-skills install <platform>    # Install for specific platform");
    log("  npx @flitzrrr/agent-skills update                # Update all skills");
    log("  npx @flitzrrr/agent-skills list                  # List all skills");
    log("");
    log("Platforms: " + Object.keys(PLATFORMS).join(", "));
    break;
  }
}
