<template>
  <Teleport to="body">
    <div
      v-show="appStore.showTipsPanel"
      class="tips-panel"
      :class="{ minimized: appStore.tipsPanelMinimized }"
    >
      <div class="tips-header" @click="appStore.toggleTipsPanel">
        <span class="tips-icon">💡</span>
        <span v-if="!appStore.tipsPanelMinimized" class="tips-title">提示词技巧</span>
        <span class="toggle-icon">{{ appStore.tipsPanelMinimized ? '◀' : '▼' }}</span>
      </div>
      
      <div v-if="!appStore.tipsPanelMinimized" class="tips-content">
        <div v-for="tip in tips" :key="tip.id" class="tip-item">
          <h4>{{ tip.title }}</h4>
          <p>{{ tip.content }}</p>
        </div>
        
        <div v-if="tips.length === 0" class="empty-tips">
          加载中...
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAppStore } from '@/stores'
import { getTips } from '@/api/requests'

const appStore = useAppStore()

interface Tip {
  id: number
  title: string
  content: string
  sortOrder: number
}

const tips = ref<Tip[]>([])

onMounted(async () => {
  try {
    const res = await getTips() as { tips: Tip[] }
    tips.value = res.tips
  } catch (error) {
    console.error('Failed to load tips:', error)
  }
})
</script>

<style lang="less" scoped>
.tips-panel {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 320px;
  max-height: 400px;
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  overflow: hidden;
  transition: all 0.3s ease;

  &.minimized {
    width: auto;
    max-height: none;
    
    .tips-header {
      border-bottom: none;
    }
  }

  .tips-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 16px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    transition: background 0.2s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.05);
    }

    .tips-icon {
      font-size: 20px;
    }

    .tips-title {
      flex: 1;
      color: #fff;
      font-weight: 500;
    }

    .toggle-icon {
      color: rgba(255, 255, 255, 0.5);
      font-size: 12px;
    }
  }

  .tips-content {
    padding: 16px;
    max-height: 320px;
    overflow-y: auto;

    .tip-item {
      padding: 12px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      margin-bottom: 12px;

      &:last-child {
        margin-bottom: 0;
      }

      h4 {
        color: #a5b4fc;
        font-size: 14px;
        margin-bottom: 8px;
      }

      p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 13px;
        line-height: 1.6;
        margin: 0;
      }
    }

    .empty-tips {
      text-align: center;
      color: rgba(255, 255, 255, 0.5);
      padding: 20px;
    }
  }
}
</style>
