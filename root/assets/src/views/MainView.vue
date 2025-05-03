<script setup lang="ts">
import WelcomeSection from '@/components/welcome/WelcomeSection.component.vue';
import Socials from '@/components/Socials.vue';
</script>

<template>
  <div class="welcome-screen d-flex flex-column justify-content-center gap-3">
    <h1 class="welcome-screen__header text-center mb-4">Добро пожаловать!</h1>
    <router-link :to="{ name: 'jewelries' }">
      <WelcomeSection>
        <template #title><b>J</b>e<b>w</b>elries.Korotkova</template>
        <template #image>
          <img class="section-image" src="/welcome/jw.korotkova-icon.png" alt="jw.korotkova-icon" />
        </template>
        <template #description>Мастерская живых украшений</template>
      </WelcomeSection>
    </router-link>
    <router-link :to="{ name: 'wonder' }">
      <WelcomeSection>
        <template #title><b>J</b>ust<b>W</b>onder.Korotkova</template>
        <template #image>
          <img class="section-image" src="/welcome/jw.korotkova-icon.png" alt="jw.korotkova-icon" />
        </template>
        <template #description>Ответы на вопросы и путь в новую жизнь</template>
      </WelcomeSection>
    </router-link>
    <div class="welcome-screen__sign mt-4">
      <span>Ваш мастер Наталья Короткова</span>
    </div>
    <Socials class="d-flex flex-row justify-content-center align-items-center mt-5" />
  </div>
</template>

<style scoped lang="scss">
$hoverTransition: 0.3s ease-in-out;

.welcome-screen {
  margin: 0 auto;
  height: 100vh;
  max-width: 640px;

  &__header {
    font-weight: 200;
    font-size: 2.3rem;
  }

  .welcome-section {
    cursor: pointer;
    transition:
      border-color $hoverTransition,
      box-shadow $hoverTransition;

    &:hover {
      border-color: #3b3b3b;
      box-shadow: #7c7c7c 0 0 10px;

      .section-image {
        opacity: unset;
      }
    }

    .section-image {
      height: 100%;
      opacity: 50%;
      transition: opacity $hoverTransition;
    }
  }

  &__sign {
    font-size: 1.5rem;
    text-align: right;
  }
}
</style>
