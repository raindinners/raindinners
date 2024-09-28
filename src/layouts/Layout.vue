<template>
  <div class="content">
    <RouterView />
  </div>
</template>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: calc(100vh - 60px);
}
</style>
