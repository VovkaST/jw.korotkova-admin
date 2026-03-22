<script setup lang="ts">
import { Award, Quote } from "lucide-vue-next";
</script>

<template>
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
            Меня зовут Наталья Короткова. Я&nbsp;сертифицированный специалист
            по&nbsp;методу &laquo;Терапия Души&raquo; Евгения Теребенина.
            Помогаю клиентам обрести внутреннюю гармонию и&nbsp;научиться
            управлять своей жизнью осознанно.
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
</template>
