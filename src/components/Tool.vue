<script setup lang="ts">
const props = defineProps<{
  tabs: { id: number, label: string}[]
}>();

const currentTab = inject("currentTab");
</script>

<template>
  <VContainer fluid>
    <VTabs
      v-model="currentTab"
      background-color="deep-purple accent-4"
      dark
      slider-color="yellow"
    >
      <VTab
        v-for="tab in props.tabs"
        :key="tab.id"
        :value="tab.id"
      >
        {{ tab.label }}
      </VTab>
    </VTabs>
  </VContainer>
</template>
