import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePromptStore = defineStore('prompt', () => {
  // Global state
  const currentGeneratedPrompt = ref<string>('')
  const currentUsageLogId = ref<number | null>(null)

  // Actions
  function setGeneratedPrompt(prompt: string, usageLogId?: number) {
    currentGeneratedPrompt.value = prompt
    currentUsageLogId.value = usageLogId || null

    // Dispatch custom event for App.vue to listen
    window.dispatchEvent(new CustomEvent('prompt-copied', {
      detail: { usageLogId }
    }))
  }

  function clearPrompt() {
    currentGeneratedPrompt.value = ''
    currentUsageLogId.value = null
  }

  return {
    currentGeneratedPrompt,
    currentUsageLogId,
    setGeneratedPrompt,
    clearPrompt
  }
})
