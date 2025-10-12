#!/usr/bin/env bash
set -o errexit

echo "🔥 FORCING PostCSS FIX..."
node verify-postcss.js

echo "📦 Installing dependencies..."
npm ci --legacy-peer-deps

echo "🧹 Clearing cache..."
rm -rf node_modules/.cache || true
rm -rf .cache || true

echo "🏗️ Building React app..."
npm run build

echo "✅ Frontend build completed!"
