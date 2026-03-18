# MapTiler SDK — Common Patterns & Gotchas

Quick reference for solving common issues and implementing standard patterns.

---

## Gotchas

### 1. Map Container Must Have Dimensions

**Problem:** Map shows as blank/empty.

**Solution:** The container element must have explicit width and height.

```css
/* Option 1: Fill viewport */
#map {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

/* Option 2: Fixed size */
#map {
  width: 800px;
  height: 600px;
}

/* Option 3: Percentage (parent must have height) */
#map {
  width: 100%;
  height: 100vh;
}
```

### 2. Layers Disappear After Style Change

**Problem:** Custom layers vanish when calling `setStyle()`.

**Solution:** Re-add layers after style loads.

```javascript
map.setStyle(maptilersdk.MapStyle.SATELLITE);

map.once('styledata', () => {
  addMyCustomLayers();
});
```

### 3. "Style not loaded" Errors

**Problem:** Adding layers before map is ready throws errors.

**Solution:** Wait for `load` event or check `isStyleLoaded()`.

```javascript
// Option 1: Wait for load
map.on('load', () => {
  map.addLayer({ ... });
});

// Option 2: Guard check
function addLayerSafe(config) {
  if (map.isStyleLoaded()) {
    map.addLayer(config);
  } else {
    map.once('load', () => map.addLayer(config));
  }
}
```

### 4. Duplicate Layer/Source Errors

**Problem:** "Source/Layer already exists" when re-adding layers.

**Solution:** Remove before adding.

```javascript
function safeAddLayer(id, sourceConfig, layerConfig) {
  if (map.getLayer(id)) map.removeLayer(id);
  if (map.getSource(id)) map.removeSource(id);

  map.addSource(id, sourceConfig);
  map.addLayer({ id, source: id, ...layerConfig });
}
```

### 5. API Key in URL Instead of SDK Config

**Problem:** Putting the API key directly in a style URL skips the SDK's session management, leading to higher billing costs.

**Solution:** Use the SDK's global config. The SDK handles API key injection and session tracking automatically.

```javascript
// ⚠️ Misses session billing — API key hardcoded in URL
import maplibregl from 'maplibre-gl';
new maplibregl.Map({
  style: 'https://api.maptiler.com/.../style.json?key=xxx'
});

// ✅ SDK manages the key + session automatically
import * as maptilersdk from '@maptiler/sdk';
maptilersdk.config.apiKey = 'xxx';
new maptilersdk.Map({
  style: maptilersdk.MapStyle.STREETS
});
```

### 6. Coordinates Are [lng, lat] Not [lat, lng]

**Problem:** Map shows wrong location.

**Solution:** MapTiler SDK uses `[longitude, latitude]` order (like GeoJSON).

```javascript
// ❌ Wrong (Google Maps order)
center: [50.1167, 14.4178]

// ✅ Correct
center: [14.4178, 50.1167]  // [lng, lat] - Prague
```

### 7. Data Layers Cover Labels

**Problem:** Polygons or lines render on top of place names and road labels.

**Solution:** Use the `beforeId` parameter to insert layers below labels.

```javascript
// ❌ Wrong - polygon covers all labels
map.addLayer({
  id: 'my-polygon',
  type: 'fill',
  source: 'my-source',
  paint: { 'fill-color': '#ff0000', 'fill-opacity': 0.5 }
});

// ✅ Correct - insert below labels
map.addLayer({
  id: 'my-polygon',
  type: 'fill',
  source: 'my-source',
  paint: { 'fill-color': '#ff0000', 'fill-opacity': 0.5 }
}, 'waterway-label');

// Helpers also support this:
maptilersdk.helpers.addPolygon(map, {
  data: geojson,
  fillColor: '#ff0000',
  beforeId: 'waterway-label'
});

// Common label layers: 'waterway-label', 'road-label', 'place-label', 'poi-label'
```

### 8. Slow Performance with Many Points

**Problem:** Map becomes sluggish with 100+ markers.

**Solution:** Enable clustering on the GeoJSON source, or use helpers.

```javascript
// Option A: Helpers (simplest)
maptilersdk.helpers.addPoint(map, {
  data: pointsGeoJSON,
  cluster: true,
  showLabel: true
});

// Option B: Manual clustering
map.addSource('points', {
  type: 'geojson',
  data: pointsGeoJSON,
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50
});
```

### 9. Memory Leaks in SPAs (React/Vue/Angular)

**Problem:** App slows down after navigating between pages with maps.

**Solution:** Always call `map.remove()` when component unmounts.

```javascript
// React
useEffect(() => {
  const map = new maptilersdk.Map({ ... });
  return () => map.remove();  // CRITICAL
}, []);

// Vue
onUnmounted(() => {
  map.remove();  // CRITICAL
});
```

### 10. Separate maplibre-gl Import Alongside SDK

**Problem:** Installing and importing `maplibre-gl` separately when `@maptiler/sdk` is already used. This leads to inconsistency — some parts of the code use the SDK ecosystem, others bypass it.

**Solution:** The SDK already includes and extends MapLibre GL JS. Import everything from `@maptiler/sdk` to keep the ecosystem consistent (session billing, helpers, config, TypeScript types).

```javascript
// ⚠️ Bypasses the SDK ecosystem — session billing, helpers, etc. are disconnected
import maplibregl from 'maplibre-gl';
new maplibregl.Marker().setLngLat([14, 50]).addTo(map);

// ✅ Consistent — use SDK namespace for the full integrated experience
import * as maptilersdk from '@maptiler/sdk';
new maptilersdk.Marker().setLngLat([14, 50]).addTo(map);
```

### 11. Using setFog() for Globe Atmosphere (v3)

**Problem:** Using verbose `setFog()` configuration for globe atmosphere.

**Solution:** In v3, use `halo` and `space` constructor options.

```javascript
// ❌ Verbose (legacy, still works)
map.on('load', () => {
  map.setFog({
    color: 'rgb(186, 210, 235)',
    'high-color': 'rgb(36, 92, 223)',
    'horizon-blend': 0.02,
    'space-color': 'rgb(11, 11, 25)',
    'star-intensity': 0.6
  });
});

// ✅ Simpler (v3 recommended)
const map = new maptilersdk.Map({
  projection: 'globe',
  halo: true,
  space: true
});
```

### 12. geolocate Option Ignored

**Problem:** Setting `geolocate: GeolocationType.POINT` but map doesn't center on visitor.

**Solution:** The `geolocate` option is ignored when `center` is explicitly provided or when `hash: true` finds existing URL hash data.

```javascript
// ❌ geolocate ignored because center is set
new maptilersdk.Map({
  center: [14.4178, 50.1167],
  geolocate: maptilersdk.GeolocationType.POINT  // ignored!
});

// ✅ Don't set center when using geolocate
new maptilersdk.Map({
  geolocate: maptilersdk.GeolocationType.POINT,
  zoom: 12
});
```

### 13. enableGlobeProjection() is Deprecated (v3.11+)

**Problem:** Using `map.enableGlobeProjection()` / `map.enableMercatorProjection()`.

**Solution:** Use `map.setProjection()` which supports persistence through style changes.

```javascript
// ❌ Deprecated
map.enableGlobeProjection();

// ✅ Recommended
map.setProjection('globe');     // persists through style changes
map.setProjection('mercator');

// Reset persistence
map.forgetPersistedProjection();
```

---

## Common Patterns

### Pattern: Layer Visibility Toggle

```javascript
function toggleLayer(layerId, visible) {
  if (map.getLayer(layerId)) {
    map.setLayoutProperty(
      layerId,
      'visibility',
      visible ? 'visible' : 'none'
    );
  }
}
```

### Pattern: Update GeoJSON Data

```javascript
function updateSourceData(sourceId, newData) {
  const source = map.getSource(sourceId);
  if (source) {
    source.setData(newData);
  }
}
```

### Pattern: Hover Effect with Cursor

```javascript
function setupHover(layerId) {
  map.on('mouseenter', layerId, () => {
    map.getCanvas().style.cursor = 'pointer';
  });

  map.on('mouseleave', layerId, () => {
    map.getCanvas().style.cursor = '';
  });
}
```

### Pattern: Feature State for Highlighting

```javascript
let hoveredId = null;

map.on('mousemove', 'my-layer', (e) => {
  if (e.features.length > 0) {
    if (hoveredId !== null) {
      map.setFeatureState(
        { source: 'my-source', id: hoveredId },
        { hover: false }
      );
    }

    hoveredId = e.features[0].id;
    map.setFeatureState(
      { source: 'my-source', id: hoveredId },
      { hover: true }
    );
  }
});

map.on('mouseleave', 'my-layer', () => {
  if (hoveredId !== null) {
    map.setFeatureState(
      { source: 'my-source', id: hoveredId },
      { hover: false }
    );
    hoveredId = null;
  }
});

// In layer paint, use feature state
map.addLayer({
  id: 'my-layer',
  // ...
  paint: {
    'circle-color': [
      'case',
      ['boolean', ['feature-state', 'hover'], false],
      '#ff0000',  // Hovered
      '#0000ff'   // Default
    ]
  }
});
```

### Pattern: Popup on Click

```javascript
map.on('click', 'my-layer', (e) => {
  const feature = e.features[0];
  const coords = feature.geometry.coordinates.slice();

  // Adjust for antimeridian wrapping
  while (Math.abs(e.lngLat.lng - coords[0]) > 180) {
    coords[0] += e.lngLat.lng > coords[0] ? 360 : -360;
  }

  new maptilersdk.Popup()
    .setLngLat(coords)
    .setHTML(`<h3>${feature.properties.name}</h3>`)
    .addTo(map);
});
```

### Pattern: Fit Map to GeoJSON Bounds

```javascript
function fitToGeoJSON(geojson) {
  const bounds = new maptilersdk.LngLatBounds();

  geojson.features.forEach(feature => {
    if (feature.geometry.type === 'Point') {
      bounds.extend(feature.geometry.coordinates);
    } else if (feature.geometry.type === 'LineString') {
      feature.geometry.coordinates.forEach(coord => bounds.extend(coord));
    } else if (feature.geometry.type === 'Polygon') {
      feature.geometry.coordinates[0].forEach(coord => bounds.extend(coord));
    }
  });

  map.fitBounds(bounds, { padding: 50 });
}
```

### Pattern: Geocoding → Fly To → Marker

```javascript
async function searchAndFlyTo(query) {
  const result = await maptilersdk.geocoding.forward(query, { limit: 1 });
  if (result.features.length === 0) return;

  const feature = result.features[0];
  const coords = feature.geometry.coordinates;

  map.flyTo({ center: coords, zoom: 14, essential: true });

  new maptilersdk.Marker({ color: '#0891b2' })
    .setLngLat(coords)
    .setPopup(new maptilersdk.Popup().setHTML(`<h3>${feature.place_name}</h3>`))
    .addTo(map);
}
```

### Pattern: Polyline from GPX via Helpers

```javascript
// Load a GPX track with one call
maptilersdk.helpers.addPolyline(map, {
  data: 'https://example.com/hiking-trail.gpx',
  lineColor: '#FF4444',
  lineWidth: 4,
  outline: true,
  outlineColor: '#AA0000',
  beforeId: 'waterway-label'
});
```

### Pattern: Debounced Move Handler

```javascript
let moveTimeout;

map.on('move', () => {
  clearTimeout(moveTimeout);
  moveTimeout = setTimeout(() => {
    updateVisibleFeatures();
  }, 100);
});
```

### Pattern: Map Resize Handler

```javascript
// Call when container size changes
window.addEventListener('resize', () => {
  map.resize();
});

// Or with ResizeObserver
const resizeObserver = new ResizeObserver(() => {
  map.resize();
});
resizeObserver.observe(document.getElementById('map'));
```

### Pattern: Save/Restore Map State

```javascript
function saveMapState() {
  return {
    center: map.getCenter().toArray(),
    zoom: map.getZoom(),
    pitch: map.getPitch(),
    bearing: map.getBearing()
  };
}

function restoreMapState(state) {
  map.jumpTo({
    center: state.center,
    zoom: state.zoom,
    pitch: state.pitch,
    bearing: state.bearing
  });
}

// Save to localStorage
localStorage.setItem('mapState', JSON.stringify(saveMapState()));

// Restore
const saved = localStorage.getItem('mapState');
if (saved) restoreMapState(JSON.parse(saved));
```

### Pattern: Globe with Atmosphere (v3)

```javascript
const map = new maptilersdk.Map({
  container: 'map',
  style: maptilersdk.MapStyle.SATELLITE,
  center: [0, 20],
  zoom: 1.5,
  projection: 'globe',
  halo: true,
  space: true
});
```

### Pattern: Toggle Globe/Mercator Projection

```javascript
function setProjection(type) {
  map.setProjection(type);  // 'globe' or 'mercator' — persists through style changes
}
```

---

## Debugging Tips

### Log All Map Events

```javascript
['load', 'styledata', 'error', 'click', 'moveend'].forEach(event => {
  map.on(event, (e) => console.log(`Event: ${event}`, e));
});
```

### Check What Layers Exist

```javascript
console.log('Layers:', map.getStyle().layers.map(l => l.id));
```

### Check What Sources Exist

```javascript
console.log('Sources:', Object.keys(map.getStyle().sources));
```

### Inspect Feature at Point

```javascript
map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point);
  console.log('Features at click:', features);
});
```

### Find Label Layers for beforeId

```javascript
const labelLayers = map.getStyle().layers
  .filter(l => l.id.includes('label'))
  .map(l => l.id);
console.log('Label layers:', labelLayers);
```
