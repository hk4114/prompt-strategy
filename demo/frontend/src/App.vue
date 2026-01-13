<template>
  <el-config-provider :locale="zhCn">
    <div id="app">
      <el-container>
        <el-header>
          <nav class="nav-header">
            <h1 class="logo">提示词生成系统</h1>
            <el-menu
              :default-active="activeMenu"
              mode="horizontal"
              router
              class="nav-menu"
            >
              <el-menu-item index="/">首页</el-menu-item>
              <el-menu-item index="/minimal-formula">最小公式</el-menu-item>
              <el-menu-item index="/templates">提示词模版</el-menu-item>
              <el-menu-item index="/complex-prompt">复杂提示词</el-menu-item>
            </el-menu>
          </nav>
        </el-header>

        <el-main>
          <router-view />
        </el-main>
      </el-container>

      <!-- Review Dialog -->
      <ReviewDialog
        v-model="reviewDialogVisible"
        :usage-log-id="currentUsageLogId"
      />

      <!-- Prompt Tips Panel -->
      <PromptTips />
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import ReviewDialog from "./components/ReviewDialog.vue";
import PromptTips from "./components/PromptTips.vue";
import { usePromptStore } from "./stores";

const route = useRoute();
const promptStore = usePromptStore();

const activeMenu = computed(() => route.path);
const reviewDialogVisible = ref(false);
const currentUsageLogId = ref<number | null>(null);

// Listen for prompt copy event
onMounted(() => {
  window.addEventListener("prompt-copied", (event: any) => {
    currentUsageLogId.value = event.detail?.usageLogId || null;
    reviewDialogVisible.value = true;
  });
});

// Provide global functions
window.showReviewDialog = (usageLogId?: number) => {
  currentUsageLogId.value = usageLogId || null;
  reviewDialogVisible.value = true;
};
</script>

<style lang="less">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0;
  height: 60px !important;
}

.nav-header {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;

  .logo {
    font-size: 20px;
    font-weight: 600;
    color: #409eff;
    margin-right: 40px;
    margin: 0 40px 0 0;
  }

  .nav-menu {
    flex: 1;
    border-bottom: none;
  }
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
}
</style>
