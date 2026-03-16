# MapTiler SDK — Helpers API Reference

High-level functions that create sources, layers, and styling in a single call. Import as `maptilersdk.helpers.*`.

> [Online docs](https://docs.maptiler.com/sdk-js/api/helpers/)

---

## Shared Options (CommonShapeLayerOptions)

All helpers accept these common options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | GeoJSON / URL / UUID / string | required | Data source — GeoJSON object, URL to GeoJSON/GPX/KML file, or MapTiler dataset UUID |
| `layerId` | string | auto | Custom layer ID |
| `sourceId` | string | auto | Custom source ID |
| `beforeId` | string | — | Insert layer before this layer ID (for z-ordering below labels) |
| `minzoom` | number | 0 | Minimum zoom for visibility |
| `maxzoom` | number | 22 | Maximum zoom for visibility |
| `outline` | boolean | false | Add outline layer |
| `outlineColor` | string / ZoomStringValues | — | Outline color |
| `outlineWidth` | number / ZoomNumberValues | — | Outline stroke width |
| `outlineOpacity` | number / ZoomNumberValues | — | Outline opacity |

---

## helpers.addPolyline(map, options)

Create a line/polyline layer from various data sources.

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | various | required | GeoJSON, GPX/KML string or URL, MapTiler dataset UUID |
| `lineColor` | string / ZoomStringValues | — | Line color (constant or zoom-ramped) |
| `lineWidth` | number / ZoomNumberValues | 3 | Stroke width in pixels |
| `lineOpacity` | number / ZoomNumberValues | 1 | Line opacity (0-1) |
| `lineBlur` | number / ZoomNumberValues | 0 | Blur effect intensity |
| `lineDashArray` | string | — | Dash pattern (e.g., `"___ _ "`) |
| `lineCap` | `'butt'` / `'round'` / `'square'` | `'round'` | Line end style |
| `lineJoin` | `'bevel'` / `'round'` / `'miter'` | `'round'` | Line join style |

### Returns

```typescript
{
  polylineLayerId: string;
  polylineOutlineLayerId: string;
  polylineSourceId: string;
}
```

### Example

```javascript
// From GeoJSON
maptilersdk.helpers.addPolyline(map, {
  data: routeGeoJSON,
  lineColor: '#0066FF',
  lineWidth: 4,
  outline: true,
  outlineColor: '#003399',
  beforeId: 'waterway-label'
});

// From GPX URL
maptilersdk.helpers.addPolyline(map, {
  data: 'https://example.com/track.gpx',
  lineColor: '#FF0000',
  lineWidth: 3
});

// From MapTiler dataset UUID
maptilersdk.helpers.addPolyline(map, {
  data: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  lineColor: '#00AA00'
});
```

---

## helpers.addPolygon(map, options)

Create a polygon/fill layer.

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | various | required | GeoJSON data source |
| `fillColor` | string / ZoomStringValues | — | Fill color |
| `fillOpacity` | number / ZoomNumberValues | — | Fill opacity (0-1) |
| `pattern` | string (URL) | — | Image URL for repeated background pattern |
| `outlinePosition` | `'center'` / `'inside'` / `'outside'` | `'center'` | Outline stroke position |
| `outlineDashArray` | string | — | Outline dash pattern |
| `outlineBlur` | number | 0 | Outline blur |

### Returns

```typescript
{
  polygonLayerId: string;
  polygonOutlineLayerId: string;
  polygonSourceId: string;
}
```

### Example

```javascript
maptilersdk.helpers.addPolygon(map, {
  data: zonesGeoJSON,
  fillColor: '#FF0000',
  fillOpacity: 0.5,
  outline: true,
  outlineColor: '#990000',
  outlineWidth: 2,
  outlinePosition: 'outside',
  beforeId: 'waterway-label'
});
```

---

## helpers.addPoint(map, options)

Create a point/circle layer with optional built-in clustering.

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | various | required | GeoJSON data source |
| `pointColor` | string / ColorRamp | — | Point color (constant or data-driven via ColorRamp) |
| `pointRadius` | number / ZoomNumberValues / PropertyValues | 8 | Point radius |
| `pointOpacity` | number / ZoomNumberValues | 1 | Point opacity |
| `minPointRadius` | number | 10 | Minimum cluster circle radius |
| `maxPointRadius` | number | 40 | Maximum cluster circle radius |
| `property` | string | — | Feature property name for data-driven styling |
| `cluster` | boolean | false | Enable clustering |
| `showLabel` | boolean | false | Show count labels on clusters |
| `labelColor` | string | `'#FFFFFF'` | Cluster label text color |
| `labelSize` | number | 12 | Cluster label font size |
| `zoomCompensation` | boolean | false | Scale points with zoom level |
| `alignOnViewport` | boolean | true | Keep points circular (vs map-aligned) |

### Returns

```typescript
{
  pointLayerId: string;
  clusterLayerId: string;
  labelLayerId: string;
  pointSourceId: string;
}
```

### Example

```javascript
// Simple clustered points
maptilersdk.helpers.addPoint(map, {
  data: pointsGeoJSON,
  pointColor: '#FF0000',
  pointRadius: 8,
  cluster: true,
  showLabel: true
});

// Data-driven points (sized/colored by property)
maptilersdk.helpers.addPoint(map, {
  data: earthquakesGeoJSON,
  property: 'magnitude',
  pointColor: maptilersdk.ColorRamp.TURBO,
  pointRadius: 6,
  minPointRadius: 5,
  maxPointRadius: 30,
  cluster: true,
  showLabel: true
});
```

---

## helpers.addHeatmap(map, options)

Create a heatmap layer.

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | various | required | GeoJSON data source |
| `colorRamp` | ColorRamp | `ColorRamp.TURBO` | Color ramp for heat colors |
| `property` | string | — | Feature property for weighting |
| `weight` | number / PropertyValues | 1 | Point weight |
| `radius` | number / ZoomNumberValues / PropertyValues | 20 | Heat blob radius |
| `opacity` | number / ZoomNumberValues | 1 | Layer opacity |
| `intensity` | number / ZoomNumberValues | 1 | Global intensity multiplier |
| `zoomCompensation` | boolean | false | Adaptive sizing with zoom |

### Returns

```typescript
{
  heatmapLayerId: string;
  heatmapSourceId: string;
}
```

### Example

```javascript
maptilersdk.helpers.addHeatmap(map, {
  data: pointsGeoJSON,
  colorRamp: maptilersdk.ColorRamp.TURBO,
  property: 'magnitude',
  radius: 25,
  opacity: 0.8,
  intensity: 1.5
});
```

---

## helpers.takeScreenshot(map, options?)

Capture the current map view as a PNG blob.

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `download` | boolean | false | Auto-download the image |
| `filename` | string | `'maptiler_screenshot.png'` | Download filename |

### Returns

`Promise<Blob>` — PNG-encoded image blob.

> **Note:** DOM elements (Markers, Popups) are NOT included in the capture — only the WebGL canvas.

### Example

```javascript
// Capture and download
await maptilersdk.helpers.takeScreenshot(map, {
  download: true,
  filename: 'my-map.png'
});

// Capture as blob for custom use
const blob = await maptilersdk.helpers.takeScreenshot(map);
const url = URL.createObjectURL(blob);
document.getElementById('preview').src = url;
```

---

## Data Format Converters

```javascript
// Convert GPX string to GeoJSON FeatureCollection
const geojson = maptilersdk.gpx(gpxStringContent);

// Convert KML string to GeoJSON FeatureCollection
const geojson = maptilersdk.kml(kmlStringContent);
```

---

## ColorRamp Built-in Presets

Used in `helpers.addPoint()` and `helpers.addHeatmap()` for data-driven coloring:

```javascript
maptilersdk.ColorRamp.TURBO       // Rainbow-like (default for heatmaps)
maptilersdk.ColorRamp.VIRIDIS     // Purple → green → yellow
maptilersdk.ColorRamp.INFERNO     // Black → red → yellow → white
maptilersdk.ColorRamp.MAGMA       // Black → purple → orange → white
maptilersdk.ColorRamp.PLASMA      // Blue → purple → orange → yellow
maptilersdk.ColorRamp.CIVIDIS     // Blue → yellow (colorblind-safe)
```

---

## Type Definitions

```typescript
// Zoom-dependent string values (e.g., colors changing with zoom)
type ZoomStringValues = Array<{ zoom: number; value: string }>;

// Zoom-dependent numeric values (e.g., width changing with zoom)
type ZoomNumberValues = Array<{ zoom: number; value: number }>;

// Property-dependent numeric values (e.g., radius based on feature property)
type PropertyValues = Array<{ propertyValue: number; value: number }>;
```
