<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import Carousel from 'primevue/carousel';
import { useProductsStore } from '@/stores/products.ts';
import { TopMenu } from '@/components/top-menu';
import { formatPrice } from '@/utils.ts';
import { Socials, ImagedInfoContainer } from '@/components';

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
    class="mt-5"
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
  <ImagedInfoContainer class="mt-5">
    <template #header>Свойства</template>
    <template #image-left>
      <img src="/internals-logo.png" alt="internals-logo" />
    </template>
    <template #text>
      <p>
        Украшения несут в&nbsp;себе состояния, которые вам сейчас необходимы. А&nbsp;мы&nbsp;все
        находимся в состояниях, в&nbsp;каждую минуту своей жизни, только одни состояния
        благотворные, а&nbsp;другие разрушительные. Поэтому так важно отслеживать негативные
        проявления.
      </p>
      <p>
        При создании украшений я&nbsp;изучаю вашу энергию в&nbsp;данный момент, слушаю, что требует
        ваше тело, и&nbsp;передаю необходимое свойство через дизайн. Когда вы&nbsp;носите украшение,
        происходит процесс изменений, вы&nbsp;напитываетесь нужным для вас состоянием. Уходит
        напряжение из&nbsp;тела, освобождается энергия, которую вы&nbsp;удерживали и&nbsp;она
        реализуется там, где требуется.
      </p>
      <p>Мои клиенты отмечают, что:</p>
      <ul class="info-container__list">
        <li class="info-container__list__item">️Стали легче принимать решения</li>
        <li class="info-container__list__item">
          ️Захотелось поработать над имиджем и&nbsp;приходят к&nbsp;своему результату
        </li>
        <li class="info-container__list__item">️Внутри становится спокойнее и&nbsp;гармоничнее</li>
        <li class="info-container__list__item">️Появляется здоровая влюбленность в&nbsp;себя</li>
        <li class="info-container__list__item">
          Становится сложнее наступать себе на&nbsp;горло, хочется выбирать себя
        </li>
      </ul>
    </template>
  </ImagedInfoContainer>
  <Socials class="d-flex flex-row justify-content-center align-items-center mt-5" />
</template>

<style scoped lang="scss">
$borderColor: #939393;

.info-container {
  .info-image {
    img {
      height: 100%;
    }
  }

  &__list {
    list-style-type: '✔️';

    &__item {
      padding-left: 1rem;
    }
  }
}
</style>
