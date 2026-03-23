<script setup lang="ts">
import { Award, Quote } from "lucide-vue-next";
</script>

<template>
  <section id="expert" class="py-20 px-6 md:px-12 lg:px-24 bg-brand-beige">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl md:text-4xl text-center mb-16">Обо мне</h2>
      <div
        class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12 md:gap-4 items-center"
      >
        <div class="aspect-square rounded-3xl overflow-hidden shadow-xl">
          <img
            src="/SpecialistPhoto.jpg"
            alt="Наталья Короткова"
            class="w-full h-full object-cover lg:object-[calc(50%+105px)_center] md:object-[calc(50%+75px)_center] object-[calc(50%+105px)_center]"
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
            Меня зовут Наталья Короткова. Работаю с&nbsp;мировоззрением
            и&nbsp;помогаю обрести внутреннюю гармонию, научиться управлять
            своей жизнью осознанно, бережно заглянуть вглубь себя, открыть свое
            сердце для любви и&nbsp;понимания, освободиться от&nbsp;барьеров
            на&nbsp;пути к&nbsp;себе.
          </p>

          <div class="space-y-4">
            <h4 class="font-bold text-lg">Образование:</h4>
            <ul class="space-y-2 text-brand-muted">
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span>Диплом по методу «Терапия Души»</span>
              </li>
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span>
                  Диплом о повышении квалификации «Психолог-консультант»
                </span>
              </li>
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span> Сертификат Цифровая психология: «Код личности» </span>
              </li>
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span>
                  Сертификат «Основы работы с психологическим портретом»
                </span>
              </li>
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span> Сертификат «Проработка связок, паттернов» </span>
              </li>
              <li class="flex items-start gap-3">
                <Award class="w-5 h-5 text-brand-accent shrink-0 mt-1" />
                <span>
                  Свидетельство о прохождении программы «Метод легализации
                  правды»
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
