#!/usr/bin/env node

/**
 * Verify PostCSS configuration is correct for Tailwind CSS v4
 */

const fs = require('fs');
const path = require('path');

const postcssConfigPath = path.join(__dirname, 'postcss.config.js');

console.log('🔍 Verifying PostCSS configuration...');

if (!fs.existsSync(postcssConfigPath)) {
  console.error('❌ postcss.config.js not found!');
  process.exit(1);
}

const content = fs.readFileSync(postcssConfigPath, 'utf8');

if (content.includes("'@tailwindcss/postcss'") || content.includes('"@tailwindcss/postcss"')) {
  console.log('✅ PostCSS configuration is correct!');
  console.log('✅ Using @tailwindcss/postcss (Tailwind CSS v4)');
  process.exit(0);
} else if (content.includes('tailwindcss')) {
  console.error('❌ ERROR: postcss.config.js is using old "tailwindcss" plugin!');
  console.error('❌ This will cause build to fail.');
  console.error('');
  console.error('Expected:');
  console.error("  '@tailwindcss/postcss': {}");
  console.error('');
  console.error('Found:');
  console.error('  tailwindcss: {}');
  console.error('');
  console.error('🔥 Fixing automatically...');
  
  const correctConfig = `module.exports = {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
`;
  
  fs.writeFileSync(postcssConfigPath, correctConfig, 'utf8');
  console.log('✅ Fixed! postcss.config.js has been updated.');
  process.exit(0);
} else {
  console.error('❌ postcss.config.js has unexpected content!');
  process.exit(1);
}