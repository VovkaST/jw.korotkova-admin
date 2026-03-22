<script setup lang="ts">
import { Motion } from "@motionone/vue";
import {
  ArrowRight,
  Award,
  CheckCircle2,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  Compass,
  Clock,
  Mail,
  Menu,
  MessageCircle,
  Phone,
  Quote,
  Send,
  ShieldCheck,
  Sparkles,
  Target,
  UserCircle2,
  X,
  Zap,
  ZoomIn,
} from "lucide-vue-next";
import { onMounted, onUnmounted, ref, watch } from "vue";
import { ReviewsService } from "@/api/v1/reviews";
import type { ReviewDto } from "@/api/v1/client";

// --- State ---
const isMenuOpen = ref<boolean>(false);
const activeAccordion = ref<number | null>(null);
const showStickyCTA = ref<boolean>(true);
const showScrollTop = ref<boolean>(false);
const reviewSlideIndex = ref<number>(0);
const reviewLightbox = ref<{ src: string; alt: string } | null>(null);

const reviewItems = ref<ReviewDto[]>([]);
const reviewsLoading = ref<boolean>(true);
const reviewsError = ref<boolean>(false);
/** Индексы слайдов, для которых уже задан src у img (ленивая подгрузка) */
const loadedSlideIndices = ref<Set<number>>(new Set());

function markSlideLoaded(index: number): void {
  if (loadedSlideIndices.value.has(index)) return;
  const next = new Set(loadedSlideIndices.value);
  next.add(index);
  loadedSlideIndices.value = next;
}

function slideSrc(index: number): string | undefined {
  if (!loadedSlideIndices.value.has(index)) return undefined;
  const item = reviewItems.value[index];
  if (!item?.screenshot_url) return undefined;
  return item.screenshot_url;
}

function slideAlt(index: number): string {
  const item = reviewItems.value[index];
  if (item?.client_label) return item.client_label;
  if (item?.quote) {
    const q = item.quote.trim();
    if (q.length > 120) return `${q.slice(0, 117)}…`;
    return q;
  }
  return `Отзыв клиента, скриншот переписки (${index + 1})`;
}

async function loadReviews(): Promise<void> {
  reviewsLoading.value = true;
  reviewsError.value = false;
  try {
    const { data, error } = await ReviewsService.getReviews();
    if (error) throw error;
    if (!Array.isArray(data)) throw new Error("bad response");
    reviewItems.value = data;
    reviewSlideIndex.value = 0;
    loadedSlideIndices.value = data.length > 0 ? new Set([0]) : new Set();
  } catch {
    reviewItems.value = [];
    loadedSlideIndices.value = new Set();
    reviewsError.value = true;
  } finally {
    reviewsLoading.value = false;
  }
}

// --- Lifecycle ---
onMounted(() => {
  void loadReviews();

  // Scroll observer for sticky CTA
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting || entry.boundingClientRect.top < 0) {
          showStickyCTA.value = false;
        } else {
          showStickyCTA.value = true;
        }
      });
    },
    { threshold: 0.1 },
  );

  const contactSection = document.getElementById("contact");
  if (contactSection) observer.observe(contactSection);

  // Scroll listener for scroll-to-top button
  window.addEventListener("scroll", () => {
    showScrollTop.value = window.scrollY > 500;
  });
});

const onReviewLightboxKeydown = (e: KeyboardEvent) => {
  if (e.key === "Escape") reviewLightbox.value = null;
};

watch(reviewLightbox, (v) => {
  if (v) {
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onReviewLightboxKeydown);
  } else {
    document.body.style.overflow = "";
    window.removeEventListener("keydown", onReviewLightboxKeydown);
  }
});

onUnmounted(() => {
  document.body.style.overflow = "";
  window.removeEventListener("keydown", onReviewLightboxKeydown);
});

const reviewTouchStartX = ref<number>(0);

const onReviewTouchStart = (e: TouchEvent) => {
  reviewTouchStartX.value = e.changedTouches[0].screenX;
};

const onReviewTouchEnd = (e: TouchEvent) => {
  const dx = e.changedTouches[0].screenX - reviewTouchStartX.value;
  if (dx < -48) nextReviewSlide();
  if (dx > 48) prevReviewSlide();
};

watch(reviewSlideIndex, (idx) => {
  if (reviewItems.value.length === 0) return;
  markSlideLoaded(idx);
});

const nextReviewSlide = () => {
  const n = reviewItems.value.length;
  if (n === 0) return;
  reviewSlideIndex.value = (reviewSlideIndex.value + 1) % n;
};

const prevReviewSlide = () => {
  const n = reviewItems.value.length;
  if (n === 0) return;
  reviewSlideIndex.value = (reviewSlideIndex.value - 1 + n) % n;
};

const openReviewLightbox = (index: number) => {
  const src = slideSrc(index);
  if (!src) return;
  reviewLightbox.value = { src, alt: slideAlt(index) };
};

const closeReviewLightbox = () => {
  reviewLightbox.value = null;
};

// --- Methods ---
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// --- Data ---
const navLinks = [
  { name: "О методе", href: "#about" },
  { name: "Запросы", href: "#requests" },
  { name: "Этапы", href: "#process" },
  { name: "Эксперт", href: "#expert" },
  { name: "Цены", href: "#prices" },
];

const aboutItems = [
  { icon: Zap, title: "Быстрый результат", desc: "изменения после 1–2 сессий" },
  { icon: Target, title: "Глубокая проработка", desc: "работа с причинами" },
  {
    icon: UserCircle2,
    title: "Индивидуальный подход",
    desc: "адаптация под клиента",
  },
  {
    icon: Sparkles,
    title: "Самопомощь",
    desc: "обучение самостоятельной работе",
  },
];

const requests = [
  "Неуверенность в себе и низкая самооценка",
  "Сложности в отношениях",
  "Финансовые блоки и страх успеха",
  "Профессиональное выгорание",
  "Последствия психологических травм",
  "Поиск своего предназначения",
];

const steps = [
  {
    num: "1",
    title: "Запрос",
    desc: "Формулирование вашего запроса и подготовка к сессии",
  },
  {
    num: "2",
    title: "Онлайн-сессия",
    desc: "Глубокий разбор и проработка в рамках часовой встречи",
  },
  {
    num: "3",
    title: "Результат",
    desc: "Получение ответов и инструментов для самостоятельной работы",
  },
];

const prices = [
  {
    title: "Консультация «Терапия Души»",
    time: "60 мин",
    price: "3 000 ₽",
    desc: "Единичная сессия по вашему запросу",
    popular: true,
  },
];

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
];

// --- Methods ---
const scrollToContact = () => {
  document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" });
  isMenuOpen.value = false;
};

/** Замените href на реальные ссылки в личные сообщения */
const messengerLinks = [
  {
    label: "Telegram",
    description: "Удобно с телефона и десктопа",
    href: "https://t.me/",
    icon: "telegram",
  },
  {
    label: "ВКонтакте",
    description: "Личные сообщения ВКонтакте",
    href: "https://vk.me/",
    icon: "vk",
  },
  {
    label: "Max",
    description: "Написать в Max",
    href: "#",
    icon: "max",
  },
] as const;

/** Каналы «Компас Души» — подставьте ссылки на каналы/сообщества */
const compassChannelLinks = [
  {
    label: "Telegram",
    href: "https://t.me/",
    icon: "telegram",
    cta: "Перейти в канал",
  },
  {
    label: "ВКонтакте",
    href: "https://vk.com/",
    icon: "vk",
    cta: "Перейти в сообщество",
  },
  {
    label: "Max",
    href: "#",
    icon: "max",
    cta: "Перейти в канал",
  },
] as const;

const toggleAccordion = (index: number) => {
  activeAccordion.value = activeAccordion.value === index ? null : index;
};
</script>

<template>
  <div class="min-h-screen">
    <!-- Navigation -->
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
            @click="scrollToContact"
            class="bg-brand-accent text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-brand-accent-light transition-all"
          >
            Написать
          </button>
        </div>

        <button class="md:hidden p-2" @click="isMenuOpen = !isMenuOpen">
          <component :is="isMenuOpen ? X : Menu" />
        </button>
      </div>

      <!-- Mobile Menu -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform -translate-y-4 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform -translate-y-4 opacity-0"
      >
        <div
          v-if="isMenuOpen"
          class="absolute top-20 left-0 right-0 bg-white border-b border-black/5 p-6 flex flex-col gap-4 md:hidden"
        >
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            @click="isMenuOpen = false"
            class="py-2 text-lg"
          >
            {{ link.name }}
          </a>
          <button
            @click="scrollToContact"
            class="w-full bg-brand-accent text-white py-4 rounded-xl font-semibold"
          >
            Написать
          </button>
        </div>
      </transition>
    </nav>

    <!-- Hero Section -->
    <section
      class="pt-32 pb-20 px-6 md:px-12 lg:px-24 min-h-[90vh] flex items-center bg-brand-beige"
    >
      <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
        <Motion
          :initial="{ opacity: 0, x: -50 }"
          :animate="{ opacity: 1, x: 0 }"
          :transition="{ duration: 0.8, easing: 'ease-out' }"
        >
          <h1 class="text-4xl md:text-6xl lg:text-7xl leading-[1.1] mb-6">
            Путь к внутренней свободе через
            <span class="text-brand-accent">«Терапию Души»</span>
          </h1>
          <p class="text-lg md:text-xl text-brand-muted mb-10 max-w-lg">
            Освободитесь от барьеров прошлого — начните жить осознанно уже
            сегодня.
          </p>
          <button
            @click="scrollToContact"
            class="w-full md:w-auto bg-brand-accent text-white px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent-light transition-all flex items-center justify-center gap-2"
          >
            Написать мне <ArrowRight class="w-5 h-5" />
          </button>
        </Motion>

        <Motion
          :initial="{ opacity: 0, scale: 0.9 }"
          :animate="{ opacity: 1, scale: 1 }"
          :transition="{ duration: 0.8, delay: 0.2, easing: 'ease-out' }"
          class="relative"
        >
          <div class="aspect-[4/5] rounded-[2rem] overflow-hidden shadow-2xl">
            <img
              src="/BusinessCardPhoto.jpg"
              alt="Наталья Короткова"
              class="w-full h-full object-cover object-[calc(50%-125px)_center]"
              referrerPolicy="no-referrer"
            />
          </div>
          <div
            class="absolute -bottom-6 -left-6 w-32 h-32 bg-brand-accent/10 rounded-full blur-3xl -z-10"
          />
          <div
            class="absolute -top-6 -right-6 w-48 h-48 bg-brand-accent/5 rounded-full blur-3xl -z-10"
          />
        </Motion>
      </div>
    </section>

    <!-- About Method -->
    <section id="about" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-16">
          Что такое «Терапия Души»?
        </h2>
        <div class="max-w-3xl mx-auto text-center mb-16">
          <p class="text-xl md:text-2xl leading-relaxed text-brand-muted">
            «Терапия Души» — авторский метод психолога Евгения Теребенина. Он
            помогает быстро проработать глубинные причины проблем: непрожитые
            эмоции, травмы, родовые сценарии. Результат ощущается уже после
            первых сессий.
          </p>
        </div>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
          <Motion
            v-for="(item, i) in aboutItems"
            :key="i"
            :initial="{ opacity: 0, y: 20 }"
            :animate="{ opacity: 1, y: 0 }"
            :transition="{ duration: 0.5, delay: i * 0.1 }"
            class="text-center p-6"
          >
            <div
              class="w-16 h-16 bg-brand-beige rounded-2xl flex items-center justify-center mx-auto mb-6 text-brand-accent"
            >
              <component :is="item.icon" class="w-8 h-8" />
            </div>
            <h3 class="text-lg mb-2">{{ item.title }}</h3>
            <p class="text-sm text-brand-muted">{{ item.desc }}</p>
          </Motion>
        </div>
      </div>
    </section>

    <!-- Requests -->
    <section id="requests" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-16">
          Решаем ваши проблемы эффективно
        </h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Motion
            v-for="(text, i) in requests"
            :key="i"
            :initial="{ opacity: 0, scale: 0.95 }"
            :animate="{ opacity: 1, scale: 1 }"
            :transition="{ duration: 0.4, delay: i * 0.05 }"
            class="p-8 rounded-2xl bg-white border border-black/5 shadow-sm hover:-translate-y-2 transition-all duration-300 flex flex-col items-start gap-4"
          >
            <div
              class="w-12 h-12 bg-brand-accent/5 rounded-xl flex items-center justify-center text-brand-accent"
            >
              <CheckCircle2 class="w-6 h-6" />
            </div>
            <p class="text-lg font-medium leading-snug">{{ text }}</p>
          </Motion>
        </div>
        <div class="mt-16 text-center">
          <button
            @click="scrollToContact"
            class="bg-transparent border-2 border-brand-accent text-brand-accent px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent/5 transition-all"
          >
            Узнать подробнее о методе
          </button>
        </div>
      </div>
    </section>

    <!-- Process -->
    <section id="process" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-16">
          Этапы работы по методу «Терапия Души»
        </h2>
        <div class="relative max-w-4xl mx-auto">
          <div class="space-y-12 relative">
            <div
              class="absolute h-full left-8 md:left-1/2 top-0 bottom-32 w-px bg-black/10 -translate-x-1/2 hidden md:block"
            />
            <div
              v-for="(step, i) in steps"
              :key="i"
              class="flex items-center gap-8"
              :class="i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'"
            >
              <div class="flex-1 hidden md:block" />
              <div
                class="w-16 h-16 rounded-full bg-brand-accent text-white flex items-center justify-center text-2xl font-bold z-10 shrink-0 shadow-lg"
              >
                {{ step.num }}
              </div>
              <div class="flex-1 bg-brand-beige p-8 rounded-2xl">
                <h3 class="text-xl mb-2">{{ step.title }}</h3>
                <p class="text-brand-muted">{{ step.desc }}</p>
              </div>
            </div>
          </div>

          <div class="mt-16 text-center">
            <div
              class="inline-flex items-center gap-4 px-6 py-3 bg-brand-accent/5 rounded-full text-brand-accent font-medium"
            >
              <Sparkles class="w-5 h-5" /> Онлайн
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Expert -->
    <section id="expert" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-16">Об эксперте</h2>
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div class="aspect-square rounded-3xl overflow-hidden shadow-xl">
            <img
              src="/SpecialistPhoto.jpg"
              alt="Наталья Короткова"
              class="w-full h-full object-cover object-[calc(50%+125px)_center]"
              referrerPolicy="no-referrer"
            />
          </div>

          <div class="space-y-8">
            <div>
              <h3 class="text-3xl mb-2">Наталья Короткова</h3>
              <p class="text-brand-accent font-semibold text-lg">
                Опыт работы: 5 лет
              </p>
            </div>

            <p class="text-lg text-brand-muted leading-relaxed">
              Меня зовут Наталья Короткова. Я сертифицированный специалист по
              методу «Терапия Души» Евгения Теребенина. Помогаю клиентам обрести
              внутреннюю гармонию и научиться управлять своей жизнью осознанно.
            </p>

            <div class="space-y-4">
              <h4 class="font-bold text-lg">Образование:</h4>
              <ul class="space-y-2 text-brand-muted">
                <li class="flex items-start gap-3">
                  <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                  <span>Сертификат по методу «Терапия Души»</span>
                </li>
              </ul>
            </div>

            <div
              class="relative p-8 bg-white rounded-2xl italic text-brand-muted border-l-4 border-brand-accent"
            >
              <Quote
                class="absolute top-4 right-4 w-12 h-12 text-brand-accent/10"
              />
              <p class="text-xl">
                «Терапия не учит — она освобождает дорогу от барьеров»
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Reviews (скриншоты из админки, API GET /api/v1/reviews/public/) -->
    <section id="reviews" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-4">Отзывы</h2>
        <p
          class="text-center text-brand-muted max-w-2xl mx-auto mb-12 md:mb-14 leading-relaxed"
        >
          Большинство отзывов приходит в личные сообщения — поэтому здесь
          собраны скриншоты переписки с телефона.
        </p>

        <div
          v-if="reviewsLoading"
          class="max-w-sm mx-auto py-16 text-center text-brand-muted text-sm"
        >
          Загрузка отзывов…
        </div>
        <p
          v-else-if="reviewsError"
          class="max-w-sm mx-auto py-8 text-center text-sm text-brand-muted"
        >
          Не удалось загрузить отзывы. Проверьте API или авторизацию сервера.
        </p>
        <p
          v-else-if="reviewItems.length === 0"
          class="max-w-sm mx-auto py-8 text-center text-sm text-brand-muted"
        >
          Отзывов пока нет — добавьте их в админке.
        </p>

        <div
          v-else
          class="relative max-w-sm mx-auto px-11 sm:px-14"
          @touchstart.passive="onReviewTouchStart"
          @touchend.passive="onReviewTouchEnd"
        >
          <button
            v-if="reviewItems.length > 1"
            type="button"
            aria-label="Предыдущий отзыв"
            class="absolute left-0 top-[42%] -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white border border-black/10 shadow-md flex items-center justify-center text-brand-accent hover:bg-brand-accent hover:text-white transition-colors"
            @click="prevReviewSlide"
          >
            <ChevronLeft class="w-6 h-6" />
          </button>
          <button
            v-if="reviewItems.length > 1"
            type="button"
            aria-label="Следующий отзыв"
            class="absolute right-0 top-[42%] -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white border border-black/10 shadow-md flex items-center justify-center text-brand-accent hover:bg-brand-accent hover:text-white transition-colors"
            @click="nextReviewSlide"
          >
            <ChevronRight class="w-6 h-6" />
          </button>

          <div
            class="overflow-hidden rounded-[2rem] shadow-2xl ring-1 ring-black/10 bg-brand-beige"
          >
            <div
              class="flex transition-transform duration-500 ease-out will-change-transform"
              :style="{ transform: `translateX(-${reviewSlideIndex * 100}%)` }"
            >
              <div
                v-for="(item, i) in reviewItems"
                :key="item.id"
                class="w-full shrink-0 flex justify-center px-1 sm:px-2"
              >
                <button
                  type="button"
                  class="group relative w-full max-w-[280px] aspect-[9/19] rounded-[1.75rem] overflow-hidden bg-neutral-200 shadow-inner focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-accent focus-visible:ring-offset-2"
                  :class="slideSrc(i) ? 'cursor-zoom-in' : 'cursor-default'"
                  @click="openReviewLightbox(i)"
                >
                  <img
                    v-if="slideSrc(i)"
                    :src="slideSrc(i)"
                    :alt="slideAlt(i)"
                    decoding="async"
                    class="absolute inset-0 w-full h-full object-cover object-top select-none pointer-events-none transition-transform duration-300 ease-out group-hover:scale-[1.04] group-focus-visible:scale-[1.04]"
                  />
                  <div
                    v-else
                    class="absolute inset-0 animate-pulse bg-neutral-300/80"
                    aria-hidden="true"
                  />
                  <div
                    v-if="slideSrc(i)"
                    class="pointer-events-none absolute inset-0 flex flex-col items-center justify-center gap-2 rounded-[1.75rem] bg-black/50 opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-visible:opacity-100"
                    aria-hidden="true"
                  >
                    <ZoomIn
                      class="w-11 h-11 text-white drop-shadow-md sm:w-10 sm:h-10"
                      stroke-width="1.75"
                    />
                    <span
                      class="text-[11px] font-semibold uppercase tracking-wider text-white drop-shadow"
                    >
                      Увеличить
                    </span>
                  </div>
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="reviewItems.length > 1"
            class="flex justify-center gap-2 mt-6"
            role="tablist"
            aria-label="Номер слайда"
          >
            <button
              v-for="(_, i) in reviewItems"
              :key="i"
              type="button"
              class="h-2 rounded-full transition-all duration-300"
              :class="
                i === reviewSlideIndex
                  ? 'w-8 bg-brand-accent'
                  : 'w-2 bg-black/15 hover:bg-black/25'
              "
              :aria-label="'Отзыв ' + (i + 1)"
              :aria-current="i === reviewSlideIndex ? 'true' : undefined"
              @click="reviewSlideIndex = i"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Prices -->
    <section id="prices" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl text-center mb-16">Стоимость услуг</h2>
        <div class="flex justify-center">
          <Motion
            v-for="(item, i) in prices"
            :key="i"
            :initial="{ opacity: 0, y: 30 }"
            :animate="{ opacity: 1, y: 0 }"
            :transition="{ duration: 0.6, delay: i * 0.1 }"
            class="relative p-10 md:p-16 rounded-[3rem] transition-all duration-300 bg-brand-accent text-white shadow-2xl max-w-2xl w-full text-center"
          >
            <h3 class="text-3xl md:text-4xl mb-4 font-display">
              {{ item.title }}
            </h3>
            <p
              class="text-lg mb-8 text-white/80 flex items-center justify-center gap-2"
            >
              <Clock class="w-5 h-5" /> {{ item.time }}
            </p>
            <div class="text-5xl md:text-6xl font-bold mb-8">
              {{ item.price }}
            </div>
            <p class="text-xl mb-12 text-white/90 leading-relaxed">
              {{ item.desc }}
            </p>
            <button
              @click="scrollToContact"
              class="w-full md:w-auto px-12 py-5 rounded-2xl font-bold bg-white text-brand-accent hover:bg-white/90 transition-all duration-300 text-lg shadow-xl"
            >
              Написать мне
            </button>
          </Motion>
        </div>
        <div
          class="mt-16 p-8 bg-brand-accent/5 rounded-3xl text-center border border-brand-accent/10 max-w-2xl mx-auto"
        >
          <p
            class="text-brand-accent font-semibold text-lg flex items-center justify-center gap-3"
          >
            <Sparkles class="w-6 h-6" />
            Спецпредложение: консультация за донат до 31 марта
          </p>
        </div>
      </div>
    </section>

    <!-- FAQ -->
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
              @click="toggleAccordion(i)"
              class="w-full py-6 flex items-center justify-between text-left hover:text-brand-accent transition-colors"
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
              @click="scrollToContact"
              class="bg-transparent text-brand-accent px-8 py-4 rounded-xl font-semibold hover:bg-brand-accent/10 transition-all"
            >
              Задать свой вопрос
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Confidentiality -->
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
            не передаётся третьим лицам. Вы можете быть уверены в безопасности и
            анонимности.
          </p>
        </div>
      </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
      <div class="max-w-7xl mx-auto">
        <div class="max-w-2xl mx-auto text-center mb-12 md:mb-14">
          <h2 class="text-3xl md:text-4xl mb-4">Напишите мне</h2>
          <p class="text-lg text-brand-muted leading-relaxed">
            Хотите обсудить запрос или задать вопрос? Выберите удобный
            мессенджер или соцсеть — отвечу в личных сообщениях, и мы согласуем
            формат и время работы.
          </p>
        </div>

        <div class="grid sm:grid-cols-3 gap-6 max-w-4xl mx-auto mb-16 md:mb-20">
          <a
            v-for="m in messengerLinks"
            :key="m.label"
            :href="m.href"
            :target="m.href !== '#' ? '_blank' : undefined"
            :rel="m.href !== '#' ? 'noopener noreferrer' : undefined"
            class="group flex flex-col items-center text-center p-8 bg-white rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-lg hover:border-brand-accent/25 transition-all duration-300"
          >
            <div
              class="w-14 h-14 mb-5 rounded-2xl bg-brand-accent/10 flex items-center justify-center text-brand-accent group-hover:bg-brand-accent group-hover:text-white transition-colors"
            >
              <Send v-if="m.icon === 'telegram'" class="w-7 h-7" />
              <svg
                v-else-if="m.icon === 'vk'"
                class="w-7 h-7 fill-current"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M13.162 18.994c-6.098 0-9.57-4.172-9.714-11.109h3.01c.107 5.089 2.348 7.248 4.122 7.693V7.885h2.833v4.393c1.734-.185 3.578-2.185 4.193-4.393h2.833c-.456 3.259-2.861 5.259-4.193 6.03 1.332.771 4.05 2.481 5.014 5.079h-3.117c-.752-2.348-2.622-4.172-5.143-4.425v4.425h-2.839z"
                />
              </svg>
              <MessageCircle v-else class="w-7 h-7" />
            </div>
            <span class="font-display font-bold text-lg text-brand-text mb-2">{{
              m.label
            }}</span>
            <span class="text-sm text-brand-muted leading-snug">{{
              m.description
            }}</span>
            <span
              class="mt-4 text-sm font-semibold text-brand-accent group-hover:underline underline-offset-2"
            >
              Открыть чат
            </span>
          </a>
        </div>

        <div
          class="max-w-2xl mx-auto text-center mb-10 pt-4 border-t border-black/10"
        >
          <div
            class="inline-flex items-center justify-center gap-2 text-brand-accent mb-3"
          >
            <Compass class="w-6 h-6" aria-hidden="true" />
            <h3 class="text-2xl md:text-3xl font-display font-bold">
              «Компас Души»
            </h3>
          </div>
          <p class="text-lg text-brand-muted leading-relaxed">
            Присоединяйтесь к личным каналам «Компас Души» — материалы, практики
            и вдохновение в тех же мессенджерах и соцсетях, где вам удобно.
          </p>
        </div>

        <div class="grid sm:grid-cols-3 gap-6 max-w-4xl mx-auto mb-16 md:mb-20">
          <a
            v-for="m in compassChannelLinks"
            :key="'compass-' + m.label"
            :href="m.href"
            :target="m.href !== '#' ? '_blank' : undefined"
            :rel="m.href !== '#' ? 'noopener noreferrer' : undefined"
            class="group flex flex-col items-center text-center p-8 bg-white rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-lg hover:border-brand-accent/25 transition-all duration-300"
          >
            <div
              class="w-14 h-14 mb-5 rounded-2xl bg-brand-accent/10 flex items-center justify-center text-brand-accent group-hover:bg-brand-accent group-hover:text-white transition-colors"
            >
              <Send v-if="m.icon === 'telegram'" class="w-7 h-7" />
              <svg
                v-else-if="m.icon === 'vk'"
                class="w-7 h-7 fill-current"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M13.162 18.994c-6.098 0-9.57-4.172-9.714-11.109h3.01c.107 5.089 2.348 7.248 4.122 7.693V7.885h2.833v4.393c1.734-.185 3.578-2.185 4.193-4.393h2.833c-.456 3.259-2.861 5.259-4.193 6.03 1.332.771 4.05 2.481 5.014 5.079h-3.117c-.752-2.348-2.622-4.172-5.143-4.425v4.425h-2.839z"
                />
              </svg>
              <MessageCircle v-else class="w-7 h-7" />
            </div>
            <span class="font-display font-bold text-lg text-brand-text mb-2">
              {{ m.label }}
            </span>
            <span
              class="mt-2 text-sm font-semibold text-brand-accent group-hover:underline underline-offset-2"
            >
              {{ m.cta }}
            </span>
          </a>
        </div>

        <div
          class="max-w-3xl mx-auto flex flex-col md:flex-row gap-12 md:gap-16 justify-center items-start"
        >
          <div class="space-y-8 w-full md:flex-1">
            <a href="tel:+79991234567" class="flex items-start gap-6 group">
              <div
                class="w-12 h-12 bg-brand-accent/10 rounded-xl flex items-center justify-center text-brand-accent shrink-0 group-hover:bg-brand-accent group-hover:text-white transition-all"
              >
                <Phone class="w-6 h-6" />
              </div>
              <div>
                <p class="text-sm text-brand-muted mb-1">Телефон</p>
                <p class="text-xl font-medium">+7 (999) 123-45-67</p>
              </div>
            </a>

            <a
              href="mailto:hello@soultherapy.ru"
              class="flex items-start gap-6 group"
            >
              <div
                class="w-12 h-12 bg-brand-accent/10 rounded-xl flex items-center justify-center text-brand-accent shrink-0 group-hover:bg-brand-accent group-hover:text-white transition-all"
              >
                <Mail class="w-6 h-6" />
              </div>
              <div>
                <p class="text-sm text-brand-muted mb-1">Email</p>
                <p class="text-xl font-medium">hello@soultherapy.ru</p>
              </div>
            </a>
          </div>

          <div
            class="w-full md:flex-1 p-6 bg-white rounded-2xl border border-black/5 shadow-sm"
          >
            <div class="space-y-1">
              <p class="text-sm font-semibold text-brand-accent">
                Наталья Короткова
              </p>
              <p class="text-xs text-brand-muted leading-relaxed">
                Самозанятая, г. Москва<br />
                ИНН: 772775846428
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer
      class="py-12 px-6 md:px-12 lg:px-24 border-t border-black/5 bg-white"
    >
      <div
        class="max-w-7xl mx-auto flex flex-col items-center text-center gap-2"
      >
        <p class="text-brand-muted text-sm">
          © 2026 Наталья Короткова. Все права защищены.
        </p>
        <a
          href="https://korotkovladimir.ru/"
          target="_blank"
          rel="noopener noreferrer"
          class="text-xs text-brand-muted hover:text-brand-accent transition-colors"
        >
          Автор сайта: Владимир Коротков
        </a>
      </div>
    </footer>

    <!-- Mobile Sticky CTA -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-y-20 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-20 opacity-0"
    >
      <div
        v-if="showStickyCTA"
        class="fixed bottom-4 left-4 right-4 z-50 md:hidden"
      >
        <button
          @click="scrollToContact"
          class="w-full bg-brand-accent text-white py-4 rounded-xl font-semibold shadow-2xl"
        >
          Написать
        </button>
      </div>
    </transition>

    <!-- Scroll to Top Button -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-y-10 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-10 opacity-0"
    >
      <button
        v-if="showScrollTop"
        @click="scrollToTop"
        class="fixed bottom-6 right-6 z-50 w-12 h-12 bg-white text-brand-accent rounded-full shadow-xl flex items-center justify-center hover:bg-brand-accent hover:text-white transition-all border border-black/5"
        :class="{ 'bottom-24': showStickyCTA && !isMenuOpen }"
      >
        <ChevronUp class="w-6 h-6" />
      </button>
    </transition>

    <Teleport to="body">
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="reviewLightbox"
          class="fixed inset-0 z-[100] flex flex-col items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label="Полный скриншот отзыва"
          @click.self="closeReviewLightbox"
        >
          <button
            type="button"
            class="absolute top-4 right-4 z-10 w-11 h-11 rounded-full bg-white/15 text-white flex items-center justify-center hover:bg-white/25 transition-colors"
            aria-label="Закрыть"
            @click="closeReviewLightbox"
          >
            <X class="w-6 h-6" />
          </button>
          <img
            :src="reviewLightbox.src"
            :alt="reviewLightbox.alt"
            class="max-h-[min(90vh,920px)] w-auto max-w-[min(100vw-2rem,440px)] object-contain rounded-lg shadow-2xl"
          />
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<style>
.font-display {
  font-family: "Manrope", sans-serif;
}
</style>
