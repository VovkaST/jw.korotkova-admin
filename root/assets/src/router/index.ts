import { NotFound } from '@/components';
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
      name: 'NotFound',
      component: NotFound,
      meta: {
        requiresAuth: false,
        noindex: true,
      }
    }
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
  if (to.name === 'NotFound') {
    document.title = '404 - Страница не найдена'
  }
  next()
})

export default router;
