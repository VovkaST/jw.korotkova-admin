<script setup lang="ts">
import { computed } from 'vue';
import Socials from './Socials.component.vue';

const baseCopyrightYear = 2025;

const copyrightPeriod = computed<string>(() => {
  const currentYear = new Date().getFullYear();
  if (currentYear === baseCopyrightYear) {
    return baseCopyrightYear;
  }
  return `${baseCopyrightYear} - ${currentYear}`;
});
</script>

<template>
  <footer class="d-flex flex-column align-items-center">
    <Socials class="d-flex flex-row justify-content-center align-items-center" />
    <ul class="requisites d-flex justify-content-center">
      <li class="requisites__item">Самозанятая Короткова Н.Д.</li>
      <li class="requisites__item">г. Москва</li>
      <li class="requisites__item">ИНН 772775846428</li>
    </ul>
    <span>
      Разработка:
      <a href="https://t.me/KorotkoVladimir" target="_blank" class="author">@KorotkoVladimir</a>
    </span>
    <span>&copy; {{ copyrightPeriod }}. Все права защищены</span>
  </footer>
</template>

<style scoped lang="scss">
footer {
  border-top: 1px solid #939393;
  margin-top: 3rem;
  padding-top: 3rem;
  padding-bottom: 3rem;

  .requisites {
    padding: 0;
    margin: 2rem 0;
    list-style: none;
    gap: 3rem;
  }

  .author {
    &:hover {
      font-weight: 300;
    }
  }
}
@media (max-width: 1024px) {
  footer {
    margin-top: 0;
    padding: 1.5rem 0 0.5rem;

    .requisites {
      margin: 1rem 0;
    }
  }
}
</style>
