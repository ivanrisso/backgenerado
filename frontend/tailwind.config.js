/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: [
                    'Inter',
                    '-apple-system',
                    'BlinkMacSystemFont',
                    'Segoe UI',
                    'Roboto',
                    'Helvetica Neue',
                    'Arial',
                    'sans-serif'
                ],
            },
            colors: {
                // Custom Apple-like neutral palette if default grays aren't enough
                // Tailwind's slate or gray is usually fine.
                'apple-gray': '#f5f5f7',
                'apple-blue': '#0071e3',
            }
        },
    },
    plugins: [],
}
