<script setup lang="ts"></script>

<template>
  <div
    class="info-container"
    :class="{ 'circle-left': !!$slots['circle-left'], 'circle-right': !!$slots['circle-right'] }"
  >
    <h2 v-if="$slots.header" class="info-container__header mb-2 px-5">
      <slot name="header" />
    </h2>
    <div class="info-container__content d-flex flex-row align-items-center justify-content-between">
      <div v-if="$slots['circle-left']" class="info-circle left">
        <div class="inner-circle font-handwritten">
          <slot name="circle-left" />
        </div>
      </div>
      <div class="info-text">
        <slot name="text" />
      </div>
      <div v-if="$slots['circle-right']" class="info-circle right">
        <div class="inner-circle font-handwritten">
          <slot name="circle-right" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
$borderColor: #939393;
$borderColorLight: #edebeb;

.info {
  &-container {
    border-top: 1px solid $borderColor;
    padding-top: 2rem;

    &.circle-right {
      [class*='__header'] {
        text-align: center;
      }
    }

    &__header {
      margin-top: 1rem;
      text-transform: uppercase;
    }

    &__content {
      .info-circle {
        padding: 10px;
        border: 1px solid $borderColor;
        border-radius: 50%;
        height: 384px;
        overflow: hidden;
        flex-basis: 30%;

        .inner-circle {
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;

          height: 100%;
          border: 1px solid $borderColorLight;
          border-radius: 50%;
          overflow: hidden;

          font-size: 3.5rem;
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
