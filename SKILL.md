---
name: maptiler-skill
description: Integrate MapTiler maps and Geocoding. Use when users mention maps, geolocation, geocoding, places API, terrain, or MapLibre.
license: MIT
metadata:
  author: maptiler
  version: "1.0.0"
---

# MapTiler Integration Agent Skill

This skill provides comprehensive instructions on how to embed MapTiler services into a project.

## When to use this skill
Use this skill whenever the user asks to:
1. Add an interactive map to their application (web, React, Vanilla JS).
2. Perform geocoding (forward/reverse search for places and addresses).
3. Use MapTiler SDK features like 3D terrain, globe projection, popups, and markers.

## Capabilities

MapTiler provides two main npm packages you can use:
1. **Visual Maps (`@maptiler/sdk`)**: For interactive map rendering, markers, popups, weather layers, 3D terrain, and WebGL mapping.
2. **API Services (`@maptiler/client`)**: For raw API calls like Geocoding, Static Maps, IP Geolocation, and Elevation without a visual map element.

## Authentication (Crucial Step)

Before writing any MapTiler code, ensure that the `MAPTILER_API_KEY` is present.
If you are starting a new project or MapTiler is not yet configured, ask the user to provide their API Key (or to create one at `https://maptiler.com/cloud/`).
*Do NOT invent or hardcode a fake API key.* Provide instructions on how they should put it in their `.env` file (`VITE_MAPTILER_API_KEY`, `NEXT_PUBLIC_MAPTILER_API_KEY`, or `REACT_APP_MAPTILER_API_KEY` depending on their framework).

## Implementation References

Depending on the user's framework or specific request, consult the appropriate reference file below:

### 1. React / Next.js Maps
If the user is using React, Next.js, or Vite + React, read the following reference before implementing the map component.
-> See [references/sdk-react.md](references/sdk-react.md)

### 2. Vanilla JS / HTML Maps
If the user is building a plain HTML/JS or a non-React framework app, read this reference.
-> See [references/sdk-vanilla.md](references/sdk-vanilla.md)

### 3. API Services (Geocoding, Static Maps, IP Geo)
If the user needs to find places, get static map images, find user location via IP, or get elevation data.
-> See [references/api-client.md](references/api-client.md)

### 4. Advanced Map Features (Markers, Weather, 3D Terrain, Localization)
If the user wants to customize the map style, add weather layers, change map language, use 3D terrain, or add interactive markers/popups.
-> See [references/styles-and-layers.md](references/styles-and-layers.md)

## Directory Structure
The skill is organized as follows:

```text
.
├── SKILL.md                  # Entry point with metadata and usage guidelines
├── references/               # Detailed implementation guides
│   ├── api-client.md         # Documentation for Geocoding, Search, and Static Maps
│   ├── sdk-react.md          # Guide for React/Next.js map integration
│   ├── sdk-vanilla.md        # Guide for Vanilla JS/HTML map integration
│   └── styles-and-layers.md  # Guide for markers, popups, and map styles
├── scripts/                  # Helper scripts for agents
│   └── install-deps.sh       # Script to install NPM dependencies
├── tests/                    # Verification tests
│   └── test_skill.py         # Automated skill verification script
└── assets/                   # Static assets (boilerplate code, examples)
```

## Automated Scripts
If you have shell access, you can run the following helper scripts to setup the environment:
- Install `@maptiler/sdk` package (Node): `bash scripts/install-deps.sh sdk`
- Install `@maptiler/client` package (Node): `bash scripts/install-deps.sh client`

## Verification
The skill's functionality can be verified using the `tests/test_skill.py` script.
*   **Method**: The script simulates an agent interaction using the Gemini API (requires `GEMINI_API_KEY`).
*   **Validation**: It checks if the generated output includes the correct SDK import, CSS link, Map instantiation, and API key configuration.

## Official Resources
- [MapTiler Documentation](https://docs.maptiler.com/)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)
