#!/bin/bash
# Create build directory if it doesn't exist
mkdir -p build

# Copy public files to build
cp -r public/* build/

# Build the React app
npm run build
