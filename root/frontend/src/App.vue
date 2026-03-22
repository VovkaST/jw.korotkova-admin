<script setup lang="ts">
import {
  AboutMethodSection,
  ConfidentialitySection,
  ContactSection,
  ExpertSection,
  FaqSection,
  HeroSection,
  MobileStickyCta,
  PricesSection,
  ProcessSection,
  RequestsSection,
  ReviewsSection,
  ScrollToTopButton,
  SiteFooter,
  SiteNav,
} from "@/components";
import { onMounted, onUnmounted, ref } from "vue";

const isMenuOpen = ref<boolean>(false);
const showStickyCTA = ref<boolean>(true);
const showScrollTop = ref<boolean>(false);

onMounted(() => {
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

  window.addEventListener("scroll", onWindowScroll);
});

function onWindowScroll(): void {
  showScrollTop.value = window.scrollY > 500;
}

onUnmounted(() => {
  window.removeEventListener("scroll", onWindowScroll);
});

const scrollToContact = () => {
  document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" });
  isMenuOpen.value = false;
};

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};
</script>

<template>
  <div class="min-h-screen">
    <SiteNav v-model:menu-open="isMenuOpen" @contact="scrollToContact" />

    <HeroSection @contact="scrollToContact" />
    <AboutMethodSection />
    <RequestsSection @contact="scrollToContact" />
    <ProcessSection />
    <ExpertSection />
    <ReviewsSection />
    <PricesSection @contact="scrollToContact" />
    <FaqSection @contact="scrollToContact" />
    <ConfidentialitySection />
    <ContactSection />
    <SiteFooter />

    <MobileStickyCta :visible="showStickyCTA" @contact="scrollToContact" />

    <ScrollToTopButton
      :visible="showScrollTop"
      :lift-for-sticky="showStickyCTA && !isMenuOpen"
      @click="scrollToTop"
    />
  </div>
</template>

<style>
.font-display {
  font-family: "Manrope", sans-serif;
}
</style>
