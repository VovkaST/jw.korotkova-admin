<script setup lang="ts">
import { Motion } from "@motionone/vue";
import { ArrowRight } from "lucide-vue-next";

const emit = defineEmits<{ contact: [] }>();
</script>

<template>
  <section
    class="pt-32 pb-20 px-6 md:px-12 lg:px-24 min-h-[90vh] flex items-center bg-brand-beige"
  >
    <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
      <Motion
        :initial="{ opacity: 0, x: -50 }"
        :animate="{ opacity: 1, x: 0 }"
        :transition="{ duration: 0.8, easing: 'ease-out' }"
      >
        <h1 class="text-4xl md:text-6xl lg:text-7xl leading-[1.1] mb-6">
          Путь к внутренней свободе через
          <span class="text-brand-accent">«Терапию Души»</span>
        </h1>
        <p class="text-lg md:text-xl text-brand-muted mb-10 max-w-lg">
          Освободитесь от&nbsp;барьеров прошлого&nbsp;&mdash; начните жить
          осознанно уже сегодня.
        </p>
        <button
          type="button"
          class="w-full md:w-auto bg-brand-accent text-white px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent-light transition-all flex items-center justify-center gap-2"
          @click="emit('contact')"
        >
          Написать мне <ArrowRight class="w-5 h-5" />
        </button>
      </Motion>

      <Motion
        :initial="{ opacity: 0, scale: 0.9 }"
        :animate="{ opacity: 1, scale: 1 }"
        :transition="{ duration: 0.8, delay: 0.2, easing: 'ease-out' }"
        class="relative"
      >
        <div class="aspect-[4/5] rounded-[2rem] overflow-hidden shadow-2xl">
          <img
            src="/BusinessCardPhoto.jpg"
            alt="Наталья Короткова"
            class="w-full h-full object-cover object-[calc(50%-125px)_center]"
            referrerPolicy="no-referrer"
          />
        </div>
        <div
          class="absolute -bottom-6 -left-6 w-32 h-32 bg-brand-accent/10 rounded-full blur-3xl -z-10"
        />
        <div
          class="absolute -top-6 -right-6 w-48 h-48 bg-brand-accent/5 rounded-full blur-3xl -z-10"
        />
      </Motion>
    </div>
  </section>
</template>
