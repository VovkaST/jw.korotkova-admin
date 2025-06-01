<script setup lang="ts">
export interface MenuItem {
  title: string;
  onClick: void;
}

defineProps<{
  title: string;
  items: Array<MenuItem>;
}>();
</script>

<template>
  <span class="menu-title">{{ title }}</span>
  <nav>
    <ul class="nav-menu d-flex flex-row justify-content-between align-items-center">
      <li class="nav-menu__item" v-for="item in items">
        <a @click.prevent="item.onClick" href="#">{{ item.title }}</a>
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
