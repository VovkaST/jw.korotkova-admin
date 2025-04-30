import { createRouter, createWebHistory } from 'vue-router';
import MainView from '@/views/MainView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainView,
    },
    {
      path: '/jewelries',
      name: 'jewelries',
      component: () => import('@/views/jewelries/MainView.vue'),
    },
    {
      path: '/wonder',
      name: 'wonder',
      component: () => import('@/views/wonder/MainView.vue'),
    },
  ],
});

export default router;
