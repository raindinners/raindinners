<script setup lang="ts">
import InputRangeWithNumber from "@/components/InputRangeWithNumber.vue";

const actionAmount = ref<number>(20);
provide("actionAmount", actionAmount);
</script>

<template>
  <div>
    <InputRangeWithNumber provide-key="actionAmount" />
  </div>
</template>
