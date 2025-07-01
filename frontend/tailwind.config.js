/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      boxShadow: {
        'clay-light': '6px 6px 12px rgb(var(--color-clay-light-shadow-dark)), -6px -6px 12px rgb(var(--color-clay-light-shadow-light))',
        'clay-dark': '6px 6px 12px rgb(var(--color-clay-dark-shadow-dark)), -6px -6px 12px rgb(var(--color-clay-dark-shadow-light))',
        'inner-clay-light': 'inset 2px 2px 5px rgb(var(--color-clay-light-shadow-dark)), inset -2px -2px 5px rgb(var(--color-clay-light-shadow-light))',
        'inner-clay-dark': 'inset 2px 2px 5px rgb(var(--color-clay-dark-shadow-dark)), inset -2px -2px 5px rgb(var(--color-clay-dark-shadow-light))',
        'clay-button-light': '4px 4px 8px rgb(var(--color-clay-light-shadow-dark)), -4px -4px 8px rgb(var(--color-clay-light-shadow-light))',
        'clay-button-dark': '4px 4px 8px rgb(var(--color-clay-dark-shadow-dark)), -4px -4px 8px rgb(var(--color-clay-dark-shadow-light))',
      },
    },
  },
  plugins: [],
}
