<script setup lang="ts">
import { Compass, Mail, MessageCircle, Phone, Send } from "lucide-vue-next";

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
</script>

<template>
  <section id="contact" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
    <div class="max-w-7xl mx-auto">
      <div class="max-w-2xl mx-auto text-center mb-12 md:mb-14">
        <h2 class="text-3xl md:text-4xl mb-4">Напишите мне</h2>
        <p class="text-lg text-brand-muted leading-relaxed">
          Хотите обсудить запрос или задать вопрос? Выберите удобный мессенджер
          или соцсеть&nbsp;&mdash; отвечу в&nbsp;личных сообщениях,
          и&nbsp;мы&nbsp;согласуем формат и&nbsp;время работы.
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
          Присоединяйтесь к&nbsp;личным каналам &laquo;Компас
          Души&raquo;&nbsp;&mdash; материалы, практики и&nbsp;вдохновение
          в&nbsp;тех&nbsp;же мессенджерах и&nbsp;соцсетях, где вам удобно.
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
</template>
