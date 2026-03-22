<script setup lang="ts">
import { useConfig } from "@/composables";
import { Motion } from "@motionone/vue";
import { Clock, Sparkles } from "lucide-vue-next";

const emit = defineEmits<{ contact: [] }>();

const { consultation } = useConfig();

const prices = [
  {
    title: consultation.title,
    time: consultation.duration,
    price: consultation.price,
    desc: consultation.description,
    popular: true,
  },
] as const;
</script>

<template>
  <section id="prices" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">Стоимость услуг</h2>
      <div class="flex justify-center">
        <Motion
          v-for="(item, i) in prices"
          :key="i"
          :initial="{ opacity: 0, y: 30 }"
          :animate="{ opacity: 1, y: 0 }"
          :transition="{ duration: 0.6, delay: i * 0.1 }"
          class="relative p-10 md:p-16 rounded-[3rem] transition-all duration-300 bg-brand-accent text-white shadow-2xl max-w-2xl w-full text-center"
        >
          <h3 class="text-3xl md:text-4xl mb-4 font-display">
            {{ item.title }}
          </h3>
          <p
            class="text-lg mb-8 text-white/80 flex items-center justify-center gap-2"
          >
            <Clock class="w-5 h-5" /> {{ item.time }}
          </p>
          <div class="text-5xl md:text-6xl font-bold mb-8">
            {{ item.price }} ₽
          </div>
          <p class="text-xl mb-12 text-white/90 leading-relaxed">
            {{ item.desc }}
          </p>
          <button
            type="button"
            class="w-full md:w-auto px-12 py-5 rounded-2xl font-bold bg-white text-brand-accent hover:bg-white/90 transition-all duration-300 text-lg shadow-xl"
            @click="emit('contact')"
          >
            Написать мне
          </button>
        </Motion>
      </div>
      <div
        v-if="consultation.specialOffer"
        class="mt-16 p-8 bg-brand-accent/5 rounded-3xl text-center border border-brand-accent/10 max-w-2xl mx-auto"
      >
        <p
          class="text-brand-accent font-semibold text-lg flex items-center justify-center gap-3"
        >
          <Sparkles class="w-6 h-6" />
          Спецпредложение: {{ consultation.specialOffer }}
        </p>
      </div>
    </div>
  </section>
</template>
