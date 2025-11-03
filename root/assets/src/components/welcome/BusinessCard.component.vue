<script setup lang="ts"></script>

<template>
  <div class="business-card-container d-flex flex-row justify-content-end align-items-center">
    <div class="business-card-container__info">
      <div class="name">Наталья Короткова</div>
      <div class="position">Дизайнер индивидуальных украшений</div>
    </div>
    <div class="business-card-container__image">
      <img src="/BusinessCardPhoto.jpg" alt="JW.Korotkova" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.business-card-container {
  background: linear-gradient(to top, #b3b3a8 20%, #bfbfb8 50%, #bab8ae 80%);
  margin-top: 1.5rem;

  &__image {
    width: 50%;

    img {
      width: 100%;
      object-fit: cover;
      mask-image: radial-gradient(
        circle at center,
        rgba(0, 0, 0, 1) 0%,
        rgba(0, 0, 0, 1) 70%,
        rgba(0, 0, 0, 0) 100%
      );
    }
  }

  &__info {
    margin-left: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    width: 50%;

    .name {
      font-size: 4rem;
      line-height: 4rem;
      font-weight: 400;
    }

    .position {
      margin-top: 2rem;
      font-size: 1.7rem;
      line-height: 2rem;
    }
  }
}

@media (max-width: 1024px) {
  .business-card-container {
    margin-top: 0;

    &__info {
      margin-left: 2.5rem;

      .name {
        font-size: 3rem;
        line-height: 3rem;
      }

      .position {
        margin-top: 1rem;
        font-size: 1.5rem;
        line-height: 1.8rem;
      }
    }

    &__image {
      width: 70%;
    }
  }
}
</style>
