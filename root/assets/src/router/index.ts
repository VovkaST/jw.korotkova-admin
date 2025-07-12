import { createRouter, createWebHistory } from 'vue-router';
import JewelleriesMainView from '@/views/jewelleries/MainView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: JewelleriesMainView,
    },
  ],
});

export default router;
