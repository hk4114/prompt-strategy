<template>
  <div class="complex-page">
    <div class="page-container">
      <h2 class="section-title">复杂任务的 8 步法</h2>
      <p class="page-desc">
        适用于需要花 2 小时以上处理的任务，如需求分析、翻译文章等复杂任务
      </p>

      <!-- 步骤说明 -->
      <div class="steps-guide card">
        <h3>处理流程</h3>
        <ol class="steps-list">
          <li>明确问题与上下文</li>
          <li>让 AI 自选必要角色</li>
          <li>让 AI 连续提问，直到 95% 理解</li>
          <li>先跑一个具体情境</li>
          <li>根据表现迭代</li>
          <li>让"红队"挑刺</li>
          <li>直到抽到 SSR，基于那个回答微调</li>
          <li>抽象成可扩展的提示模板</li>
        </ol>
      </div>

      <div class="content-wrapper">
        <!-- 表单区域 -->
        <div class="form-section card">
          <el-form :model="form" label-position="top">
            <el-form-item label="角色">
              <el-input
                v-model="form.role"
                placeholder="例如：产品规划、技术架构、用户研究"
              />
            </el-form-item>

            <el-form-item label="背景">
              <el-input
                v-model="form.background"
                type="textarea"
                :rows="3"
                placeholder="当前面临的问题，任务发生的场景以及目标群体"
              />
            </el-form-item>

            <el-form-item label="任务">
              <el-input
                v-model="form.task"
                type="textarea"
                :rows="4"
                placeholder="第一轮、第二轮、第三轮的具体任务"
              />
            </el-form-item>

            <el-form-item label="要求">
              <el-input
                v-model="form.requirements"
                type="textarea"
                :rows="3"
                placeholder="具体要求和约束条件"
              />
            </el-form-item>

            <el-form-item label="格式">
              <el-input
                v-model="form.format"
                type="textarea"
                :rows="3"
                placeholder="输出格式要求，如 Markdown、评分标准等"
              />
            </el-form-item>

            <el-form-item label="范例">
              <el-input
                v-model="form.example"
                type="textarea"
                :rows="3"
                placeholder="示例说明，帮助 AI 理解预期"
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
import { generateComplexPrompt, createReview } from '@/api'

const loading = ref(false)
const generatedPrompt = ref('')
const currentLogId = ref<number | null>(null)
const showReview = ref(false)

const form = reactive({
  role: '',
  background: '',
  task: '',
  requirements: '',
  format: '',
  example: ''
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
    const { data } = await generateComplexPrompt(form)
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
.complex-page {
  .page-desc {
    color: #909399;
    margin-bottom: 20px;
  }

  .steps-guide {
    margin-bottom: 20px;

    h3 {
      margin-bottom: 12px;
    }

    .steps-list {
      margin: 0;
      padding-left: 24px;
      line-height: 2;
      color: #606266;
    }
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
      min-height: 500px;

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
