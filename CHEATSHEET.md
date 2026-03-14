# 🗺️ Agent Skills Cheatsheet

> Quick decision guide: **which skill, when, and why.**

---

## ⚡ Quick Decision Matrix

| You want to... | Use this skill | Source | Rating |
|---|---|---|---|
| **Security audit** code changes | `security-review` | Sentry | ★★★★★ |
| **Code review** a PR | `code-review` | Sentry | ★★★★★ |
| **Find bugs** in local changes | `find-bugs` | Sentry | ★★★★★ |
| **Audit GH Actions** for supply chain attacks | `gha-security-review` | Sentry | ★★★★★ |
| **Review Django access control** / IDOR | `django-access-review` | Sentry | ★★★★☆ |
| **Review Django performance** / N+1 queries | `django-perf-review` | Sentry | ★★★★☆ |
| **Write a commit message** (Conventional Commits) | `commit` | Sentry | ★★★★★ |
| **Create a branch** | `create-branch` | Sentry | ★★★★☆ |
| **Write a PR description** | `pr-writer` | Sentry | ★★★★★ |
| **Fix CI failures** iteratively | `iterate-pr` | Sentry | ★★★★★ |
| **Simplify** complex code | `code-simplifier` | Sentry | ★★★★☆ |
| **Scan skills** for prompt injection | `skill-scanner` | Sentry | ★★★★☆ |
| **Create new skills** | `skill-writer` / `anthropic-skill-creator` | Sentry / Anthropic | ★★★★☆ |
| **Run SEO audit** on a website | `seo` | Agentic SEO | ★★★★★ |
| **Plan a multi-session** project | `create-plan` | OpenCode | ★★★★★ |
| **Resume** a previous plan | `resume-plan` | OpenCode | ★★★★★ |
| **Execute** a work packet from plan | `execute-work-packet` | OpenCode | ★★★★★ |
| **Generate project docs** | `generate-docs` | OpenCode | ★★★★☆ |
| **Update existing docs** | `update-docs` | OpenCode | ★★★★☆ |
| **Create handover** summary for next session | `generate-handover` | OpenCode | ★★★★☆ |
| **Create/edit PDFs** | `anthropic-pdf` | Anthropic | ★★★★★ |
| **Create/edit Word docs** | `anthropic-docx` | Anthropic | ★★★★★ |
| **Create presentations** | `anthropic-pptx` | Anthropic | ★★★★★ |
| **Create/edit spreadsheets** | `anthropic-xlsx` | Anthropic | ★★★★★ |
| **Build an MCP server** | `anthropic-mcp-builder` | Anthropic | ★★★★★ |
| **Test web apps** with Playwright | `anthropic-webapp-testing` | Anthropic | ★★★★★ |
| **Design stunning frontends** | `anthropic-frontend-design` | Anthropic | ★★★★★ |
| **Build Claude API apps** | `anthropic-claude-api` | Anthropic | ★★★★★ |
| **Create generative art** with p5.js | `anthropic-algorithmic-art` | Anthropic | ★★★★☆ |
| **Design artistic visuals** (posters, canvases) | `anthropic-canvas-design` | Anthropic | ★★★★☆ |
| **Apply professional themes** to artifacts | `anthropic-theme-factory` | Anthropic | ★★★★☆ |
| **Write internal comms** (3P, newsletters) | `anthropic-internal-comms` | Anthropic | ★★★☆☆ |
| **Create Slack GIFs** | `anthropic-slack-gif-creator` | Anthropic | ★★★☆☆ |
| **Build complex React artifacts** | `anthropic-web-artifacts-builder` | Anthropic | ★★★★☆ |
| **Coauthor documents** collaboratively | `anthropic-doc-coauthoring` | Anthropic | ★★★★☆ |
| **Optimize React/Next.js** performance | `vercel-react-best-practices` | Vercel | ★★★★★ |
| **Audit web UI** for accessibility & UX | `vercel-web-design-guidelines` | Vercel | ★★★★★ |
| **Fix React component architecture** | `vercel-composition-patterns` | Vercel | ★★★★☆ |
| **Build React Native** apps | `vercel-react-native-skills` | Vercel | ★★★★☆ |
| **Deploy to Vercel** | `vercel-deploy-to-vercel` | Vercel | ★★★★☆ |

---

## 🏗️ Skills by Source

### 🔒 Sentry (getsentry/skills) — 24 skills

Security, code quality, and Git workflow. Battle-tested at scale.

#### Tier 1 — Must-Have

| Skill | Purpose |
|-------|---------|
| `security-review` | OWASP-based security audit with exploitation-focused analysis |
| `code-review` | Comprehensive code review following engineering best practices |
| `find-bugs` | Bug hunting in local branch changes with security prioritization |
| `gha-security-review` | GitHub Actions supply chain security analysis |
| `commit` | Conventional Commits formatting with AI attribution |
| `pr-writer` | Structured PR descriptions (what & why) |
| `iterate-pr` | Automated CI fix loop until green + review feedback resolution |
| `create-branch` | Branch creation with naming conventions |

#### Tier 2 — Highly Useful

| Skill | Purpose |
|-------|---------|
| `django-access-review` | Django IDOR & access control review |
| `django-perf-review` | Django N+1 queries & performance optimization |
| `code-simplifier` | Reduce complexity while maintaining functionality |
| `skill-scanner` | Security analysis of agent skills for prompt injection |
| `skill-writer` / `skill-creator` | Create new agent skills following best practices |
| `create-pr` | Direct PR creation workflow |

#### Tier 3 — Specialized

| Skill | Purpose |
|-------|---------|
| `agents-md` | AGENTS.md file management |
| `blog-writing-guide` | Technical blog post creation |
| `brand-guidelines` | Brand consistency enforcement |
| `claude-settings-audit` | Claude configuration audit |
| `doc-coauthoring` | Collaborative document editing |
| `gh-review-requests` | GitHub review request management |
| `presentation-creator` | Slide deck creation |
| `sred-project-organizer` / `sred-work-summary` | SR&ED tax credit documentation |

---

### 🔍 Agentic SEO (Bhanunamikaze) — 16 sub-skills

Comprehensive SEO auditing toolkit with Playwright integration.

| Sub-Skill | Purpose |
|-----------|---------|
| `seo audit` | Full technical + on-page + performance audit |
| `seo page` | Individual page analysis (meta, headings, content) |
| `seo schema` | Schema.org structured data validation |
| `seo sitemap` | Sitemap analysis and validation |
| `seo robots` | robots.txt evaluation |
| `seo images` | Image optimization (alt text, size, format) |
| `seo links` | Internal/external link analysis |
| `seo performance` | Core Web Vitals & speed metrics |
| `seo mobile` | Mobile-friendliness check |
| `seo social` | Open Graph & social meta validation |
| `seo accessibility` | WCAG accessibility audit |
| `seo security` | HTTPS, headers, CSP analysis |
| `seo competitive` | Competitor comparison |
| `seo keyword` | Keyword research & density analysis |
| `seo content` | Content quality & readability scoring |
| `seo report` | Comprehensive PDF/HTML report generation |

**Dependencies:** Python 3.8+, optional Playwright for JS-heavy sites

---

### 📋 OpenCode Processing (DasDigitaleMomentum) — 9 skills

Multi-session project planning and documentation framework.

| Skill | Purpose | When |
|-------|---------|------|
| `create-plan` | Initialize structured project plan | Starting a new multi-step project |
| `resume-plan` | Continue previous session's plan | Returning to unfinished work |
| `update-plan` | Modify plan with new requirements | Scope changes mid-project |
| `execute-work-packet` | Execute a specific plan item | Implementing individual tasks |
| `generate-docs` | Create project documentation | After major milestones |
| `update-docs` | Update existing documentation | After changes to documented features |
| `generate-handover` | Create session handover summary | End of work session |
| `archive-legacy-docs` | Archive outdated documentation | During documentation cleanup |
| `author-and-verify-implementation-plan` | Write & validate implementation plans | Before complex implementations |

---

### 🎨 Anthropic (anthropics/skills) — 17 skills

Document creation, creative design, developer tools, and enterprise workflows.

#### Document Skills (Source-Available)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| `anthropic-pdf` | PDF read/write/merge/split/OCR | pypdf, pdfplumber, reportlab, pytesseract |
| `anthropic-docx` | Word document creation & editing | docx-js (new), XML manipulation (edit), tracked changes |
| `anthropic-pptx` | Presentation creation & editing | pptxgenjs (new), XML (edit), visual QA workflow |
| `anthropic-xlsx` | Spreadsheet creation & analysis | openpyxl, pandas, formula recalculation |

#### Creative & Design

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| `anthropic-frontend-design` | Production-grade UI design | Bold aesthetics, anti-AI-slop philosophy |
| `anthropic-canvas-design` | Artistic visual creation (posters, art) | Design philosophy → canvas execution pipeline |
| `anthropic-algorithmic-art` | Generative art with p5.js | Seeded randomness, interactive parameter exploration |
| `anthropic-theme-factory` | 10 professional themes for any artifact | Color palettes + font pairings, custom theme creation |
| `anthropic-slack-gif-creator` | Animated GIFs optimized for Slack | PIL/Pillow, GIFBuilder, easing functions |

#### Developer Tools

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| `anthropic-mcp-builder` | Build MCP servers for LLM integration | TypeScript/Python, 4-phase workflow, evaluation creation |
| `anthropic-webapp-testing` | Web app testing with Playwright | Server lifecycle management, reconnaissance patterns |
| `anthropic-claude-api` | Build apps with Claude API/SDK | Multi-language support (8 langs), Agent SDK, tool use |
| `anthropic-web-artifacts-builder` | Complex React artifacts for claude.ai | React 18 + TypeScript + Tailwind + shadcn/ui |

#### Enterprise & Communication

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| `anthropic-internal-comms` | Internal communications (3P, newsletters) | Template-based, format guides per comm type |
| `anthropic-doc-coauthoring` | Collaborative document editing | Multi-author workflows |
| `anthropic-brand-guidelines` | Brand consistency enforcement | Visual identity standards |
| `anthropic-skill-creator` | Create new agent skills | Structured skill development |

---

### ⚛️ Vercel (vercel-labs/agent-skills) — 5 skills

React/Next.js performance, web design, and deployment.

| Skill | Purpose | Rules |
|-------|---------|-------|
| `vercel-react-best-practices` | React/Next.js performance optimization | 62 rules, 8 categories (waterfalls, bundles, SSR, re-renders) |
| `vercel-web-design-guidelines` | UI accessibility & UX audit | 100+ rules (a11y, forms, animation, dark mode, i18n) |
| `vercel-composition-patterns` | React component architecture | Compound components, state lifting, boolean prop elimination |
| `vercel-react-native-skills` | React Native/Expo best practices | FlashList, Reanimated, gesture handling, monorepo |
| `vercel-deploy-to-vercel` | Deploy apps to Vercel | Auto-detects 40+ frameworks, preview/production deploys |

---

## 🎯 Scenario Guide

### "I'm starting a new feature"

1. `create-plan` → Structure the work
2. `create-branch` → Create feature branch
3. `execute-work-packet` → Implement tasks from plan
4. `commit` → Write proper commits
5. `pr-writer` → Create PR description
6. `iterate-pr` → Fix CI until green

### "I need to review code"

1. `code-review` → General code review
2. `security-review` → Security-focused review
3. `find-bugs` → Bug hunting in diff
4. `django-access-review` → Django IDOR check (if Django)
5. `django-perf-review` → Django N+1 check (if Django)
6. `gha-security-review` → GitHub Actions audit (if GHA changes)

### "I'm building a web app"

1. `vercel-react-best-practices` → Performance patterns
2. `vercel-composition-patterns` → Component architecture
3. `anthropic-frontend-design` → Stunning UI design
4. `vercel-web-design-guidelines` → Accessibility audit
5. `anthropic-webapp-testing` → Playwright testing
6. `vercel-deploy-to-vercel` → Ship it

### "I need to create documents"

| Format | Skill |
|--------|-------|
| PDF | `anthropic-pdf` |
| Word (.docx) | `anthropic-docx` |
| PowerPoint (.pptx) | `anthropic-pptx` |
| Excel (.xlsx) | `anthropic-xlsx` |

### "I need SEO analysis"

1. `seo` → Run `seo audit` for comprehensive analysis
2. Focus sub-skills: `seo page`, `seo schema`, `seo performance`
3. Generate: `seo report` for stakeholder deliverables

### "I'm building an MCP server"

1. `anthropic-mcp-builder` → Full 4-phase development guide
2. Research → Plan → Implement → Test → Evaluate

### "I need to hand off work to next session"

1. `generate-handover` → Session summary
2. `update-docs` → Keep docs current
3. `resume-plan` → Pick up where you left off next time

---

## 📊 Compatibility Matrix

| Skill Category | Antigravity | Claude Code | Cursor | Generic Agent |
|---------------|:-----------:|:-----------:|:------:|:-------------:|
| Sentry (code/security) | ✅ | ✅ | ✅ | ✅ |
| Agentic SEO | ✅ | ✅ | ⚠️ | ✅ |
| OpenCode (planning) | ✅ | ✅ | ✅ | ✅ |
| Anthropic (docs) | ⚠️ | ✅ | ⚠️ | ⚠️ |
| Anthropic (creative) | ⚠️ | ✅ | ⚠️ | ⚠️ |
| Anthropic (dev tools) | ✅ | ✅ | ⚠️ | ⚠️ |
| Vercel (React) | ✅ | ✅ | ✅ | ✅ |
| Vercel (deploy) | ⚠️ | ✅ | ⚠️ | ⚠️ |

✅ = Full support · ⚠️ = Partial (may need adaptation)
