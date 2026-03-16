# MapTiler SDK — Map Styles Reference

Complete reference for all available `MapStyle` enum values in the MapTiler SDK v3.

> [Online docs](https://docs.maptiler.com/sdk-js/api/map-styles/)

## Usage

```javascript
import * as maptilersdk from '@maptiler/sdk';

const map = new maptilersdk.Map({
  style: maptilersdk.MapStyle.STREETS
});

// Change style at runtime
map.setStyle(maptilersdk.MapStyle.SATELLITE);

// Use a variant
map.setStyle(maptilersdk.MapStyle.STREETS.DARK);
```

---

## All Styles and Variants

| Style | Variants | Description |
|-------|----------|-------------|
| `MapStyle.STREETS` | `.DARK`, `.LIGHT`, `.PASTEL` | Default street map with roads, labels, POIs |
| `MapStyle.SATELLITE` | — | Satellite/aerial imagery without labels |
| `MapStyle.HYBRID` | — | Satellite imagery with street labels overlay |
| `MapStyle.OUTDOOR` | `.DARK` | Hiking, cycling, trails, elevation |
| `MapStyle.WINTER` | `.DARK` | Ski slopes, lifts, winter terrain |
| `MapStyle.DATAVIZ` | `.DARK`, `.LIGHT` | Clean background for data overlays |
| `MapStyle.BACKDROP` | `.DARK`, `.LIGHT` | High contrast with hillshading |
| `MapStyle.BASIC` | `.DARK`, `.LIGHT` | Simplified, minimal |
| `MapStyle.BRIGHT` | `.DARK`, `.LIGHT`, `.PASTEL` | Vibrant, colorful |
| `MapStyle.TOPO` | `.SHINY`, `.PASTEL`, `.TOPOGRAPHIQUE` | Topographic with contours |
| `MapStyle.VOYAGER` | `.DARK`, `.LIGHT`, `.VINTAGE` | Classic cartography style |
| `MapStyle.TONER` | `.BACKGROUND`, `.LITE`, `.LINES` | High-contrast black & white |
| `MapStyle.OCEAN` | — | Maritime/nautical with depth contours |
| `MapStyle.LANDSCAPE` | `.DARK`, `.VIVID` | Natural landscape emphasis |
| `MapStyle.AQUARELLE` | `.DARK`, `.VIVID` | Watercolor artistic style |
| `MapStyle.OPENSTREETMAP` | — | Classic OSM look |
| `MapStyle.STAGE` | `.DARK`, `.LIGHT` | Presentation/demo style |

---

## Accessing Style URLs (Advanced)

If you need the raw style URL (not recommended):

```javascript
const styleUrl = maptilersdk.MapStyle.STREETS.getUrl();
```

**Always prefer the enum directly** — it enables session billing optimization, auto-uses the latest version, and provides TypeScript type safety.

---

## Style Change Best Practices

Changing styles at runtime removes all custom layers. Re-add them after style loads:

```javascript
function changeStyle(newStyle) {
  map.setStyle(newStyle);
  map.once('styledata', () => {
    addMyCustomLayers();
  });
}
```

---

## Language Configuration

```javascript
// Global
maptilersdk.config.primaryLanguage = maptilersdk.Language.CZECH;
maptilersdk.config.secondaryLanguage = maptilersdk.Language.ENGLISH;

// Per-instance
const map = new maptilersdk.Map({
  language: maptilersdk.Language.GERMAN
});

// Runtime change
map.setLanguage(maptilersdk.Language.FRENCH);
```

### Special Language Modes

| Value | Behavior |
|-------|----------|
| `Language.AUTO` | Browser language detection (default) |
| `Language.LOCAL` | Native language of each region |
| `Language.VISITOR` | Browser language + local fallback |
| `Language.VISITOR_ENGLISH` | English + local fallback |
| `Language.STYLE_LOCK` | Lock to style's language, prevent updates |
| `Language.LATIN` / `Language.NON_LATIN` | Script-based selection |

### Available Languages

`Language.ENGLISH`, `Language.GERMAN`, `Language.FRENCH`, `Language.SPANISH`, `Language.ITALIAN`, `Language.PORTUGUESE`, `Language.CZECH`, `Language.POLISH`, `Language.DUTCH`, `Language.CHINESE`, `Language.JAPANESE`, `Language.KOREAN`, `Language.ARABIC`, `Language.HINDI`, `Language.RUSSIAN`, `Language.TURKISH`, and many more.

RTL languages (Arabic, Hebrew) are supported by default — no plugins needed.
