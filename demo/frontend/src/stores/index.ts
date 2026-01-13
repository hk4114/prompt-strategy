import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
    // 复盘弹窗状态
    const showReviewDialog = ref(false)
    const currentLogId = ref<number | null>(null)
    const copiedPrompt = ref('')

    // 提示词技巧面板状态
    const showTipsPanel = ref(true)
    const tipsPanelMinimized = ref(false)

    // 显示复盘弹窗
    const openReviewDialog = (logId: number | null, prompt: string) => {
        currentLogId.value = logId
        copiedPrompt.value = prompt
        showReviewDialog.value = true
    }

    // 关闭复盘弹窗
    const closeReviewDialog = () => {
        showReviewDialog.value = false
        currentLogId.value = null
        copiedPrompt.value = ''
    }

    // 切换技巧面板
    const toggleTipsPanel = () => {
        tipsPanelMinimized.value = !tipsPanelMinimized.value
    }

    return {
        showReviewDialog,
        currentLogId,
        copiedPrompt,
        showTipsPanel,
        tipsPanelMinimized,
        openReviewDialog,
        closeReviewDialog,
        toggleTipsPanel
    }
})
