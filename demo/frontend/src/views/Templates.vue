<template>
  <div class="templates-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="section-title">提示词模版</h2>
        <el-button type="primary" @click="showAddDialog = true">
          添加模板
        </el-button>
      </div>

      <!-- 搜索区域 -->
      <div class="search-section card">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索模板..."
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <!-- 模板列表 -->
      <div class="templates-list">
        <div
          v-for="template in templates"
          :key="template.id"
          class="template-card card"
        >
          <div class="template-header">
            <h3 class="template-title">{{ template.title }}</h3>
            <div class="template-actions">
              <el-button size="small" type="primary" @click="copyTemplate(template)">
                复制
              </el-button>
              <el-button
                v-if="!template.isSystem"
                size="small"
                type="danger"
                @click="handleDelete(template.id)"
              >
                删除
              </el-button>
            </div>
          </div>
          <pre class="template-content">{{ template.content }}</pre>
          <div class="template-footer">
            <div class="template-tags">
              <el-tag
                v-for="tag in template.tags"
                :key="tag"
                size="small"
                type="info"
              >
                {{ tag }}
              </el-tag>
            </div>
            <span class="usage-count">使用次数：{{ template.usageCount }}</span>
          </div>
        </div>

        <el-empty v-if="templates.length === 0" description="暂无模板" />
      </div>
    </div>

    <!-- 添加模板弹窗 -->
    <el-dialog v-model="showAddDialog" title="添加模板" width="600px">
      <el-form :model="newTemplate" label-position="top">
        <el-form-item label="模板标题" required>
          <el-input v-model="newTemplate.title" placeholder="输入模板标题" />
        </el-form-item>
        <el-form-item label="模板内容" required>
          <el-input
            v-model="newTemplate.content"
            type="textarea"
            :rows="8"
            placeholder="输入模板内容"
          />
        </el-form-item>
        <el-form-item label="标签（用逗号分隔）">
          <el-input
            v-model="newTemplate.tagsInput"
            placeholder="例如：翻译,文章,中文"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd" :loading="addLoading">
          添加
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getTemplates, createTemplate, deleteTemplate, copyTemplate as apiCopyTemplate } from '@/api'

interface Template {
  id: number
  title: string
  content: string
  templateType: string
  isSystem: boolean
  usageCount: number
  tags: string[]
}

const templates = ref<Template[]>([])
const searchKeyword = ref('')
const showAddDialog = ref(false)
const addLoading = ref(false)

const newTemplate = reactive({
  title: '',
  content: '',
  tagsInput: ''
})

const loadTemplates = async (keyword = '') => {
  try {
    const { data } = await getTemplates({ keyword })
    templates.value = data.templates
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
}

const handleSearch = () => {
  loadTemplates(searchKeyword.value)
}

const copyTemplate = async (template: Template) => {
  try {
    await apiCopyTemplate(template.id)
    await navigator.clipboard.writeText(template.content)
    ElMessage.success('已复制到剪贴板')
    loadTemplates(searchKeyword.value)
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const handleAdd = async () => {
  if (!newTemplate.title || !newTemplate.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }

  addLoading.value = true
  try {
    const tags = newTemplate.tagsInput
      .split(/[,，]/)
      .map(t => t.trim())
      .filter(t => t)

    await createTemplate({
      title: newTemplate.title,
      content: newTemplate.content,
      templateType: 'custom',
      tags
    })
    ElMessage.success('添加成功')
    showAddDialog.value = false
    newTemplate.title = ''
    newTemplate.content = ''
    newTemplate.tagsInput = ''
    loadTemplates()
  } catch (error) {
    ElMessage.error('添加失败')
  } finally {
    addLoading.value = false
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个模板吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteTemplate(id)
    ElMessage.success('删除成功')
    loadTemplates(searchKeyword.value)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadTemplates()
})
</script>

<style lang="less" scoped>
.templates-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .section-title {
      margin-bottom: 0;
    }
  }

  .search-section {
    margin-bottom: 20px;
    padding: 16px;
  }

  .templates-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .template-card {
    .template-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .template-title {
      margin: 0;
      font-size: 18px;
    }

    .template-content {
      background: #fafafa;
      border-radius: 8px;
      padding: 16px;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-family: inherit;
      font-size: 14px;
      line-height: 1.6;
      margin: 0 0 16px 0;
    }

    .template-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .template-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
      }

      .usage-count {
        font-size: 12px;
        color: #909399;
      }
    }
  }
}
</style>
