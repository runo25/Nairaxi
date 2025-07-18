// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './static/src/**/*.js',
    './node_modules/flowbite/**/*.js'
  ],
  important: true,
  theme: {
    container: {
      center: true,
      padding: '1.5rem',
    },
    extend: {
      spacing: {
        4.5: '1.125rem',
        15: '3.75rem',
      },
      boxShadow: {
        card: '0 1px 3px rgba(0,0,0,0.12)',
        button: '0 1px 2px rgba(0,0,0,0.1)',
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
      },
      // Your theme customizations (colors, fonts)
      colors: {
        'nairaxi-blue': 'var(--color-brand-primary)',
        'nairaxi-dark': 'var(--color-brand-secondary)',
        'nairaxi-grey-text': '#637988',
        'nairaxi-grey-bg': '#f0f3f4',
        'nairaxi-border': '#dce1e5',
      },
      

      fontFamily: {
        sans: ['sometimes', 'sans-serif'],
        'cabin-sketch': ['"Cabin Sketch"', 'sans-serif'],
        'finger-paint': ['"Finger Paint"', 'sans-serif'],
      },

    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    // require('@tailwindcss/container-queries'), // if you installed and plan to use it
  ],
}
