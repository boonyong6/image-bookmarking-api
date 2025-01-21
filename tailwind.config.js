/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./accounts/templates/**/*.html", "./dist/js/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["winter", "night"],
    darkTheme: "night",
  },
};
