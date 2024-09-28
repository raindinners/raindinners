<script setup lang="ts">
import CARD_MAP from "@/helpers/cardMap";

const props = defineProps<{ card?: string}>();

const cardSrc = CARD_MAP[props.card ? props.card.toUpperCase() : "B"];
</script>

<template>
  <div class="card">
    <img alt="Card" :src="cardSrc">
  </div>
</template>

<style scoped>
.card {
  width: 100%; /* Занимает 100% ширины родительского элемента */
  height: auto; /* Высота будет пропорциональна ширине */
  display: flex; /* Центрирует изображение, если необходимо */
  justify-content: center; /* Центрирование по горизонтали */
  align-items: center; /* Центрирование по вертикали */
}

.card img {
  max-width: 100%; /* Не выходит за пределы родительского элемента */
  height: auto; /* Высота будет пропорциональна ширине */
}
</style>
