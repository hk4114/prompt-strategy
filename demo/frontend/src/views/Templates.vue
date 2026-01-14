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
              accept=".md"
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
          <el-button type="primary" link @click="loadTemplates(searchKeyword)"
            >重试</el-button
          >
        </div>

        <template v-else>
          <div
            v-for="template in templates"
            :key="template.id"
            class="template-card"
            :class="{ 'is-expanded': expandedTemplates.has(template.id) }"
          >
            <div class="template-header" @click="toggleExpand(template.id)">
              <div class="header-left">
                <div class="icon-wrapper">
                  <el-icon
                    class="expand-icon"
                    :class="{
                      'is-rotated': expandedTemplates.has(template.id),
                    }"
                  >
                    <ArrowRight />
                  </el-icon>
                </div>
                <div class="title-wrapper">
                  <h3 class="template-title">{{ template.title }}</h3>
                  <div
                    class="template-meta"
                    v-if="!expandedTemplates.has(template.id)"
                  >
                    <span
                      class="meta-tag"
                      v-for="tag in template.tags.slice(0, 3)"
                      :key="tag"
                      >{{ tag }}</span
                    >
                  </div>
                </div>
              </div>
              <div class="template-actions">
                <el-button
                  link
                  type="primary"
                  @click.stop="copyTemplate(template)"
                >
                  复制
                </el-button>
                <el-button
                  v-if="!template.isSystem"
                  link
                  type="danger"
                  @click.stop="handleDelete(template.id)"
                >
                  删除
                </el-button>
              </div>
            </div>

            <el-collapse-transition>
              <div
                v-show="expandedTemplates.has(template.id)"
                class="template-body"
              >
                <!-- 编辑模式 -->
                <div
                  v-if="editingId === template.id"
                  class="edit-mode"
                  @click.stop
                >
                  <MdEditor
                    v-model="editingContent"
                    height="400px"
                    :preview="false"
                  />
                  <div class="edit-actions-bar">
                    <el-button @click="cancelEdit">取消</el-button>
                    <el-button
                      type="primary"
                      :loading="saveLoading"
                      @click="saveEdit(template)"
                    >
                      确认保存
                    </el-button>
                  </div>
                </div>

                <!-- 查看模式 -->
                <div v-else class="content-wrapper">
                  <div
                    class="template-content"
                    @dblclick.stop="startEdit(template)"
                    title="双击进入编辑模式"
                  >
                    <MdEditor
                      v-model="template.content"
                      height="400px"
                      :preview="false"
                      :disabled="true"
                    />
                  </div>
                </div>

                <div class="template-footer">
                  <div class="template-tags">
                    <el-tag
                      v-for="tag in template.tags"
                      :key="tag"
                      size="small"
                      effect="plain"
                      round
                      class="tag-item"
                    >
                      {{ tag }}
                    </el-tag>
                  </div>
                  <span class="usage-count">
                    <i class="el-icon-view"></i>
                    {{ template.usageCount }} 次使用
                  </span>
                </div>
              </div>
            </el-collapse-transition>
          </div>

          <el-empty
            v-if="templates.length === 0 && !loading"
            description="暂无模板"
          />
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
import { ref, reactive, onMounted, nextTick } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Search, ArrowRight } from "@element-plus/icons-vue";
import { MdEditor, MdPreview } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import {
  getTemplates,
  createTemplate,
  deleteTemplate,
  updateTemplate,
} from "@/api";

interface Template {
  id: number;
  title: string;
  content: string;
  templateType: string;
  isSystem: boolean;
  usageCount: number;
  tags: string[];
}

// 简单的防抖函数
const debounce = (fn: Function, delay: number) => {
  let timeout: any;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
};

// 缓存对象
const templateCache = new Map<string, Template[]>();

const templates = ref<Template[]>([]);
const expandedTemplates = ref(new Set<number>());
const searchKeyword = ref("");
const showAddDialog = ref(false);
const addLoading = ref(false);
const loading = ref(false);
const error = ref("");

// 编辑相关状态
const editingId = ref<number | null>(null);
const editingContent = ref("");
const saveLoading = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const newTemplate = reactive({
  title: "",
  content: "",
  tagsInput: "",
});

const toggleExpand = (id: number) => {
  if (expandedTemplates.value.has(id)) {
    expandedTemplates.value.delete(id);
  } else {
    expandedTemplates.value.add(id);
  }
};

const loadTemplates = async (keyword = "", useCache = true) => {
  // 如果使用缓存且缓存中存在
  if (useCache && templateCache.has(keyword)) {
    templates.value = templateCache.get(keyword)!;
    expandedTemplates.value.clear(); // 重置折叠状态
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const { data } = await getTemplates({ keyword });
    templates.value = data.templates;
    // 更新缓存
    templateCache.set(keyword, data.templates);
    expandedTemplates.value.clear(); // 重置折叠状态
  } catch (err) {
    console.error("Failed to load templates:", err);
    error.value = "加载失败，请检查网络连接";
  } finally {
    loading.value = false;
  }
};

const handleSearch = debounce(() => {
  loadTemplates(searchKeyword.value);
}, 300);

const copyTemplate = async (template: Template) => {
  try {
    await navigator.clipboard.writeText(template.content);
    ElMessage.success("已复制到剪贴板");
  } catch (err) {
    ElMessage.error("复制失败");
  }
};

const handleAdd = async () => {
  if (!newTemplate.title || !newTemplate.content) {
    ElMessage.warning("请填写标题和内容");
    return;
  }

  addLoading.value = true;
  try {
    const tags = newTemplate.tagsInput
      .split(/[,，]/)
      .map((t) => t.trim())
      .filter((t) => t);

    await createTemplate({
      title: newTemplate.title,
      content: newTemplate.content,
      templateType: "custom",
      tags,
    });
    ElMessage.success("添加成功");
    showAddDialog.value = false;
    newTemplate.title = "";
    newTemplate.content = "";
    newTemplate.tagsInput = "";

    // 清除缓存并重新加载
    templateCache.clear();
    loadTemplates();
  } catch (err) {
    ElMessage.error("添加失败");
  } finally {
    addLoading.value = false;
  }
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm("确定要删除这个模板吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await deleteTemplate(id);
    ElMessage.success("删除成功");

    // 清除缓存并重新加载
    templateCache.clear();
    loadTemplates(searchKeyword.value, false);
  } catch (err) {
    if (err !== "cancel") {
      ElMessage.error("删除失败");
    }
  }
};

// 导入导出功能
const triggerImport = () => {
  fileInput.value?.click();
};

const handleFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files || input.files.length === 0) return;

  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = async (e) => {
    try {
      const content = e.target?.result as string;

      // Markdown Parsing Logic
      // Split by H2 headers (## )
      const sections = content.split(/(?:^|\n)##\s+/);

      let successCount = 0;

      // sections[0] is usually empty or preamble
      for (let i = 1; i < sections.length; i++) {
        const section = sections[i];
        const firstLineBreak = section.indexOf("\n");

        if (firstLineBreak === -1) continue;

        const title = section.substring(0, firstLineBreak).trim();
        let body = section.substring(firstLineBreak).trim();

        // Extract content from code block if present
        const codeBlockMatch = body.match(
          /```(?:markdown|text)?\n([\s\S]*?)\n```/
        );
        if (codeBlockMatch) {
          body = codeBlockMatch[1];
        }

        if (!title || !body) continue;

        await createTemplate({
          title: title,
          content: body,
          templateType: "custom",
          tags: ["导入"],
        });
        successCount++;
      }

      if (successCount === 0) {
        throw new Error("未找到有效的模板格式");
      }

      ElMessage.success(`成功导入 ${successCount} 个模板`);
      templateCache.clear();
      loadTemplates();
    } catch (err: any) {
      console.error("Import failed:", err);
      ElMessage.error(err.message || "导入失败，文件格式不正确");
    } finally {
      // 重置 input value 以便下次可以导入同名文件
      input.value = "";
    }
  };

  reader.readAsText(file);
};

const handleExport = () => {
  try {
    let markdownContent = "";

    templates.value.forEach((t) => {
      markdownContent += `## ${t.title}\n\n`;
      markdownContent += "```markdown\n";
      markdownContent += t.content;
      markdownContent += "\n```\n\n";
    });

    const blob = new Blob([markdownContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `templates_export_${new Date().getTime()}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    ElMessage.success("导出成功");
  } catch (err) {
    ElMessage.error("导出失败");
  }
};

// 编辑功能
const startEdit = (template: Template) => {
  editingId.value = template.id;
  editingContent.value = template.content;
};

const cancelEdit = () => {
  editingId.value = null;
  editingContent.value = "";
};

const saveEdit = async (template: Template) => {
  if (!editingContent.value.trim()) {
    ElMessage.warning("内容不能为空");
    return;
  }

  if (editingContent.value === template.content) {
    cancelEdit();
    return;
  }

  saveLoading.value = true;
  try {
    await updateTemplate(template.id, {
      content: editingContent.value,
    });

    ElMessage.success("更新成功");

    // 更新本地数据
    const index = templates.value.findIndex((t) => t.id === template.id);
    if (index !== -1) {
      templates.value[index].content = editingContent.value;
    }

    // 更新缓存
    templateCache.clear();

    cancelEdit();
  } catch (err) {
    ElMessage.error("更新失败");
  } finally {
    saveLoading.value = false;
  }
};

onMounted(() => {
  loadTemplates();
});
</script>

<style lang="less" scoped>
.templates-page {
  background-color: #f5f7fa;
  min-height: 100vh;
  padding-bottom: 60px;

  .page-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .sticky-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    margin: 0 -20px 24px -20px;
    padding: 20px 20px 10px 20px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.03);
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;

    .section-title {
      margin-bottom: 0;
      font-size: 24px;
      font-weight: 600;
      color: #1a1a1a;
    }

    .header-actions {
      display: flex;
      gap: 12px;
    }
  }

  .search-section {
    margin-bottom: 10px;

    :deep(.el-input__wrapper) {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      border-radius: 8px;
      padding: 4px 12px;

      &.is-focus {
        box-shadow: 0 0 0 1px var(--el-color-primary) inset;
      }
    }
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
    gap: 12px;
    padding: 40px;
    background: #fff;
    border-radius: 12px;
  }

  .template-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    border: 1px solid transparent;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    overflow: hidden;

    &:hover {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
      transform: translateY(-2px);
    }

    &.is-expanded {
      border-color: rgba(0, 0, 0, 0.05);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
      transform: none; // Reset hover transform when expanded

      .template-header {
        border-bottom: 1px solid #f0f0f0;
        background-color: #fafafa;
      }
    }

    .template-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      cursor: pointer;
      background: #fff;
      transition: background-color 0.2s;

      &:hover {
        background-color: #fcfcfc;
      }

      .header-left {
        display: flex;
        align-items: center;
        gap: 16px;
        flex: 1;

        .icon-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: #f5f7fa;
          transition: all 0.2s;

          .expand-icon {
            font-size: 12px;
            color: #909399;
            transition: transform 0.3s ease;

            &.is-rotated {
              transform: rotate(90deg);
            }
          }
        }

        .title-wrapper {
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;

          .template-title {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #303133;
          }

          .template-meta {
            display: flex;
            gap: 6px;

            .meta-tag {
              font-size: 12px;
              color: #909399;
              background: #f5f7fa;
              padding: 2px 6px;
              border-radius: 4px;
            }
          }
        }
      }

      .template-actions {
        opacity: 0.8;
        transition: opacity 0.2s;

        &:hover {
          opacity: 1;
        }
      }
    }

    .template-body {
      padding: 20px 24px;
    }

    .content-wrapper {
      max-height: 65vh; // Ensure it fits within viewport
      overflow-y: auto;
      margin-bottom: 20px;
      padding-right: 4px;

      // Custom Scrollbar
      &::-webkit-scrollbar {
        width: 6px;
      }
      &::-webkit-scrollbar-thumb {
        background: #e4e7ed;
        border-radius: 3px;
      }
      &::-webkit-scrollbar-track {
        background: transparent;
      }
    }

    .template-content {
      font-family: "Menlo", "Monaco", "Consolas", "Courier New", monospace;
      font-size: 14px;
      line-height: 1.7;
      color: #4a4a4a;
      padding: 4px 0;
    }

    .edit-mode {
      margin-bottom: 20px;

      .edit-textarea {
        font-family: monospace;
      }

      .edit-actions-bar {
        display: flex;
        justify-content: flex-end;
        margin-top: 16px;
        gap: 12px;
      }
    }

    .template-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 16px;
      border-top: 1px solid #f5f7fa;

      .template-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;

        .tag-item {
          border-color: #e4e7ed;
          color: #606266;
        }
      }

      .usage-count {
        font-size: 13px;
        color: #909399;
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
  }
}

@media (max-width: 768px) {
  .templates-page {
    .sticky-header {
      padding: 16px 16px 10px 16px;
      margin: 0 -16px 20px -16px;
    }

    .page-container {
      padding: 0 16px;
    }

    .page-header {
      flex-direction: column;
      align-items: stretch;
      gap: 16px;

      .header-actions {
        justify-content: flex-end;
        overflow-x: auto;
        padding-bottom: 4px; // For scrollbar if needed
      }
    }

    .template-card {
      .template-header {
        padding: 12px 16px;

        .header-left {
          gap: 10px;

          .title-wrapper {
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
          }
        }
      }

      .template-body {
        padding: 16px;
      }

      .content-wrapper {
        max-height: 50vh; // Smaller max-height on mobile
      }
    }
  }
}
</style>
