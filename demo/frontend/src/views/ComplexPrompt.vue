<template>
  <div class="complex-prompt-page">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">复杂提示词生成</h1>
        <p class="page-subtitle">使用8步法构建高质量提示词</p>
      </div>

      <!-- 8 Steps -->
      <el-card class="steps-card" shadow="never">
        <el-steps :active="currentStep" finish-status="success" align-center>
          <el-step
            v-for="(step, index) in steps"
            :key="index"
            :title="step.title"
            @click="currentStep = index"
          />
        </el-steps>

        <div class="step-content">
          <div v-if="currentStep === 0" class="step-form">
            <h3>{{ steps[0].title }}</h3>
            <el-form label-position="top">
              <el-form-item label="你面临的核心问题是什么：">
                <el-input
                  v-model="stepData.problem"
                  type="textarea"
                  :rows="4"
                  placeholder="描述你的核心问题..."
                />
              </el-form-item>
              <el-form-item label="相关背景信息：">
                <el-input
                  v-model="stepData.background"
                  type="textarea"
                  :rows="3"
                  placeholder="提供相关的背景信息..."
                />
              </el-form-item>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else-if="currentStep === 1" class="step-form">
            <h3>{{ steps[1].title }}</h3>
            <p class="step-description">我会帮你选择最合适的专家角色来解决问题。</p>
            <el-button type="primary" @click="autoGenerateRoles">生成推荐角色</el-button>
            <div v-if="stepData.roles.length > 0" class="roles-list">
              <h4>推荐角色：</h4>
              <el-tag
                v-for="role in stepData.roles"
                :key="role"
                size="large"
                effect="dark"
                style="margin: 4px"
              >
                {{ role }}
              </el-tag>
            </div>
            <el-button type="primary" @click="nextStep" style="margin-top: 20px">下一步</el-button>
          </div>

          <div v-else-if="currentStep === 2" class="step-form">
            <h3>{{ steps[2].title }}</h3>
            <el-form label-position="top">
              <el-form-item label="让AI通过提问更好地理解你的需求：">
                <div class="questions-list">
                  <div v-for="question in stepData.questions" :key="question" class="question-item">
                    <el-icon><QuestionFilled /></el-icon>
                    {{ question }}
                  </div>
                </div>
                <el-button type="primary" @click="generateQuestions" style="margin-top: 10px">
                  生成问题
                </el-button>
              </el-form-item>
              <el-form-item label="你的回答：">
                <el-input
                  v-model="stepData.answers"
                  type="textarea"
                  :rows="4"
                  placeholder="回答上述问题..."
                />
              </el-form-item>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else-if="currentStep === 3" class="step-form">
            <h3>{{ steps[3].title }}</h3>
            <el-form label-position="top">
              <el-form-item label="具体情境描述：">
                <el-input
                  v-model="stepData.scenario"
                  type="textarea"
                  :rows="4"
                  placeholder="描述一个具体的使用情境..."
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="previewScenario">预览情境</el-button>
              </el-form-item>
              <el-form-item label="预览：" v-if="stepData.scenarioPreview">
                <el-alert :title="stepData.scenarioPreview" type="info" :closable="false" />
              </el-form-item>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else-if="currentStep === 4" class="step-form">
            <h3>{{ steps[4].title }}</h3>
            <p class="step-description">请评估第一次尝试的效果</p>
            <el-form label-position="top">
              <el-form-item label="第一次尝试的结果：">
                <el-input
                  v-model="stepData.firstAttempt"
                  type="textarea"
                  :rows="4"
                  placeholder="记录你的第一次尝试..."
                />
              </el-form-item>
              <el-form-item label="需要改进的地方：">
                <el-input
                  v-model="stepData.improvements"
                  type="textarea"
                  :rows="3"
                  placeholder="列出需要改进的地方..."
                />
              </el-form-item>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else-if="currentStep === 5" class="step-form">
            <h3>{{ steps[5].title }}</h3>
            <el-form label-position="top">
              <el-form-item label="让红队来挑刺：">
                <el-input
                  v-model="stepData.redTeamFeedback"
                  type="textarea"
                  :rows="4"
                  placeholder="假设方案失败，最可能的原因是什么？"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="simulateRedTeam">模拟红队挑刺</el-button>
              </el-form-item>
              <el-alert
                v-if="stepData.redTeamResult"
                :title="stepData.redTeamResult"
                type="warning"
                :closable="false"
                style="margin-bottom: 20px"
              />
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else-if="currentStep === 6" class="step-form">
            <h3>{{ steps[6].title }}</h3>
            <el-form label-position="top">
              <el-form-item label="找到的最佳回答（SSR）：">
                <el-input
                  v-model="stepData.ssrAnswer"
                  type="textarea"
                  :rows="6"
                  placeholder="粘贴你认为最好的回答..."
                />
              </el-form-item>
              <el-form-item label="微调要点：">
                <el-input
                  v-model="stepData.refinements"
                  type="textarea"
                  :rows="3"
                  placeholder="基于最佳回答的微调要点..."
                />
              </el-form-item>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </el-form>
          </div>

          <div v-else class="step-form">
            <el-result icon="success" title="生成完成" sub-title="你的复杂提示词已经生成">
              <template #extra>
                <el-button type="primary" @click="generateFinalPrompt">生成最终提示词</el-button>
              </template>
            </el-result>
          </div>
        </div>
      </el-card>

      <!-- Final Result -->
      <el-card v-if="finalPrompt" class="result-card" shadow="never" style="margin-top: 20px">
        <h3>最终生成的提示词</h3>
        <el-input
          v-model="finalPrompt"
          type="textarea"
          :rows="15"
          readonly
          style="margin: 20px 0"
        />
        <el-button type="success" @click="copyFinal" icon="DocumentCopy">复制提示词</el-button>
        <el-button @click="resetAll">重新开始</el-button>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { generatePrompt as apiGeneratePrompt } from '@/api'
import { usePromptStore } from '@/stores'

const promptStore = usePromptStore()

const currentStep = ref(0)
const finalPrompt = ref('')
const usageLogId = ref<number | null>(null)

const steps = [
  { title: '明确问题与上下文' },
  { title: '自选必要角色' },
  { title: '连续提问' },
  { title: '具体情境' },
  { title: '根据表现迭代' },
  { title: '红队挑刺' },
  { title: '抽到SSR' },
  { title: '抽象成模板' }
]

const stepData = reactive({
  problem: '',
  background: '',
  roles: [] as string[],
  questions: [] as string[],
  answers: '',
  scenario: '',
  scenarioPreview: '',
  firstAttempt: '',
  improvements: '',
  redTeamFeedback: '',
  redTeamResult: '',
  ssrAnswer: '',
  refinements: ''
})

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    generateFinalPrompt()
  }
}

function autoGenerateRoles() {
  stepData.roles = ['领域专家', '产品经理', '技术架构师']
  ElMessage.success('已生成推荐角色')
}

function generateQuestions() {
  stepData.questions = [
    '这个任务的目标用户是谁？',
    '期望的最终输出是什么格式？',
    '有没有必须遵循的约束条件？',
    '任务的优先级如何？',
    '预期的时间范围是多少？'
  ]
  ElMessage.success('已生成提问清单')
}

function previewScenario() {
  stepData.scenarioPreview = `情境预览：${stepData.scenario}`
}

function simulateRedTeam() {
  stepData.redTeamResult = `红队分析：方案如果失败，最可能的原因是：${stepData.redTeamFeedback || '缺乏充分的用户调研和技术可行性分析'}`
}

async function generateFinalPrompt() {
  const prompt = `### 角色
作为 ${stepData.roles.join(', ') || '[领域专家]'} 专家

### 背景
当前面临 ${stepData.problem || '[未定义的问题]'} 问题
${stepData.background || '[未提供背景信息]'}

### 任务
${stepData.scenario || '[未提供具体情境]'}

### 要求
基于用户回答：${stepData.answers || '[无回答]'}
优化方向：${stepData.improvements || '[未提供]'}

### 红队反馈
${stepData.redTeamResult || '[无红队反馈]'}

### 最终优化
${stepData.refinements || '[未提供微调要点]'}

### 格式
1. 请使用 Markdown 格式输出
2. 首先给出一个 1-10 分的总体评分和一句话总结
3. 然后分 '优势'、'劣势' 和 '致命风险' 三个板块进行详细论述`

  finalPrompt.value = prompt

  // Save to backend
  try {
    const result = await apiGeneratePrompt({
      prompt_type: 'complex_8step',
      generated_prompt: finalPrompt.value,
      form_data: stepData
    })
    usageLogId.value = result.usage_log_id
    ElMessage.success('提示词已生成并保存')
  } catch (error) {
    console.error('Save error:', error)
    ElMessage.warning('生成成功，但保存失败')
  }
}

function copyFinal() {
  navigator.clipboard.writeText(finalPrompt.value).then(() => {
    ElMessage.success('已复制到剪贴板')
    promptStore.setGeneratedPrompt(finalPrompt.value, usageLogId.value)
  })
}

function resetAll() {
  currentStep.value = 0
  finalPrompt.value = ''
  Object.assign(stepData, {
    problem: '', background: '', roles: [], questions: [],
    answers: '', scenario: '', scenarioPreview: '',
    firstAttempt: '', improvements: '', redTeamFeedback: '',
    redTeamResult: '', ssrAnswer: '', refinements: ''
  })
}
</script>

<style scoped>
.complex-prompt-page {
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
}

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

.steps-card {
  margin-bottom: 20px;
}

.step-content {
  margin-top: 30px;
  padding: 20px;
}

.step-form h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 24px;
}

.step-description {
  color: #606266;
  margin-bottom: 20px;
}

.roles-list {
  margin: 20px 0;
}

.questions-list {
  margin-bottom: 20px;
}

.question-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid #e4e7ed;
}

@media (max-width: 768px) {
  .page-title { font-size: 28px; }
  .page-subtitle { font-size: 16px; }
}
</style>
