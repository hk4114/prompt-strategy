import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/HomeView.vue'),
            meta: { title: '首页' }
        },
        {
            path: '/minimal',
            name: 'minimal',
            component: () => import('@/views/MinimalFormula.vue'),
            meta: { title: '最小公式' }
        },
        {
            path: '/templates',
            name: 'templates',
            component: () => import('@/views/TemplateList.vue'),
            meta: { title: '提示词模板' }
        },
        {
            path: '/complex',
            name: 'complex',
            component: () => import('@/views/ComplexPrompt.vue'),
            meta: { title: '复杂提示词' }
        }
    ]
})

router.beforeEach((to) => {
    document.title = `${to.meta.title} - 提示词生成系统`
})

export default router
