import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'event',
      component: () => import('../views/EventView.vue')
    },
    {
      path: '/rank',
      name: 'rank',
      component: () => import('../views/RankView.vue')
    }
  ]
})

export default router
