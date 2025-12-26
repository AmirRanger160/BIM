<template>
  <teleport to="body">
    <div v-if="visible" class="toast" :class="toastClass">
      <div class="toast-content">
        <span class="toast-icon" :class="iconClass">
          <i v-if="type === 'success'" class="icon">✓</i>
          <i v-else-if="type === 'error'" class="icon">✕</i>
          <i v-else-if="type === 'warning'" class="icon">⚠</i>
          <i v-else class="icon">ℹ</i>
        </span>
        <span class="toast-message">{{ message }}</span>
        <button class="toast-close" @click="close">
          <i>✕</i>
        </button>
      </div>
      <div v-if="showProgress" class="toast-progress" :style="{ width: progress + '%' }"></div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'info', // success, error, warning, info
    validator: (val) => ['success', 'error', 'warning', 'info'].includes(val)
  },
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 5000 // milliseconds
  },
  showProgress: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['close']);

const visible = ref(true);
const progress = ref(100);
let closeTimer = null;
let progressTimer = null;

const toastClass = computed(() => {
  return {
    'toast-success': props.type === 'success',
    'toast-error': props.type === 'error',
    'toast-warning': props.type === 'warning',
    'toast-info': props.type === 'info'
  };
});

const iconClass = computed(() => {
  return {
    'icon-success': props.type === 'success',
    'icon-error': props.type === 'error',
    'icon-warning': props.type === 'warning',
    'icon-info': props.type === 'info'
  };
});

const close = () => {
  visible.value = false;
  clearTimers();
  emit('close');
};

const clearTimers = () => {
  if (closeTimer) clearTimeout(closeTimer);
  if (progressTimer) clearInterval(progressTimer);
};

onMounted(() => {
  if (props.duration > 0) {
    closeTimer = setTimeout(() => {
      close();
    }, props.duration);

    if (props.showProgress) {
      const interval = 16; // ~60fps
      const decrement = 100 / (props.duration / interval);
      progressTimer = setInterval(() => {
        progress.value = Math.max(0, progress.value - decrement);
      }, interval);
    }
  }
});

onUnmounted(() => {
  clearTimers();
});
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  min-width: 300px;
  max-width: 500px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
  z-index: 9999;
  overflow: hidden;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast-success {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.toast-error {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.toast-warning {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  color: #856404;
}

.toast-info {
  background-color: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  font-size: 18px;
  font-weight: bold;
}

.icon-success {
  color: #28a745;
}

.icon-error {
  color: #dc3545;
}

.icon-warning {
  color: #ffc107;
}

.icon-info {
  color: #17a2b8;
}

.toast-message {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 16px;
  opacity: 0.7;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.toast-close:hover {
  opacity: 1;
}

.toast-progress {
  height: 3px;
  background: currentColor;
  opacity: 0.5;
  transition: width 0.016s linear;
}

/* RTL Support */
:global([dir="rtl"]) .toast {
  right: auto;
  left: 20px;
}

@media (max-width: 600px) {
  .toast {
    min-width: 280px;
    max-width: calc(100vw - 40px);
    right: 20px;
    left: auto;
  }

  :global([dir="rtl"]) .toast {
    right: auto;
    left: 20px;
  }
}
</style>
