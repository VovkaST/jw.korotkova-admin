<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import Carousel from 'primevue/carousel';
import ScrollTop from 'primevue/scrolltop';
import Image from 'primevue/image';
import { useProductsStore } from '@/stores/products.ts';
import { formatPrice } from '@/utils.ts';
import { Footer, InfoContainer, TopMenu } from '@/components';

const router = useRouter();

const productsStore = useProductsStore();
const origin = window.location.origin;

const internals = ref<typeof InfoContainer>(null);
const care = ref<typeof InfoContainer>(null);
const order = ref<typeof InfoContainer>(null);

const products = ref([]);

const onMenuClick = (item) => {
  item.value.$el.scrollIntoView({ behavior: 'smooth' });
};

const menuItems = [
  {
    title: 'Главная',
    onClick: () => {
      router.push({ name: 'home' });
    },
  },
  {
    title: 'Свойства',
    onClick: () => onMenuClick(internals),
  },
  {
    title: 'Уход',
    onClick: () => onMenuClick(care),
  },
  {
    title: 'Заказ',
    onClick: () => onMenuClick(order),
  },
];

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
  <TopMenu title="Jewellery" :items="menuItems" />

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
            <Image
              :src="slotProps.data.image"
              :alt="slotProps.data.name"
              class="w-full rounded"
              width="100%"
              preview
              zoom-in-disabled
              zoom-out-disabled
              :pt="{ rotateLeftButton: { disabled: true }, rotateRightButton: { disabled: true } }"
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

  <InfoContainer class="mt-5" id="services" ref="internals">
    <template #circle-left> Свойства </template>
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
      <ul class="info-container__list check-style">
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
  </InfoContainer>

  <InfoContainer class="mt-5" ref="care">
    <template #text>
      <p>Факторы, которые могут повлиять на&nbsp;внешний вид изделий:</p>
      <ul class="info-container__list">
        <li class="info-container__list__item">Повышенная влажность, вода, перепады температур</li>
        <li class="info-container__list__item">Химические средства, использующиеся в&nbsp;быту</li>
        <li class="info-container__list__item">Косметика, гигиенические средства, парфюм</li>
        <li class="info-container__list__item">Естественные выделения тела</li>
      </ul>
      <p>
        Ваши украшения в&nbsp;себе имеют состояния и&nbsp;когда в&nbsp;вашей жизни случается стресс,
        они берут на себя удар, что тоже может приводить к&nbsp;их&nbsp;странной деформации.
      </p>
      <p>
        Стоит отметить, что физические воздействия, если вы&nbsp;ударились, зацепились, дернули,
        изделия, конечно, не&nbsp;выдержат.
      </p>
      <p>Как продлить срок службы изделий:</p>
      <ul class="info-container__list check-style">
        <li class="info-container__list__item">
          Храните украшения подальше от&nbsp;источников тепла и&nbsp;влаги, предохраняйте
          от&nbsp;прямых солнечных лучей
        </li>
        <li class="info-container__list__item">
          Обязательно снимайте бижутерию на&nbsp;ночь, во&nbsp;время водных процедур, физического
          труда и тренировок
        </li>
        <li class="info-container__list__item">
          Сначала наносите кремы и&nbsp;парфюм, подождите, когда все впитается и&nbsp;только потом
          надевайте украшения
        </li>
      </ul>
    </template>
    <template #circle-right> Уход </template>
  </InfoContainer>

  <InfoContainer class="mt-5" ref="order">
    <template #text>
      <p>Для заказа нужно:</p>
      <ul class="info-container__list check-style">
        <li class="info-container__list__item">Сделать селфи на момент обращения</li>
        <li class="info-container__list__item">Указать дату рождения</li>
        <li class="info-container__list__item">
          Выразить пожелания по виду изделия, для браслетов нужно указать размер запястья
        </li>
        <li class="info-container__list__item">Указать ваш адрес</li>
        <li class="info-container__list__item">
          Внести <b>предоплату 1000 рублей</b>. Эта сумма будет взиматься
          <b>за разработку изделия</b> и <b>возврату не подлежит</b>
        </li>
      </ul>
      <p>
        Как только я сажусь за изготовление, значит уже работаю в вашем поле, что дает начало вашим
        изменениям.
      </p>
      <p>
        Изготовление занимает от 3 до 10 дней, затем я направлю вам фото результата и конечную
        стоимость изделия.
      </p>
      <p>
        Полная оплата производится в день получения фото готового изделия. Если потребуется чек,
        укажите. Если оплата не производится, заказ аннулируется.
      </p>
    </template>
    <template #circle-left> Заказ </template>
  </InfoContainer>

  <Footer />

  <ScrollTop />
</template>

<style scoped lang="scss">
$borderColor: #939393;

.info-container {
  .info-circle {
    img {
      height: 100%;
    }
  }

  &__list {
    &.check-style {
      list-style-type: '✔️';
    }

    &__item {
      padding-left: 1rem;
    }
  }
}

.p-button {
  background: var(--p-button-secondary-color);
  border: 1px solid var(--p-button-secondary-border-color);

  &:not(:disabled) {
    &:hover,
    &:active {
      background: var(--p-button-secondary-hover-background);
      border: 1px solid var(--p-button-secondary-hover-border-color);
    }
  }
}
</style>
