import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/minimal',
      name: 'Minimal',
      component: () => import('@/views/Minimal.vue')
    },
    {
      path: '/templates',
      name: 'Templates',
      component: () => import('@/views/Templates.vue')
    },
    {
      path: '/complex',
      name: 'Complex',
      component: () => import('@/views/Complex.vue')
    }
  ]
})

export default router
