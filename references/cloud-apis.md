# MapTiler Cloud APIs — SDK Reference

All Cloud APIs are accessible directly from `@maptiler/sdk` via `config.apiKey`. No extra packages or manual URL construction needed.

> **REST endpoints** are available at `https://api.maptiler.com/` for server-side or non-JS use cases. See [full REST docs](https://docs.maptiler.com/cloud/api/). This reference focuses on the SDK JS wrappers that agents should use.

---

## 1. Geocoding

```js
// Forward — search places by name
const result = await maptilersdk.geocoding.forward("Zurich", {
  language: [maptilersdk.Language.ENGLISH],
  proximity: [8.5285, 47.377],
  country: ["ch"],
  limit: 5,
});
// result.features[0].geometry.coordinates → [lng, lat]
// result.features[0].place_name → "Zurich, Switzerland"

// Reverse — coordinates to address
const reverse = await maptilersdk.geocoding.reverse([8.5285, 47.377]);

// Batch — multiple queries at once
const batch = await maptilersdk.geocoding.batch(["Zurich", "Geneva"]);
```

### Geocoding Options

| Parameter | Description |
|-----------|-------------|
| `language` | Response language(s), array of `Language` enum values |
| `proximity` | Bias results toward `[lng, lat]` |
| `bbox` | Bounding box filter `[west, south, east, north]` |
| `limit` | Max results (1-10, default 5) |
| `types` | Filter by place type(s) |
| `country` | Filter by ISO country codes, e.g. `["sk", "cz"]` |
| `fuzzyMatch` | Enable fuzzy matching (boolean) |

### PlaceType Values

`country`, `region`, `subregion`, `county`, `municipality`, `municipal_district`, `locality`, `neighbourhood`, `place`, `postal_code`, `address`, `road`, `poi`

---

## 2. Static Maps

```js
// Centered on a point
const url = maptilersdk.staticMaps.centered(
  [8.5285, 47.377], 12,
  { hiDPI: true, width: 1000, height: 600, style: maptilersdk.MapStyle.OUTDOOR }
);

// Bounded by bbox
const bounded = maptilersdk.staticMaps.bounded(
  [5.95, 45.82, 10.49, 47.81],
  { width: 2048, height: 1024, style: maptilersdk.MapStyle.STREETS.DARK }
);

// Auto-fitted to markers/path
const auto = maptilersdk.staticMaps.automatic({
  hiDPI: true, width: 2048, height: 1024,
  style: maptilersdk.MapStyle.STREETS.LIGHT,
  path: routePoints,
  markers: [[8.53, 47.38, "#0a0"]],
  pathStrokeColor: "red",
});
```

---

## 3. Elevation

```js
// Single point → returns [lng, lat, elevation]
const point = await maptilersdk.elevation.at([6.864884, 45.832743]);

// Batch
const batch = await maptilersdk.elevation.batch([
  [6.864, 45.832], [86.925, 27.988]
]);

// From GeoJSON LineString (adds elevation to each coordinate)
const elevated = await maptilersdk.elevation.fromLineString(lineStringGeoJSON);
```

---

## 4. Geolocation (IP-based)

```js
const loc = await maptilersdk.geolocation.info();
// loc.city, loc.country, loc.latitude, loc.longitude
// loc.country_code, loc.timezone, loc.region, loc.postal
```

---

## 5. Coordinates (CRS Transform)

10,000+ EPSG coordinate reference systems supported.

```js
// Search for a CRS
const results = await maptilersdk.coordinates.search("france");

// Transform coordinates between CRS
const transformed = await maptilersdk.coordinates.transform(
  [1, 45], { targetCrs: 9793 }
);

// Batch transform
const batch = await maptilersdk.coordinates.transform(
  [[1, 45], [2, 46], [3, 47]],
  { targetCrs: 2154 }
);
```

---

## 6. Data (Cloud Datasets)

```js
// Fetch GeoJSON dataset from MapTiler Cloud
const geojson = await maptilersdk.data.get("dataset-uuid");

// Use directly with vector layer helpers
maptilersdk.helpers.addPolygon(map, { data: "dataset-uuid", fillColor: "#3388ff" });
```

---

## 7. Math (Local, No API Call)

```js
// Haversine distance between two points (meters)
const distance = maptilersdk.math.haversineDistanceWgs84(
  [8.5285, 47.377], [6.6323, 46.5197]
);
```

---

## Further Reading

- [MapTiler Cloud API docs](https://docs.maptiler.com/cloud/api/)
- [API key management](https://cloud.maptiler.com/account/keys/)
- [MapTiler JS SDK reference](https://docs.maptiler.com/sdk-js/)
