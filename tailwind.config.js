// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './apps/**/forms.py', // Good to have for form styling
  ],
  theme: {
    extend: {
      // Define our font families
      fontFamily: {
        // Zodiak will be our 'serif' font, used for headings (CORRECTED)
        serif: ['sometimes', 'serif'],
        // 'sometimes' will be our default 'sans' font, used for body text (CORRECTED)
        sans: ['serif'],//'Zodiak-Regular',
      },
      // Define our custom color names that use CSS variables
      colors: {
        'accent': 'var(--color-accent)',
        'accent-hover': 'var(--color-accent-hover)',
        'text-dark': 'var(--color-text-dark)',
        'text-subtle': 'var(--color-text-subtle)',
        'bg-main': 'var(--color-bg-main)',
        'bg-subtle': 'var(--color-bg-subtle)',
        'footer-bg': 'var(--color-footer-bg, #111827)', // Added a footer bg color with fallback
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'), // For the redesigned vehicle card
    require('@tailwindcss/line-clamp'),  // For the redesigned vehicle card
  ],
}