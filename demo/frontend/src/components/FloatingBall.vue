<template>
  <div>
    <div
      ref="ballRef"
      class="floating-ball"
      :class="{ 'is-dragging': isDragging }"
      :style="{ left: position.x + 'px', top: position.y + 'px' }"
      @mousedown="startDrag"
      @click="handleClick"
    >
      <div class="ball-content">
        <el-icon class="ball-icon"><MagicStick /></el-icon>
        <div class="ripple"></div>
      </div>
    </div>

    <el-dialog
      v-model="dialogVisible"
      title="Mom Test"
      width="800px"
      append-to-body
      class="custom-dialog"
    >
      <div class="image-container">
        <img src="@/assets/Taming_AI_Through_Structure-图片-6.jpg" alt="Mom Test" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { MagicStick } from '@element-plus/icons-vue'

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
  const maxX = window.innerWidth - 60
  const maxY = window.innerHeight - 60
  
  newX = Math.max(0, Math.min(newX, maxX))
  newY = Math.max(0, Math.min(newY, maxY))
  
  position.x = newX
  position.y = newY
}

const stopDrag = () => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  
  // 拖拽结束后的吸附效果（可选）
  // snapToEdge()
}

const handleClick = () => {
  if (!isDragging.value) {
    dialogVisible.value = true
  }
}

// 窗口大小改变时重置位置
const handleResize = () => {
  position.x = Math.min(position.x, window.innerWidth - 60)
  position.y = Math.min(position.y, window.innerHeight - 60)
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
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409eff, #36cfc9);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: grab;
  z-index: 9999;
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.4);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  user-select: none;
  overflow: hidden;

  &.is-dragging {
    cursor: grabbing;
    transform: scale(1.1);
    box-shadow: 0 12px 30px rgba(64, 158, 255, 0.5);
  }

  &:hover:not(.is-dragging) {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 10px 25px rgba(64, 158, 255, 0.5);

    .ball-icon {
      transform: scale(1.2);
    }
  }

  .ball-content {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .ball-icon {
    font-size: 28px;
    transition: transform 0.3s ease;
    z-index: 2;
  }

  .ripple {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
    transform: translate(-50%, -50%) scale(0);
    animation: ripple-effect 3s infinite;
    pointer-events: none;
  }
}

@keyframes ripple-effect {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.8;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

.image-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  
  img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    
    &:hover {
      transform: scale(1.02);
    }
  }
}

:deep(.custom-dialog) {
  border-radius: 12px;
  overflow: hidden;
  
  .el-dialog__header {
    margin: 0;
    padding: 20px;
    border-bottom: 1px solid #eee;
  }
  
  .el-dialog__body {
    padding: 0;
  }
}
</style>