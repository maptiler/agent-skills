# Skill Naming Analysis

Analysis of naming options for the MapTiler SDK JS agent skill. The `name` field becomes the `/slash-command` and appears in skill listings.

## How Naming Affects Discoverability

Research findings:
- The `description` field has **10x more impact** on trigger accuracy than the `name`
- Claude uses LLM reasoning on the full description to decide which skill to load
- The name primarily affects: slash command UX, marketplace listings, and human recognition
- Best practice: gerund form (verb + -ing), lowercase, hyphens, max 64 chars

## Options Comparison

| Name | Slash Command | Pros | Cons |
|------|--------------|------|------|
| `maptiler-sdk-js` | `/maptiler-sdk-js` | Brand awareness, matches npm package name, clear identity for MapTiler users | Doesn't match natural language ("add a map to my app"), invisible to users who don't know MapTiler |
| `building-web-maps` | `/building-web-maps` | Gerund form (best practice), matches natural user intent, catches generic queries | Loses MapTiler brand, could match non-MapTiler map requests |
| `maptiler-web-maps` | `/maptiler-web-maps` | Brand + generic intent, balanced | Longer, less natural as a command |
| `web-map-builder` | `/web-map-builder` | Descriptive, action-oriented | No MapTiler brand, "builder" implies a tool not a library |
| `maptiler-maps` | `/maptiler-maps` | Short, branded, clear | Doesn't convey "SDK" or "JS" specificity |

## Marketplace Context

Top installed skills use task-oriented names:
- `vercel-react-best-practices` (176K installs) — brand + domain
- `frontend-design` (124K installs) — generic domain
- `web-design-guidelines` (137K installs) — generic domain

Pattern: **Brand names work when the brand IS the domain** (Vercel = React deployment). MapTiler is less universally known, so a mixed approach may be optimal.

## Recommendation

**Keep `maptiler-sdk-js` for now.** The description field (optimized with 15+ trigger intents including "add map to app", "store locator", "geocoding", "MapLibre") will handle discoverability. The brand name is valuable for:
- Users who already know MapTiler
- NPM package name matching
- Enterprise/partner recognition
- Marketplace differentiation from generic "maps" skills

**If trigger testing shows < 50% activation rate**, consider renaming to `maptiler-web-maps` as a compromise.

## Impact on Description

Regardless of name, the description MUST include:
- Generic terms: "web map", "interactive map", "map to web application"
- User intents: "show locations", "store locator", "geocoding", "3D terrain"
- Competitor terms: "MapLibre GL JS" (the underlying engine)
- Framework names: React, Vue, Next.js, Svelte, Angular

The current optimized description (~850 chars) covers all of these.
