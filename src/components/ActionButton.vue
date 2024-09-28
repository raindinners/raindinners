<script setup lang="ts">
import { Action } from "@/enums/action";
import { Position } from "@/enums/position";

const props = defineProps<{
  action: Action,
  actionAmount: number,
  actionPosition: Position
}>();

const executeAction = inject<{(action: Action, amount: number, position: Position): void }>("executeAction");
</script>

<template>
  <VBtn
    class="actionButton"
    @click="executeAction(props.action, props.actionAmount, props.actionPosition)"
  >
    <slot />
  </VBtn>
</template>
