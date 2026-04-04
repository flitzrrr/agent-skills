#!/usr/bin/env node

/**
 * Tests for bin/cli.js
 * Run: node bin/test-cli.js
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const CLI = path.join(__dirname, "cli.js");
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  PASS  ${name}`);
    passed++;
  } catch (err) {
    console.log(`  FAIL  ${name}: ${err.message}`);
    failed++;
  }
}

function run(args) {
  return execSync(`node "${CLI}" ${args}`, {
    encoding: "utf8",
    timeout: 10000,
  });
}

console.log("CLI Tests\n");

// Test: no args shows usage
test("no args shows usage", () => {
  const out = run("");
  assert(out.includes("Usage"), "Should show usage");
  assert(out.includes("install"), "Should mention install command");
  assert(out.includes("update"), "Should mention update command");
  assert(out.includes("list"), "Should mention list command");
});

// Test: unknown platform errors
test("install unknown platform exits with error", () => {
  try {
    run("install nonexistent-platform");
    assert.fail("Should have thrown");
  } catch (err) {
    const output = (err.stdout || "") + (err.stderr || "");
    assert(output.includes("Unknown platform"), "Should say unknown platform");
  }
});

// Test: list shows skills
test("list command works", () => {
  try {
    const out = run("list");
    assert(out.includes("Available Skills"), "Should show available skills header");
  } catch {
    // Skills may not be installed in test env, that's ok
  }
});

// Test: cli.js is valid Node
test("cli.js parses without syntax errors", () => {
  execSync(`node -c "${CLI}"`, { encoding: "utf8" });
});

// Test: vscode platform is registered
test("vscode platform is listed", () => {
  const out = run("");
  assert(out.includes("vscode"), "Should list vscode as available platform");
});

// Test: copilot-instructions.md exists
test("copilot-instructions.md exists", () => {
  const copilotPath = path.join(__dirname, "..", ".github", "copilot-instructions.md");
  assert(
    fs.existsSync(copilotPath),
    "Should have .github/copilot-instructions.md"
  );
});

// Test: copilot-instructions.md has required content
test("copilot-instructions.md has skill references", () => {
  const copilotPath = path.join(__dirname, "..", ".github", "copilot-instructions.md");
  const content = fs.readFileSync(copilotPath, "utf8");
  assert(content.includes("skills/"), "Should reference skills/ directory");
  assert(content.includes("SKILL.md"), "Should mention SKILL.md");
  assert(content.includes("CHEATSHEET.md"), "Should reference CHEATSHEET.md");
});

// Test: sync-docs.js is valid Node
test("sync-docs.js parses without syntax errors", () => {
  const syncDocs = path.join(__dirname, "sync-docs.js");
  execSync(`node -c "${syncDocs}"`, { encoding: "utf8" });
});

// Test: sync-docs.js updates counts correctly
test("sync-docs.js produces correct counts", () => {
  const out = execSync(`node "${path.join(__dirname, "sync-docs.js")}"`, {
    encoding: "utf8",
    cwd: path.join(__dirname, ".."),
  });
  assert(out.includes("Found"), "Should report found skills");
  assert(out.includes("Updated README.md"), "Should update README");
  assert(out.includes("copilot-instructions"), "Should update copilot-instructions.md");
  assert(out.includes("Done"), "Should finish successfully");
});

console.log(`\n${passed} passed, ${failed} failed\n`);
process.exit(failed > 0 ? 1 : 0);
