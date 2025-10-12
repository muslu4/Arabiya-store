const fs = require('fs');
const path = require('path');

module.exports = function override(config, env) {
  // 🔥 FORCE FIX PostCSS configuration
  const postcssConfigPath = path.join(__dirname, 'postcss.config.js');
  const correctConfig = `module.exports = {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
`;
  
  // Always overwrite postcss.config.js
  fs.writeFileSync(postcssConfigPath, correctConfig, 'utf8');
  console.log('🔥 PostCSS config FORCED in config-overrides.js');

  // Fix webpack resolve fallbacks
  config.resolve.fallback = {
    ...config.resolve.fallback,
    "http": require.resolve("stream-http"),
    "https": require.resolve("https-browserify"),
    "util": require.resolve("util/"),
    "zlib": require.resolve("browserify-zlib"),
    "stream": require.resolve("stream-browserify"),
    "assert": require.resolve("assert/"),
    "url": require.resolve("url/"),
    "crypto": require.resolve("crypto-browserify"),
  };

  // 🔥 FORCE PostCSS loader configuration
  const postcssLoader = config.module.rules.find(
    rule => rule.oneOf
  );
  
  if (postcssLoader && postcssLoader.oneOf) {
    postcssLoader.oneOf.forEach(rule => {
      if (rule.use) {
        rule.use.forEach(loader => {
          if (loader.loader && loader.loader.includes('postcss-loader')) {
            loader.options = {
              ...loader.options,
              postcssOptions: {
                plugins: [
                  require('@tailwindcss/postcss'),
                  require('autoprefixer'),
                ],
              },
            };
            console.log('🔥 PostCSS loader FORCED in webpack config');
          }
        });
      }
    });
  }

  return config;
}