<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <el-header class="app-header">
        <div class="logo">提示词生成系统</div>
        <el-menu
          :default-active="route.path"
          mode="horizontal"
          :router="true"
          class="nav-menu"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/minimal">最小公式</el-menu-item>
          <el-menu-item index="/templates">提示词模版</el-menu-item>
          <el-menu-item index="/complex">复杂提示词</el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
      <FloatingBall />
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import FloatingBall from './components/FloatingBall.vue'

const route = useRoute()
</script>

<style lang="less">
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  align-items: center;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 20px;

  .logo {
    font-size: 20px;
    font-weight: bold;
    color: #409eff;
    margin-right: 40px;
  }

  .nav-menu {
    flex: 1;
    border-bottom: none;
  }
}

.app-main {
  flex: 1;
  background: #f5f7fa;
  padding: 20px;
}
</style>
