/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./djangochat/**/*.html",
    "./djangochat/**/*.js",
    // Add paths to all your app's templates and JavaScript files
    "./core/templates/**/*.html",
    "./room/templates/**/*.html",
    "./friend/templates/**/*.html",
    // Add paths to any other templates or JavaScript files
  ],
  theme: {
    extend: {
      colors: {
        violet: {
          50: "#f5f3ff",
          100: "#ede9fe",
          200: "#ddd6fe",
          300: "#c4b5fd",
          400: "#a78bfa",
          500: "#8b5cf6",
          600: "#7c3aed",
          700: "#6d28d9",
          800: "#5b21b6",
          900: "#4c1d95",
          950: "#2e1065",
        },
      },
      fontFamily: {
        customFont: ["Lato", "sans-serif"],
      },
    },
  },
  plugins: [],
};

