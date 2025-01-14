/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["winter", "night"],
    darkTheme: "night",
  },
};
