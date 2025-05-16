/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        jakarta: ['"Plus Jakarta Sans Variable", system-ui, sans-serif'],
        quickquick: ['"QuickQuick Condensed Italic"', 'sans-serif'],
        edgeRacer: ['"Edge Racer Engraved Italic"', 'sans-serif'],
        quadrillion: ['"Quadrillion"', 'sans-serif'],
        
      },
      
    },
  },
    plugins: [require('tailwind-scrollbar-hide')],

}