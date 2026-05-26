import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0e17',
        foreground: '#e8edf5',
        card: {
          DEFAULT: 'rgba(15, 23, 42, 0.7)',
          foreground: '#e8edf5'
        },
        primary: {
          DEFAULT: '#00d4ff',
          foreground: '#0a0e17',
          50: '#e6fcff',
          100: '#b3f5ff',
          200: '#80eeff',
          300: '#4de7ff',
          400: '#1ae0ff',
          500: '#00d4ff',
          600: '#00a8cc',
          700: '#007c99',
          800: '#005066',
          900: '#002433'
        },
        secondary: {
          DEFAULT: '#06b6d4',
          foreground: '#0a0e17'
        },
        accent: {
          DEFAULT: '#ff6b35',
          foreground: '#ffffff',
          red: '#ff3d3d'
        },
        muted: {
          DEFAULT: '#1e293b',
          foreground: '#94a3b8'
        },
        border: 'rgba(0, 212, 255, 0.2)',
        input: 'rgba(30, 41, 59, 0.8)',
        ring: '#00d4ff'
      },
      fontFamily: {
        sans: ['Inter', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 212, 255, 0.3)',
        'glow-lg': '0 0 40px rgba(0, 212, 255, 0.4)',
        'glow-accent': '0 0 20px rgba(255, 107, 53, 0.3)',
        'card': '0 8px 32px rgba(0, 0, 0, 0.4)',
      },
      backdropBlur: {
        'glass': '16px',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'slide-up': 'slideUp 0.6s ease-out',
        'fade-in': 'fadeIn 0.8s ease-out',
        'particle': 'particle 20s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 212, 255, 0.6)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        particle: {
          '0%': { transform: 'translateY(100vh) rotate(0deg)', opacity: '0' },
          '10%': { opacity: '1' },
          '90%': { opacity: '1' },
          '100%': { transform: 'translateY(-100vh) rotate(720deg)', opacity: '0' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
