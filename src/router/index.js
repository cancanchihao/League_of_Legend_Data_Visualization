import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/App.vue'; // 假设你的首页是 Home.vue

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'LOL比赛数据平台' }
  },
  // 其他路由
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 使用路由导航守卫来动态设置标题
router.afterEach((to) => {
  document.title = to.meta.title || '默认标题';
});

export default router;
