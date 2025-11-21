<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true
})

const renderedContent = computed(() => {
  return md.render(props.content)
})
</script>

<template>
  <div class="w-full max-w-2xl bg-black/90 border border-mib-green/30 p-6 rounded-lg shadow-[0_0_30px_rgba(0,255,65,0.1)] backdrop-blur-sm text-gray-300">
    <div class="prose prose-invert prose-green max-w-none" v-html="renderedContent"></div>
  </div>
</template>

<style>
/* Custom Markdown Styles for MIB feel */
.prose h1 {
  @apply text-mib-green font-mono uppercase tracking-widest border-b border-mib-green/50 pb-2 mb-6;
}
.prose h2 {
  @apply text-white font-mono mt-8 mb-4 flex items-center gap-2;
}
.prose strong {
  @apply text-mib-green;
}
.prose ul {
  @apply list-disc list-inside space-y-2 my-4;
}
.prose p {
  @apply leading-relaxed mb-4;
}
/* Warning banner specific styling if agent returns markdown like that */
.prose h1:first-child {
  /* Handle danger warnings */
  @apply text-red-500 border-red-500;
}
</style>

