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
          <el-form :model="form" label-position="top">
            <el-form-item label="角色 (Persona)">
              <el-input
                v-model="form.persona"
                placeholder="例如：资深产品经理、10年Python开发专家"
              />
            </el-form-item>

            <el-form-item label="背景 (Context)">
              <el-input
                v-model="form.context"
                type="textarea"
                :rows="3"
                placeholder="必须避免的禁忌项，优先考虑的关键要素"
              />
            </el-form-item>

            <el-form-item label="任务 (Task)">
              <el-input
                v-model="form.task"
                type="textarea"
                :rows="3"
                placeholder="实现的具体目标，量化标准，目标用户"
              />
            </el-form-item>

            <el-form-item label="限制 (Limit)">
              <el-input
                v-model="form.limit"
                type="textarea"
                :rows="2"
                placeholder="最多3条，量化优先，如'100字内''3个要点'"
              />
            </el-form-item>

            <el-form-item label="目标输出 (Goal)">
              <el-input
                v-model="form.goal"
                type="textarea"
                :rows="2"
                placeholder="期望的输出格式和风格"
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
            <el-button
              v-if="generatedPrompt"
              type="primary"
              size="small"
              @click="copyPrompt"
            >
              复制
            </el-button>
          </div>
          <div class="result-content">
            <pre v-if="generatedPrompt">{{ generatedPrompt }}</pre>
            <el-empty v-else description="填写表单后生成提示词" />
          </div>
        </div>
      </div>
    </div>

    <!-- 复盘弹窗 -->
    <el-dialog v-model="showReview" title="复盘检查清单" width="500px">
      <el-form :model="reviewForm" label-position="top">
        <el-form-item label="1. 预期达到的效果？">
          <el-input v-model="reviewForm.expectedEffect" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="2. 如何评价（验证）这次生成的结果？">
          <el-input v-model="reviewForm.evaluationMethod" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="3. 是否有明显错误答案？你怎么处理的？">
          <el-input v-model="reviewForm.errorHandling" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="4. 生成的内容和你的预期不符，我是如何调整优化的？">
          <el-input v-model="reviewForm.adjustmentNotes" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="5. 我为什么这么写提示词？">
          <el-input v-model="reviewForm.promptReasoning" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showReview = false">跳过</el-button>
        <el-button type="primary" @click="submitReview">提交复盘</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { generateMinimalPrompt, createReview } from '@/api'

const loading = ref(false)
const generatedPrompt = ref('')
const currentLogId = ref<number | null>(null)
const showReview = ref(false)

const form = reactive({
  persona: '',
  context: '',
  task: '',
  limit: '',
  goal: '',
  note: '这对我的职业生涯非常重要!'
})

const reviewForm = reactive({
  expectedEffect: '',
  evaluationMethod: '',
  errorHandling: '',
  adjustmentNotes: '',
  promptReasoning: ''
})

const generatePrompt = async () => {
  loading.value = true
  try {
    const { data } = await generateMinimalPrompt(form)
    generatedPrompt.value = data.prompt
    currentLogId.value = data.logId
    ElMessage.success('生成成功')
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

const copyPrompt = async () => {
  try {
    await navigator.clipboard.writeText(generatedPrompt.value)
    ElMessage.success('已复制到剪贴板')
    showReview.value = true
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const submitReview = async () => {
  try {
    await createReview({
      usageLogId: currentLogId.value ?? undefined,
      ...reviewForm
    })
    ElMessage.success('复盘已保存')
    showReview.value = false
  } catch (error) {
    ElMessage.error('保存失败')
  }
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
