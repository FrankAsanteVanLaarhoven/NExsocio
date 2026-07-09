/** Ephemeral Precision design tokens */
export const tokens = {
  colors: {
    base: "#0A0A0A",
    surface: "#111111",
    surfaceElevated: "#1A1A1A",
    border: "#2A2A2A",
    borderSubtle: "#1F1F1F",
    text: "#F5F5F5",
    textMuted: "#8A8A8A",
    textDim: "#5A5A5A",
    accent: "#00E5FF",
    accentMuted: "#00B8CC",
    accentGlow: "rgba(0, 229, 255, 0.15)",
    success: "#00C853",
    warning: "#FFB300",
    danger: "#FF5252",
    kids: "#7C4DFF",
    prime: "#00E5FF",
    professional: "#4FC3F7",
  },
  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
    "2xl": "3rem",
  },
  radius: {
    sm: "4px",
    md: "8px",
    lg: "12px",
  },
  font: {
    sans: "var(--font-inter), system-ui, sans-serif",
    mono: "var(--font-geist-mono), monospace",
  },
  motion: {
    spring: { type: "spring" as const, stiffness: 400, damping: 30 },
    fade: { duration: 0.2 },
  },
} as const;