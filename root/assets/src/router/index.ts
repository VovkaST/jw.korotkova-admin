import { NotFound } from '@/components';
import { Config } from '@/config';
import JewelleriesMainView from '@/views/jewelleries/MainView.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: JewelleriesMainView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notFound',
      component: NotFound,
      meta: {
        requiresAuth: false,
        noindex: true,
        title: '404 - Страница не найдена',
      },
    },
  ],
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    }
  },
});

router.beforeEach((to, from, next) => {
  document.title = to.meta?.title as string ?? Config.siteTitle;
  next();
});

export default router;
