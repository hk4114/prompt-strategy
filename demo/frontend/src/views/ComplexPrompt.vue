<template>
  <div class="complex-prompt">
    <div class="page-header">
      <h1 class="section-title">
        <span class="highlight">复杂任务</span> 8步法
      </h1>
      <p class="page-desc">适用于值得花2小时处理的复杂任务</p>
    </div>

    <!-- 步骤指示器 -->
    <div class="steps-indicator glass-card">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step-item"
        :class="{ active: currentStep === index, completed: currentStep > index }"
        @click="currentStep = index"
      >
        <span class="step-number">{{ index + 1 }}</span>
        <span class="step-name">{{ step.name }}</span>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 当前步骤表单 -->
      <div class="step-content glass-card">
        <div class="step-header">
          <h2>{{ steps[currentStep].name }}</h2>
          <p class="step-desc">{{ steps[currentStep].description }}</p>
        </div>

        <el-form label-position="top" size="large">
          <!-- 步骤1: 明确问题 -->
          <template v-if="currentStep === 0">
            <el-form-item label="你要解决的问题是什么？">
              <el-input
                v-model="formData.problem"
                type="textarea"
                :rows="4"
                placeholder="详细描述你遇到的问题或任务"
              />
            </el-form-item>
            <el-form-item label="上下文背景">
              <el-input
                v-model="formData.background"
                type="textarea"
                :rows="3"
                placeholder="提供相关的背景信息"
              />
            </el-form-item>
          </template>

          <!-- 步骤2: 选择角色 -->
          <template v-if="currentStep === 1">
            <el-form-item label="你需要哪些专家角色？">
              <el-input
                v-model="formData.role"
                type="textarea"
                :rows="3"
                placeholder="例如：资深产品经理、技术架构师、用户体验专家"
              />
            </el-form-item>
            <el-alert type="info" :closable="false">
              💡 提示：可以让 AI 自选角色 - "你们认为解决这个问题，最需要哪三类专家角色？"
            </el-alert>
          </template>

          <!-- 步骤3: 连续提问 -->
          <template v-if="currentStep === 2">
            <el-form-item label="边界条件和约束">
              <el-input
                v-model="formData.constraints"
                type="textarea"
                :rows="4"
                placeholder="列出所有限制条件、边界、必须满足的要求"
              />
            </el-form-item>
            <el-alert type="info" :closable="false">
              💡 提示：加入这句话 - "在行动前，请向我连续提问，直到你 95%确信理解我的目标和边界。"
            </el-alert>
          </template>

          <!-- 步骤4: 具体情境 -->
          <template v-if="currentStep === 3">
            <el-form-item label="第一个具体任务">
              <el-input
                v-model="formData.task"
                type="textarea"
                :rows="4"
                placeholder="先跑一个最具体、最小的任务来验证"
              />
            </el-form-item>
          </template>

          <!-- 步骤5: 迭代表现 -->
          <template v-if="currentStep === 4">
            <el-form-item label="输出要求">
              <el-input
                v-model="formData.requirements"
                type="textarea"
                :rows="3"
                placeholder="根据上一轮的表现，明确输出要求"
              />
            </el-form-item>
          </template>

          <!-- 步骤6: 红队挑刺 -->
          <template v-if="currentStep === 5">
            <el-form-item label="潜在风险和漏洞">
              <el-input
                v-model="formData.risks"
                type="textarea"
                :rows="3"
                placeholder="假设这个项目彻底失败，最可能的原因是什么？"
              />
            </el-form-item>
            <el-alert type="warning" :closable="false">
              ⚠️ 红队思维：成立一个小组，唯一任务就是挑这个方案的毛病
            </el-alert>
          </template>

          <!-- 步骤7: 输出格式 -->
          <template v-if="currentStep === 6">
            <el-form-item label="期望的输出格式">
              <el-input
                v-model="formData.format"
                type="textarea"
                :rows="3"
                placeholder="例如：Markdown格式、分点列出、包含代码示例"
              />
            </el-form-item>
            <el-form-item label="范例">
              <el-input
                v-model="formData.example"
                type="textarea"
                :rows="3"
                placeholder="提供一个你期望的输出范例"
              />
            </el-form-item>
          </template>

          <!-- 步骤8: 生成模板 -->
          <template v-if="currentStep === 7">
            <el-alert type="success" :closable="false" style="margin-bottom: 20px;">
              🎉 太棒了！你已完成所有步骤，点击下方按钮生成最终提示词
            </el-alert>
          </template>
        </el-form>

        <div class="step-actions">
          <el-button v-if="currentStep > 0" @click="currentStep--">
            上一步
          </el-button>
          <el-button 
            v-if="currentStep < steps.length - 1" 
            type="primary" 
            @click="currentStep++"
          >
            下一步
          </el-button>
          <el-button 
            v-if="currentStep === steps.length - 1" 
            type="primary" 
            @click="handleGenerate"
            :loading="generating"
          >
            ✨ 生成提示词
          </el-button>
        </div>
      </div>

      <!-- 结果预览 -->
      <div class="result-section glass-card">
        <div class="result-header">
          <h3>生成结果预览</h3>
          <el-button 
            v-if="generatedPrompt" 
            type="primary" 
            size="small"
            @click="handleCopy"
          >
            📋 复制
          </el-button>
        </div>
        <div class="result-content">
          <pre v-if="generatedPrompt">{{ generatedPrompt }}</pre>
          <div v-else class="empty-state">
            <span class="empty-icon">🎯</span>
            <p>完成8个步骤后生成提示词</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { generatePrompt } from '@/api/requests'
import { useAppStore } from '@/stores'

const appStore = useAppStore()

const steps = [
  { name: '明确问题', description: '清晰定义要解决的问题和上下文' },
  { name: '选择角色', description: '确定需要哪些专家角色' },
  { name: '连续提问', description: '明确边界条件，让AI充分理解' },
  { name: '具体情境', description: '先跑一个最小化的具体任务' },
  { name: '迭代优化', description: '根据表现调整要求' },
  { name: '红队挑刺', description: '识别潜在风险和漏洞' },
  { name: '输出格式', description: '定义期望的输出格式和范例' },
  { name: '生成模板', description: '生成可复用的提示词模板' }
]

const currentStep = ref(0)
const generating = ref(false)
const generatedPrompt = ref('')
const currentLogId = ref<number | null>(null)

const formData = reactive({
  problem: '',
  background: '',
  role: '',
  constraints: '',
  task: '',
  requirements: '',
  risks: '',
  format: '',
  example: ''
})

const handleGenerate = async () => {
  generating.value = true
  try {
    const res = await generatePrompt({
      promptType: 'complex_8step',
      formData: {
        role: formData.role,
        background: `${formData.problem}\n\n背景：${formData.background}\n\n约束条件：${formData.constraints}`,
        task: formData.task,
        requirements: `${formData.requirements}\n\n需要规避的风险：${formData.risks}`,
        format: formData.format,
        example: formData.example
      }
    }) as { prompt: string; logId: number }
    
    generatedPrompt.value = res.prompt
    currentLogId.value = res.logId
    ElMessage.success('生成成功!')
  } catch (error) {
    ElMessage.error('生成失败，请重试')
  } finally {
    generating.value = false
  }
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(generatedPrompt.value)
    ElMessage.success('已复制到剪贴板')
    
    // 弹出复盘检查清单
    appStore.openReviewDialog(currentLogId.value, generatedPrompt.value)
  } catch (error) {
    ElMessage.error('复制失败')
  }
}
</script>

<style lang="less" scoped>
.complex-prompt {
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    text-align: center;
    margin-bottom: 32px;

    .page-desc {
      color: rgba(255, 255, 255, 0.7);
    }
  }

  .steps-indicator {
    display: flex;
    padding: 20px;
    margin-bottom: 24px;
    overflow-x: auto;
    gap: 8px;

    .step-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      white-space: nowrap;
      color: rgba(255, 255, 255, 0.5);

      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }

      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
      }

      &.completed {
        color: #10b981;

        .step-number {
          background: #10b981;
          border-color: #10b981;
        }
      }

      .step-number {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid currentColor;
        border-radius: 50%;
        font-size: 12px;
        font-weight: 600;
      }

      .step-name {
        font-size: 14px;
      }
    }
  }

  .content-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;

    @media (max-width: 900px) {
      grid-template-columns: 1fr;
    }
  }

  .step-content {
    padding: 32px;

    .step-header {
      margin-bottom: 24px;

      h2 {
        color: #fff;
        font-size: 20px;
        margin-bottom: 8px;
      }

      .step-desc {
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
      }
    }

    .step-actions {
      display: flex;
      gap: 12px;
      margin-top: 24px;
      justify-content: flex-end;
    }
  }

  .result-section {
    padding: 32px;
    display: flex;
    flex-direction: column;

    .result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        color: #fff;
        font-size: 18px;
      }
    }

    .result-content {
      flex: 1;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 12px;
      padding: 20px;
      overflow: auto;
      min-height: 400px;

      pre {
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 14px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-break: break-word;
        margin: 0;
      }

      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: rgba(255, 255, 255, 0.5);

        .empty-icon {
          font-size: 48px;
          margin-bottom: 16px;
        }
      }
    }
  }
}
</style>
