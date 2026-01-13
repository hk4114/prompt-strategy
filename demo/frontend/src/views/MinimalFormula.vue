<template>
  <div class="minimal-formula-page">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">最小公式</h1>
        <p class="page-subtitle">通过基础要素快速生成结构化提示词</p>
      </div>

      <el-row :gutter="24">
        <!-- Left: Form -->
        <el-col :xs="24" :md="12">
          <el-card class="form-card" shadow="never">
            <h2 class="form-title">填写表单</h2>

            <el-form
              ref="formRef"
              :model="formData"
              label-position="top"
              label-width="100px"
            >
              <el-form-item label="角色 (Persona):">
                <el-input
                  v-model="formData.persona"
                  type="textarea"
                  :rows="2"
                  placeholder="例如：资深前端工程师"
                />
              </el-form-item>

              <el-form-item label="背景 (Context):">
                <el-input
                  v-model="formData.context"
                  type="textarea"
                  :rows="2"
                  placeholder="必须避免什么，优先考虑什么"
                />
              </el-form-item>

              <el-form-item label="任务 (Task):">
                <el-input
                  v-model="formData.task"
                  type="textarea"
                  :rows="2"
                  placeholder="具体目标、量化标准、目标用户"
                />
              </el-form-item>

              <el-form-item label="限制条件 (Limit):">
                <el-input
                  v-model="formData.limit"
                  type="textarea"
                  :rows="2"
                  placeholder="最多3条，量化优先，如'100字内''3个要点'"
                />
              </el-form-item>

              <el-form-item label="目标输出 (Goal):">
                <el-input
                  v-model="formData.goal"
                  type="textarea"
                  :rows="2"
                  placeholder="期望的输出形式和目标"
                />
              </el-form-item>

              <el-form-item label="备注:">
                <el-input
                  v-model="formData.notes"
                  type="textarea"
                  :rows="1"
                  placeholder="这对我的职业生涯非常重要!"
                />
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  size="large"
                  @click="generatePrompt"
                  :loading="loading"
                  style="width: 100%"
                >
                  生成提示词
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- Right: Result -->
        <el-col :xs="24" :md="12">
          <el-card class="result-card" shadow="never">
            <h2 class="form-title">生成结果</h2>

            <div v-if="generatedPrompt" class="result-display">
              <el-input
                v-model="generatedPrompt"
                type="textarea"
                :rows="15"
                readonly
                class="prompt-textarea"
              />

              <div class="result-actions">
                <el-button
                  type="success"
                  @click="copyPrompt"
                  :icon="DocumentCopy"
                >
                  复制提示词
                </el-button>

                <el-button
                  type="info"
                  @click="resetForm"
                >
                  重新填写
                </el-button>
              </div>
            </div>

            <el-empty v-else description="填写表单后点击'生成提示词'" />
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentCopy } from '@element-plus/icons-vue'
import { generatePrompt as apiGeneratePrompt } from '@/api'
import { usePromptStore } from '@/stores'

const promptStore = usePromptStore()

interface FormData {
  persona: string
  context: string
  task: string
  limit: string
  goal: string
  notes: string
}

const formData = ref<FormData>({
  persona: '',
  context: '',
  task: '',
  limit: '',
  goal: '',
  notes: ''
})

const loading = ref(false)
const generatedPrompt = ref('')
const usageLogId = ref<number | null>(null)

const formulaStructure = computed(() => {
  return {
    structure: `## 角色\n作为 [领域专家]\n\n## 背景  \n必须避免 [禁忌项],优先考虑 [关键要素]\n\n## 任务  \n实现 [具体目标],要求 [量化标准],最终输出服务于 [目标用户]\n\n## 限制  \n[最多3条,量化优先,如"100字内""3个要点"]\n\n## 输出  \n1. 以 Markdown 形式输出\n2. 输出结果必须包含 [参考资料]\n3. 输出风格 [犀利、凝练、有力]\n4. 展示至少两种备选方案及其淘汰理由`,
    formula: '[Persona：角色] + [Context：背景] + [Task：任务] + [Limit：限制条件] + [Goal：目标输出]'
  }
})

function generatePrompt() {
  loading.value = true

  const { persona, context, task, limit, goal, notes } = formData.value

  const prompt = `## 角色
作为 ${persona || '[领域专家]'}

## 背景
${context || '必须避免 [禁忌项],优先考虑 [关键要素]'}

## 任务
${task || '实现 [具体目标],要求 [量化标准],最终输出服务于 [目标用户]'}

## 限制
${limit || '[最多3条,量化优先,如"100字内""3个要点"]'}

## 输出
${goal || '1. 以 Markdown 形式输出\n2. 输出结果必须包含 [参考资料]\n3. 输出风格 [犀利、凝练、有力]\n4. 展示至少两种备选方案及其淘汰理由'}

## 备注
${notes || '这对我的职业生涯非常重要!'}

## 公式原理
${formulaStructure.value.formula}`

  generatedPrompt.value = prompt
  loading.value = false

  // Save to backend
  savePromptToBackend()
}

async function savePromptToBackend() {
  try {
    const result = await apiGeneratePrompt({
      prompt_type: 'minimal_formula',
      generated_prompt: generatedPrompt.value,
      form_data: formData.value
    })

    usageLogId.value = result.usage_log_id
    ElMessage.success('提示词已生成并保存')
  } catch (error) {
    console.error('Save error:', error)
    ElMessage.warning('生成成功，但保存失败')
  }
}

function copyPrompt() {
  navigator.clipboard.writeText(generatedPrompt.value).then(() => {
    ElMessage.success('已复制到剪贴板')

    // Trigger review dialog
    promptStore.setGeneratedPrompt(generatedPrompt.value, usageLogId.value)
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

function resetForm() {
  formData.value = {
    persona: '',
    context: '',
    task: '',
    limit: '',
    goal: '',
    notes: ''
  }
  generatedPrompt.value = ''
  usageLogId.value = null
}
</script>

<style scoped lang="less">
.minimal-formula-page {
  min-height: 100vh;
  padding: 20px 0;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;

  .page-title {
    font-size: 36px;
    margin: 0 0 8px 0;
    color: #333;
  }

  .page-subtitle {
    font-size: 18px;
    color: #666;
    margin: 0;
  }
}

.form-card, .result-card {
  height: 100%;
}

.form-title {
  font-size: 20px;
  margin: 0 0 20px 0;
  color: #333;
}

.result-display {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.prompt-textarea {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.result-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

@media (max-width: 768px) {
  .page-header .page-title {
    font-size: 28px;
  }

  .page-header .page-subtitle {
    font-size: 16px;
  }
}
</style>