/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mib: {
          black: '#0a0a0a',
          dark: '#1a1a1a',
          green: '#00ff41',
          'green-dim': '#008f24',
          silver: '#e5e5e5',
          glass: 'rgba(0, 255, 65, 0.05)',
        }
      },
      fontFamily: {
        mono: ['"Courier New"', 'Courier', 'monospace'],
        sans: ['"Inter"', 'sans-serif'],
        display: ['"Orbitron"', '"Arial Black"', 'sans-serif'], // Hypothetical font for headers if available, otherwise fallbacks
      },
      boxShadow: {
        'glow': '0 0 10px rgba(0, 255, 65, 0.5)',
        'glow-lg': '0 0 20px rgba(0, 255, 65, 0.6)',
        'glow-text': '0 0 5px rgba(0, 255, 65, 0.8)',
      },
      animation: {
        'scan': 'scan 2s linear infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

