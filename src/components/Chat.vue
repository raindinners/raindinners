<script setup lang="ts">
const props = defineProps<{
  log: { title: string, text: string }[]
}>();
</script>

<template>
  <div class="chat">
    <div class="messages">
      <div v-for="(message, index) in props.log" :key="index" class="message">
        <strong>{{ message.title }}:</strong> {{ message.text }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat {
  margin-top: auto;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

.messages {
  display: flex;
  flex-direction: column;
}

.message {
  padding: 1px;
}
</style>
