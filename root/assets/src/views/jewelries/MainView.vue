<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import Carousel from 'primevue/carousel';
import { useProductsStore } from '@/stores/products.ts';
import { TopMenu } from '@/components/top-menu';
import { formatPrice } from '@/utils.ts';

const productsStore = useProductsStore();
const origin = window.location.origin;

const products = ref([]);

onBeforeMount(async () => {
  await productsStore.getProductsInStock().then((response) => {
    response.forEach((item) => {
      products.value.push({
        guid: item.guid,
        name: item.title,
        description: item.description,
        image: item.files.length ? item.files[0].file : '',
        price: item.price,
        category: item.type.name,
      });
    });
  });
});
</script>

<template>
  <TopMenu title="Jewelry" />
  <Carousel
    v-if="products.length"
    :value="products"
    :numVisible="3"
    :numScroll="1"
    :circular="true"
    :showIndicators="false"
  >
    <template #item="slotProps">
      <div
        class="product-container border border-surface-200 dark:border-surface-700 rounded m-2 p-4"
      >
        <div class="mb-4">
          <div class="relative mx-auto">
            <img :src="slotProps.data.image" :alt="slotProps.data.name" class="w-full rounded" />
          </div>
        </div>
        <div class="mb-4 font-medium">{{ slotProps.data.name }}</div>
        <div class="flex justify-content-between align-items-center">
          <div class="mt-0 font-semibold text-xl">
            {{ formatPrice(slotProps.data.price) }}
          </div>
        </div>
      </div>
    </template>
  </Carousel>
</template>

<style scoped lang="scss"></style>
