// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173, // 원하는 포트 번호
    proxy: {
    '/tts': 'http://localhost:8000',
    '/stt-tts': 'http://localhost:8000',
    '/uploads': 'http://localhost:8000', 
  }
  },
})
