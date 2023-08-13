/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: "media",
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

