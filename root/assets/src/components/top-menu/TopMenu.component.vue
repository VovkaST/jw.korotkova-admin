<script setup lang="ts">
import { TopMenuItem } from './';
defineProps<{
  title: string;
}>();
</script>

<template>
  <span class="menu-title">{{ title }}</span>
  <nav>
    <ul class="nav-menu d-flex flex-row justify-content-between align-items-center">
      <li class="nav-menu__item">
        <top-menu-item to="services"> Услуги </top-menu-item>
      </li>
      <li>
        <top-menu-item to="reviews"> Отзывы </top-menu-item>
      </li>
      <li>
        <top-menu-item to="about"> Обо мне </top-menu-item>
      </li>
      <li>
        <top-menu-item to="contacts"> Контакты </top-menu-item>
      </li>
    </ul>
  </nav>
</template>

<style scoped lang="scss">
.menu-title {
  font-family: var(--font-family-calligraphy);
  font-size: 2rem;
}
.nav-menu {
  list-style: none;

  &__item {
    display: block;
    border: 1px solid red;
  }
}
</style>
