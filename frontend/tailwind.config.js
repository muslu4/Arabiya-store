/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#ecf9fb',
          100: '#cdf0f7',
          200: '#9ee1ee',
          300: '#6dd2e6',
          400: '#41c3de',
          500: '#0891b2',
          600: '#0778a0',
          700: '#056b8c',
          800: '#045578',
          900: '#034464',
        },
        secondary: {
          50: '#f0fef9',
          100: '#dcfdf2',
          200: '#b9fae5',
          300: '#7ef7d6',
          400: '#4ef5c3',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0a7968',
          800: '#085d54',
          900: '#064e45',
        }
      },
      fontFamily: {
        'arabic': ['Cairo', 'Tajawal', 'system-ui', 'sans-serif'],
        'sans': ['Cairo', 'Tajawal', 'system-ui', 'sans-serif'],
      },
      animation: {
        'bounce-in': 'bounceIn 0.5s ease-out',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        bounceIn: {
          '0%': { transform: 'scale(0.3)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'glow': '0 0 20px rgba(139, 92, 246, 0.3)',
      }
    },
  },
  plugins: [],
}