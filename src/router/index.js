import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/event'  // 默认重定向到 /event
    },
    {
      path: '/event',
      name: 'event',
      component: () => import('../views/EventView.vue'),
      // 子路由跟嵌套路由一样，需要router-view来渲染路由组件，我把playerList放进app.vue了
      // children: [
      //   {
      //     path: '/playerList',
      //     component: () => import('../views/EventChildrenView/PlayerList.vue'),
      //   }

      // ]

    },
    {
      path: '/rank',
      name: 'rank',
      component: () => import('../views/RankView.vue')
    },
    {
      path: '/playerList',
      name: 'playerList',
      component: () => import('../views/EventChildrenView/PlayerList.vue'),
    }
  ]
})

export default router
