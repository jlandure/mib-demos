<script setup>
import { ref, onUnmounted } from 'vue'
import CameraScanner from './components/CameraScanner.vue'
import AgentResponse from './components/AgentResponse.vue'

const appState = ref('landing') // 'landing', 'scanning', 'processing', 'result'
const agentResponse = ref(null)
const error = ref(null)
const showConfig = ref(false)
const progress = ref(0)
let progressInterval = null

// Default config - Updated to Cloud Run URL
const config = ref({
  endpoint: (typeof window !== 'undefined' && window.config?.VITE_AGENT_URL) || import.meta.env.VITE_AGENT_URL || 'https://mib-bodysafety-simple-347864781165.europe-west1.run.app/agent/chat',
  token: '' // No token needed for public Cloud Run
})

const toggleConfig = () => {
  showConfig.value = !showConfig.value
}

const startScan = () => {
  appState.value = 'scanning'
  error.value = null
}

const simulateProgress = () => {
  progress.value = 0
  if (progressInterval) clearInterval(progressInterval)
  
  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 5
    }
  }, 200)
}

const handleCapture = async (imageBlob) => {
  appState.value = 'processing'
  simulateProgress()
  error.value = null
  
  try {
    const formData = new FormData()
    const file = new File([imageBlob], "scan.jpg", { type: "image/jpeg" })
    
    formData.append('file', file)
    formData.append('prompt', "Analyze this alien image and identify it from the MIB database.")

    // Direct call to Cloud Run (or via proxy in dev)
    let fetchUrl = config.value.endpoint

    // Simple POST request
    const response = await fetch(fetchUrl, {
      method: 'POST',
      body: formData
      // No Authorization header needed for unauthenticated Cloud Run
    })

    if (!response.ok) {
      const errText = await response.text()
      throw new Error(`Server Error (${response.status}): ${errText}`)
    }

    const data = await response.json()
    console.log("Agent Response:", data)
    
    // The simple server returns { "response": "markdown text..." }
    agentResponse.value = data.response || "No response content."
    
    // Finish progress
    progress.value = 100
    setTimeout(() => {
      appState.value = 'result'
    }, 500)
    
  } catch (err) {
    console.error(err)
    error.value = "COMMUNICATION ERROR: " + err.message
    appState.value = 'result' // Show error in result view
  } finally {
    if (progressInterval) clearInterval(progressInterval)
  }
}

const reset = () => {
  agentResponse.value = null
  appState.value = 'landing'
  error.value = null
  progress.value = 0
}

onUnmounted(() => {
  if (progressInterval) clearInterval(progressInterval)
})
</script>

<template>
  <div class="min-h-screen bg-black text-white flex flex-col font-mono overflow-hidden relative selection:bg-mib-green selection:text-black">
    
    <!-- Background Grid Effect -->
    <div class="absolute inset-0 bg-[linear-gradient(rgba(0,255,65,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,65,0.05)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none z-0"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black pointer-events-none z-0"></div>

    <!-- Header -->
    <header class="w-full flex justify-between items-center p-6 relative z-10">
      <div class="flex items-center gap-4 cursor-pointer" @click="reset">
        <div class="relative group">
          <div class="absolute inset-0 bg-mib-green blur opacity-20 group-hover:opacity-40 transition-opacity"></div>
          <div class="relative border border-mib-green/50 bg-black px-3 py-1 text-mib-green font-bold text-xl tracking-widest shadow-[0_0_10px_rgba(0,255,65,0.2)]">MIB</div>
        </div>
      </div>
      
      <button @click="toggleConfig" class="text-mib-green/50 hover:text-mib-green transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>
    </header>

    <!-- Config Panel -->
    <div v-if="showConfig" class="absolute top-20 right-4 z-50 w-80 p-6 bg-black/90 border border-mib-green rounded shadow-[0_0_20px_rgba(0,255,65,0.2)] animate-fade-in backdrop-blur-md">
      <h2 class="text-mib-green font-mono mb-4 text-sm uppercase flex items-center gap-2">
        <span class="w-2 h-2 bg-mib-green rounded-full animate-pulse"></span>
        System Configuration
      </h2>
      <div class="space-y-4">
        <div>
          <label class="block text-xs text-gray-400 mb-1">Agent Endpoint</label>
          <input v-model="config.endpoint" type="text" class="w-full bg-black border border-gray-800 p-2 text-xs font-mono text-gray-300 focus:border-mib-green focus:shadow-[0_0_10px_rgba(0,255,65,0.2)] focus:outline-none transition-all" />
        </div>
        <div class="flex justify-end">
          <button @click="showConfig = false" class="px-4 py-2 bg-mib-green text-black text-xs font-bold uppercase hover:bg-white hover:shadow-[0_0_15px_rgba(255,255,255,0.5)] transition-all duration-300">
            Save & Close
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center justify-center p-4 z-10 w-full max-w-5xl mx-auto">
      
      <!-- LANDING STATE -->
      <div v-if="appState === 'landing'" class="flex flex-col items-center text-center space-y-12 animate-fade-in">
        <div class="space-y-6">
          <h1 class="text-6xl md:text-8xl font-black tracking-tighter text-white drop-shadow-[0_0_15px_rgba(0,255,65,0.5)]">
            MIB
          </h1>
          <h2 class="text-xl md:text-2xl text-mib-green tracking-[0.3em] uppercase font-light border-b border-mib-green/30 pb-4">
            Alien Detection System
          </h2>
        </div>
        
        <p class="max-w-md text-gray-400 text-sm leading-relaxed">
          Advanced extraterrestrial threat identification and classification protocol.
          <br>
          <span class="text-mib-green font-bold mt-2 block">Clearance Level: Alpha</span>
        </p>

        <button @click="startScan" class="group relative px-12 py-4 bg-black border border-mib-green text-mib-green font-bold text-lg tracking-widest uppercase overflow-hidden transition-all duration-300 hover:shadow-[0_0_30px_rgba(0,255,65,0.4)]">
          <span class="relative z-10 group-hover:text-black transition-colors duration-300 flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 4.875c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5A1.125 1.125 0 013.75 9.375v-4.5zM3.75 14.625c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5a1.125 1.125 0 01-1.125-1.125v-4.5zM13.5 4.875c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5A1.125 1.125 0 0113.5 9.375v-4.5z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 6.75h.75v.75h-.75v-.75zM6.75 16.5h.75v.75h-.75v-.75zM16.5 6.75h.75v.75h-.75v-.75zM13.5 13.5h.75v.75h-.75v-.75zM13.5 19.5h.75v.75h-.75v-.75zM19.5 13.5h.75v.75h-.75v-.75zM19.5 19.5h.75v.75h-.75v-.75zM16.5 16.5h.75v.75h-.75v-.75z" />
            </svg>
            Initiate Scan
          </span>
          <div class="absolute inset-0 bg-mib-green transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300 ease-out"></div>
        </button>

        <div class="flex gap-12 text-xs text-gray-600 font-mono mt-12">
          <div class="flex flex-col items-center gap-2">
            <span class="text-2xl font-bold text-gray-800">01</span>
            <span>SECURE</span>
          </div>
          <div class="flex flex-col items-center gap-2">
            <span class="text-2xl font-bold text-gray-800">02</span>
            <span>IDENTIFY</span>
          </div>
          <div class="flex flex-col items-center gap-2">
            <span class="text-2xl font-bold text-gray-800">03</span>
            <span>PROTECT</span>
          </div>
        </div>
      </div>

      <!-- SCANNING STATE -->
      <div v-else-if="appState === 'scanning'" class="w-full h-full flex flex-col items-center justify-center">
        <div class="relative w-full max-w-2xl aspect-video border border-mib-green/30 rounded-lg overflow-hidden shadow-[0_0_30px_rgba(0,255,65,0.1)]">
           <CameraScanner @capture="handleCapture" />
           
           <!-- Corner Markers -->
           <div class="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-mib-green"></div>
           <div class="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-mib-green"></div>
           <div class="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-mib-green"></div>
           <div class="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-mib-green"></div>
        </div>
        <div class="mt-6 text-mib-green text-sm tracking-widest animate-pulse">CAMERA ACTIVE // WAITING FOR INPUT</div>
      </div>

      <!-- PROCESSING STATE -->
      <div v-else-if="appState === 'processing'" class="w-full max-w-xl flex flex-col items-center justify-center space-y-8">
        <!-- Decorative scanning box -->
        <div class="relative w-64 h-64 border border-mib-green/20 rounded-lg flex items-center justify-center overflow-hidden">
          <div class="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,255,65,0.1)_50%)] bg-[size:100%_4px]"></div>
          <div class="w-full h-1 bg-mib-green shadow-[0_0_15px_#00ff41] animate-scan"></div>
        </div>

        <div class="w-full space-y-2">
          <div class="text-center mb-2">
             <div class="text-2xl font-bold text-white tracking-widest drop-shadow-[0_0_10px_rgba(0,255,65,0.8)]">ANALYZING TARGET</div>
             <div class="text-mib-green font-mono text-4xl font-black mt-2">{{ Math.floor(progress) }}%</div>
          </div>
          
          <!-- Progress Bar -->
          <div class="w-full h-2 bg-gray-900 rounded-full overflow-hidden border border-gray-800">
            <div class="h-full bg-mib-green shadow-[0_0_10px_#00ff41] transition-all duration-200 ease-out" :style="{ width: progress + '%' }"></div>
          </div>
          
          <div class="flex justify-between text-xs text-gray-500 font-mono mt-2">
            <span>BIOMETRIC MATCHING...</span>
            <span>DATABASE: GALACTIC</span>
          </div>
        </div>
      </div>

      <!-- RESULT STATE -->
      <div v-else-if="appState === 'result'" class="w-full flex flex-col items-center animate-fade-in pb-20">
        
        <div v-if="error" class="w-full max-w-2xl text-red-500 font-mono p-6 border border-red-500/50 rounded bg-red-900/10 mb-8 text-center">
          <strong class="block text-2xl mb-4 tracking-widest">ACCESS DENIED</strong>
          <div class="text-sm opacity-80">{{ error }}</div>
          <button @click="reset" class="mt-6 px-6 py-2 border border-red-500 hover:bg-red-500 hover:text-white transition-colors text-xs uppercase tracking-wider">
            Retry Authentication
          </button>
        </div>
        
        <AgentResponse v-else-if="agentResponse" :content="agentResponse" />
        
        <button 
          @click="reset"
          class="mt-16 group inline-flex items-center gap-3 px-10 py-3 border border-mib-green/80 rounded-full bg-black/70 text-mib-green tracking-[0.25em] uppercase text-xs shadow-[0_0_18px_rgba(0,255,65,0.35)] hover:bg-mib-green hover:text-black hover:shadow-[0_0_28px_rgba(0,255,65,0.6)] transition-all duration-300"
        >
          <span class="w-2 h-2 bg-mib-green/60 group-hover:bg-black rounded-full shadow-[0_0_6px_rgba(0,255,65,0.9)] transition-colors"></span>
          <span class="font-mono">Process Next Subject</span>
        </button>
      </div>

    </main>
    
    <!-- Footer -->
    <footer class="py-6 text-center">
      <div class="text-[10px] text-gray-700 font-mono tracking-widest uppercase">
        Men In Black // Division 6 // Classified Material // v2.0.0
      </div>
    </footer>
  </div>
</template>

<style>
.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
