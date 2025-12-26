<template>
  <div class="toast-container">
    <Toast
      v-for="toast in toasts"
      :key="toast.id"
      :type="toast.type"
      :message="toast.message"
      :duration="toast.duration"
      @close="removeToast(toast.id)"
    />
  </div>
</template>

<script setup>
import { watch } from 'vue';
import Toast from './Toast.vue';
import { globalToast, useToast } from '../composables/useToast';
import { apiErrorEmitter } from '../services/api';

const { toasts, remove: removeToast } = useToast();

// Mirror global toasts
watch(globalToast.toasts, (newToasts) => {
  toasts.value = newToasts;
}, { deep: true });

// Listen to API errors and show them as toast notifications
const handleApiError = (error) => {
  if (error.type === 'auth_expired') {
    globalToast.warning(error.message, 5000);
  } else if (error.type === 'network_error') {
    globalToast.error(error.message, 7000);
  } else if (error.type === 'api_error') {
    if (error.status === 400) {
      globalToast.warning(error.message, 5000);
    } else {
      globalToast.error(error.message, 7000);
    }
  }
};

apiErrorEmitter.on(handleApiError);
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9998;
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
  margin-bottom: 10px;
}

@media (max-width: 600px) {
  .toast-container {
    right: auto;
    left: 10px;
  }
}
</style>
