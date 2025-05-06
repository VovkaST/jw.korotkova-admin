<script setup lang="ts"></script>

<template>
  <div class="info-container image-left">
    <h2 v-if="$slots.header" class="info-container__header mb-2 ps-5">
      <slot name="header" />
    </h2>
    <div class="info-container__content d-flex flex-row align-items-center justify-content-between">
      <div v-if="$slots['image-left']" class="info-image left">
        <div class="inner-circle">
          <slot name="image-left" />
        </div>
      </div>
      <div class="info-text">
        <slot name="text" />
      </div>
      <div v-if="$slots['image-right']" class="info-image right">
        <div class="inner-circle">
          <slot name="image-right" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
$borderColor: #939393;

.info {
  &-container {
    border-top: 1px solid $borderColor;

    &__header {
      margin-top: 2rem;
      text-transform: uppercase;
    }

    &__content {
      .info-image {
        padding: 10px;
        border: 1px solid $borderColor;
        border-radius: 50%;
        height: 384px;
        overflow: hidden;
        flex-basis: 30%;

        .inner-circle {
          height: 100%;
          border-radius: 50%;
          overflow: hidden;
        }

        img {
          height: 100%;
        }

        &.left + .info-text {
          padding-left: 20px;
          padding-right: 10px;
        }
      }

      .info-text {
        padding: 0 20px 0 10px;
        flex-basis: 70%;
        line-height: 2;
      }
    }
  }
}
</style>
