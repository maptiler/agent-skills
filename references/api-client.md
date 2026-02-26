# MapTiler API Client (`@maptiler/client`)

If the user wants to fetch data (like geocoding/search, IP geolocation, static map images) without actually rendering a dynamic interactive map, you should use the `@maptiler/client` package.

## 1. Installation
```bash
npm install @maptiler/client
```

## 2. Global configuration

Before using any of the APIs, you must provide your API key.

```javascript
import * as maptilerClient from '@maptiler/client';

// Pass the API key securely from environment variables
maptilerClient.config.apiKey = process.env.MAPTILER_API_KEY || 'YOUR_MAPTILER_API_KEY_HERE';
```

## 3. Geocoding (Forward) - Address to Coordinates

To search for a place by name, use the forward geocoding method.

```javascript
async function searchPlace(query) {
  // Returns a GeoJSON FeatureCollection
  const result = await maptilerClient.geocoding.forward(query, {
    limit: 5,
    // Optional: Bias the search to a specific location
    // proximity: [14.42, 50.08] // [lng, lat]
    // Optional: Filter by country
    // country: ['CZ', 'US']
  });
  
  // result.features[0].geometry.coordinates will give [longitude, latitude]
  // result.features[0].place_name gives the full string
  return result;
}

// searchPlace("Eiffel Tower")
```

## 4. Geocoding (Reverse) - Coordinates to Address

To find an address from coordinates `[lng, lat]`.

```javascript
async function getAddressFromCoords(lng, lat) {
  const result = await maptilerClient.geocoding.reverse([lng, lat], {
    limit: 1,
    // Optional: language bias
    // language: ['en']
  });
  
  return result.features.length > 0 ? result.features[0].place_name : null;
}
```

## 5. Static Maps

Generate a static map image URL for use in `<img>` tags, emails, or reports where interactivity is not needed.

```javascript
// URL for a static map center on Prague
const staticMapUrl = maptilerClient.staticMaps.centered(
  [14.42, 50.08], // center [lng, lat]
  12,             // zoom
  {
    width: 800,
    height: 600,
    style: 'streets-v2', // or 'satellite', 'outdoor', etc.
    // Optional: Add markers
    // markers: [{ lng: 14.42, lat: 50.08, color: '#ff0000' }] 
  }
);

console.log(staticMapUrl); 
// Output: https://api.maptiler.com/maps/streets-v2/static/14.42,50.08,12/800x600.png?key=...
```

## 6. IP Geolocation

Get the user's approximate location based on their IP address.

```javascript
async function getUserLocation() {
  const result = await maptilerClient.geolocation.info();
  
  // result includes:
  // result.country, result.city, result.latitude, result.longitude
  console.log(`User is in ${result.city}, ${result.country}`);
  return [result.longitude, result.latitude];
}
```

## 7. Elevation

Get the elevation (height in meters) for a specific coordinate.

```javascript
async function getElevation(lng, lat) {
  // Returns the elevation in meters (e.g., 235)
  const elevation = await maptilerClient.elevation.at([lng, lat]);
  return elevation;
}
```

## 8. Official Resources

- [MapTiler Client JS API Reference](https://docs.maptiler.com/client-js/api/)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)

## Important Note
If the user also needs interactive maps, `@maptiler/sdk` actually re-exports `@maptiler/client` underneath, meaning they can just do:
```javascript
import { geocoding, config } from '@maptiler/sdk';

config.apiKey = '...';
geocoding.forward('Paris');
```
This saves them from installing both packages. Only install `@maptiler/client` if they DO NOT need a map visual.