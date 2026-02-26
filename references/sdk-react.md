# MapTiler SDK in React/Next.js

This guide explains how to integrate MapTiler SDK (`@maptiler/sdk`) in a React, Next.js, or Vite + React environment.

## 1. Installation
Install the SDK and optionally the client:
```bash
npm install @maptiler/sdk
```

## 2. Basic Setup (React Hooks)

A map component in React requires a `useRef` for the map container DOM element and a `useRef` to store the Map instance itself, to prevent re-initializing it on every render.
You must ensure the map is only initialized *once* inside a `useEffect`.

```tsx
import React, { useRef, useEffect, useState } from 'react';
import * as maptilersdk from '@maptiler/sdk';
import "@maptiler/sdk/dist/maptiler-sdk.css";

// IMPORTANT: Do not forget to import the CSS file!

export default function MapComponent() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maptilersdk.Map | null>(null);
  const [zoom] = useState(14);
  const [center] = useState({ lng: 14.42076, lat: 50.08804 });

  useEffect(() => {
    // Prevent re-initialization
    if (map.current) return;

    // IMPORTANT: Set the API Key
    // Retrieve this from your environment variables:
    // e.g., import.meta.env.VITE_MAPTILER_API_KEY
    maptilersdk.config.apiKey = process.env.NEXT_PUBLIC_MAPTILER_API_KEY || 'YOUR_MAPTILER_API_KEY_HERE';

    map.current = new maptilersdk.Map({
      container: mapContainer.current!,
      style: maptilersdk.MapStyle.STREETS,
      center: [center.lng, center.lat],
      zoom: zoom,
      // Optional: globe projection is great for lower zoom levels
      // projection: 'globe' 
    });

    // Example of cleanup logic
    return () => {
      if (map.current) {
         // Do not call map.current.remove() aggressively in React Strict Mode if not handled well
         // but ideally you'd clean up event listeners here.
      }
    };
  }, [center.lng, center.lat, zoom]);

  return (
    <div className="map-wrap" style={{ position: 'relative', width: '100%', height: '100vh' }}>
      <div ref={mapContainer} className="map" style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
```

## 3. Important Notes for Next.js

If you use Next.js App Router (Next.js 13+):
1. **`"use client"`**: You *must* add `"use client";` at the very top of your map component file, because maps require the browser DOM and Window objects.
2. **Environment Variables**: Use `process.env.NEXT_PUBLIC_MAPTILER_API_KEY`. The variable *must* start with `NEXT_PUBLIC_` so it is exposed to the browser.
3. MapTiler SDK relies on WebGL. It cannot be server-side rendered. If Next.js throws `window is not defined`, you might need to dynamically import the Map component using `next/dynamic` with `{ ssr: false }`.

## 4. Common Pitfalls

- **Forgetting CSS**: If the map loads but looks completely chaotic or controls are unstyled, you forgot to import `"@maptiler/sdk/dist/maptiler-sdk.css"`.
- **Double Rendering**: In React Strict Mode, `useEffect` fires twice. The `if (map.current) return;` check is crucial.
- **API Key**: If tiles fail to load with a 401 or 403 error, the API key is missing or invalid.

-> Next: For custom styles, markers, or advanced maps, see `styles-and-layers.md`.

## 5. Official Resources

- [MapTiler React SDK Reference](https://docs.maptiler.com/react/)
- [MapTiler SDK JS API Reference](https://docs.maptiler.com/sdk-js/api/)
- [MapTiler Cloud Console](https://cloud.maptiler.com/)