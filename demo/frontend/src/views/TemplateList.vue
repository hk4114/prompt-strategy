<template>
  <div class="template-list">
    <div class="page-header">
      <h1 class="section-title">
        <span class="highlight">提示词</span> 模板库
      </h1>
      <p class="page-desc">快速复用经典提示词模板</p>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-bar glass-card">
      <el-input
        v-model="keyword"
        placeholder="搜索模板标题或内容..."
        prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
      <el-button type="primary" @click="showAddDialog = true">
        + 添加模板
      </el-button>
    </div>

    <!-- 模板列表 -->
    <div class="templates-grid">
      <div
        v-for="template in templates"
        :key="template.id"
        class="template-card glass-card fade-in-up"
      >
        <div class="card-header">
          <h3 class="template-title">{{ template.title }}</h3>
          <div class="card-meta">
            <span class="usage-count">📊 {{ template.usageCount }} 次使用</span>
            <el-tag v-if="template.isSystem" size="small" type="info">系统模板</el-tag>
          </div>
        </div>
        
        <div class="template-content">
          <pre>{{ template.content }}</pre>
        </div>
        
        <div class="tag-list" v-if="template.tags?.length">
          <el-tag v-for="tag in template.tags" :key="tag" size="small">
            {{ tag }}
          </el-tag>
        </div>
        
        <div class="card-actions">
          <el-button type="primary" @click="handleCopy(template)">
            📋 复制
          </el-button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="templates.length === 0" class="empty-state glass-card">
      <span class="empty-icon">📭</span>
      <p>暂无模板，添加一个吧</p>
    </div>

    <!-- 添加模板弹窗 -->
    <el-dialog
      v-model="showAddDialog"
      title="添加新模板"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="newTemplate" label-position="top">
        <el-form-item label="模板标题" required>
          <el-input v-model="newTemplate.title" placeholder="输入模板标题" />
        </el-form-item>
        <el-form-item label="模板内容" required>
          <el-input
            v-model="newTemplate.content"
            type="textarea"
            :rows="10"
            placeholder="输入模板内容"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="newTemplate.tagsInput" placeholder="用逗号分隔多个标签" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddTemplate" :loading="adding">
          添加
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getTemplates, createTemplate, copyTemplate } from '@/api/requests'
import { useAppStore } from '@/stores'

const appStore = useAppStore()

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
const keyword = ref('')
const showAddDialog = ref(false)
const adding = ref(false)

const newTemplate = reactive({
  title: '',
  content: '',
  tagsInput: ''
})

const loadTemplates = async () => {
  try {
    const res = await getTemplates({ keyword: keyword.value }) as { templates: Template[] }
    templates.value = res.templates
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
}

let searchTimer: ReturnType<typeof setTimeout>
const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    loadTemplates()
  }, 300)
}

const handleCopy = async (template: Template) => {
  try {
    await copyTemplate(template.id)
    await navigator.clipboard.writeText(template.content)
    ElMessage.success('已复制到剪贴板')
    
    // 更新使用次数
    template.usageCount++
    
    // 弹出复盘检查清单
    appStore.openReviewDialog(null, template.content)
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const handleAddTemplate = async () => {
  if (!newTemplate.title || !newTemplate.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }

  adding.value = true
  try {
    await createTemplate({
      title: newTemplate.title,
      content: newTemplate.content,
      templateType: 'custom',
      tags: newTemplate.tagsInput.split(',').map(t => t.trim()).filter(Boolean)
    })
    
    ElMessage.success('添加成功')
    showAddDialog.value = false
    
    // 重置表单
    newTemplate.title = ''
    newTemplate.content = ''
    newTemplate.tagsInput = ''
    
    // 刷新列表
    loadTemplates()
  } catch (error) {
    ElMessage.error('添加失败')
  } finally {
    adding.value = false
  }
}

onMounted(() => {
  loadTemplates()
})
</script>

<style lang="less" scoped>
.template-list {
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    text-align: center;
    margin-bottom: 32px;

    .page-desc {
      color: rgba(255, 255, 255, 0.7);
    }
  }

  .filter-bar {
    display: flex;
    gap: 16px;
    padding: 20px;
    margin-bottom: 24px;

    .el-input {
      flex: 1;
    }
  }

  .templates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 24px;
  }

  .template-card {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;

    .card-header {
      .template-title {
        font-size: 18px;
        color: #fff;
        margin-bottom: 8px;
      }

      .card-meta {
        display: flex;
        align-items: center;
        gap: 12px;

        .usage-count {
          font-size: 12px;
          color: rgba(255, 255, 255, 0.6);
        }
      }
    }

    .template-content {
      background: rgba(0, 0, 0, 0.2);
      border-radius: 8px;
      padding: 16px;
      max-height: 200px;
      overflow: auto;

      pre {
        color: rgba(255, 255, 255, 0.8);
        font-size: 13px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        margin: 0;
      }
    }

    .card-actions {
      margin-top: auto;
    }
  }

  .empty-state {
    padding: 60px;
    text-align: center;
    color: rgba(255, 255, 255, 0.5);

    .empty-icon {
      font-size: 48px;
      display: block;
      margin-bottom: 16px;
    }
  }
}

// 弹窗样式
:deep(.el-dialog) {
  background: #1e293b;
  border-radius: 16px;

  .el-dialog__title {
    color: #fff;
  }

  .el-dialog__body {
    padding: 20px;
  }
}
</style>
