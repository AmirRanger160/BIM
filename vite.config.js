import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import spaFallback from './vite-plugin-spa-fallback.js'

export default defineConfig({
  plugins: [vue(), spaFallback()],
  server: {
    port: 5173,
    open: true
  },
  preview: {
    port: 5173
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
