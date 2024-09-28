<script setup lang="ts">
const props = defineProps<{
  sbBet: number,
  bbBet: number,
  minRaise: number
}>();
</script>

<template>
  <span>
    Small Blind: <strong>{{ props.sbBet }}</strong> | Big Blind: <strong>{{
      props.bbBet
    }}</strong> | Min Raise: <strong>{{ props.minRaise }}</strong>
  </span>
</template>
