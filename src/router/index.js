import { createRouter, createWebHistory } from 'vue-router'
<<<<<<< HEAD
=======
import HomeView from '../views/HomeView.vue'
>>>>>>> bc04a23cb9fa011a1fb26c2cda57e5aad82311b9

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
<<<<<<< HEAD
      name: 'event',
      component: () => import('../views/EventView.vue')
    },
    {
      path: '/rank',
      name: 'rank',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RankView.vue')
=======
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
>>>>>>> bc04a23cb9fa011a1fb26c2cda57e5aad82311b9
    }
  ]
})

export default router
