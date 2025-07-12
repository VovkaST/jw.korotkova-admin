<script setup lang="ts"></script>

<template>
  <div class="business-card-container d-flex flex-row justify-content-end align-items-center">
    <div class="business-card-container__image">
      <img src="/internals-logo.png" alt="JW.Korotkova" />
    </div>
    <div class="business-card-container__info">
      <div class="name">Наталья Короткова</div>
      <div class="position">Дизайнер индивидуальных украшений</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.business-card-container {
  &__image {
    width: 50%;

    img {
      width: 100%;
    }
  }

  &__info {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    width: 50%;

    .name {
      font-size: 4rem;
      line-height: 4rem;
      font-weight: 300;
    }

    .position {
      margin-top: 2rem;
      font-size: 2rem;
      line-height: 2rem;
    }
  }
}
</style>
