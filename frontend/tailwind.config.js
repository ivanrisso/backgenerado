import defaultTheme from "tailwindcss/defaultTheme";

export default {
    content: ["./index.html", "./src/**/*.{vue,ts}"],
    theme: {
        extend: {
            colors: {
                primary: "#7C5CFF",
                app: "#F6F7FB",
                surface: "#FFFFFF",
                sidebar: "#F2F3F8",
                border: "#E2E8F0",
                text: {
                    primary: "#0F172A",
                    muted: "#64748B"
                },
                semantic: {
                    success: { fg: "#16A34A", bg: "#EAFBF1" },
                    warning: { fg: "#D97706", bg: "#FFF7E6" },
                    error: { fg: "#DC2626", bg: "#FFECEC" },
                    overdue: { fg: "#EA580C", bg: "#FFF0E8" },
                    info: { fg: "#0EA5E9", bg: "#E7F6FF" }
                }
            },
            borderRadius: {
                sm: "10px",
                md: "12px",
                lg: "16px",
                xl: "20px"
            },
            boxShadow: {
                sm: "0 1px 2px rgba(15,23,42,.06)",
                md: "0 6px 18px rgba(15,23,42,.08)"
            },
            fontFamily: {
                sans: ["Inter", ...defaultTheme.fontFamily.sans]
            }
        }
    },
    plugins: []
};
