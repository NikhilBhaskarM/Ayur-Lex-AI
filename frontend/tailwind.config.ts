import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { 50: '#f0f4f8', 100: '#d9e2ec', 200: '#bcccdc', 300: '#9fb3c8', 400: '#829ab1', 500: '#627d98', 600: '#486581', 700: '#334e68', 800: '#243b53', 900: '#1a365d', 950: '#102a43' },
        accent: { 50: '#e6fffa', 100: '#b2f5ea', 200: '#81e6d9', 300: '#4fd1c5', 400: '#38b2ac', 500: '#319795', 600: '#2c7a7b', 700: '#285e61', 800: '#234e52', 900: '#1d4044' },
        gold: { 50: '#fffff0', 100: '#fefcbf', 200: '#faf089', 300: '#f6e05e', 400: '#ecc94b', 500: '#d69e2e', 600: '#b7791f', 700: '#975a16', 800: '#744210', 900: '#5f370e' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config
