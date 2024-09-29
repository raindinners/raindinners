<script setup lang="ts">
import Card from "./Card.vue";
import { getEnumName } from "@/utils/enumName";
import { Position } from "@/enums/position";

const props = defineProps<{
  id: string,
  back?: string,
  front?: string
}>();
</script>

<template>
  <div>
    <span>#{{ props.id }}</span>
    <div class="cards">
      <Card :card="props.back" />
      <Card :card="props.front" />
    </div>
  </div>
</template>

<style scoped>
.cards {
  display: flex;
  gap: 1px;
}
</style>
