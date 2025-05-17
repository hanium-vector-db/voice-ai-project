<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-xl font-bold mb-2">STT → GPT → TTS</h2>
    <label class="block mb-2">
      <span class="mr-2">GPT 응답 언어:</span>
      <select v-model="language" class="border rounded p-1">
        <option value="한국어">한국어</option>
        <option value="영어">영어</option>
        <option value="일본어">일본어</option>
      </select>
    </label>
    <!-- 예시: provider/model 선택 드롭다운 -->
    <label class="block mb-2">
      <span class="mr-2">Provider:</span>
      <select v-model="provider" class="border rounded p-1">
        <option value="openai">OpenAI</option>
        <option value="ollama">Ollama</option>
      </select>
    </label>
    <label class="block mb-2">
      <span class="mr-2">Model:</span>
      <select v-model="model" class="border rounded p-1">
        <option value="gpt-4">gpt-4</option>
        <option value="korean-yanolja-eeve:latest">korean-yanolja-eeve:latest</option>
        <option value="exaone3.5:7.8b">exaone3.5:7.8b</option>
        <option value="deepseek-r1:7b">deepseek-r1:7b</option>
      </select>
    </label>
    <button @click="toggleRecording" class="bg-green-500 text-white px-4 py-2 rounded mb-2">
      {{ isRecording ? '녹음 중지' : '녹음 시작' }}
    </button>
    <div v-if="sttText" class="mt-2">STT 텍스트: {{ sttText }}</div>
    <div v-if="gptResponse" class="mt-2">GPT 응답: {{ gptResponse }}</div>
    <audio v-if="ttsUrl" :src="ttsUrl" controls class="w-full mt-4"></audio>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isRecording = ref(false)
let mediaRecorder: MediaRecorder | null = null
let audioChunks: BlobPart[] = []

const sttText = ref('')
const gptResponse = ref('')
const ttsUrl = ref('')
const language = ref('한국어') // 기본값
const provider = ref('openai') // 기본값
const model = ref('gpt-4') // 기본값

async function toggleRecording() {
  if (!isRecording.value) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data)
    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      const formData = new FormData()
      formData.append('audio', blob, 'recording.webm')
      formData.append('language', language.value) // 언어 추가
      formData.append('provider', provider.value)
      formData.append('model', model.value)
      const res = await fetch('/stt-tts/', { method: 'POST', body: formData })
      const data = await res.json()
      sttText.value = data.stt_text
      gptResponse.value = data.gpt_response
      ttsUrl.value = data.tts_file_path
    }
    mediaRecorder.start()
    isRecording.value = true
  } else {
    mediaRecorder?.stop()
    isRecording.value = false
  }
}
</script>