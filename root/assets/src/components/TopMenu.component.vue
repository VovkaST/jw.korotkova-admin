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
  <nav class="top-menu-container navbar navbar-expand-lg navbar-white bg-white">
    <div class="container-fluid">
      <span class="menu-title navbar-brand" ref="titleEl">{{ title }}</span>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#topMenu"
        aria-controls="topMenu"
        aria-expanded="false"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="topMenu">
        <ul class="nav-menu navbar-nav me-auto m-0 p-0">
          <li class="nav-menu__item" v-for="item in items">
            <a @click.prevent="item.onClick" href="#">{{ item.title }}</a>
          </li>
        </ul>
      </div>
      <div class="user-section" :style="{ width: titleWidth }"></div>
    </div>
  </nav>
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
.user-section {
  display: none;
}

@media (max-width: 992px) {
  // For Bootstrap navbar
  .nav-menu {
    gap: unset;

    &__item a:hover {
      border-bottom: 1px solid transparent;
    }
  }
}
</style>
