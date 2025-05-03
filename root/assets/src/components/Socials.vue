<script setup lang="ts">
import { InstagramIcon, TelegramIcon, VKIcon, WhatsAppIcon } from '@/components/icons/socials';
</script>

<template>
  <div class="socials">
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
</style>
