<template>
  <div class="home-view">
    <!-- 任务诊断决策树 -->
    <section class="decision-section glass-card fade-in-up">
      <h1 class="section-title">
        <span class="highlight">任务诊断</span> 决策树
      </h1>
      <p class="section-desc">选择合适的提示词策略，让 AI 更好地帮助你</p>
      
      <div class="decision-buttons">
        <div class="decision-card" @click="router.push('/minimal')">
          <div class="card-icon">⚡</div>
          <h3>简单任务</h3>
          <p>使用最小公式快速生成</p>
          <span class="card-tag">推荐</span>
        </div>
        
        <div class="decision-card" @click="router.push('/complex')">
          <div class="card-icon">🎯</div>
          <h3>复杂任务</h3>
          <p>8步法深度思考</p>
          <span class="card-tag">进阶</span>
        </div>
        
        <div class="decision-card" @click="scrollToSection('knowledge')">
          <div class="card-icon">🤖</div>
          <h3>智能体</h3>
          <p>自动化工作流</p>
          <span class="card-tag">效率</span>
        </div>
      </div>
    </section>

    <!-- AI 产品导航 -->
    <section class="products-section">
      <h2 class="section-title">
        <span class="highlight">AI 工具</span> 导航
      </h2>
      
      <div class="category-tabs">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="category-tab"
          :class="{ active: activeCategory === cat.id }"
          @click="activeCategory = cat.id"
        >
          <span class="tab-icon">{{ cat.icon }}</span>
          <span class="tab-name">{{ cat.name }}</span>
        </div>
      </div>

      <div class="products-grid" :id="activeCategory">
        <div
          v-for="product in currentProducts"
          :key="product.name"
          class="product-card glass-card fade-in-up"
        >
          <div class="product-header">
            <h3 class="product-name">{{ product.name }}</h3>
            <span class="product-price">{{ product.price }}</span>
          </div>
          <p class="product-reason">{{ product.recommendReason }}</p>
          <div class="tag-list">
            <el-tag v-for="tag in product.tags" :key="tag" size="small">
              {{ tag }}
            </el-tag>
          </div>
          <a :href="product.url" target="_blank" class="product-link gradient-btn">
            访问 →
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories } from '@/api/requests'

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
const activeCategory = ref('chat')

const currentProducts = computed(() => {
  const cat = categories.value.find(c => c.id === activeCategory.value)
  return cat?.products || []
})

const scrollToSection = (sectionId: string) => {
  activeCategory.value = sectionId
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(async () => {
  try {
    const res = await getCategories() as { categories: Category[] }
    categories.value = res.categories
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
})
</script>

<style lang="less" scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

.decision-section {
  padding: 40px;
  margin-bottom: 40px;
  text-align: center;

  .section-desc {
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 32px;
  }

  .decision-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    
    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }

  .decision-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 32px 24px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;

    &:hover {
      transform: translateY(-4px);
      border-color: #667eea;
      background: rgba(102, 126, 234, 0.1);
    }

    .card-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    h3 {
      font-size: 20px;
      color: #fff;
      margin-bottom: 8px;
    }

    p {
      color: rgba(255, 255, 255, 0.6);
      font-size: 14px;
    }

    .card-tag {
      position: absolute;
      top: 16px;
      right: 16px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      color: #fff;
    }
  }
}

.products-section {
  .category-tabs {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;

    .category-tab {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      cursor: pointer;
      transition: all 0.3s ease;
      color: rgba(255, 255, 255, 0.7);

      &:hover,
      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: transparent;
        color: #fff;
      }

      .tab-icon {
        font-size: 18px;
      }

      .tab-name {
        font-size: 14px;
      }
    }
  }

  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
  }

  .product-card {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;

    .product-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .product-name {
        font-size: 18px;
        color: #fff;
      }

      .product-price {
        font-size: 14px;
        color: #a5b4fc;
        background: rgba(102, 126, 234, 0.2);
        padding: 4px 12px;
        border-radius: 8px;
      }
    }

    .product-reason {
      color: rgba(255, 255, 255, 0.7);
      font-size: 14px;
      line-height: 1.6;
    }

    .product-link {
      text-decoration: none;
      text-align: center;
      margin-top: auto;
    }
  }
}
</style>
