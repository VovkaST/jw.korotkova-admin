<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import Carousel from 'primevue/carousel';
import Image from 'primevue/image';
import { formatPrice } from '@/utils.ts';
import { useProductsStore } from '@/stores/products.ts';

const props = withDefaults(defineProps<{ header: string }>(), { header: 'Товары' });

const productsStore = useProductsStore();
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
  <div class="products-container">
    <h2 class="header font-handwritten">{{ header }}</h2>

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
              <Image
                :src="slotProps.data.image"
                :alt="slotProps.data.name"
                class="w-full rounded"
                width="100%"
                preview
                zoom-in-disabled
                zoom-out-disabled
                :pt="{
                  rotateLeftButton: { disabled: true },
                  rotateRightButton: { disabled: true },
                }"
              >
                <template #preview="slotProps">
                  <img
                    src="https://primefaces.org/cdn/primevue/images/galleria/galleria11.jpg"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                  />
                </template>
              </Image>
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
  </div>
</template>

<style scoped lang="scss">
$borderColor: #939393;

.products-container {
  border-top: 1px solid $borderColor;

  .header {
    margin: 1rem 0 2rem;
    font-size: 3rem;
    font-weight: 300;
  }
}
</style>
