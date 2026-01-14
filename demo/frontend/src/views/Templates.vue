<template>
  <div class="templates-page">
    <div class="page-container">
      <!-- 吸顶头部区域 -->
      <div class="sticky-header">
        <div class="page-header">
          <h2 class="section-title">提示词模版</h2>
          <div class="header-actions">
            <input
              type="file"
              ref="fileInput"
              style="display: none"
              accept=".json"
              @change="handleFileChange"
            />
            <el-button @click="triggerImport">导入模板</el-button>
            <el-button @click="handleExport">导出模板</el-button>
            <el-button type="primary" @click="showAddDialog = true">
              添加模板
            </el-button>
          </div>
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
      </div>

      <!-- 模板列表 -->
      <div 
        class="templates-list" 
        v-loading="loading"
        element-loading-text="加载中..."
      >
        <div v-if="error" class="error-state">
          <el-alert :title="error" type="error" show-icon :closable="false" />
          <el-button type="primary" link @click="loadTemplates(searchKeyword)">重试</el-button>
        </div>

        <template v-else>
          <div
            v-for="template in templates"
            :key="template.id"
            class="template-card card"
          >
            <div class="template-header" @click="toggleExpand(template.id)">
              <div class="header-left">
                <el-icon 
                  class="expand-icon"
                  :class="{ 'is-expanded': expandedTemplates.has(template.id) }"
                >
                  <ArrowRight />
                </el-icon>
                <h3 class="template-title">{{ template.title }}</h3>
              </div>
              <div class="template-actions">
                <el-button size="small" type="primary" @click.stop="copyTemplate(template)">
                  复制
                </el-button>
                <el-button
                  v-if="!template.isSystem"
                  size="small"
                  type="danger"
                  @click.stop="handleDelete(template.id)"
                >
                  删除
                </el-button>
              </div>
            </div>
            
            <el-collapse-transition>
              <div v-show="expandedTemplates.has(template.id)">
                <!-- 编辑模式 -->
                <div v-if="editingId === template.id" class="edit-mode" @click.stop>
                  <el-input
                    v-model="editingContent"
                    type="textarea"
                    :rows="6"
                    placeholder="请输入模板内容"
                    ref="editInputRef"
                  />
                  <div class="edit-actions-bar">
                    <el-button size="small" @click="cancelEdit">取消</el-button>
                    <el-button 
                      size="small" 
                      type="primary" 
                      :loading="saveLoading" 
                      @click="saveEdit(template)"
                    >
                      确认
                    </el-button>
                  </div>
                </div>
                
                <!-- 查看模式 -->
                <pre 
                  v-else 
                  class="template-content" 
                  @dblclick.stop="startEdit(template)"
                  title="双击可编辑内容"
                >{{ template.content }}</pre>

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
            </el-collapse-transition>
          </div>

          <el-empty v-if="templates.length === 0 && !loading" description="暂无模板" />
        </template>
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
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, ArrowRight } from '@element-plus/icons-vue'
import { getTemplates, createTemplate, deleteTemplate, updateTemplate } from '@/api'

interface Template {
  id: number
  title: string
  content: string
  templateType: string
  isSystem: boolean
  usageCount: number
  tags: string[]
}

// 简单的防抖函数
const debounce = (fn: Function, delay: number) => {
  let timeout: any
  return (...args: any[]) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => fn(...args), delay)
  }
}

// 缓存对象
const templateCache = new Map<string, Template[]>()

const templates = ref<Template[]>([])
const expandedTemplates = ref(new Set<number>())
const searchKeyword = ref('')
const showAddDialog = ref(false)
const addLoading = ref(false)
const loading = ref(false)
const error = ref('')

// 编辑相关状态
const editingId = ref<number | null>(null)
const editingContent = ref('')
const saveLoading = ref(false)
const editInputRef = ref<any>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const newTemplate = reactive({
  title: '',
  content: '',
  tagsInput: ''
})

const toggleExpand = (id: number) => {
  if (expandedTemplates.value.has(id)) {
    expandedTemplates.value.delete(id)
  } else {
    expandedTemplates.value.add(id)
  }
}

const loadTemplates = async (keyword = '', useCache = true) => {
  // 如果使用缓存且缓存中存在
  if (useCache && templateCache.has(keyword)) {
    templates.value = templateCache.get(keyword)!
    expandedTemplates.value.clear() // 重置折叠状态
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    const { data } = await getTemplates({ keyword })
    templates.value = data.templates
    // 更新缓存
    templateCache.set(keyword, data.templates)
    expandedTemplates.value.clear() // 重置折叠状态
  } catch (err) {
    console.error('Failed to load templates:', err)
    error.value = '加载失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

const handleSearch = debounce(() => {
  loadTemplates(searchKeyword.value)
}, 300)

const copyTemplate = async (template: Template) => {
  try {
    await navigator.clipboard.writeText(template.content)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
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
    
    // 清除缓存并重新加载
    templateCache.clear()
    loadTemplates()
  } catch (err) {
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
    
    // 清除缓存并重新加载
    templateCache.clear()
    loadTemplates(searchKeyword.value, false)
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 导入导出功能
const triggerImport = () => {
  fileInput.value?.click()
}

const handleFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  const file = input.files[0]
  const reader = new FileReader()

  reader.onload = async (e) => {
    try {
      const content = e.target?.result as string
      const data = JSON.parse(content)

      if (!Array.isArray(data)) {
        throw new Error('格式错误：文件内容必须是数组')
      }

      // 验证和导入
      let successCount = 0
      for (const item of data) {
        if (!item.name || !item.content) {
          console.warn('跳过无效模板:', item)
          continue
        }

        await createTemplate({
          title: item.name,
          content: item.content,
          templateType: 'custom',
          tags: []
        })
        successCount++
      }

      ElMessage.success(`成功导入 ${successCount} 个模板`)
      templateCache.clear()
      loadTemplates()
    } catch (err: any) {
      console.error('Import failed:', err)
      ElMessage.error(err.message || '导入失败，文件格式不正确')
    } finally {
      // 重置 input value 以便下次可以导入同名文件
      input.value = ''
    }
  }

  reader.readAsText(file)
}

const handleExport = () => {
  try {
    const exportData = templates.value.map(t => ({
      name: t.title,
      content: t.content
    }))

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `templates_export_${new Date().getTime()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (err) {
    ElMessage.error('导出失败')
  }
}

// 编辑功能
const startEdit = (template: Template) => {
  editingId.value = template.id
  editingContent.value = template.content
  
  nextTick(() => {
    editInputRef.value?.[0]?.focus()
  })
}

const cancelEdit = () => {
  editingId.value = null
  editingContent.value = ''
}

const saveEdit = async (template: Template) => {
  if (!editingContent.value.trim()) {
    ElMessage.warning('内容不能为空')
    return
  }
  
  if (editingContent.value === template.content) {
    cancelEdit()
    return
  }

  saveLoading.value = true
  try {
    await updateTemplate(template.id, {
      content: editingContent.value
    })
    
    ElMessage.success('更新成功')
    
    // 更新本地数据
    const index = templates.value.findIndex(t => t.id === template.id)
    if (index !== -1) {
      templates.value[index].content = editingContent.value
    }
    
    // 更新缓存
    templateCache.clear() // 简单处理：清除所有缓存，或者更新对应缓存
    
    cancelEdit()
  } catch (err) {
    ElMessage.error('更新失败')
  } finally {
    saveLoading.value = false
  }
}

onMounted(() => {
  loadTemplates()
})
</script>

<style lang="less" scoped>
.templates-page {
  .sticky-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(5px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: -20px -20px 20px -20px;
    padding: 20px 20px 0 20px;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;

    .section-title {
      margin-bottom: 0;
    }
    
    .header-actions {
      display: flex;
      gap: 10px;
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
    min-height: 200px;
  }
  
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 20px;
  }

  .template-card {
    transition: all 0.3s ease;

    .template-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0; // Remove bottom margin when collapsed
      padding: 12px 16px; // Add padding to header area
      cursor: pointer;
      border-radius: 4px;
      
      &:hover {
        background-color: #f5f7fa;
      }
      
      .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
        
        .expand-icon {
          transition: transform 0.3s ease;
          color: #909399;
          
          &.is-expanded {
            transform: rotate(90deg);
          }
        }
      }
    }

    .template-title {
      margin: 0;
      font-size: 18px;
    }

    // Add padding wrapper for content and footer
    .template-content, .template-footer, .edit-mode {
      margin-left: 16px;
      margin-right: 16px;
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
      margin-top: 12px;
      margin-bottom: 16px;
      cursor: pointer;
      transition: background-color 0.2s;
      
      &:hover {
        background: #f0f0f0;
      }
    }
    
    .edit-mode {
      margin-top: 12px;
      margin-bottom: 16px;
      
      .edit-actions-bar {
        display: flex;
        justify-content: flex-end;
        margin-top: 8px;
        gap: 8px;
      }
    }

    .template-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px; // Add bottom padding

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

@media (max-width: 768px) {
  .templates-page {
    .page-header {
      flex-direction: column;
      align-items: stretch;
      
      .header-actions {
        justify-content: flex-end;
      }
    }
  }
}
</style>