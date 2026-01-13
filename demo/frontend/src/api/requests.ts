import api from './index'

// 分类和产品
export const getCategories = () => api.get('/categories')

// 提示词模板
export const getTemplates = (params?: { keyword?: string; type?: string }) =>
    api.get('/templates', { params })

export const createTemplate = (data: { title: string; content: string; templateType?: string; tags?: string[] }) =>
    api.post('/templates', data)

export const copyTemplate = (id: number) =>
    api.post(`/templates/${id}/copy`)

// 提示词生成
export const generatePrompt = (data: { promptType: string; formData: Record<string, string> }) =>
    api.post('/prompts/generate', data)

// 复盘记录
export const saveReview = (data: {
    usageLogId?: number
    expectedEffect?: string
    evaluationMethod?: string
    errorHandling?: string
    adjustmentNotes?: string
    promptReasoning?: string
}) => api.post('/prompts/review', data)

// 提示词技巧
export const getTips = () => api.get('/tips')
