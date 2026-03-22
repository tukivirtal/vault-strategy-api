/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: '#D4AF37',
        'gold-light': '#FFF5D1',
        'gold-dark': '#A67C00',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        terminal: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
