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
          50: '#fdf8f5',
          100: '#f5ede1',
          200: '#e8d7c3',
          300: '#d4af37',
          400: '#c99a00',
          500: '#8B6F47',
          600: '#7a6140',
          700: '#6b5339',
          800: '#5c4532',
          900: '#4d372b',
        },
        secondary: {
          50: '#f5f9f0',
          100: '#e8f5e0',
          200: '#d1ebc2',
          300: '#8FBC8F',
          400: '#556B2F',
          500: '#3d5c25',
          600: '#354d1f',
          700: '#2d3e19',
          800: '#252f13',
          900: '#1d200d',
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
        'glow': '0 0 20px rgba(139, 111, 71, 0.3)',
      }
    },
  },
  plugins: [],
}