# MapTiler Ecosystem Packages

Reference for all MapTiler ecosystem packages beyond the core `@maptiler/sdk`.

---

## @maptiler/geocoding-control

Search bar UI control with autocomplete for address/place lookup.

```bash
npm install @maptiler/geocoding-control @maptiler/sdk
```

```js
import * as maptilersdk from "@maptiler/sdk";
import { GeocodingControl } from "@maptiler/geocoding-control/maptilersdk";
import "@maptiler/geocoding-control/style.css";

maptilersdk.config.apiKey = "YOUR_KEY";
const map = new maptilersdk.Map({ container: "map" });
map.addControl(new GeocodingControl(), "top-left");
```

- Forward and reverse geocoding with autocomplete
- Restrict by country, bounding box, or proximity bias
- Entry points for each framework: `/maptilersdk`, `/maplibregl`, `/leaflet`, `/openlayers`, `/react`, `/svelte`, `/vanilla`

**Docs:** https://docs.maptiler.com/sdk-js/modules/geocoding/api/api-reference/

---

## @maptiler/weather

Animated weather visualization at 60fps with 4-day forecast, global coverage, hourly precision.

```bash
npm install @maptiler/weather
```

### Layer Types

| Class | Description |
|---|---|
| `TemperatureLayer` | Animated temperature heatmap |
| `PrecipitationLayer` | Rain/snow precipitation |
| `WindLayer` | Animated wind particles |
| `RadarLayer` | Weather radar overlay |
| `PressureLayer` | Atmospheric pressure |
| `WindArrowLayer` | Wind direction arrows |
| `PressureIsolinesLayer` | Pressure isobar lines |

```js
import { TemperatureLayer, WindLayer } from "@maptiler/weather";

const tempLayer = new TemperatureLayer();
map.addLayer(tempLayer, "first-label-layer");
map.addLayer(new WindLayer(), "first-label-layer");

// Time animation (all layers share these methods)
tempLayer.setAnimationTime(timestamp);     // ISO 8601 or Unix
tempLayer.animateTo(targetTime, duration); // smooth transition

// Value picking at coordinates
map.on("mousemove", (e) => {
  const val = tempLayer.pickAt(e.lngLat.lng, e.lngLat.lat);
});
```

- All layers support time animation, value picking, and custom `ColorRamp`

**Docs:** https://docs.maptiler.com/sdk-js/modules/weather/

---

## @maptiler/3d

Place glTF/GLB 3D models on maps using ThreeJS under the hood.

```bash
npm install @maptiler/3d
```

```js
import { Layer3D, AltitudeReference } from "@maptiler/3d";

map.on("ready", async () => {
  const layer3D = new Layer3D("custom-3D-layer");
  map.addLayer(layer3D);
  await layer3D.addMeshFromURL("building", "model.glb", {
    lngLat: { lat: 40.7407, lng: -73.9892 },
    heading: 91.1, scale: 39.5,
    altitude: 74.38, altitudeReference: AltitudeReference.GROUND,
  });
});
```

- Position by lng/lat with altitude relative to ground or mean sea level
- Heading (0-360), scale (uniform or `[x, y, z]`), opacity, wireframe
- Clone meshes, add point lights, manage ambient lighting
- Play embedded glTF animations (`playAnimation`, `pauseAnimation`, `stopAnimation`)
- Interactive states for hover/active

**Docs:** https://docs.maptiler.com/sdk-js/modules/3d/

---

## @maptiler/elevation-profile

Elevation chart control for GeoJSON route traces with automatic elevation fetching.

```bash
npm install @maptiler/elevation-profile-control
```

```js
import { ElevationProfileControl } from "@maptiler/elevation-profile-control";

const elevCtrl = new ElevationProfileControl({
  unit: "metric", visible: true, profileLineColor: "#ff4444",
});
map.addControl(elevCtrl);
elevCtrl.setData(geojsonLineString);
```

- Supports LineString, MultiLineString, Feature, FeatureCollection
- Auto-fetches elevation via MapTiler API if coordinates are 2D `[lon, lat]`
- Metric and imperial units

**Docs:** https://docs.maptiler.com/sdk-js/modules/elevation-profile/api/api-reference/

---

## @maptiler/marker-layout

Non-colliding DOM marker manager from vector tile features.

```bash
npm install @maptiler/marker-layout
```

```js
import { MarkerLayout } from "@maptiler/marker-layout";
await map.onReadyAsync();
const layout = new MarkerLayout(map, {
  layers: ["Capital city labels", "City labels"],
  markerSize: [140, 80], markerAnchor: "top", sortingProperty: "rank", max: 50,
});
map.on("move", () => {
  const s = layout.update();
  if (!s) return;
  s.new.forEach((m) => { /* create DOM */ });
  s.updated.forEach((m) => { /* reposition */ });
  s.removed.forEach((m) => { /* remove DOM */ });
});
```

- Resolves screen-space overlaps, sort by property or function
- Returns `new`, `updated`, `removed` arrays for incremental DOM management

**Docs:** https://docs.maptiler.com/sdk-js/modules/marker-layout/

---

## @maptiler/ar

Augmented reality terrain view via WebXR or Apple Quick Look.

```bash
npm install @maptiler/ar-control
```

```js
import { MaptilerARControl } from "@maptiler/ar-control";
map.addControl(new MaptilerARControl());
```

- Generates 3D terrain model from current viewport, includes GeoJSON overlays
- WebXR (Android/desktop) and Apple Quick Look (iOS); button auto-shown on supported devices

**Docs:** https://docs.maptiler.com/sdk-js/modules/ar/api/api-reference/

---

## @maptiler/client

Headless API client for MapTiler Cloud. Runs in browser and Node.js without map rendering.

```bash
npm install @maptiler/client
```

```js
import { config, geocoding, elevation, staticMaps } from "@maptiler/client";
config.apiKey = "YOUR_KEY";

const result = await geocoding.forward("Paris");
const elev = await elevation.at([6.864, 45.832]);
const url = staticMaps.centered([-71.06, 42.36], 12, { width: 800, height: 600 });
```

**When to use:** `@maptiler/client` for headless/server-side (Node.js, APIs, CLI) -- `@maptiler/sdk` for browser apps (includes client internally). Modules: `geocoding`, `geolocation`, `elevation`, `coordinates`, `staticMaps`, `data`, `math`.

**Docs:** https://docs.maptiler.com/client-js/

---

## @maptiler/leaflet-maptilersdk

Leaflet plugin for MapTiler vector tiles.

```bash
npm install @maptiler/leaflet-maptilersdk
```

```js
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { MaptilerLayer } from "@maptiler/leaflet-maptilersdk";

const map = L.map("map").setView([40.7468, -73.98775], 13);
new MaptilerLayer({ apiKey: "YOUR_KEY" }).addTo(map);
```

- Same `MapStyle` shorthands as the main SDK
- Language auto-detection, CDN and ES module support

**Docs:** https://docs.maptiler.com/leaflet/

---

## maplibre-grid

Grid / graticule overlay plugin for MapLibre GL JS and MapTiler SDK.

```bash
npm install maplibre-grid
```

```js
import * as MaplibreGrid from "maplibre-grid";

const grid = new MaplibreGrid.Grid({
  gridWidth: 10, gridHeight: 10,
  units: "degrees", paint: { "line-opacity": 0.2 },
});
map.addControl(grid);
```

- Units: degrees, radians, miles, kilometers
- Stack multiple grids (major + minor at different zoom levels)

**Docs:** https://github.com/maptiler/maplibre-grid

---

## AnimatedRouteLayer (built-in, v3.11+)

Path animation along a GeoJSON route with camera following. Built into `@maptiler/sdk`.

```js
import { AnimatedRouteLayer } from "@maptiler/sdk";

const route = new AnimatedRouteLayer({
  source: { id: "my-geojson-source", layerID: "route-layer" },
  duration: 5000,
  pathStrokeAnimation: {
    activeColor: [0, 128, 0, 1], inactiveColor: [128, 128, 128, 0.5],
  },
  cameraAnimation: { follow: true },
  autoplay: true,
});
map.addLayer(route);
route.play();
```

- Stroke animation with active/inactive color segments
- Camera follows animated path with configurable smoothing
- Playback control: `play()`, `pause()`, `autoplay`

**Docs:** https://docs.maptiler.com/sdk-js/

---

## ImageViewer (built-in, v3.8+)

Non-georeferenced image viewer with map-like pan/zoom. Built into `@maptiler/sdk`.

```js
import { ImageViewer } from "@maptiler/sdk";

const viewer = new ImageViewer({
  container: "viewer",
  url: "https://example.com/large-image.jpg",
});
```

- Pan and zoom like a map -- for large satellite images, aerial photos, or scans

**Docs:** https://docs.maptiler.com/sdk-js/
