<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <el-header class="app-header">
      <div class="logo" @click="router.push('/')">
        <span class="logo-icon">✨</span>
        <span class="logo-text">提示词生成系统</span>
      </div>
      <el-menu
        mode="horizontal"
        :default-active="route.path"
        router
        class="nav-menu"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/minimal">最小公式</el-menu-item>
        <el-menu-item index="/templates">提示词模板</el-menu-item>
        <el-menu-item index="/complex">复杂提示词</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="app-main">
      <router-view />
    </el-main>

    <!-- 提示词技巧浮窗 -->
    <PromptTips />

    <!-- 复盘检查弹窗 -->
    <ReviewDialog />
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import PromptTips from './components/PromptTips.vue'
import ReviewDialog from './components/ReviewDialog.vue'

const route = useRoute()
const router = useRouter()
</script>

<style lang="less">
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.app-header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .logo {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin-right: 40px;

    .logo-icon {
      font-size: 24px;
      margin-right: 8px;
    }

    .logo-text {
      font-size: 18px;
      font-weight: 600;
      color: #fff;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .nav-menu {
    flex: 1;
    background: transparent;
    border: none;

    .el-menu-item {
      color: rgba(255, 255, 255, 0.7);
      border-bottom: none;

      &:hover {
        color: #fff;
        background: rgba(255, 255, 255, 0.1);
      }

      &.is-active {
        color: #667eea;
        border-bottom: 2px solid #667eea;
      }
    }
  }
}

.app-main {
  padding: 24px;
  min-height: calc(100vh - 60px);
}
</style>
