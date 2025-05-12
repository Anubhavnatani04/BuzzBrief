/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  extend: {
    fontFamily: {
      sans: ['Inter', 'sans-serif'],         // override default sans
      serif: ['Merriweather', 'serif'],      // custom serif font
      mono: ['Fira Code', 'monospace'],      // custom monospaced
      poppins: ['Poppins', 'sans-serif'],    // new custom font
    },
  },
  
  plugins: [],
}

