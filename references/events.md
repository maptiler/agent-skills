# MapTiler SDK — Events Reference

Complete reference for all map events with signatures and usage examples.

> [Online docs](https://docs.maptiler.com/sdk-js/api/events/)

## Lifecycle Events

### load
Fired when the map has finished loading all resources (style, tiles, etc.). **This is the safest place to add layers.**

```javascript
map.on('load', () => {
  map.addSource('my-source', { ... });
  map.addLayer({ ... });
});
```

### style.load
Fired when the style has finished loading. Fires before `load`.

```javascript
map.on('style.load', () => {
  console.log('Style loaded');
});
```

### styledata
Fired when the style is changed via `setStyle()`. **Critical for re-adding custom layers after style change.**

```javascript
// One-time listener (recommended for style changes)
map.once('styledata', () => {
  reAddCustomLayers();
});
```

### idle
Fired when the map enters an idle state (nothing loading, no animations).

```javascript
map.on('idle', () => {
  console.log('Map is idle');
});
```

### remove
Fired when the map is destroyed via `map.remove()`.

```javascript
map.on('remove', () => {
  // Cleanup custom resources
});
```

---

## Camera Events

### move / movestart / moveend
Fired during camera movement (pan, zoom, rotate, pitch).

```javascript
map.on('movestart', () => {
  console.log('Camera movement started');
});

map.on('move', () => {
  console.log('Moving...', map.getCenter());
});

map.on('moveend', () => {
  console.log('Camera stopped at:', map.getCenter());
});
```

### zoom / zoomstart / zoomend
Fired specifically during zoom changes.

```javascript
map.on('zoomend', () => {
  console.log('Zoom level:', map.getZoom());
});
```

### rotate / rotatestart / rotateend
Fired during bearing changes.

```javascript
map.on('rotateend', () => {
  console.log('Bearing:', map.getBearing());
});
```

### pitch / pitchstart / pitchend
Fired during pitch (tilt) changes.

```javascript
map.on('pitchend', () => {
  console.log('Pitch:', map.getPitch());
});
```

---

## Interaction Events

### click
Fired on map click. Use layer-specific version for feature clicks.

```javascript
// Click anywhere on map
map.on('click', (e) => {
  console.log('Clicked at:', e.lngLat.lng, e.lngLat.lat);
  console.log('Screen point:', e.point.x, e.point.y);
});

// Click on specific layer
map.on('click', 'my-points-layer', (e) => {
  const feature = e.features[0];
  console.log('Clicked feature:', feature.properties);

  new maptilersdk.Popup()
    .setLngLat(e.lngLat)
    .setHTML(`<h3>${feature.properties.name}</h3>`)
    .addTo(map);
});
```

### dblclick
Fired on double click. Default behavior zooms in.

```javascript
map.on('dblclick', (e) => {
  e.preventDefault(); // Prevent zoom
  console.log('Double clicked at:', e.lngLat);
});
```

### contextmenu
Fired on right-click.

```javascript
map.on('contextmenu', (e) => {
  showCustomContextMenu(e.lngLat);
});
```

### mouseenter / mouseleave
Fired when mouse enters/leaves a layer's features. **Essential for hover effects.**

```javascript
map.on('mouseenter', 'my-points-layer', (e) => {
  map.getCanvas().style.cursor = 'pointer';

  const featureId = e.features[0].id;
  map.setFeatureState(
    { source: 'my-source', id: featureId },
    { hover: true }
  );
});

map.on('mouseleave', 'my-points-layer', () => {
  map.getCanvas().style.cursor = '';
});
```

### mousemove
Fired on mouse move over map.

```javascript
map.on('mousemove', (e) => {
  coordsDisplay.textContent = `${e.lngLat.lng.toFixed(4)}, ${e.lngLat.lat.toFixed(4)}`;
});

// Layer-specific
map.on('mousemove', 'my-layer', (e) => {
  const feature = e.features[0];
});
```

---

## Touch Events

### touchstart / touchend / touchcancel
Touch equivalents for mobile devices.

```javascript
map.on('touchstart', (e) => {
  if (e.points.length === 2) {
    console.log('Two-finger touch');
  }
});
```

---

## Data Events

### data
Fired when any data (style, source, tile) changes.

```javascript
map.on('data', (e) => {
  if (e.dataType === 'source') {
    console.log('Source data changed:', e.sourceId);
  }
});
```

### sourcedata
Fired when a source's data changes.

```javascript
map.on('sourcedata', (e) => {
  if (e.sourceId === 'my-source' && e.isSourceLoaded) {
    console.log('My source finished loading');
  }
});
```

### sourcedataabort
Fired when a source data request is aborted.

---

## Error Events

### error
Fired when an error occurs.

```javascript
map.on('error', (e) => {
  console.error('Map error:', e.error);
});
```

---

## Event Object Properties

All events include an event object with these common properties:

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Event type name |
| `target` | Map | The map instance |
| `originalEvent` | Event | Original DOM event (if applicable) |

Mouse/Touch events also include:

| Property | Type | Description |
|----------|------|-------------|
| `point` | Point | Screen coordinates `{x, y}` |
| `lngLat` | LngLat | Geographic coordinates `{lng, lat}` |
| `features` | Feature[] | Features at point (layer-specific events only) |

---

## Removing Event Listeners

```javascript
// Named function (recommended for removal)
function handleClick(e) {
  console.log('Clicked');
}

map.on('click', handleClick);
map.off('click', handleClick);

// One-time listener
map.once('load', () => {
  // Only fires once, auto-removes
});
```

---

## Event Propagation

For layer-specific events, you can stop propagation to prevent the generic map event from firing:

```javascript
map.on('click', 'my-layer', (e) => {
  // Handle layer click
  e.preventDefault(); // Stop propagation to map-level click handler
});

map.on('click', (e) => {
  // This won't fire if layer click called preventDefault()
});
```

> **Note:** In MapLibre GL JS v5 (used by SDK v3), `e.preventDefault()` is the preferred way to stop event propagation. The behavior is consistent with DOM event handling.
