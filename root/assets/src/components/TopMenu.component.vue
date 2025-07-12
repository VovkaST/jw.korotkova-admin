<script setup lang="ts">
import { computed, ref } from 'vue';

export interface MenuItem {
  title: string;
  onClick: () => void;
}

defineProps<{
  title: string;
  items: Array<MenuItem>;
}>();

const titleEl = ref();
const titleWidth = computed(() => {
  return titleEl.value ? `${titleEl.value.offsetWidth}px` : null;
});
</script>

<template>
  <div class="top-menu-container d-flex flex-row nowrap justify-content-between align-items-center">
    <span class="menu-title" ref="titleEl">{{ title }}</span>
    <nav>
      <ul class="nav-menu m-0 p-0 d-flex flex-row">
        <li class="nav-menu__item" v-for="item in items">
          <a @click.prevent="item.onClick" href="#">{{ item.title }}</a>
        </li>
      </ul>
    </nav>
    <div class="user-section" :style="{ width: titleWidth }"></div>
  </div>
</template>

<style scoped lang="scss">
$textColor: #6a6a6acc;
$borderColor: #939393;

.menu-title {
  font-family: var(--font-family-calligraphy);
  font-size: 2rem;
}
.nav-menu {
  list-style: none;
  gap: 3rem;

  &__item {
    & a {
      display: block;
      font-weight: 400;
      padding: 1rem 3rem;
      transition:
        color 0.3s,
        border-bottom-color 0.3s;
      color: $textColor;
      border-bottom: 1px solid transparent;

      &:hover {
        color: hsl(from $textColor h s calc(l - 100));
        border-bottom: 1px solid $borderColor;
      }
    }
  }
}
</style>
