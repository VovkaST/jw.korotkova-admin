<script setup lang="ts"></script>

<template>
  <div class="welcome-section">
    <div class="welcome-section__inner-wrapper d-flex flex-column align-items-end">
      <div
        class="welcome-section__item welcome-section__top d-flex flex-row flex-nowrap justify-content-between align-items-start mb-3"
      >
        <div class="welcome-section__title alter-font">
          <slot name="title" />
        </div>
        <div class="welcome-section__image">
          <slot name="image" />
        </div>
      </div>
      <hr class="welcome-section__item welcome-section__delimiter" />
      <div class="welcome-section__item welcome-section__bottom mt-3 mb-2">
        <div class="welcome-section__description text-center">
          <slot name="description" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
$borderColor: #939393;

.welcome-section {
  border: 2px solid $borderColor;
  border-radius: 10px;
  padding: 5px;
  margin: 0 auto;
  width: 470px;

  &__inner-wrapper {
    padding: 10px 15px;
    border: 1px solid $borderColor;
  }

  &__item {
    width: 100%;
  }

  &__title {
    font-size: 1.6rem;
    line-height: 1.6rem;
    letter-spacing: 0.05px;
  }

  &__image {
    height: 45px;
    border-radius: 10px;
    overflow: hidden;

    img {
      height: 100%;
    }
  }

  &__description {
    font-size: 1.1rem;
    font-weight: 200;
  }

  &__delimiter {
    width: 60%;
  }
}
</style>
