<script setup lang="ts">
const props = defineProps<{
  text: string
}>();

const showAlert = inject<boolean>("showAlert");
</script>

<template>
  <div>
    <v-alert
      v-model="showAlert"
      border="start"
      closable
      color="deep-purple-accent-4"
      max-height="200px"
      title="Information"
      variant="tonal"
    >
      <div class="content">
        {{ props.text }}
      </div>
    </v-alert>
  </div>
</template>

<style scoped>
.content {
  max-height: 200px;
  white-space: pre-line; /* This will respect newlines in your text */
  overflow-y: auto;
}

.content::-webkit-scrollbar {
  display: none;
}
</style>
