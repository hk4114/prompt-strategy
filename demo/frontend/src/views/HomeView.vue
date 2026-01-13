<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="page-container">
        <h1 class="hero-title">任务诊断决策树</h1>
        <p class="hero-subtitle">帮助你选择合适的提示词生成方式</p>

        <div class="decision-buttons">
          <el-button
            type="primary"
            size="large"
            @click="$router.push('/minimal-formula')"
          >
            简单任务<br />
            <small>快速生成简洁提示词</small>
          </el-button>

          <el-button
            type="success"
            size="large"
            @click="$router.push('/complex-prompt')"
          >
            复杂任务<br />
            <small>使用8步法深度生成</small>
          </el-button>

          <el-button
            type="warning"
            size="large"
            @click="scrollToAgent"
          >
            智能体<br />
            <small>查看AI工具推荐</small>
          </el-button>
        </div>
      </div>
    </section>

    <!-- AI Tools Navigation -->
    <section class="tools-section" ref="agentSection">
      <div class="page-container">
        <h2 class="section-title">🤖 效率与知识库</h2>

        <el-tabs v-model="activeCategory" class="category-tabs">
          <el-tab-pane
            v-for="category in categories"
            :key="category.category_key"
            :label="`${category.icon} ${category.name}`"
            :name="category.category_key"
          >
            <div class="products-grid">
              <el-card
                v-for="product in category.products"
                :key="product.name"
                class="product-card"
                shadow="hover"
              >
                <div class="product-header">
                  <h3 class="product-name">{{ product.name }}</h3>
                  <div class="product-tags">
                    <el-tag
                      v-for="tag in product.tags.slice(0, 3)"
                      :key="tag"
                      size="small"
                      type="info"
                    >
                      {{ tag }}
                    </el-tag>
                  </div>
                </div>

                <p class="product-reason">{{ product.recommendReason }}</p>

                <div class="product-price">{{ product.price }}</div>

                <div class="product-actions">
                  <el-button
                    type="primary"
                    link
                    @click="openProduct(product.url)"
                  >
                    访问网站
                  </el-button>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getCategories } from '@/api'

interface Product {
  id: number
  name: string
  url: string
  recommendReason: string
  price: string
  tags: string[]
}

interface Category {
  id: number
  category_key: string
  name: string
  icon: string
  products: Product[]
}

const categories = ref<Category[]>([])
const activeCategory = ref('knowledge')
const agentSection = ref<HTMLElement>()

onMounted(async () => {
  try {
    const data = await getCategories()
    categories.value = data.categories
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  }
})

function scrollToAgent() {
  agentSection.value?.scrollIntoView({ behavior: 'smooth' })
}

function openProduct(url: string) {
  window.open(url, '_blank')
}
</script>

<style scoped lang="less">
.hero-section {
  padding: 80px 0;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;

  .hero-title {
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 16px;
  }

  .hero-subtitle {
    font-size: 20px;
    opacity: 0.9;
    margin-bottom: 40px;
  }

  .decision-buttons {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;

    .el-button {
      height: auto;
      padding: 20px 32px;
      font-size: 18px;

      small {
        display: block;
        font-size: 14px;
        opacity: 0.9;
        margin-top: 4px;
      }
    }
  }
}

.tools-section {
  padding: 60px 0;
}

.section-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 24px;
  text-align: center;
}

.category-tabs {
  :deep(.el-tabs__item) {
    font-size: 16px;
    padding: 0 24px;
  }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.product-card {
  height: 100%;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
  }

  :deep(.el-card__body) {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 20px;
  }
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;

  .product-name {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    margin: 0;
  }

  .product-tags {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
  }
}

.product-reason {
  color: #606266;
  line-height: 1.6;
  flex: 1;
  margin: 12px 0;
}

.product-price {
  font-size: 14px;
  color: #909399;
  margin-bottom: 12px;
}

.product-actions {
  margin-top: auto;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 0;

    .hero-title {
      font-size: 32px;
    }

    .decision-buttons {
      flex-direction: column;
      align-items: center;
    }
  }

  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<style lang="less">
body {
  margin: 0;
  padding: 0;
}
</style>
