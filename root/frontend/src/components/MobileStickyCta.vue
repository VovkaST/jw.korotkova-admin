<script setup lang="ts">
const emit = defineEmits<{ contact: [] }>();

defineProps<{
  visible: boolean;
}>();
</script>

<template>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="translate-y-20 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-20 opacity-0"
  >
    <div
      v-if="visible"
      class="fixed bottom-4 left-4 right-4 z-50 md:hidden"
    >
      <button
        type="button"
        class="w-full bg-brand-accent text-white py-4 rounded-xl font-semibold shadow-2xl"
        @click="emit('contact')"
      >
        Написать
      </button>
    </div>
  </transition>
</template>
