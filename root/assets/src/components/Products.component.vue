<script setup lang="ts">
import { computed, onBeforeMount, onMounted, onUnmounted, ref } from 'vue';
import Carousel from 'primevue/carousel';
import Image from 'primevue/image';
import { formatPrice } from '@/utils.ts';
import { useProductsStore } from '@/stores/products.ts';
import { ImageSizes, type IProductFile } from '@/stores/types';

type ProductData = {
  guid: string;
  name: string;
  description: string;
  previewImage: string;
  image: string;
  price: number;
  category: string;
};

function filterImage(files: IProductFile[], sizeCode: ImageSizes): string {
  for (const file of files) {
    if (file.meta && file.meta.size_code === sizeCode.toString()) {
      return file.file;
    }
  }
  if (files.length > 0) {
    return files[0].file;
  }
  return '';
}

withDefaults(defineProps<{ header: string }>(), { header: 'Товары' });

const productsStore = useProductsStore();
const products = ref<ProductData[]>([]);

const isMobile = ref<boolean>(false);
const isTablet = ref<boolean>(false);

let mobileMediaQuery: MediaQueryList;
let tabletMediaQuery: MediaQueryList;

const checkBreakpoints = () => {
  isMobile.value = mobileMediaQuery.matches;
  isTablet.value = tabletMediaQuery.matches;
};

const numVisibleProducts = computed<number>(() => {
  if (isMobile.value) return 1;
  if (isTablet.value) return 2;
  return 3;
});
const carouselKey = computed<string>(() => `carousel-${numVisibleProducts.value}`);

onBeforeMount(async () => {
  await productsStore.getProductsInStock().then((response) => {
    response.forEach((item) => {
      products.value.push({
        guid: item.guid,
        name: item.title,
        description: item.description,
        previewImage: filterImage(item.files || [], ImageSizes.M),
        image: filterImage(item.files || [], ImageSizes.ORIGINAL),
        price: item.price as number,
        category: item.type.name,
      });
    });
  });
});

onMounted(() => {
  mobileMediaQuery = window.matchMedia('(max-width: 767px)');
  tabletMediaQuery = window.matchMedia('(min-width: 768px) and (max-width: 1023px)');

  checkBreakpoints();

  mobileMediaQuery.addEventListener('change', checkBreakpoints);
  tabletMediaQuery.addEventListener('change', checkBreakpoints);
});

onUnmounted(() => {
  mobileMediaQuery.removeEventListener('change', checkBreakpoints);
  tabletMediaQuery.removeEventListener('change', checkBreakpoints);
});
</script>

<template>
  <div class="products-container">
    <h2 class="header font-handwritten">{{ header }}</h2>

    <Carousel
      v-if="products.length"
      :key="carouselKey"
      :value="products"
      :numVisible="numVisibleProducts"
      :numScroll="1"
      :circular="true"
      :showIndicators="false"
    >
      <template #item="slotProps">
        <div
          class="product-container border border-surface-200 dark:border-surface-700 rounded m-2"
        >
          <div class="product-image">
            <div class="relative mx-auto">
              <Image
                :src="slotProps.data.previewImage"
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
                <template #preview="imageSlotProps">
                  <img
                    class="p-image-original"
                    :src="slotProps.data.image"
                    alt="preview"
                    :style="imageSlotProps.style"
                  />
                </template>
              </Image>
            </div>
          </div>
          <div class="product-name font-medium">{{ slotProps.data.name }}</div>
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
  margin-top: 3rem;

  .header {
    margin: 1rem 0 2rem;
    font-size: 3rem;
    font-weight: 300;
  }

  .product-container {
    padding: 1.5rem;

    .product-image {
      margin-bottom: 1.5rem;
    }
    .product-name {
      margin-bottom: 1.5rem;
    }
  }
}
@media (max-width: 1024px) {
  .products-container {
    margin-top: 1.5rem;
    padding: 0 1rem;

    .header {
      margin: 0.5rem 0 1rem;
      font-size: 2.5rem;
    }

    .product-container {
      padding: 1.5rem;
      padding: 1rem;

      .product-image {
        margin-bottom: 0.5rem;
      }
      .product-name {
        margin-bottom: 0.5rem;
      }
    }
  }
}
</style>
