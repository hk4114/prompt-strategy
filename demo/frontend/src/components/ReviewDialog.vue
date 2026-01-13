<template>
  <el-dialog
    v-model="appStore.showReviewDialog"
    title="📝 复盘检查清单"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="review-intro">
      <p>提示词已复制！花1分钟记录你的思考，帮助你不断进步。</p>
    </div>

    <el-form :model="reviewData" label-position="top">
      <el-form-item label="1. 预期达到的效果？">
        <el-input
          v-model="reviewData.expectedEffect"
          type="textarea"
          :rows="2"
          placeholder="你希望AI生成什么样的内容？"
        />
      </el-form-item>

      <el-form-item label="2. 如何评价（验证）这次生成的结果？">
        <el-input
          v-model="reviewData.evaluationMethod"
          type="textarea"
          :rows="2"
          placeholder="你会用什么标准来判断结果好不好？"
        />
      </el-form-item>

      <el-form-item label="3. 是否有明显错误答案？你怎么处理的？">
        <el-input
          v-model="reviewData.errorHandling"
          type="textarea"
          :rows="2"
          placeholder="遇到错误时的处理方式"
        />
      </el-form-item>

      <el-form-item label="4. 生成的内容和预期不符，如何调整优化？">
        <el-input
          v-model="reviewData.adjustmentNotes"
          type="textarea"
          :rows="2"
          placeholder="你做了哪些调整？"
        />
      </el-form-item>

      <el-form-item label="5. 我为什么这么写提示词？">
        <el-input
          v-model="reviewData.promptReasoning"
          type="textarea"
          :rows="2"
          placeholder="记录你的思考过程"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleSkip">跳过</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">
        保存复盘
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAppStore } from '@/stores'
import { saveReview } from '@/api/requests'

const appStore = useAppStore()
const submitting = ref(false)

const reviewData = reactive({
  expectedEffect: '',
  evaluationMethod: '',
  errorHandling: '',
  adjustmentNotes: '',
  promptReasoning: ''
})

// 重置表单
watch(() => appStore.showReviewDialog, (show) => {
  if (show) {
    reviewData.expectedEffect = ''
    reviewData.evaluationMethod = ''
    reviewData.errorHandling = ''
    reviewData.adjustmentNotes = ''
    reviewData.promptReasoning = ''
  }
})

const handleSubmit = async () => {
  submitting.value = true
  try {
    await saveReview({
      usageLogId: appStore.currentLogId ?? undefined,
      expectedEffect: reviewData.expectedEffect,
      evaluationMethod: reviewData.evaluationMethod,
      errorHandling: reviewData.errorHandling,
      adjustmentNotes: reviewData.adjustmentNotes,
      promptReasoning: reviewData.promptReasoning
    })
    
    ElMessage.success('复盘已保存！继续加油 💪')
    appStore.closeReviewDialog()
  } catch (error) {
    ElMessage.error('保存失败，请重试')
  } finally {
    submitting.value = false
  }
}

const handleSkip = () => {
  appStore.closeReviewDialog()
}

const handleClose = () => {
  appStore.closeReviewDialog()
}
</script>

<style lang="less" scoped>
.review-intro {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;

  p {
    color: #a5b4fc;
    margin: 0;
    font-size: 14px;
  }
}

:deep(.el-dialog) {
  background: #1e293b;
  border-radius: 16px;

  .el-dialog__title {
    color: #fff;
    font-size: 18px;
  }

  .el-dialog__body {
    padding: 20px 24px;
  }

  .el-form-item__label {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
  }

  .el-textarea__inner {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #fff;
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.4);
    }

    &:focus {
      border-color: #667eea;
    }
  }
}
</style>
