import { ref } from 'vue';

// Store for active toasts
const toasts = ref([]);
let toastId = 0;

export const useToast = () => {
  const add = (message, type = 'info', duration = 5000) => {
    const id = toastId++;
    const toast = {
      id,
      message,
      type,
      duration
    };
    toasts.value.push(toast);
    return id;
  };

  const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  };

  const success = (message, duration = 5000) => add(message, 'success', duration);
  const error = (message, duration = 7000) => add(message, 'error', duration);
  const warning = (message, duration = 6000) => add(message, 'warning', duration);
  const info = (message, duration = 5000) => add(message, 'info', duration);

  return {
    toasts,
    add,
    remove,
    success,
    error,
    warning,
    info
  };
};

export const globalToast = useToast();
