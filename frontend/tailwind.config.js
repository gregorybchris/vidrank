module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./widgets/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    fontFamily: {
      manrope: ["Manrope Variable"],
      work: ["Work Sans Variable"],
    },
    extend: {
      colors: {},
    },
  },
  plugins: [require("tailwindcss-dotted-background")],
};
