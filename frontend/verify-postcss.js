#!/usr/bin/env node

/**
 * 🔥 FORCE FIX PostCSS configuration for Tailwind CSS v4
 * This script ALWAYS overwrites postcss.config.js to ensure correct configuration
 */

const fs = require('fs');
const path = require('path');

const postcssConfigPath = path.join(__dirname, 'postcss.config.js');

console.log('');
console.log('🔥🔥🔥 FORCING PostCSS FIX 🔥🔥🔥');
console.log('');

const correctConfig = `module.exports = {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
`;

// ALWAYS overwrite the file - no checks, just fix it!
fs.writeFileSync(postcssConfigPath, correctConfig, 'utf8');

console.log('✅ PostCSS configuration FORCED to correct version!');
console.log('✅ Using @tailwindcss/postcss (Tailwind CSS v4)');
console.log('');

process.exit(0);