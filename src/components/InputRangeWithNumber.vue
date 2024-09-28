<script setup lang="ts">
const props = defineProps<{
  min: number,
  max: number,
  step: number,
  provideKey: string
}>();

const amount = inject<number>(props.provideKey);
</script>

<template>
  <div>
    <InputText
      id="number"
      label="Bet"
      :max="props.max"
      :model-value="amount"
      oninput="range.value = number.value"
      placeholder="Chips"
      :provide-key="props.provideKey"
      type="number"
    />
    <InputText
      id="range"
      :max="props.max"
      :min="props.min"
      :model-value="amount"
      oninput="number.value = range.value"
      :provide-key="props.provideKey"
      :step="props.step"
      type="range"
    />
  </div>
</template>
