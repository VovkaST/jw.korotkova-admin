<script setup lang="ts"></script>

<template>
  <div class="business-card-container d-flex">
    <div class="business-card-container__info">
      <div class="name">Наталья Короткова</div>
      <div class="position">Дизайнер индивидуальных украшений</div>
    </div>
    <div class="business-card-container__image">
      <img src="/assets/images/BusinessCardPhoto.jpg" alt="JW.Korotkova" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.business-card-container {
  background: linear-gradient(to top, #b3b3a8 20%, #bfbfb8 50%, #bab8ae 80%);
  margin-top: 1.5rem;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  position: relative;

  &__image {
    width: 50%;
    overflow: hidden;

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

@media (max-width: 767px) {
  .business-card-container {
    flex-direction: column-reverse;

    &__info {
      margin-left: 1.5rem;
      align-self: flex-start;
      align-items: flex-start;
      position: absolute;
      z-index: 10;
      bottom: calc(50% - 6rem);
      width: 33%;

      .position {
        font-size: 1rem;
        line-height: 1.3rem;
      }
    }

    &__image {
      width: 95%;
      align-self: flex-end;

      img {
        width: 110%;
      }
    }
  }
}

@media (max-width: 550px) {
  .business-card-container {
    &__info {
      .name {
        font-size: 2.5rem;
      }
    }
  }
}

@media (max-width: 470px) {
  .business-card-container {
    &__info {
      bottom: calc(50% - 5rem);

      .name {
        font-size: 2.1rem;
        line-height: 2rem;
      }
      .position {
        font-size: 0.9rem;
        line-height: 1.2rem;
      }
    }
  }
}
</style>
