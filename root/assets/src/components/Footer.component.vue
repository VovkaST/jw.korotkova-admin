<script setup lang="ts">
import Socials from './Socials.component.vue';

const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="mt-5 pt-5 pb-5 d-flex flex-column align-items-center">
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
    <span>&copy; {{ currentYear }}</span>
  </footer>
</template>

<style scoped lang="scss">
footer {
  border-top: 1px solid #939393;

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
</style>
