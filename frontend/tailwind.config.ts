import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Base - warm off-whites and clean whites
        'warm-white': '#fafaf8',
        'off-white': '#f5f3f0',
        'cream': '#fffbf7',
        
        // Text - deep navy/charcoal
        'text-primary': '#1a1a2e',
        'text-secondary': '#6b6b7f',
        'text-muted': '#9a9aaa',
        
        // Accent - rich teal/deep ocean blue
        'teal': '#0d7377',
        'teal-light': '#14919b',
        'teal-lighter': '#3fb9cf',
        'ocean': '#084c61',
        
        // Functional
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'error-light': '#fee2e2',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Lora', 'serif'],
      },
      fontSize: {
        xs: ['12px', '16px'],
        sm: ['14px', '20px'],
        base: ['16px', '24px'],
        lg: ['18px', '28px'],
        xl: ['20px', '28px'],
        '2xl': ['24px', '32px'],
        '3xl': ['30px', '36px'],
        '4xl': ['36px', '44px'],
      },
      borderRadius: {
        sm: '8px',
        md: '10px',
        lg: '12px',
        xl: '16px',
        '2xl': '20px',
        full: '9999px',
      },
      boxShadow: {
        xs: '0 1px 2px 0 rgba(26, 26, 46, 0.05)',
        sm: '0 1px 3px 0 rgba(26, 26, 46, 0.1), 0 1px 2px 0 rgba(26, 26, 46, 0.06)',
        md: '0 4px 6px -1px rgba(26, 26, 46, 0.1), 0 2px 4px -1px rgba(26, 26, 46, 0.06)',
        lg: '0 10px 15px -3px rgba(26, 26, 46, 0.1), 0 4px 6px -2px rgba(26, 26, 46, 0.05)',
        xl: '0 20px 25px -5px rgba(26, 26, 46, 0.1), 0 10px 10px -5px rgba(26, 26, 46, 0.04)',
      },
      animation: {
        'pulse-soft': 'pulse-soft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fade-in 0.3s ease-in-out',
        'slide-up': 'slide-up 0.3s ease-out',
        'highlight': 'highlight 1s ease-in-out',
        'typing': 'typing 0.6s ease-in-out infinite',
      },
      keyframes: {
        'pulse-soft': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'highlight': {
          '0%': { backgroundColor: 'rgba(13, 115, 119, 0)' },
          '50%': { backgroundColor: 'rgba(13, 115, 119, 0.1)' },
          '100%': { backgroundColor: 'rgba(13, 115, 119, 0)' },
        },
        'typing': {
          '0%, 60%, 100%': { opacity: '0.3' },
          '30%': { opacity: '1' },
        },
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
        '20': '80px',
        '24': '96px',
      },
    },
  },
  plugins: [],
}

export default config
