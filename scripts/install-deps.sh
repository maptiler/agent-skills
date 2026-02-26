#!/bin/bash

# install-deps.sh
# Installs MapTiler dependencies based on the requested module

if [ "$1" == "sdk" ]; then
    echo "Installing @maptiler/sdk..."
    npm install @maptiler/sdk
elif [ "$1" == "client" ]; then
    echo "Installing @maptiler/client..."
    npm install @maptiler/client
else
    echo "Usage: bash scripts/install-deps.sh [sdk|client]"
    exit 1
fi
