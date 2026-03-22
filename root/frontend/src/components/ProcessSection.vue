<script setup lang="ts">
import { Sparkles } from "lucide-vue-next";

const steps = [
  {
    num: "1",
    title: "Запрос",
    desc: "Формулирование вашего запроса и готовность идти в глубину",
  },
  {
    num: "2",
    title: "Онлайн-сессия",
    desc: "Глубокий разбор и проработка, перезапись нейронных связей",
  },
  {
    num: "3",
    title: "Результат",
    desc: "Ваше новое состояние и высвобожденная энергия на новые действия",
  },
] as const;
</script>

<template>
  <section id="process" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">Этапы работы</h2>
      <div class="relative max-w-4xl mx-auto">
        <div class="space-y-12 relative">
          <div
            class="absolute h-full left-8 md:left-1/2 top-0 bottom-32 w-px bg-black/10 -translate-x-1/2 hidden md:block"
          />
          <div
            v-for="(step, i) in steps"
            :key="i"
            class="flex items-center gap-8"
            :class="i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'"
          >
            <div class="flex-1 hidden md:block" />
            <div
              class="w-16 h-16 rounded-full bg-brand-accent text-white flex items-center justify-center text-2xl font-bold z-10 shrink-0 shadow-lg"
            >
              {{ step.num }}
            </div>
            <div class="flex-1 bg-brand-beige p-8 rounded-2xl">
              <h3 class="text-xl mb-2">{{ step.title }}</h3>
              <p class="text-brand-muted">{{ step.desc }}</p>
            </div>
          </div>
        </div>

        <div class="mt-16 text-center">
          <div
            class="inline-flex items-center gap-4 px-6 py-3 bg-brand-accent/5 rounded-full text-brand-accent font-medium"
          >
            <Sparkles class="w-5 h-5" /> Онлайн
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
