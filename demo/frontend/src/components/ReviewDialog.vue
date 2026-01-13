<template>
  <el-dialog
    v-model="dialogVisible"
    title="复盘检查清单"
    width="600px"
    :close-on-click-modal="false"
  >
    <div class="review-dialog">
      <p class="review-intro">
        复制提示词后，请花几分钟回答以下问题，帮助改进提示词质量：
      </p>

      <el-form ref="formRef" :model="reviewForm" label-position="top">
        <el-form-item label="1. 预期达到的效果？">
          <el-input
            v-model="reviewForm.expected_effect"
            type="textarea"
            :rows="2"
            placeholder="描述你期望这个提示词达到什么效果..."
          />
        </el-form-item>

        <el-form-item label="2. 如何评价（验证）这次生成的结果？">
          <el-input
            v-model="reviewForm.evaluation_method"
            type="textarea"
            :rows="2"
            placeholder="说明你将如何验证AI的回答是否符合预期..."
          />
        </el-form-item>

        <el-form-item label="3. 是否有明显错误答案？你怎么处理的？">
          <el-input
            v-model="reviewForm.error_handling"
            type="textarea"
            :rows="2"
            placeholder="记录是否有明显错误的回答，以及你的处理方法..."
          />
        </el-form-item>

        <el-form-item label="4. 生成的内容和你的预期不符，我是如何调整优化的？">
          <el-input
            v-model="reviewForm.adjustment_notes"
            type="textarea"
            :rows="2"
            placeholder="记录如果结果不符预期，你做了哪些调整..."
          />
        </el-form-item>

        <el-form-item label="5. 我为什么这么写提示词？">
          <el-input
            v-model="reviewForm.prompt_reasoning"
            type="textarea"
            :rows="2"
            placeholder="思考你为什么会这样写提示词，背后的逻辑是什么..."
          />
        </el-form-item>
      </el-form>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">
          稍后再说
        </el-button>
        <el-button
          type="primary"
          @click="saveReview"
          :loading="saving"
          :icon="Check"
        >
          保存复盘
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import { saveReview } from '@/api'

interface Props {
  modelValue: boolean
  usageLogId?: number | null
}

interface Emit {
  (e: 'update:modelValue', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

const dialogVisible = ref(false)
const saving = ref(false)

const reviewForm = ref({
  expected_effect: '',
  evaluation_method: '',
  error_handling: '',
  adjustment_notes: '',
  prompt_reasoning: ''
})

watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
})

watch(dialogVisible, (val) => {
  emit('update:modelValue', val)
})

async function saveReview() {
  if (!props.usageLogId) {
    ElMessage.warning('请先复制提示词')
    return
  }

  saving.value = true
  try {
    await saveReview({
      usage_log_id: props.usageLogId,
      expected_effect: reviewForm.value.expected_effect,
      evaluation_method: reviewForm.value.evaluation_method,
      error_handling: reviewForm.value.error_handling,
      adjustment_notes: reviewForm.value.adjustment_notes,
      prompt_reasoning: reviewForm.value.prompt_reasoning
    })

    ElMessage.success('复盘已保存')
    dialogVisible.value = false

    // Reset form
    reviewForm.value = {
      expected_effect: '',
      evaluation_method: '',
      error_handling: '',
      adjustment_notes: '',
      prompt_reasoning: ''
    }
  } catch (error) {
    console.error('Save review error:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped lang="less">
.review-dialog {
  .review-intro {
    color: #909399;
    margin-bottom: 20px;
    line-height: 1.6;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
