import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  optimizeDeps: {
    include: ['lineupjs']
  },
  resolve: {
    alias: {
      lineupjs: 'lineupjs/build/LineUpJS.js'
    }
  }
})
