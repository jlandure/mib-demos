import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true,
    proxy: {
      // Proxy pour le dev local, pointe maintenant vers Cloud Run
      '/agent/chat': {
        target: 'https://mib-bodysafety-simple-347864781165.europe-west1.run.app',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
