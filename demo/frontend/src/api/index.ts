import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 首页接口
export const getCategories = () => api.get('/categories')

// 模板接口
export const getTemplates = (params?: { keyword?: string; type?: string }) =>
  api.get('/templates', { params })

export const createTemplate = (data: {
  title: string
  content: string
  templateType?: string
  tags?: string[]
}) => api.post('/templates', data)

export const deleteTemplate = (id: number) => api.delete(`/templates/${id}`)

export const copyTemplate = (id: number) => api.post(`/templates/${id}/copy`)

// 提示词生成接口
export const generateMinimalPrompt = (data: {
  persona: string
  context: string
  task: string
  limit: string
  goal: string
  note?: string
}) => api.post('/prompt/generate/minimal', data)

export const generateComplexPrompt = (data: {
  role: string
  background: string
  task: string
  requirements: string
  format: string
  example: string
}) => api.post('/prompt/generate/complex', data)

// 复盘接口
export const createReview = (data: {
  usageLogId?: number
  expectedEffect?: string
  evaluationMethod?: string
  errorHandling?: string
  adjustmentNotes?: string
  promptReasoning?: string
}) => api.post('/review', data)

// 提示词技巧
export const getTips = () => api.get('/tips')

export default api
