<script setup lang="ts">
import { ChevronLeft, ChevronRight, X, ZoomIn } from "lucide-vue-next";
import { onMounted, onUnmounted, ref, watch } from "vue";
import { ReviewsService } from "@/api/v1/reviews";
import type { ReviewDto } from "@/api/v1/client";

const reviewSlideIndex = ref<number>(0);
const reviewLightbox = ref<{ src: string; alt: string } | null>(null);

const reviewItems = ref<ReviewDto[]>([]);
const reviewsLoading = ref<boolean>(true);
const reviewsError = ref<boolean>(false);
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

onMounted(() => {
  void loadReviews();
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
</script>

<template>
  <section id="reviews" class="py-20 px-6 md:px-12 lg:px-24 bg-white">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-4">Отзывы</h2>
      <p
        class="text-center text-brand-muted max-w-2xl mx-auto mb-12 md:mb-14 leading-relaxed"
      >
        Большинство отзывов приходит в&nbsp;личные сообщения&nbsp;&mdash;
        поэтому здесь собраны скриншоты переписки с&nbsp;телефона.
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
</template>
