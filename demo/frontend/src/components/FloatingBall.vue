<template>
  <div>
    <div
      ref="ballRef"
      class="floating-ball"
      :style="{ left: position.x + 'px', top: position.y + 'px' }"
      @mousedown="startDrag"
      @click="handleClick"
    >
      MomTest
    </div>

    <el-dialog
      v-model="dialogVisible"
      title="Mom Test"
      width="90vw"
      append-to-body
    >
      <div class="image-container">
        <img src="@/assets/Taming_AI_Through_Structure-图片-6.jpg" alt="Mom Test" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'

const dialogVisible = ref(false)
const ballRef = ref<HTMLElement | null>(null)
const isDragging = ref(false)
const position = reactive({ x: window.innerWidth - 80, y: window.innerHeight - 150 })
const dragOffset = reactive({ x: 0, y: 0 })

const startDrag = (e: MouseEvent) => {
  isDragging.value = false
  dragOffset.x = e.clientX - position.x
  dragOffset.y = e.clientY - position.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e: MouseEvent) => {
  isDragging.value = true
  let newX = e.clientX - dragOffset.x
  let newY = e.clientY - dragOffset.y
  
  // 边界检查
  const maxX = window.innerWidth - 50
  const maxY = window.innerHeight - 50
  
  newX = Math.max(0, Math.min(newX, maxX))
  newY = Math.max(0, Math.min(newY, maxY))
  
  position.x = newX
  position.y = newY
}

const stopDrag = () => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

const handleClick = () => {
  dialogVisible.value = !dialogVisible.value
}

// 窗口大小改变时重置位置
const handleResize = () => {
  position.x = Math.min(position.x, window.innerWidth - 50)
  position.y = Math.min(position.y, window.innerHeight - 50)
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="less">
.floating-ball {
  position: fixed;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--el-color-primary);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: grab;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s, box-shadow 0.2s;
  user-select: none;

  &:active {
    cursor: grabbing;
    transform: scale(0.95);
  }

  &:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }

  .el-icon {
    font-size: 24px;
  }
}

.image-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  
  img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
}
</style>