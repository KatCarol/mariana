/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.html", "../**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {},
      fontFamily: {
        body: ['Poppins', 'sans-serif']
      },
    },
  },
  plugins: [],
}

