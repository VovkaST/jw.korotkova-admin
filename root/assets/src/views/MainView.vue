<script setup lang="ts">
import WelcomeSection from '@/components/welcome/WelcomeSection.component.vue';
</script>

<template>
  <div class="welcome-screen d-flex flex-column justify-content-center gap-3">
    <h1 class="welcome-screen__header text-center">Добро пожаловать</h1>
    <WelcomeSection>
      <template #title><b>J</b>e<b>w</b>elries.Korotkova</template>
      <template #image>
        <img src="/welcome/jw.korotkova-icon.png" alt="jw.korotkova-icon" />
      </template>
      <template #description>Мастерская живых украшений</template>
    </WelcomeSection>
    <WelcomeSection>
      <template #title><b>J</b>ust<b>W</b>onder.Korotkova</template>
      <template #image>
        <img src="/welcome/jw.korotkova-icon.png" alt="jw.korotkova-icon" />
      </template>
      <template #description>Ответы на вопросы и путь в новую жизнь</template>
    </WelcomeSection>
    <div class="welcome-screen__sign">
      <span>Ваш мастер Наталья Короткова</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.welcome-screen {
  margin: 0 auto;
  height: 100vh;
  max-width: 640px;

  &__header {
    font-weight: 200;
    font-size: 2.3rem;
  }

  .welcome-section__image {
    img {
      height: 100%;
      opacity: 50%;
    }
  }

  &__sign {
    font-size: 1.5rem;
    text-align: right;
  }
}
</style>
