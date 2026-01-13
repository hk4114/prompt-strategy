<template>
  <div class="prompt-tips-panel" :class="{ collapsed: isCollapsed }">
    <div class="panel-header" @click="toggleCollapse">
      <h3 class="panel-title">
        <el-icon><Lightning /></el-icon>
        提示词技巧
      </h3>
      <el-icon class="collapse-icon">
        <ArrowRight v-if="isCollapsed" />
        <ArrowDown v-else />
      </el-icon>
    </div>

    <div v-if="!isCollapsed" class="panel-content">
      <div v-if="loading" class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        加载中...
      </div>

      <div v-else class="tips-list">
        <div v-for="tip in tips" :key="tip.id" class="tip-item">
          <h4 class="tip-title">{{ tip.title }}</h4>
          <p class="tip-content">{{ tip.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Lightning, ArrowDown, ArrowRight, Loading } from '@element-plus/icons-vue'
import { getTips } from '@/api'

interface Tip {
  id: number
  title: string
  content: string
  sort_order: number
}

const tips = ref<Tip[]>([])
const loading = ref(false)
const isCollapsed = ref(false)

async function loadTips() {
  try {
    loading.value = true
    const data = await getTips()
    tips.value = data.tips.sort((a: Tip, b: Tip) => a.sort_order - b.sort_order)
  } catch (error) {
    console.error('Failed to load tips:', error)
  } finally {
    loading.value = false
  }
}

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

onMounted(() => {
  loadTips()
})
</script>

<style scoped lang="less">
.prompt-tips-panel {
  position: fixed;
  left: 20px;
  bottom: 20px;
  width: 320px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border: 1px solid #e4e7ed;
  z-index: 1000;
  max-height: 500px;
  overflow: hidden;
  transition: all 0.3s ease;

  &.collapsed {
    width: 200px;
    height: 60px;
    cursor: pointer;

    &:hover {
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
  }
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background-color: #409eff;
  color: white;
  cursor: pointer;
  user-select: none;

  &:hover {
    background-color: #66b1ff;
  }
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.collapse-icon {
  transition: transform 0.3s;
}

.panel-content {
  max-height: 400px;
  overflow-y: auto;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #909399;

  .is-loading {
    animation: rotating 2s linear infinite;
    margin-right: 8px;
  }
}

.tips-list {
  padding: 16px;
}

.tip-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
}

.tip-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.tip-content {
  font-size: 13px;
  line-height: 1.6;
  color: #606266;
  margin: 0;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .prompt-tips-panel {
    left: 10px;
    right: 10px;
    bottom: 10px;
    width: auto;
    max-width: none;
  }
}
</style>
