/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./app/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        'beige': '#f0e7d5',
        'dark-beige': '#e0d7c5',
        'green': '#95cc97',
        'darkgreen': '#678568',
        'black': '#000000',
      },
      fontFamily: {
        'roboto': ['"Roboto"', 'monospace'],
      },
      boxShadow: {
        'header': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      },
      borderWidth: {
        '2': '2px',
      },
    },
  },
  plugins: [],
}