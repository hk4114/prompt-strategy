import request from './requests'

// Categories and Products
export function getCategories() {
  return request.get('/categories')
}

// Templates
export function getTemplates(params?: {
  type?: string
  search?: string
  tag?: string
}) {
  return request.get('/templates', { params })
}

export function getTemplate(id: number) {
  return request.get(`/templates/${id}`)
}

export function createTemplate(data: {
  title: string
  content: string
  template_type: string
  tags: string[]
}) {
  return request.post('/templates', data)
}

export function incrementTemplateUsage(id: number) {
  return request.post(`/templates/${id}/use`)
}

export function getTemplateTags() {
  return request.get('/templates/tags')
}

// Prompts
export function generatePrompt(data: {
  prompt_type: string
  generated_prompt: string
  form_data: Record<string, any>
}) {
  return request.post('/prompts/generate', data)
}

export function saveReview(data: {
  usage_log_id: number
  expected_effect: string
  evaluation_method: string
  error_handling: string
  adjustment_notes: string
  prompt_reasoning: string
}) {
  return request.post('/prompts/review', data)
}

export function getReview(usageLogId: number) {
  return request.get(`/prompts/review/${usageLogId}`)
}

// Tips
export function getTips() {
  return request.get('/tips')
}

export function createTip(data: { title: string; content: string }) {
  return request.post('/tips', data)
}
