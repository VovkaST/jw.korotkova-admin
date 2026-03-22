<script setup lang="ts">
import { Motion } from "@motionone/vue";
import { CheckCircle2 } from "lucide-vue-next";

const emit = defineEmits<{ contact: [] }>();

const requests = [
  "Самообесценивание, ненужность, чувство вины",
  "Сложности в отношениях (семья, дети, работа)",
  "Мысли о разводе, развод, измены",
  "Угнетенное душевное состояние, потеря смысла жизни, обиды",
  "Странные повторяющиеся события в жизни и др.",
  "Состояние тупика, чувство тревожности, недолюбленности",
] as const;
</script>

<template>
  <section id="requests" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">
        Решаем ваши запросы
      </h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Motion
          v-for="(text, i) in requests"
          :key="i"
          :initial="{ opacity: 0, scale: 0.95 }"
          :animate="{ opacity: 1, scale: 1 }"
          :transition="{ duration: 0.4, delay: i * 0.05 }"
          class="p-8 rounded-2xl bg-white border border-black/5 shadow-sm hover:-translate-y-2 transition-all duration-300 flex flex-col items-start gap-4"
        >
          <div
            class="w-12 h-12 bg-brand-accent/5 rounded-xl flex items-center justify-center text-brand-accent"
          >
            <CheckCircle2 class="w-6 h-6" />
          </div>
          <p class="text-lg font-medium leading-snug">{{ text }}</p>
        </Motion>
      </div>
      <div class="mt-16 text-center">
        <button
          type="button"
          class="bg-transparent border-2 border-brand-accent text-brand-accent px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent/5 transition-all"
          @click="emit('contact')"
        >
          Узнать подробнее
        </button>
      </div>
    </div>
  </section>
</template>
