<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['capture'])

const videoEl = ref(null)
const canvasEl = ref(null)
const stream = ref(null)
const error = ref(null)

const startCamera = async () => {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    if (videoEl.value) {
      videoEl.value.srcObject = stream.value
    }
  } catch (err) {
    console.error("Camera access error:", err)
    error.value = "Unable to access camera. Please allow permissions."
  }
}

const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
}

const capture = () => {
  if (!videoEl.value || !canvasEl.value) return

  const context = canvasEl.value.getContext('2d')
  canvasEl.value.width = videoEl.value.videoWidth
  canvasEl.value.height = videoEl.value.videoHeight
  context.drawImage(videoEl.value, 0, 0)
  
  canvasEl.value.toBlob((blob) => {
    emit('capture', blob)
  }, 'image/jpeg', 0.8)
}

onMounted(() => {
  startCamera()
})

onUnmounted(() => {
  stopCamera()
})
</script>

<template>
  <div class="relative w-full h-full flex flex-col items-center justify-center bg-black overflow-hidden">
    <div v-if="error" class="text-red-500 p-4 text-center">
      {{ error }}
    </div>
    
    <div v-else class="relative w-full max-w-md aspect-[3/4] bg-gray-900 rounded-lg overflow-hidden border-2 border-mib-green shadow-[0_0_15px_rgba(0,255,65,0.3)]">
      <video 
        ref="videoEl" 
        autoplay 
        playsinline 
        class="w-full h-full object-cover"
      ></video>
      
      <!-- Scanner overlay -->
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-0 left-0 w-full h-1 bg-mib-green/50 animate-scan shadow-[0_0_10px_#00ff41]"></div>
        
        <!-- Corners -->
        <div class="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-mib-green"></div>
        <div class="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-mib-green"></div>
        <div class="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-mib-green"></div>
        <div class="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-mib-green"></div>
      </div>
    </div>

    <button 
      @click="capture"
      class="mt-8 px-8 py-4 bg-mib-green/10 border border-mib-green text-mib-green font-mono font-bold tracking-widest text-lg rounded hover:bg-mib-green hover:text-black transition-all duration-300 shadow-[0_0_20px_rgba(0,255,65,0.2)] hover:shadow-[0_0_30px_rgba(0,255,65,0.6)] uppercase"
    >
      Initialize Scan
    </button>
    
    <canvas ref="canvasEl" class="hidden"></canvas>
  </div>
</template>


