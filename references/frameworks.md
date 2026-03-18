# Framework Integration Reference

Same core pattern everywhere: get a DOM ref, create the map on mount, call `map.remove()` on unmount. The SDK needs WebGL/DOM -- **client-side only**.

```bash
npm install @maptiler/sdk
```

## React

```tsx
import { useEffect, useRef } from "react";
import { Map, config, MapStyle } from "@maptiler/sdk";
import "@maptiler/sdk/dist/maptiler-sdk.css";

config.apiKey = import.meta.env.VITE_MAPTILER_KEY;

export default function MapView() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<Map | null>(null);

  useEffect(() => {
    if (mapRef.current) return; // Strict Mode guard
    mapRef.current = new Map({
      container: containerRef.current!,
      style: MapStyle.STREETS,
      center: [8.5285, 47.377],
      zoom: 12,
    });
    mapRef.current.on("load", () => { /* add layers here */ });
    return () => { mapRef.current?.remove(); mapRef.current = null; };
  }, []);

  return <div ref={containerRef} style={{ width: "100%", height: "100vh" }} />;
}
```

**Strict Mode**: React 18 fires `useEffect` twice in dev. The `if (mapRef.current) return` guard + `null` reset in cleanup is essential. Env: `VITE_` (Vite), `REACT_APP_` (CRA).

## Next.js App Router

Same React component with two additions -- `"use client"` directive and `NEXT_PUBLIC_` env vars:

```tsx
// app/components/MapView.tsx
"use client";
import { useEffect, useRef } from "react";
import { Map, config, MapStyle } from "@maptiler/sdk";
import "@maptiler/sdk/dist/maptiler-sdk.css";

config.apiKey = process.env.NEXT_PUBLIC_MAPTILER_KEY!;

export default function MapView() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<Map | null>(null);
  useEffect(() => {
    if (mapRef.current) return;
    mapRef.current = new Map({
      container: containerRef.current!, style: MapStyle.STREETS,
      center: [8.5285, 47.377], zoom: 12,
    });
    return () => { mapRef.current?.remove(); mapRef.current = null; };
  }, []);
  return <div ref={containerRef} style={{ width: "100%", height: "100vh" }} />;
}
```

If `"use client"` alone still fails (`window is not defined`), wrap with dynamic import:
```tsx
import dynamic from "next/dynamic";
const MapView = dynamic(() => import("./components/MapView"), { ssr: false });
```

- **Why SSR fails**: SDK references `window`, `document`, WebGL canvas -- none exist in Node.
- **Env vars must** start with `NEXT_PUBLIC_` to reach the browser bundle.

## Vue 3 (Composition API)

```vue
<template>
  <div ref="mapContainer" style="width: 100%; height: 100vh" />
</template>
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { Map, config, MapStyle } from "@maptiler/sdk";
import "@maptiler/sdk/dist/maptiler-sdk.css";

config.apiKey = import.meta.env.VITE_MAPTILER_KEY;
const mapContainer = ref(null);
let map = null; // plain let, NOT ref() — Vue reactivity on Map causes perf issues

onMounted(() => {
  map = new Map({
    container: mapContainer.value, style: MapStyle.STREETS,
    center: [8.5285, 47.377], zoom: 12,
  });
});
onUnmounted(() => { map?.remove(); map = null; });
</script>
```

- **Nuxt SSR**: wrap with `<ClientOnly>` or guard with `process.client`.

## Svelte

```svelte
<script>
  import { onMount, onDestroy } from "svelte";
  import { Map, config, MapStyle } from "@maptiler/sdk";
  import "@maptiler/sdk/dist/maptiler-sdk.css";

  config.apiKey = import.meta.env.VITE_MAPTILER_KEY;
  let mapContainer;
  let map;

  onMount(() => {
    map = new Map({
      container: mapContainer, style: MapStyle.STREETS,
      center: [8.5285, 47.377], zoom: 12,
    });
  });
  onDestroy(() => { map?.remove(); });
</script>
<div bind:this={mapContainer} style="width: 100%; height: 100vh;" />
```

`bind:this` gives the raw DOM element. **SvelteKit SSR**: `onMount` only runs client-side; for top-level imports, guard with `browser` from `$app/environment`.

## Angular

```typescript
import { Component, ElementRef, OnInit, OnDestroy, ViewChild } from "@angular/core";
import { Map, config, MapStyle } from "@maptiler/sdk";

@Component({
  selector: "app-map",
  template: `<div #mapEl style="width: 100%; height: 100vh"></div>`,
})
export class MapComponent implements OnInit, OnDestroy {
  @ViewChild("mapEl", { static: true }) mapEl!: ElementRef;
  private map!: Map;

  ngOnInit() {
    config.apiKey = "YOUR_KEY";
    this.map = new Map({
      container: this.mapEl.nativeElement, style: MapStyle.STREETS,
      center: [8.5285, 47.377], zoom: 12,
    });
  }
  ngOnDestroy() { this.map?.remove(); }
}
```

Import SDK CSS in `angular.json` `styles` array. `{ static: true }` ensures the element is ready in `ngOnInit`. **SSR**: guard with `isPlatformBrowser()`.

## Vanilla JS / Vite

```js
import { Map, config, MapStyle } from "@maptiler/sdk";
import "@maptiler/sdk/dist/maptiler-sdk.css";

config.apiKey = import.meta.env.VITE_MAPTILER_KEY;
const map = new Map({ container: "map", style: MapStyle.STREETS, center: [8.5285, 47.377], zoom: 12 });
```

```html
<div id="map" style="width: 100%; height: 100vh;"></div>
```

---

## Cleanup & Style Changes

Always call `map.remove()` when the map leaves the DOM. Without it: WebGL contexts leak (browsers cap at 8-16), memory grows from tile caches/listeners, and mobile devices crash from GPU exhaustion.

`setStyle()` strips all custom sources/layers. Re-add after the new style loads:
```js
map.setStyle(MapStyle.SATELLITE);
map.once("styledata", () => { addYourCustomLayers(); });
```

## Env Var Quick Reference

| Tool | Prefix | Access |
|---|---|---|
| Vite | `VITE_` | `import.meta.env.VITE_MAPTILER_KEY` |
| Next.js | `NEXT_PUBLIC_` | `process.env.NEXT_PUBLIC_MAPTILER_KEY` |
| CRA | `REACT_APP_` | `process.env.REACT_APP_MAPTILER_KEY` |
| Angular | -- | `environment.ts` |
| SvelteKit | `PUBLIC_` | `$env/static/public` |

## Starter Templates

| Framework | Repo |
|---|---|
| React | [maptiler/get-started-react](https://github.com/maptiler/get-started-react) |
| Next.js | [maptiler/get-started-nextjs](https://github.com/maptiler/get-started-nextjs) |
| Vue.js | [maptiler/get-started-vuejs](https://github.com/maptiler/get-started-vuejs) |
| Svelte | [maptiler/get-started-svelte](https://github.com/maptiler/get-started-svelte) |
| Angular | [maptiler/get-started-angular](https://github.com/maptiler/get-started-angular) |
