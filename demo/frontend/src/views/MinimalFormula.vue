<template>
  <div class="minimal-formula">
    <div class="page-header">
      <h1 class="section-title">
        <span class="highlight">最小公式</span> 提示词生成
      </h1>
      <p class="page-desc">
        公式：[角色] + [背景] + [任务] + [限制] + [目标输出]
      </p>
    </div>

    <div class="content-wrapper">
      <!-- 表单区域 -->
      <div class="form-section glass-card">
        <el-form :model="formData" label-position="top" size="large">
          <el-form-item label="🎭 角色 (Persona)">
            <el-input
              v-model="formData.persona"
              placeholder="例如：资深产品经理、10年经验的Python开发者"
            />
          </el-form-item>

          <el-form-item label="📋 背景 (Context)">
            <el-input
              v-model="formData.context"
              type="textarea"
              :rows="3"
              placeholder="例如：必须避免技术债务，优先考虑用户体验"
            />
          </el-form-item>

          <el-form-item label="🎯 任务 (Task)">
            <el-input
              v-model="formData.task"
              type="textarea"
              :rows="3"
              placeholder="例如：实现用户登录功能，要求支持手机验证码"
            />
          </el-form-item>

          <el-form-item label="⚠️ 限制 (Limit)">
            <el-input
              v-model="formData.limit"
              type="textarea"
              :rows="2"
              placeholder="例如：100字内、3个要点、使用TypeScript"
            />
          </el-form-item>

          <el-form-item label="📝 输出目标 (Goal)">
            <el-input
              v-model="formData.goal"
              placeholder="例如：输出风格犀利、凝练、有力"
            />
          </el-form-item>

          <el-form-item label="💡 备注">
            <el-input
              v-model="formData.note"
              placeholder="默认：这对我的职业生涯非常重要!"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" class="generate-btn" @click="handleGenerate" :loading="generating">
              ✨ 生成提示词
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 结果区域 -->
      <div class="result-section glass-card">
        <div class="result-header">
          <h3>生成结果</h3>
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
            <span class="empty-icon">📝</span>
            <p>填写左侧表单，生成你的提示词</p>
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

const formData = reactive({
  persona: '',
  context: '',
  task: '',
  limit: '',
  goal: '',
  note: '这对我的职业生涯非常重要!'
})

const generatedPrompt = ref('')
const generating = ref(false)
const currentLogId = ref<number | null>(null)

const handleGenerate = async () => {
  if (!formData.persona || !formData.task) {
    ElMessage.warning('请至少填写角色和任务')
    return
  }

  generating.value = true
  try {
    const res = await generatePrompt({
      promptType: 'minimal_formula',
      formData: { ...formData }
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
.minimal-formula {
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    text-align: center;
    margin-bottom: 32px;

    .page-desc {
      color: rgba(255, 255, 255, 0.7);
      font-size: 16px;
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

  .form-section {
    padding: 32px;

    .generate-btn {
      width: 100%;
      height: 48px;
      font-size: 16px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
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
        min-height: 300px;
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
