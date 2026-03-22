<script setup lang="ts">
import { Motion } from "@motionone/vue";
import { Brain, HeartHandshake, Shield, Sprout } from "lucide-vue-next";

const aboutItems = [
  {
    icon: HeartHandshake,
    title: "Бережное отношение",
    desc: "уважение к вашему личному опыту",
  },
  {
    icon: Sprout,
    title: "Раскрытие ресурсов",
    desc: "активизация внутренних сил и возможностей",
  },
  {
    icon: Shield,
    title: "Безопасное пространство",
    desc: "атмосфера доверия и конфиденциальности",
  },
  {
    icon: Brain,
    title: "Осознанный выбор",
    desc: "поддержка в принятии решений",
  },
] as const;
</script>

<template>
  <section id="about" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">
        Принципы психологической работы
      </h2>
      <div class="max-w-3xl mx-auto text-center mb-16">
        <p class="text-xl md:text-2xl leading-relaxed text-brand-muted">
          Психологическая поддержка помогает проработать глубинные причины
          проблем: непрожитые эмоции, травмы, повторяющиеся жизненные сценарии.
          Результат ощущается уже после первых сессий.
        </p>
      </div>

      <div
        class="grid grid-cols-2 gap-6 md:gap-8"
        :class="`lg:grid-cols-${aboutItems.length}`"
      >
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
