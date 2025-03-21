<script setup lang="ts">
import ActionButton from "./ActionButton.vue";
import InputRangeWithNumber from "./InputRangeWithNumber.vue";
import { Action } from "@/enums/action";
import { Position } from "@/enums/position";
import { Information } from "@/types/information";

const emits = defineEmits(["executeAction"]);
const props = defineProps<{
  information: Information,
}>();

const actionAmount = ref<number>(props.information.traits.min_raise);

provide("executeAction", (action: Action, amount: number, position: Position) => {
  emits("executeAction", action, amount, position);
});
provide("actionAmount", actionAmount);
watch(actionAmount, newActionAmount => {
  actionAmount.value = newActionAmount < props.information.players[props.information.current].behind ? newActionAmount : props.information.players[props.information.current].behind;
});

const getAction = (find: Action) => {
  for (const action of props.information.actions) {
    if (action.action === find) {
      return action;
    }
  }
  return {
    action: Action.NONE,
    amount: 0,
    position: Position.NONE
  };
};
const isInActions = (find: Action): boolean => {
  for (const action of props.information.actions) {
    if (action.action === find) {
      return true;
    }
  }
  return false;
};
</script>

<template>
  <div v-if="isInActions(Action.FOLD) && isInActions(Action.RAISE)">
    <div class="actions">
      <InputRangeWithNumber
        v-if="props.information.traits.min_raise <= props.information.players[props.information.current].behind"
        :max="props.information.players[props.information.current].behind"
        :min="props.information.traits.min_raise"
        provide-key="actionAmount"
        :step="1"
      />
      <VBtnGroup class="actionsButtons">
        <ActionButton
          :action="Action.FOLD"
          :action-amount="getAction(Action.FOLD).amount"
          :action-position="getAction(Action.FOLD).position"
        >
          Fold
        </ActionButton>
        <ActionButton
          :action="Action.CALL"
          :action-amount="getAction(Action.CALL).amount"
          :action-position="getAction(Action.CALL).position"
        >
          Call {{ getAction(Action.CALL).amount }}
        </ActionButton>
        <ActionButton
          v-if="props.information.traits.min_raise <= props.information.players[props.information.current].behind"
          :action="Action.RAISE"
          :action-amount="actionAmount"
          :action-position="getAction(Action.RAISE).position"
        >
          Raise To {{ actionAmount }}
        </ActionButton>
        <ActionButton
          v-else
          :action="Action.RAISE"
          :action-amount="props.information.players[props.information.current].behind"
          :action-position="getAction(Action.RAISE).position"
        >
          Allin
        </ActionButton>
      </VBtnGroup>
    </div>
  </div>
  <div v-else-if="isInActions(Action.BET)">
    <div class="actions">
      <InputRangeWithNumber
        :max="props.information.players[props.information.current].behind"
        :min="props.information.traits.min_raise"
        provide-key="actionAmount"
        :step="1"
      />
      <VBtnGroup class="actionsButtons">
        <ActionButton
          :action="Action.CHECK"
          :action-amount="getAction(Action.CHECK).amount"
          :action-position="getAction(Action.CHECK).position"
        >
          Check
        </ActionButton>
        <ActionButton
          :action="Action.BET"
          :action-amount="actionAmount"
          :action-position="getAction(Action.BET).position"
        >
          Bet {{ actionAmount }}
        </ActionButton>
      </VBtnGroup>
    </div>
  </div>
  <div v-else-if="!isInActions(Action.RAISE)">
    <div class="actions">
      <VBtnGroup class="actionsButtons">
        <ActionButton
          :action="Action.FOLD"
          :action-amount="getAction(Action.FOLD).amount"
          :action-position="getAction(Action.FOLD).position"
        >
          Fold
        </ActionButton>
        <ActionButton
          :action="Action.CALL"
          :action-amount="getAction(Action.CALL).amount"
          :action-position="getAction(Action.CALL).position"
        >
          Call {{ getAction(Action.CALL).amount }}
        </ActionButton>
      </VBtnGroup>
    </div>
  </div>
  <div v-else>
    <div class="actions">
      <InputRangeWithNumber
        v-if="props.information.traits.min_raise <= props.information.players[props.information.current].behind"
        :max="props.information.players[props.information.current].behind"
        :min="props.information.traits.min_raise"
        provide-key="actionAmount"
        :step="1"
      />
      <div class="actionsButtons">
        <ActionButton
          :action="Action.CHECK"
          :action-amount="getAction(Action.CHECK).amount"
          :action-position="getAction(Action.CHECK).position"
        >
          Check
        </ActionButton>
        <ActionButton
          v-if="props.information.traits.min_raise <= props.information.players[props.information.current].behind"
          :action="Action.RAISE"
          :action-amount="actionAmount"
          :action-position="getAction(Action.RAISE).position"
        >
          Raise To {{ actionAmount }}
        </ActionButton>
        <ActionButton
          v-else
          :action="Action.RAISE"
          :action-amount="props.information.players[props.information.current].behind"
          :action-position="getAction(Action.RAISE).position"
        >
          Allin
        </ActionButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.actions {
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 400px;
  bottom: 0;
  left: auto;
  text-align: center;
}

.actionsButtons {
  display: flex;
  flex-direction: row;
  position: relative;
  gap: 5px;
}
</style>
