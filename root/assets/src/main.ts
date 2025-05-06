import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

import 'bootstrap/dist/css/bootstrap-reboot.min.css';
import 'bootstrap/dist/css/bootstrap.css';

import './assets/main.scss';

const app = createApp(App);

app.use(createPinia());
app.use(router).use(PrimeVue, {
  theme: {
    preset: Aura,
  },
});

app.mount('#app');
