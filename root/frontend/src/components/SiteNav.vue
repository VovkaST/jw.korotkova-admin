<script setup lang="ts">
import { Menu, X } from "lucide-vue-next";

const navLinks = [
  { name: "О методе", href: "#about" },
  { name: "Запросы", href: "#requests" },
  { name: "Этапы", href: "#process" },
  { name: "Эксперт", href: "#expert" },
  { name: "Цены", href: "#prices" },
] as const;

const menuOpen = defineModel<boolean>("menuOpen", { default: false });

const emit = defineEmits<{ contact: [] }>();

function onContact(): void {
  emit("contact");
  menuOpen.value = false;
}
</script>

<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-black/5"
  >
    <div
      class="max-w-7xl mx-auto px-6 md:px-12 h-20 flex items-center justify-between"
    >
      <a
        href="#"
        class="text-xl font-display font-bold tracking-tight text-brand-accent uppercase"
      >
        Наталья Короткова
      </a>

      <div class="hidden md:flex items-center gap-8">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="text-sm font-medium hover:text-brand-accent transition-colors"
        >
          {{ link.name }}
        </a>
        <button
          type="button"
          class="bg-brand-accent text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-brand-accent-light transition-all"
          @click="onContact"
        >
          Написать
        </button>
      </div>

      <button
        type="button"
        class="md:hidden p-2"
        aria-label="Меню"
        @click="menuOpen = !menuOpen"
      >
        <component :is="menuOpen ? X : Menu" />
      </button>
    </div>

    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform -translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-4 opacity-0"
    >
      <div
        v-if="menuOpen"
        class="absolute top-20 left-0 right-0 bg-white border-b border-black/5 p-6 flex flex-col gap-4 md:hidden"
      >
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="py-2 text-lg"
          @click="menuOpen = false"
        >
          {{ link.name }}
        </a>
        <button
          type="button"
          class="w-full bg-brand-accent text-white py-4 rounded-xl font-semibold"
          @click="onContact"
        >
          Написать
        </button>
      </div>
    </transition>
  </nav>
</template>
