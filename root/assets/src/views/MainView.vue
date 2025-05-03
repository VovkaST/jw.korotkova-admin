<script setup lang="ts">
import WelcomeSection from '@/components/welcome/WelcomeSection.component.vue';

import { InstagramIcon, VKIcon, TelegramIcon, WhatsAppIcon } from '@/components/icons/socials';
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
    <div class="socials d-flex flex-row justify-content-center align-items-center mt-5">
      <a href="https://www.instagram.com/jw.korotkova" target="_blank" class="social-link">
        <InstagramIcon class="social-icon instagram" />
      </a>
      <a href="https://vk.com/id2518849" target="_blank" class="social-link">
        <VKIcon class="social-icon vk" />
      </a>
      <a href="https://t.me/JW_Korotkova" target="_blank" class="social-link">
        <TelegramIcon class="social-icon telegram" />
      </a>
      <a href="https://wa.me/79686281681" target="_blank" class="social-link">
        <WhatsAppIcon class="social-icon whatsapp" />
      </a>
    </div>
  </div>
</template>

<style scoped lang="scss">
$hoverTransition: 0.3s ease-in-out;

.socials {
  height: 45px;

  .social-link {
    margin: 1rem;
  }

  .social-icon {
    height: 35px;
    fill: #939393;
    transition:
      fill $hoverTransition,
      height $hoverTransition;

    &:hover {
      height: 45px;
    }

    &.instagram {
      &:hover {
        fill: #000100;
      }
    }

    &.vk {
      &:hover {
        fill: #0077ff;
      }
    }

    &.telegram {
      &:hover {
        fill: #2aabee;
      }
    }

    &.whatsapp {
      &:hover {
        fill: #25d366;
      }
    }
  }
}

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
