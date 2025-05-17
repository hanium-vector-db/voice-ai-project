<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-xl font-bold mb-2">Text-to-Speech (TTS)</h2>
    <textarea v-model="text" class="w-full border rounded p-2 mb-2" rows="4" placeholder="텍스트를 입력하세요..." />
    <button @click="generateTTS" class="bg-blue-500 text-white px-4 py-2 rounded">TTS 생성</button>
    <audio v-if="ttsUrl" :src="ttsUrl" controls class="w-full mt-4"></audio>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const text = ref('')
const ttsUrl = ref('')

async function generateTTS() {
  if (!text.value.trim()) {
    alert('텍스트를 입력하세요!')
    return
  }
  const res = await fetch('/tts/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ text: text.value }),
  })
  if (!res.ok) {
    const err = await res.json()
    alert('TTS 생성 실패: ' + err.detail)
    return
  }
  const data = await res.json()
  console.log('TTS 응답:', data)
  // 캐시 우회 쿼리스트링 추가
  ttsUrl.value = (data.tts_file_path || data.file_path) + '?t=' + Date.now()
}
</script>