<script setup lang="ts"></script>

<template>
  <div class="minimal-not-found">
    <div class="content">
      <div class="title">JW.Korotkova</div>
      <div class="code">404</div>
      <h1>Страница не найдена</h1>
      <p>Запрашиваемая страница не существует.</p>
      <div class="link">
        <router-link :to="{ name: 'home' }">← Вернуться на главную</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.minimal-not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}

.content {
  .title {
    margin-bottom: 2rem;
    font-family: var(--font-family-calligraphy);
    font-size: 3rem;
  }

  text-align: center;
  padding: 2rem;
}

.code {
  font-size: 8rem;
  font-weight: 100;
  margin: 0;
  line-height: 0.8;
}

h1 {
  font-size: 1.5rem;
  font-weight: 400;
  margin: 1rem 0;
}

p {
  font-size: 1rem;
  color: #666666;
  margin: 0 0 2rem 0;
  line-height: 1.5;
}

.link a {
  text-decoration: none;
  border-bottom: 1px solid #000000;
  padding-bottom: 2px;
  transition: opacity 0.2s ease;
}

.link a:hover {
  opacity: 0.7;
}

@media (max-width: 480px) {
  .code {
    font-size: 5rem;
  }

  h1 {
    font-size: 1.25rem;
  }
}
</style>
