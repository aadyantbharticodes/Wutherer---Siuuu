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
        sans: ["'Space Grotesk'", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
      colors: {
        background: "#07111a",
        foreground: "#e8f4f8",
        surface: "#0c1924",
        "surface-hover": "#112634",
        card: "#0e1d29",
        "card-border": "#1d3544",
        "border-light": "#29485a",
        primary: {
          DEFAULT: "#2dd4bf",
          hover: "#14b8a6",
          light: "#7dd3fc",
          subtle: "rgba(45, 212, 191, 0.12)",
        },
        secondary: {
          DEFAULT: "#09151f",
          hover: "#102532",
        },
        danger: {
          DEFAULT: "#ef4444",
          hover: "#dc2626",
        },
        success: "#22c55e",
        warning: "#f59e0b",
        muted: "#64748b",
      },
      borderRadius: {
        DEFAULT: "6px",
        md: "8px",
        lg: "12px",
      },
    },
  },
  plugins: [],
};
export default config;
