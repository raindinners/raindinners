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
  height: 20vh;
  max-width: 300px;
  background-color: white;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

.messages {
  display: flex;
  flex-direction: column;
  max-height: calc(20vh - 20px);
  overflow-y: auto;
  margin-bottom: 10px;
}

.message {
  padding: 1px;
  border-bottom: 1px solid #eee;
}
</style>
