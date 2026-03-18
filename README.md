# MapTiler SDK JS — Agent Skill

Expert coding skill for building interactive web maps. Helps AI agents generate correct, production-ready code using [MapTiler SDK JS](https://www.npmjs.com/package/@maptiler/sdk).

Built on the [Agent Skills](https://agentskills.io) open standard — works with **Claude Code**, **Cursor**, **Windsurf**, **Goose**, and other compatible AI agents.

## What this skill does

When a user asks to add maps, geocoding, location data, or geospatial features to their web application, the AI agent will:
- Use `@maptiler/sdk` with correct SDK patterns (config, enums, helpers)
- Handle API key setup with proper environment variables
- Generate framework-specific code (React, Vue, Svelte, Angular, Next.js)
- Use session-based billing via the SDK (not raw URL parameters)
- Apply best practices for performance, cleanup, and error handling

## Installation

### Claude Code

```bash
# As a plugin (recommended)
npx claude-code plugin add maptiler/agent-skills

# Or manually — copy to your project
mkdir -p .claude/skills/maptiler-sdk-js
cp -r SKILL.md references/ scripts/ .claude/skills/maptiler-sdk-js/
```

### Cursor

Copy `SKILL.md` and `references/` into `.cursor/rules/maptiler-sdk-js/`.

### Windsurf

Append the content of `SKILL.md` to your `.windsurfrules` file.

### Other agents

Any agent supporting the [Agent Skills standard](https://agentskills.io) can use this skill. Place `SKILL.md` and `references/` where the agent looks for skill definitions.

## Contents

```
SKILL.md                    — Main skill definition (~410 lines)
references/
  helpers-api.md            — Vector layer helpers (polyline, polygon, point, heatmap)
  patterns-gotchas.md       — 13 common pitfalls + 13 reusable code patterns
  map-styles.md             — All MapStyle enum variants + Language config
  events.md                 — Map event reference (lifecycle, camera, interaction)
  cloud-apis.md             — MapTiler Cloud REST API endpoints
  frameworks.md             — React, Vue, Svelte, Angular, Next.js integration
  ecosystem.md              — Weather, 3D, AR, geocoding control, and more
scripts/
  install-deps.sh           — Quick package installer
  *.html                    — 8 working CDN-based demo pages
tests/
  eval_cases.json           — Trigger and correctness test cases
```

## Prerequisites

Users need a MapTiler API key from [cloud.maptiler.com](https://cloud.maptiler.com/account/keys/).

## Links

- [MapTiler SDK JS Documentation](https://docs.maptiler.com/sdk-js/)
- [MapTiler SDK JS on GitHub](https://github.com/maptiler/maptiler-sdk-js)
- [MapTiler SDK JS on NPM](https://www.npmjs.com/package/@maptiler/sdk)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)

## License

MIT
