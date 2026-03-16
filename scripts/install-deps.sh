#!/bin/bash
# Install MapTiler SDK packages
# Usage: bash scripts/install-deps.sh [sdk|client|geocoding|weather|3d|all]

set -e

case "$1" in
  sdk)
    npm install @maptiler/sdk
    echo "Installed @maptiler/sdk"
    ;;
  client)
    npm install @maptiler/client
    echo "Installed @maptiler/client"
    ;;
  geocoding)
    npm install @maptiler/geocoding-control
    echo "Installed @maptiler/geocoding-control"
    ;;
  weather)
    npm install @maptiler/weather
    echo "Installed @maptiler/weather"
    ;;
  3d)
    npm install @maptiler/3d
    echo "Installed @maptiler/3d"
    ;;
  all)
    npm install @maptiler/sdk @maptiler/geocoding-control
    echo "Installed @maptiler/sdk + @maptiler/geocoding-control"
    ;;
  *)
    echo "Usage: bash scripts/install-deps.sh [sdk|client|geocoding|weather|3d|all]"
    echo ""
    echo "  sdk        - @maptiler/sdk (interactive maps)"
    echo "  client     - @maptiler/client (headless API, no map)"
    echo "  geocoding  - @maptiler/geocoding-control (search bar UI)"
    echo "  weather    - @maptiler/weather (animated weather layers)"
    echo "  3d         - @maptiler/3d (glTF/GLB 3D models)"
    echo "  all        - sdk + geocoding-control"
    exit 1
    ;;
esac
