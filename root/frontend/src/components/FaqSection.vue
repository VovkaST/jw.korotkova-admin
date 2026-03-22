<script setup lang="ts">
import { ChevronDown } from "lucide-vue-next";
import { ref } from "vue";

const emit = defineEmits<{ contact: [] }>();

const faqs = [
  {
    q: "Подходит ли метод для детей?",
    a: "Метод «Терапия Души» ориентирован на взрослых, так как требует осознанной работы с эмоциями. Однако проработка родителей часто положительно сказывается на состоянии детей.",
  },
  {
    q: "Сколько нужно времени для результата?",
    a: "Первые изменения вы почувствуете уже после 1-2 сессий. Для устойчивого результата по глубоким запросам обычно требуется от 4 до 8 встреч.",
  },
  {
    q: "Можно ли совмещать с другой терапией?",
    a: "Да, метод отлично дополняет классическую психотерапию, ускоряя процесс за счет работы с подсознательными сценариями.",
  },
] as const;

const activeAccordion = ref<number | null>(null);

const toggleAccordion = (index: number) => {
  activeAccordion.value = activeAccordion.value === index ? null : index;
};
</script>

<template>
  <section id="faq" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">
        Часто задаваемые вопросы
      </h2>
      <div class="max-w-3xl mx-auto">
        <div
          v-for="(item, i) in faqs"
          :key="i"
          class="border-b border-black/10 last:border-0"
        >
          <button
            type="button"
            class="w-full py-6 flex items-center justify-between text-left hover:text-brand-accent transition-colors"
            @click="toggleAccordion(i)"
          >
            <span class="text-lg font-medium pr-8">{{ item.q }}</span>
            <ChevronDown
              class="w-5 h-5 transition-transform duration-300"
              :class="activeAccordion === i ? 'rotate-180' : ''"
            />
          </button>
          <transition
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="max-h-0 opacity-0"
            enter-to-class="max-h-[500px] opacity-100"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="max-h-[500px] opacity-100"
            leave-to-class="max-h-0 opacity-0"
          >
            <div v-if="activeAccordion === i" class="overflow-hidden">
              <p class="pb-6 text-brand-muted leading-relaxed">
                {{ item.a }}
              </p>
            </div>
          </transition>
        </div>
        <div class="mt-12 text-center">
          <button
            type="button"
            class="bg-transparent text-brand-accent px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent/10 transition-all"
            @click="emit('contact')"
          >
            Задать свой вопрос
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
