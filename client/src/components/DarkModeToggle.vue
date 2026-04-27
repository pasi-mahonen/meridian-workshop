<template>
  <button class="dark-mode-toggle" @click="toggle" :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
    {{ isDark ? 'Light' : 'Dark' }}
  </button>
</template>

<script>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'meridian-dark-mode'

export default {
  name: 'DarkModeToggle',
  setup() {
    const isDark = ref(false)

    const applyDark = (value) => {
      if (value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      isDark.value = value
    }

    const toggle = () => {
      const next = !isDark.value
      applyDark(next)
      localStorage.setItem(STORAGE_KEY, next ? '1' : '')
    }

    onMounted(() => {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored === '1') {
        applyDark(true)
      }
    })

    return { isDark, toggle }
  }
}
</script>

<style scoped>
.dark-mode-toggle {
  padding: 0.375rem 0.875rem;
  font-size: 0.813rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 0.75rem;
  white-space: nowrap;
}

.dark-mode-toggle:hover {
  color: #0f172a;
  border-color: #cbd5e1;
  background: #f1f5f9;
}
</style>
