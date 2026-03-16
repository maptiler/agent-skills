# Agent Skill v2 — Optimization Plan

## Why this change

The current skill works but has low discoverability and limited content coverage. Research shows that:
- The `description` field is the #1 factor for skill activation (Claude uses LLM reasoning to match user queries to skill descriptions)
- SKILL.md should be < 500 lines with progressive disclosure to reference files
- Baseline trigger rate for unoptimized skills is ~20%; optimized skills achieve 70-90%
- Top skills have 100K+ installs (e.g., vercel-react-best-practices: 176K)

## Sources being merged

| Source | What | Strengths | Weaknesses |
|--------|------|-----------|------------|
| **S1** `maptiler/agent-skill` (this repo) | Modular SKILL.md + 4 references | Good structure, security guidance | Thin content, suboptimal description |
| **S2** Colleague's skill (58KB, 1900 lines) | Massive single-file reference | Extremely comprehensive, covers REST APIs, weather, AR, 3D | Too large for single SKILL.md (4x limit) |
| **S3** `jakubbican/maptiler-sdk-skill` | SKILL.md + 5 references + 8 HTML examples | Best balanced architecture, battle-tested patterns | Limited framework coverage |

## Key changes proposed

### 1. Description optimization (~850 chars, currently ~130)

```
Expert coding skill for building interactive web maps with MapTiler SDK JS (built on MapLibre GL JS). USE WHEN the user wants to add a map to a web application, show locations on a map, display geographic data, build a store locator, create data visualizations on maps, add geocoding or address search, show routes or GPS tracks, display 3D terrain or globe view, use satellite imagery, add markers or popups, create heatmaps or clustering, embed static map images, get elevation data, or do IP geolocation. Also USE WHEN the user mentions MapLibre GL JS — MapTiler SDK extends MapLibre with built-in cloud services, helpers, and session billing. Covers React, Vue, Svelte, Angular, Next.js, and vanilla JS. Includes MapTiler Cloud REST APIs, vector layer helpers, weather visualization, and framework-specific patterns.
```

Key improvements:
- Third person (required by skill system)
- Explicit "USE WHEN" trigger language
- 15+ natural language user intents
- MapLibre as trigger term (redirects to MapTiler SDK)
- Framework mentions

### 2. SKILL.md restructure (~370 lines)

| Section | Lines | Content |
|---------|-------|---------|
| Overview | ~15 | What SDK is, two packages, links |
| **Why MapTiler SDK (not raw MapLibre)** | ~12 | Bullet-point highlights: helpers, config, billing, geocoding, terrain, enums |
| Critical First Steps | ~40 | API key, env vars, install, CSS, minimal map |
| Core Concepts | ~60 | Map constructor, MapStyle table, Language, Controls |
| Common Recipes | ~100 | 10 recipes (markers, geocoding, GeoJSON, cluster, heatmap, terrain, globe, static map, flyTo) |
| Framework Integration | ~50 | React/Next.js, Vue, Vanilla |
| Cloud APIs | ~30 | Table of 8 APIs + SDK wrapper vs REST |
| Critical Gotchas | ~30 | Top 5 most common mistakes |
| Ecosystem | ~20 | Package table |
| Resources | ~15 | Links, starter templates |

### 3. Reference files (7 files, ~1700 lines total)

| File | Source | Content |
|------|--------|---------|
| `helpers-api.md` | S3 | Complete helpers API with type tables |
| `patterns-gotchas.md` | S3 | 13 gotchas + 13 reusable patterns |
| `map-styles.md` | S2+S3 | All MapStyle variants, Language enum |
| `events.md` | S3 | Lifecycle, camera, interaction, data events |
| `cloud-apis.md` | S2 | REST API endpoints for all 8 APIs |
| `frameworks.md` | S2+S1 | React, Vue, Svelte, Angular, Next.js |
| `ecosystem.md` | S2 | weather, 3d, AR, elevation-profile, geocoding-control |

### 4. HTML examples (8 files from S3)

Working CDN-based demos: basic-map, geocoding, 3d-terrain, globe, clustering, heatmap, interactive-layers, helpers-dataviz.

### 5. Test suite

10+ eval cases targeting trigger accuracy and code correctness. Target: 90%+ eval pass rate, 70%+ trigger accuracy.

### 6. Naming analysis

Separate document comparing naming options (maptiler-sdk-js vs building-web-maps vs maptiler-web-maps) — for team decision.

## Proposed file structure

```
SKILL.md                    (~370 lines)
README.md                   (installation guide for all agents)
NAMING-ANALYSIS.md          (naming options analysis)
references/
  helpers-api.md
  patterns-gotchas.md
  map-styles.md
  events.md
  cloud-apis.md
  frameworks.md
  ecosystem.md
scripts/
  install-deps.sh
  basic-map.html ... (8 HTML examples)
tests/
  eval_cases.json
  test_skill.py
```

## Distribution plan (after merge)

1. GitHub topics: `claude-code-skill`, `agent-skill`, `maps`, `maptiler`, `maplibre`
2. skills.sh listing
3. awesome-claude-skills PR
4. SkillsMP submission
5. awesome-maplibre cross-promotion
6. MapTiler blog post
