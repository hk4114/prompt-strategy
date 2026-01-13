<template>
  <div class="home-page">
    <!-- 上部交互区 -->
    <div class="decision-section card">
      <h2 class="section-title">任务诊断决策树</h2>
      <p class="section-desc">选择你的任务类型，快速开始</p>
      <div class="button-group">
        <el-button type="primary" size="large" @click="router.push('/minimal')">
          简单任务
        </el-button>
        <el-button type="success" size="large" @click="router.push('/complex')">
          复杂任务
        </el-button>
        <el-button type="warning" size="large" @click="scrollToSection('knowledge')">
          智能体
        </el-button>
      </div>
    </div>

    <!-- 下部分导航 - 产品分类 -->
    <div class="categories-section">
      <div
        v-for="category in categories"
        :key="category.id"
        :id="category.id"
        class="category-card card"
      >
        <h3 class="category-title">
          <span class="category-icon">{{ category.icon }}</span>
          {{ category.name }}
        </h3>
        <div class="products-grid">
          <div
            v-for="product in category.products"
            :key="product.name"
            class="product-item"
          >
            <div class="product-header">
              <a :href="product.url" target="_blank" class="product-name">
                {{ product.name }}
              </a>
              <span class="product-price">{{ product.price }}</span>
            </div>
            <p class="product-reason">{{ product.recommendReason }}</p>
            <div class="product-tags">
              <el-tag
                v-for="tag in product.tags"
                :key="tag"
                size="small"
                type="info"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories } from '@/api'

const router = useRouter()

interface Product {
  name: string
  url: string
  recommendReason: string
  price: string
  tags: string[]
}

interface Category {
  id: string
  name: string
  icon: string
  products: Product[]
}

const categories = ref<Category[]>([])

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(async () => {
  try {
    const { data } = await getCategories()
    categories.value = data.categories
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
})
</script>

<style lang="less" scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.decision-section {
  text-align: center;
  margin-bottom: 30px;

  .section-desc {
    color: #909399;
    margin-bottom: 20px;
  }

  .button-group {
    display: flex;
    justify-content: center;
    gap: 20px;

    .el-button {
      min-width: 150px;
    }
  }
}

.categories-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.category-card {
  .category-title {
    font-size: 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;

    .category-icon {
      font-size: 24px;
    }
  }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.product-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .product-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .product-name {
    font-size: 16px;
    font-weight: 600;
    color: #409eff;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  .product-price {
    font-size: 12px;
    color: #67c23a;
    background: #f0f9eb;
    padding: 2px 8px;
    border-radius: 4px;
  }

  .product-reason {
    font-size: 14px;
    color: #606266;
    margin-bottom: 12px;
    line-height: 1.5;
  }

  .product-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
}
</style>
