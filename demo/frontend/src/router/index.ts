import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MinimalFormula from '@/views/MinimalFormula.vue'
import TemplateList from '@/views/TemplateList.vue'
import ComplexPrompt from '@/views/ComplexPrompt.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/minimal-formula',
      name: 'minimal-formula',
      component: MinimalFormula
    },
    {
      path: '/templates',
      name: 'templates',
      component: TemplateList
    },
    {
      path: '/complex-prompt',
      name: 'complex-prompt',
      component: ComplexPrompt
    }
  ]
})

export default router
