# Map Styles, Markers, and 3D Features

This guide assumes you already have a MapTiler Map instance (`map`). See `sdk-react.md` or `sdk-vanilla.md` for initialization.

## Built-in Map Styles

The `maptilersdk.MapStyle` enum contains built-in styles. Provide this to the `style` option in the `Map` constructor, or update it later using `map.setStyle()`.
- `MapStyle.STREETS`: Default detailed streets style.
- `MapStyle.OUTDOOR`: Topographic map for outdoors, hiking, etc.
- `MapStyle.SATELLITE`: High-resolution global satellite imagery.
- `MapStyle.TOPO`: Topographic map for professional cartography.
- `MapStyle.BASIC`: Minimalist clean base map.
- `MapStyle.OCEAN`: Map with detailed bathymetry (ocean depths).

**Example**:
```javascript
map.setStyle(maptilersdk.MapStyle.OUTDOOR);
```

## Adding Interactive Markers

You can add markers (custom images, HTML elements, or default pins) to the map.

```javascript
import * as maptilersdk from '@maptiler/sdk';

// Basic Marker
const marker = new maptilersdk.Marker({
  color: "#FF0000",
  draggable: true,
})
  .setLngLat([14.42, 50.08]) // [longitude, latitude]
  .addTo(map);

// Handling marker drag
marker.on('dragend', () => {
  const lngLat = marker.getLngLat();
  console.log('Marker moved to:', lngLat.lng, lngLat.lat);
});
```

## Popups

Popups can be attached to markers or triggered manually.

```javascript
const popup = new maptilersdk.Popup({ offset: 25 })
  .setText('This is Prague!');

// Attach to marker
const marker = new maptilersdk.Marker()
  .setLngLat([14.42, 50.08])
  .setPopup(popup) // popup appears on click
  .addTo(map);
```

## 3D Terrain

MapTiler supports full 3D terrain rendering out of the box, assuming the `style` supports terrain. It's usually easier to simply pass `terrainControl: true` during Map instantiation.

```javascript
const map = new maptilersdk.Map({
  container: 'map',
  style: maptilersdk.MapStyle.SATELLITE,
  center: [14.42, 50.08],
  zoom: 12,
  pitch: 60,         // Tile the map back
  bearing: 45,       // Rotate the map
  terrain: true,     // <--- Enable built-in 3D terrain
  terrainControl: true // Let the user toggle terrain via UI
});
```

## Globe Projection

To view the world as a globe instead of a flat Mercator projection:

```javascript
const map = new maptilersdk.Map({
  // ... other options
  projection: 'globe', // <--- Enable globe view
});
```

The globe projection disables map repetition at the poles and eliminates Greenland size distortion at low zoom levels.

## Adding GeoJSON Data

To visualize custom data (e.g., lines, polygons, points), use Sources and Layers.

```javascript
map.on('load', () => {
  // Add a data source containing GeoJSON
  map.addSource('route', {
    type: 'geojson',
    data: {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: [
          [14.42, 50.08],
          [14.43, 50.09],
          [14.45, 50.10]
        ]
      }
    }
  });

  // Add a layer to style the data
  map.addLayer({
    id: 'route-layer',
    type: 'line',
    source: 'route',
    layout: {
      'line-join': 'round',
      'line-cap': 'round'
    },
    paint: {
      'line-color': '#ff0000',
      'line-width': 5
    }
  });
});

## Map Language & Localization

You can change the language of the map labels.

```javascript
const map = new maptilersdk.Map({
  container: 'map',
  style: maptilersdk.MapStyle.STREETS,
  center: [14.42, 50.08],
  zoom: 12,
  language: maptilersdk.Language.ENGLISH, // Force English labels
  // language: maptilersdk.Language.GERMAN,
  // language: maptilersdk.Language.JAPANESE,
  // language: maptilersdk.Language.AUTO, // Detect from browser
});

// Or update dynamically
map.setLanguage(maptilersdk.Language.FRENCH);
```

## Weather Layers

MapTiler provides specialized weather layers like precipitation, wind, temperature, and radar. These are added as layers on top of the base map.

```javascript
map.on('load', function () {
  // Add Precipitation Layer
  map.addLayer({
    'id': 'precipitation',
    'type': 'raster',
    'source': {
      'type': 'raster',
      'tiles': [
        // Ensure you use the correct endpoint and key
        `https://api.maptiler.com/tiles/weather-precipitation/{z}/{x}/{y}.png?key=${maptilersdk.config.apiKey}`
      ],
      'tileSize': 512
    },
    'paint': {
      'raster-opacity': 0.8
    }
  });
});
```

## Official Resources

- [MapTiler SDK Styles Reference](https://docs.maptiler.com/sdk-js/api/map-styles/)
- [MapTiler Weather Documentation](https://docs.maptiler.com/weather/)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)