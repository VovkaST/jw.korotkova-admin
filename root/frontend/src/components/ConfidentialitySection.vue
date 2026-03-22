<script setup lang="ts">
import { ShieldCheck } from "lucide-vue-next";
</script>

<template>
  <section class="py-12 px-6 md:px-12 lg:px-24 bg-white">
    <div
      class="max-w-4xl mx-auto p-10 bg-brand-accent text-white rounded-[2.5rem] flex flex-col md:flex-row items-center gap-8 shadow-2xl"
    >
      <div
        class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center shrink-0"
      >
        <ShieldCheck class="w-10 h-10" />
      </div>
      <div>
        <h3 class="text-2xl mb-4">Конфиденциальность</h3>
        <p class="text-white/80 text-lg leading-relaxed">
          Все консультации проходят строго конфиденциально. Личная информация
          не&nbsp;передаётся третьим лицам. Вы&nbsp;можете быть уверены
          в&nbsp;безопасности и&nbsp;анонимности.
        </p>
      </div>
    </div>
  </section>
</template>
