# MapTiler Cloud REST API Reference

All MapTiler Cloud APIs use the base URL `https://api.maptiler.com/` with a required `key` parameter. Access is read-only and safe for public applications. Obtain an API key at <https://cloud.maptiler.com/account/keys/>.

```
https://api.maptiler.com/{METHOD}/{QUERY}.json?{PARAMS}&key=YOUR_MAPTILER_API_KEY
```

---

## 1. Maps API

Retrieve map styles, raster tiles, sprites, and TileJSON metadata.

| Endpoint | URL Pattern |
|----------|-------------|
| Style JSON | `GET /maps/{mapId}/style.json?key=KEY` |
| Raster XYZ Tiles | `GET /maps/{mapId}/{z}/{x}/{y}.png?key=KEY` |
| TileJSON | `GET /maps/{mapId}/tiles.json?key=KEY` |
| Map Sprites | `GET /maps/{mapId}/sprite.json?key=KEY` |
| Embeddable Viewer | `GET /maps/{mapId}/?key=KEY` |
| WMTS Capabilities | `GET /maps/{mapId}/wmts?key=KEY` |
| OGC API Tiles | `GET /maps/{mapId}/tiles/{tileMatrixSetId}/{z}/{y}/{x}?key=KEY` |

```js
// SDK JS — style from Maps API (automatic)
const map = new Map({ style: MapStyle.STREETS });

// Direct URL for raster tiles
const tileUrl = `https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=${apiKey}`;
```

---

## 2. Tiles API

Access individual data tilesets (satellite, terrain, vector tiles, etc.).

| Endpoint | URL Pattern |
|----------|-------------|
| XYZ Tiles | `GET /tiles/{tilesetId}/{z}/{x}/{y}?key=KEY` |
| TileJSON | `GET /tiles/{tilesetId}/tiles.json?key=KEY` |
| Embeddable Viewer | `GET /tiles/{tilesetId}/?key=KEY` |
| WMTS | `GET /tiles/{tilesetId}/wmts?key=KEY` |

**Common tileset IDs:** `satellite-v2`, `terrain-rgb-v2`, `v3` (OpenMapTiles), `contours-v2`, `hillshades`, `ocean`

```js
// Add satellite tiles as a raster source
map.addSource("satellite", {
  type: "raster",
  tiles: [`https://api.maptiler.com/tiles/satellite-v2/{z}/{x}/{y}.jpg?key=${apiKey}`],
  tileSize: 512,
});
map.addLayer({ id: "sat-layer", type: "raster", source: "satellite" });
```

---

## 3. Geocoding API

Forward, reverse, and batch geocoding with rich place metadata.

| Endpoint | URL Pattern |
|----------|-------------|
| Forward (by name) | `GET /geocoding/{query}.json?key=KEY` |
| Reverse (by coords) | `GET /geocoding/{lng},{lat}.json?key=KEY` |
| By Feature ID | `GET /geocoding/{featureId}.json?key=KEY` |
| Batch | `POST /geocoding` |

### Query Parameters (forward geocoding)

| Parameter | Description |
|-----------|-------------|
| `bbox` | Bounding box filter `[west,south,east,north]` |
| `proximity` | Bias results toward `[lon,lat]` or `ip` for user IP |
| `language` | Response language(s), e.g. `de,en` |
| `limit` | Max results (1-10, default 5) |
| `types` | Filter by PlaceType(s) |
| `country` | Filter by ISO country codes, e.g. `sk,cz` |
| `autocomplete` | Enable/disable autocomplete (`true`/`false`) |
| `fuzzyMatch` | Enable fuzzy matching (`true`/`false`) |
| `worldview` | Political worldview filter (`auto`, `default`, `ch`, `us`) |

### PlaceType Values

`continental_marine`, `country`, `major_landform`, `region`, `subregion`, `county`, `joint_municipality`, `joint_submunicipality`, `municipality`, `municipal_district`, `locality`, `neighbourhood`, `place`, `postal_code`, `address`, `road`, `poi`

```js
// SDK JS — forward geocoding
const result = await maptilersdk.geocoding.forward("Zurich", {
  language: [maptilersdk.geocoding.languages.ENGLISH],
  proximity: [8.5285, 47.377],
  types: ["municipality", "place"],
  country: ["ch"],
  limit: 5,
});

// SDK JS — reverse geocoding
const reverse = await maptilersdk.geocoding.reverse([8.5285, 47.377]);

// Response shape:
// result.features[0].properties: { ref, country_code, kind, osm_id, ... }
// result.features[0].geometry:   { type: "Point", coordinates: [lon, lat] }
// result.features[0].bbox:       [west, south, east, north]
// result.features[0].context:    [ { id, text } ] — hierarchy chain
```

---

## 4. Static Maps API

Generate map images (PNG/JPEG) server-side without JavaScript.

| Mode | URL Pattern |
|------|-------------|
| Center-based | `GET /maps/{mapId}/static/{lon},{lat},{zoom}/{width}x{height}.png?key=KEY` |
| Bounds-based | `GET /maps/{mapId}/static/{west},{south},{east},{north}/{width}x{height}.png?key=KEY` |
| Auto-fitted | `GET /maps/{mapId}/static/auto/{width}x{height}.png?key=KEY&markers=...&path=...` |

**Parameters:** `@2x` (HiDPI), `markers` (pin markers), `path` (draw polylines), `fill` (polygon fill), `attribution` (true/false)

```js
// SDK JS — centered
const centeredUrl = maptilersdk.staticMaps.centered(
  [8.5285, 47.377], 12,
  { hiDPI: true, width: 1000, height: 600, style: MapStyle.OUTDOOR }
);

// SDK JS — bounded
const boundedUrl = maptilersdk.staticMaps.bounded(
  [5.95, 45.82, 10.49, 47.81],
  { width: 2048, height: 1024, style: MapStyle.STREETS.DARK }
);

// SDK JS — auto-fitted to content
const autoUrl = maptilersdk.staticMaps.automatic({
  hiDPI: true, width: 2048, height: 1024,
  style: MapStyle.STREETS.LIGHT,
  path: routePoints,
  markers: [[8.53, 47.38, "#0a0"]],
  pathStrokeColor: "red",
});
```

---

## 5. Elevation API

Get elevation values for one or more coordinates.

| Endpoint | URL Pattern |
|----------|-------------|
| Get elevation | `GET /elevation/{lng},{lat}[;{lng2},{lat2}...].json?key=KEY` |

**Parameters:** `unit` — `meters` (default) or `feet`
**Coordinate limits:** lng > -180, < 180; lat >= -85, <= 85

```json
// Response (ElevationResults)
{
  "results": [
    { "lat": 50.0, "lng": 17.0, "elevation": 234.5 },
    { "lat": 58.39, "lng": -133.5, "elevation": 1023.8 }
  ]
}
```

```js
// SDK JS — single point
const point = await maptilersdk.elevation.at([6.864884, 45.832743]);
// Returns [lng, lat, elevation]

// SDK JS — batch
const batch = await maptilersdk.elevation.batch([
  [6.864, 45.832], [86.925, 27.988]
]);

// SDK JS — from GeoJSON LineString
const elevated = await maptilersdk.elevation.fromLineString(lineStringGeoJSON);
```

---

## 6. Geolocation API

Obtain visitor location based on IP address.

| Endpoint | URL Pattern |
|----------|-------------|
| IP Geolocation | `GET /geolocation/ip.json?key=KEY` |

### GeolocationResult Fields

| Field | Description |
|-------|-------------|
| `country` | Country name (e.g. "Switzerland") |
| `country_code` | ISO 3166-1 alpha-2 (e.g. "CH") |
| `country_bounds` | `[west, south, east, north]` |
| `country_languages` | ISO 639-1 codes (e.g. `["de","fr","it"]`) |
| `continent` | Continent name |
| `continent_code` | Continent code (e.g. "EU") |
| `city` | City name |
| `latitude` | Latitude coordinate |
| `longitude` | Longitude coordinate |
| `postal` | Postal code |
| `region` | State/canton name |
| `region_code` | State/canton code |
| `timezone` | IANA timezone (e.g. "Europe/Zurich") |
| `eu` | EU member boolean |

```js
// SDK JS
const loc = await maptilersdk.geolocation.info();
console.log(loc.city, loc.country, loc.latitude, loc.longitude);
```

---

## 7. Coordinates API

Search coordinate reference systems (CRS) and transform coordinates between them. Based on EPSG database version 12.029.

| Endpoint | URL Pattern |
|----------|-------------|
| Search CRS | `GET /coordinates/search/{query}.json?key=KEY` |
| Transform | `GET /coordinates/transform/{coords}.json?key=KEY&target_crs={epsg}` |

**Search options:** `transformations` (boolean), `exports` (boolean)

```js
// SDK JS — search
const crsResults = await maptilersdk.coordinates.search("france");

// SDK JS — single transform
const transformed = await maptilersdk.coordinates.transform([1, 45], { targetCrs: 9793 });

// SDK JS — batch transform
const batch = await maptilersdk.coordinates.transform(
  [[1, 45], [2, 46], [3, 47]],
  { targetCrs: 2154 }
);
```

---

## 8. Data API

Retrieve uploaded GeoJSON datasets from MapTiler Cloud.

| Endpoint | URL Pattern |
|----------|-------------|
| GeoJSON | `GET /data/{datasetId}/features.json?key=KEY` |

```js
// SDK JS
const geojson = await maptilersdk.data.get("dataset-uuid");

// Use with vector layer helpers
helpers.addPolygon(map, { data: "dataset-uuid", fillColor: "#3388ff" });
```

---

## Further Reading

- [MapTiler Cloud API docs](https://docs.maptiler.com/cloud/api/)
- [API key management](https://cloud.maptiler.com/account/keys/)
- [Static Maps generator](https://www.maptiler.com/cloud/static-maps/generator/)
- [MapTiler JS SDK reference](https://docs.maptiler.com/sdk-js/)
