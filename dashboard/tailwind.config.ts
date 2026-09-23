import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Outfit", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
      colors: {
        background: "#050708",
        foreground: "#F3F6F7",
        surface: "#071118",
        "surface-hover": "#0E2230",
        card: "#0B1B24",
        "card-border": "#1A3340",
        "border-light": "#274858",
        primary: {
          DEFAULT: "#18D8C0",
          hover: "#12C4AE",
          light: "#22C7F2",
          subtle: "rgba(24, 216, 192, 0.12)",
        },
        secondary: {
          DEFAULT: "#071118",
          hover: "#0B1B24",
        },
        danger: {
          DEFAULT: "#ef4444",
          hover: "#dc2626",
        },
        success: "#22c55e",
        warning: "#f59e0b",
        muted: "#7A93A1",
      },
      borderRadius: {
        DEFAULT: "10px",
        md: "12px",
        lg: "18px",
      },
    },
  },
  plugins: [],
};
export default config;
