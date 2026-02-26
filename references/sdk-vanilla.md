# MapTiler SDK in Vanilla JS

This guide covers integrating the MapTiler Map into a plain HTML/JS application (or any framework outside React that relies on DOM nodes).

## 1. Installation

If using a bundler (Vite, Webpack):
```bash
npm install @maptiler/sdk
```

If using via CDN in an HTML file:
```html
<script src="https://cdn.maptiler.com/maptiler-sdk-js/v3.0.0/maptiler-sdk.umd.js"></script>
<link href="https://cdn.maptiler.com/maptiler-sdk-js/v3.0.0/maptiler-sdk.css" rel="stylesheet" />
```

## 2. Basic Setup (Bundler)

You must create an HTML container and import the CSS.

```html
<!-- index.html -->
<div id="map" style="width: 100vw; height: 100vh;"></div>
```

```javascript
// main.js
import * as maptilersdk from '@maptiler/sdk';
import "@maptiler/sdk/dist/maptiler-sdk.css"; // Required!

// 1. Set the API key
maptilersdk.config.apiKey = import.meta.env.VITE_MAPTILER_API_KEY || 'YOUR_MAPTILER_API_KEY_HERE';

// 2. Initialize the map
const map = new maptilersdk.Map({
  container: 'map', // id of the HTML element
  style: maptilersdk.MapStyle.STREETS, // built-in style
  center: [14.42076, 50.08804], // starting position [lng, lat]
  zoom: 14 // starting zoom
});

// 3. (Optional) Add map load listener
map.on('load', () => {
  console.log('Map has fully loaded');
});
```

## 3. Basic Setup (CDN)

When using the CDN approach, `maptilersdk` is available on the `window` object.

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="https://cdn.maptiler.com/maptiler-sdk-js/v3.0.0/maptiler-sdk.umd.js"></script>
    <link href="https://cdn.maptiler.com/maptiler-sdk-js/v3.0.0/maptiler-sdk.css" rel="stylesheet" />
    <style>
        body { margin: 0; padding: 0; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
    </style>
</head>
<body>
<div id="map"></div>
<script>
    maptilersdk.config.apiKey = 'YOUR_MAPTILER_API_KEY_HERE';
    const map = new maptilersdk.Map({
        container: 'map', // container's id or the HTML element to render the map
        style: maptilersdk.MapStyle.STREETS,
        center: [16.62662018, 49.2125578], // starting position [lng, lat]
        zoom: 14 // starting zoom
    });
</script>
</body>
</html>
```

## 4. Troubleshooting
- If the map renders as a thin line, the container `#map` does not have a defined height or absolute positioning. Ensure `height: 100vh;` or absolute positioning.
- Ensure the API key is valid. Missing API keys result in gray/white maps and 401 Unauthorized errors in the network tab.

## 5. Official Resources

- [MapTiler SDK JS API Reference](https://docs.maptiler.com/sdk-js/api/)
- [MapTiler Examples](https://docs.maptiler.com/sdk-js/examples/)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)