<script setup lang="ts">
const emits = defineEmits(["update:modelValue"]);
const props = defineProps<{
  modelValue: any,
  id: string,
  label?: string,
  type?: string,
  placeholder?: string,
  validation?: Function,
  min?: number,
  max?: number,
  step?: number,
  provideKey: string
}>();

const modelValue = inject(props.provideKey);
const getType = computed(() => {
  return props.type ? props.type : "text";
});
const validate = computed(() => {
  return props.validation && props.validation(modelValue.value).valid;
});

const rules = [value => (value && validate) || "Required"];
</script>

<template>
  <div class="inputContainer">
    <VTextField
      v-if="props.type == 'range'"
      :id="id"
      v-model="modelValue"
      :max="props.max"
      :min="props.min"
      :step="props.step"
      :type="getType"
      @input="emits('update:modelValue', $event.target.value)"
    />
    <VTextField
      v-else
      :id="id"
      v-model="modelValue"
      :label="props.label"
      :placeholder="props.placeholder"
      :rules="rules"
      :type="getType"
      @blur="validate"
      @input="emits('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<style scoped>
.inputContainer {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 256px;
}

</style>
