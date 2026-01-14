<template>
  <div class="minimal-page">
    <div class="page-container">
      <h2 class="section-title">最小公式</h2>
      <p class="page-desc">
        公式：[Persona：角色] + [Context：背景] + [Task：任务] + [Limit：限制条件] + [Goal：目标输出]
      </p>

      <div class="content-wrapper">
        <!-- 表单区域 -->
        <div class="form-section card">
          <el-form ref="formRef" :model="form" label-position="top" :rules="rules">
            <el-form-item label="角色 (Persona)">
              <el-input
                v-model="form.persona"
                placeholder="例如：SaaS 销售专家 (按 Tab 填充示例)"
                @keydown.tab="handleTabFill('persona')"
              />
            </el-form-item>

            <el-form-item label="背景 (Context)">
              <el-input
                v-model="form.context"
                type="textarea"
                :rows="3"
                placeholder="例如：对方是中型企业 CTO... (按 Tab 填充示例)"
                @keydown.tab="handleTabFill('context')"
              />
            </el-form-item>

            <el-form-item label="任务 (Task)">
              <el-input
                v-model="form.task"
                type="textarea"
                :rows="3"
                placeholder="例如：用 150 字内说清楚... (按 Tab 填充示例)"
                @keydown.tab="handleTabFill('task')"
              />
            </el-form-item>

            <el-form-item label="限制 (Limit)">
              <el-input
                v-model="form.limit"
                type="textarea"
                :rows="2"
                placeholder="例如：不出现&quot;行业领先&quot;... (按 Tab 填充示例)"
                @keydown.tab="handleTabFill('limit')"
              />
            </el-form-item>

            <el-form-item label="目标输出 (Goal)" prop="goal">
              <el-input
                v-model="form.goal"
                type="textarea"
                :rows="2"
                placeholder="例如：给出 2 个版本... (按 Tab 填充示例)"
                @keydown.tab="handleTabFill('goal')"
              />
            </el-form-item>

            <el-form-item label="备注">
              <el-input
                v-model="form.note"
                placeholder="这对我的职业生涯非常重要!"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="generatePrompt" :loading="loading">
                生成提示词
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 结果区域 -->
        <div class="result-section card">
          <div class="result-header">
            <h3>生成结果</h3>
            <div class="result-actions">
              <el-button
                v-if="generatedPrompt"
                type="warning"
                size="small"
                @click="resetForm"
              >
                重置
              </el-button>
              <el-button
                v-if="generatedPrompt"
                type="primary"
                size="small"
                @click="copyPrompt"
              >
                复制
              </el-button>
            </div>
          </div>
          <div class="result-content">
            <el-input
              v-if="generatedPrompt"
              v-model="generatedPrompt"
              type="textarea"
              :rows="20"
              placeholder="生成结果将显示在这里，您可以直接编辑"
            />
            <el-empty v-else description="填写表单后生成提示词" />
          </div>
        </div>
      </div>
    </div>

    <!-- 复盘弹窗 (已移除) -->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const loading = ref(false)
const generatedPrompt = ref('')
const formRef = ref<FormInstance>()

const form = reactive({
  persona: '',
  context: '',
  task: '',
  limit: '',
  goal: '',
  note: '这对我的职业生涯非常重要!'
})

const rules = reactive<FormRules>({
  goal: [
    { required: true, message: '请输入目标输出', trigger: 'blur' }
  ]
})

const exampleValues = {
  persona: 'SaaS 销售专家',
  context: '对方是中型企业 CTO,每天收 200+ 邮件,讨厌营销话术',
  task: '用 150 字内说清楚我们的 API 监控工具能解决他什么痛点,最终让他愿意点击 Demo 链接',
  limit: '- 不出现"行业领先""赋能"等废话\n- 必须有 1 个具体数据支撑\n- 开头第一句必须是问题而非自我介绍',
  goal: '给出 2 个版本:一个强调"省钱",一个强调"避免故障"'
}

const handleTabFill = (field: keyof typeof exampleValues) => {
  if (!form[field]) {
    form[field] = exampleValues[field]
  }
}

const generatePrompt = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      const parts: string[] = []
      
      if (form.persona) {
        parts.push(`## 角色\n作为 ${form.persona}`)
      }
      
      if (form.context) {
        parts.push(`## 背景\n${form.context}`)
      }
      
      if (form.task) {
        parts.push(`## 任务\n${form.task}`)
      }
      
      if (form.limit) {
        parts.push(`## 限制\n${form.limit}`)
      }
      
      if (form.goal) {
        parts.push(`## 输出\n${form.goal}`)
      }
      
      if (form.note) {
        parts.push(`---\n${form.note}`)
      }
      
      generatedPrompt.value = parts.join('\n\n')
      ElMessage.success('生成成功')
    }
  })
}

const copyPrompt = async () => {
  try {
    await navigator.clipboard.writeText(generatedPrompt.value)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
  generatedPrompt.value = ''
  // 仅重置了绑定 prop 的字段（如 goal），其他字段手动清空
  form.persona = ''
  form.context = ''
  form.task = ''
  form.limit = ''
  form.note = '这对我的职业生涯非常重要!'
  ElMessage.success('已重制')
}
</script>

<style lang="less" scoped>
.minimal-page {
  .page-desc {
    color: #909399;
    margin-bottom: 20px;
  }

  .content-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;

    @media (max-width: 900px) {
      grid-template-columns: 1fr;
    }
  }

  .result-section {
    .result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
      }
    }

    .result-content {
      background: #fafafa;
      border-radius: 8px;
      padding: 16px;
      min-height: 400px;

      pre {
        white-space: pre-wrap;
        word-wrap: break-word;
        font-family: inherit;
        margin: 0;
        line-height: 1.6;
      }
    }
  }
}
</style>
