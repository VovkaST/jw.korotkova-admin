<script setup lang="ts">
import { ChevronUp } from "lucide-vue-next";

defineProps<{
  visible: boolean;
  liftForSticky: boolean;
}>();

const emit = defineEmits<{ click: [] }>();
</script>

<template>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="translate-y-10 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-10 opacity-0"
  >
    <button
      v-if="visible"
      type="button"
      class="fixed bottom-6 right-6 z-50 w-12 h-12 bg-white text-brand-accent rounded-full shadow-xl flex items-center justify-center hover:bg-brand-accent hover:text-white transition-all border border-black/5"
      :class="{ 'bottom-24': liftForSticky }"
      aria-label="Наверх"
      @click="emit('click')"
    >
      <ChevronUp class="w-6 h-6" />
    </button>
  </transition>
</template>
