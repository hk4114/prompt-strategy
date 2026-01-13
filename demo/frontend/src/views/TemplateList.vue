<template>
  <div class="templates-page">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">提示词模版</h1>
        <p class="page-subtitle">管理和使用你的提示词模板</p>
      </div>

      <!-- Search and Filter -->
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="12">
            <el-input
              v-model="searchText"
              placeholder="搜索模板..."
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-select
              v-model="selectedType"
              placeholder="模板类型"
              clearable
              @change="handleFilter"
              style="width: 100%"
            >
              <el-option label="最小公式" value="minimal_formula" />
              <el-option label="8步法" value="complex_8step" />
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="24" :md="6">
            <div class="button-group">
              <el-button type="primary" @click="showAddDialog = true" icon="Plus">添加模板</el-button>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- Templates Grid -->
      <div class="templates-grid">
        <el-card
          v-for="template in templates"
          :key="template.id"
          class="template-card"
          shadow="hover"
        >
          <template #header>
            <div class="card-header">
              <h3 class="template-title">{{ template.title }}</h3>
              <div class="template-type">
                <el-tag size="small" :type="getTypeTag(template.template_type)">
                  {{ formatType(template.template_type) }}
                </el-tag>
              </div>
            </div>
          </template>

          <div class="template-content">
            <p class="template-description">
              {{ template.content.substring(0, 150) }}
              {{ template.content.length > 150 ? '...' : '' }}
            </p>
            <div class="template-tags" v-if="template.tags?.length">
              <el-tag
                v-for="tag in template.tags"
                :key="tag.id"
                size="small"
                type="info"
              >
                {{ tag.name }}
              </el-tag>
            </div>
          </div>

          <div class="template-footer">
            <div class="template-stats">
              <span class="usage-count">
                <el-icon><Star /></el-icon>
                {{ template.usage_count || 0 }} 次使用
              </span>
            </div>
            <div class="template-actions">
              <el-button
                type="primary"
                size="small"
                @click="viewTemplate(template)"
                icon="View"
              >
                查看
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="usePremadeTemplate(template)"
                icon="DocumentCopy"
              >
                使用
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>

  <!-- Add Template Dialog -->
  <el-dialog
    v-model="showAddDialog"
    title="添加模板"
    width="600px"
  >
    <el-form ref="addFormRef" :model="newTemplate" label-width="100px">
      <el-form-item label="标题" required>
        <el-input v-model="newTemplate.title" />
      </el-form-item>
      <el-form-item label="内容" required>
        <el-input
          v-model="newTemplate.content"
          type="textarea"
          :rows="8"
        />
      </el-form-item>
      <el-form-item label="类型" required>
        <el-select v-model="newTemplate.template_type">
          <el-option label="最小公式" value="minimal_formula" />
          <el-option label="8步法" value="complex_8step" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showAddDialog = false">取消</el-button>
      <el-button type="primary" @click="addTemplate">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Star, Plus, View, DocumentCopy } from '@element-plus/icons-vue'
import { getTemplates, createTemplate, getTemplateTags } from '@/api'
import { usePromptStore } from '@/stores'

interface Template {
  id: number
  title: string
  content: string
  template_type: string
  is_system: boolean
  tags: any[]
  usage_count: number
}

const promptStore = usePromptStore()

const templates = ref<Template[]>([])
const searchText = ref('')
const selectedType = ref('')
const showAddDialog = ref(false)

const newTemplate = ref({
  title: '',
  content: '',
  template_type: 'minimal_formula'
})

async function loadTemplates() {
  try {
    const params: any = {}
    if (searchText.value) params.search = searchText.value
    if (selectedType.value) params.type = selectedType.value

    const data = await getTemplates(params)
    templates.value = data.templates
  } catch (error) {
    console.error(error)
    ElMessage.error('加载模板失败')
  }
}

function handleSearch() {
  loadTemplates()
}

function handleFilter() {
  loadTemplates()
}

function formatType(type: string) {
  if (type === 'minimal_formula') return '最小公式'
  if (type === 'complex_8step') return '8步法'
  return type
}

function getTypeTag(type: string) {
  if (type === 'minimal_formula') return ''
  return 'success'
}

function viewTemplate(template: Template) {
  ElMessage({
    message: template.content,
    duration: 0,
    showClose: true,
    grouping: true
  })
}

async function useTemplate(template: Template) {
  promptStore.setGeneratedPrompt(template.content, null)
  await navigator.clipboard.writeText(template.content)
  ElMessage.success('已复制到剪贴板')
}

async function addTemplate() {
  try {
    const result = await createTemplate(newTemplate.value as any)
    ElMessage.success('模板添加成功')
    showAddDialog.value = false
    newTemplate.value = { title: '', content: '', template_type: 'minimal_formula' }
    loadTemplates()
  } catch (error) {
    console.error(error)
    ElMessage.error('添加失败')
  }
}

function usePremadeTemplate(template: Template) {
  useTemplate(template)
}

onMounted(() => {
  loadTemplates()
})
</script>

<style scoped>
.templates-page { padding: 20px 0; }
.page-container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.page-header { text-align: center; margin-bottom: 40px; }
.page-title { font-size: 36px; margin: 0 0 8px 0; }
.page-subtitle { font-size: 18px; color: #666; }

.filter-section { margin-bottom: 30px; }

.button-group { display: flex; justify-content: flex-end; }

.templates-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 24px; }

.template-card { height: 100%; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.template-title {
  font-size: 18px;
  margin: 0;
  flex: 1;
}

.template-content {
  flex: 1;
}

.template-description {
  color: #606266;
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.template-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.template-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.template-stats {
  .usage-count {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    color: #909399;
  }
}

@media (max-width: 768px) {
  .templates-grid { grid-template-columns: 1fr; }
  .button-group { margin-top: 12px; }
}
</style>
