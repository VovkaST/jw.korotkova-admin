<script setup lang="ts">
import { Motion } from "@motionone/vue";
import { Sparkles, Target, UserCircle2, Zap } from "lucide-vue-next";

const aboutItems = [
  { icon: Zap, title: "Быстрый результат", desc: "изменения после 1–2 сессий" },
  { icon: Target, title: "Глубокая проработка", desc: "работа с причинами" },
  {
    icon: UserCircle2,
    title: "Индивидуальный подход",
    desc: "адаптация под клиента",
  },
  {
    icon: Sparkles,
    title: "Самопомощь",
    desc: "обучение самостоятельной работе",
  },
] as const;
</script>

<template>
  <section id="about" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">
        Что такое «Терапия Души»?
      </h2>
      <div class="max-w-3xl mx-auto text-center mb-16">
        <p class="text-xl md:text-2xl leading-relaxed text-brand-muted">
          &laquo;Терапия Души&raquo;&nbsp;&mdash; авторский метод психолога
          Евгения Теребенина. Он&nbsp;помогает быстро проработать глубинные
          причины проблем: непрожитые эмоции, травмы, родовые сценарии.
          Результат ощущается уже после первых сессий.
        </p>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
        <Motion
          v-for="(item, i) in aboutItems"
          :key="i"
          :initial="{ opacity: 0, y: 20 }"
          :animate="{ opacity: 1, y: 0 }"
          :transition="{ duration: 0.5, delay: i * 0.1 }"
          class="text-center p-6"
        >
          <div
            class="w-16 h-16 bg-brand-beige rounded-2xl flex items-center justify-center mx-auto mb-6 text-brand-accent"
          >
            <component :is="item.icon" class="w-8 h-8" />
          </div>
          <h3 class="text-lg mb-2">{{ item.title }}</h3>
          <p class="text-sm text-brand-muted">{{ item.desc }}</p>
        </Motion>
      </div>
    </div>
  </section>
</template>
