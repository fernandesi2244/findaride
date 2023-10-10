import vue from '@vitejs/plugin-vue'
import { defineConfig, splitVendorChunkPlugin } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), splitVendorChunkPlugin(), tsconfigPaths()],
  build: {
    manifest: true,
   },
  base: process.env.NODE_ENV=="production" ? "/static/" : "/",
  root: "./src",
})
