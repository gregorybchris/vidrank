module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    fontFamily: {
      roboto: ["roboto"],
    },
    extend: {
      colors: {
        "tint-dark": "rgba(0, 0, 0, 0.2)",
        "tint-light": "rgba(255, 255, 255, 0.1)",
      },
    },
  },
  plugins: [require("tailwindcss-dotted-background")],
};
