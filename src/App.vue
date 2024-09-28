<script setup lang="ts">
const isScrollDisabled = ref(false);
</script>

<template>
  <VApp id="app">
    <VMain>
      <RouterView />
    </VMain>
  </VApp>
</template>

<style module>
.scrollHidden {
  overflow: hidden;
}
</style>
