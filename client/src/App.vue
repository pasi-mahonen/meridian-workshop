<template>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-mark">MC</div>
        <div class="brand-text">
          <span class="brand-name">{{ t('nav.companyName') }}</span>
          <span class="brand-sub">{{ t('nav.subtitle') }}</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" :class="{ active: $route.path === '/' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          {{ t('nav.overview') }}
        </router-link>
        <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
          {{ t('nav.inventory') }}
        </router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
          {{ t('nav.orders') }}
        </router-link>
        <router-link to="/spending" :class="{ active: $route.path === '/spending' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          {{ t('nav.finance') }}
        </router-link>
        <router-link to="/demand" :class="{ active: $route.path === '/demand' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
          {{ t('nav.demandForecast') }}
        </router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
          {{ t('nav.reports') }}
        </router-link>
        <router-link to="/restocking" :class="{ active: $route.path === '/restocking' }">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          {{ t('nav.restocking') }}
        </router-link>
      </nav>

    </aside>

    <div class="content-wrapper">
      <FilterBar>
        <template #controls>
          <LanguageSwitcher />
          <DarkModeToggle />
          <ProfileMenu
            @show-profile-details="showProfileDetails = true"
            @show-tasks="showTasks = true"
          />
        </template>
      </FilterBar>
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import DarkModeToggle from './components/DarkModeToggle.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher,
    DarkModeToggle
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
/* ============================================================
   DESIGN TOKENS — edit here, cascade everywhere
   ============================================================ */
:root {
  --color-primary:        #2563eb;
  --color-primary-light:  #eff6ff;
  --color-primary-hover:  #1d4ed8;
  --color-bg:             #f1f5f9;
  --color-chrome:         #f8fafc;
  --color-surface:        #ffffff;
  --color-surface-raised: #ffffff;
  --color-border:         #e2e8f0;
  --color-border-subtle:  #f1f5f9;
  --color-text-primary:   #0f172a;
  --color-text-secondary: #64748b;
  --color-text-tertiary:  #94a3b8;
  --color-success:        #10b981;
  --color-warning:        #f59e0b;
  --color-danger:         #ef4444;
  --shadow-sm:            0 1px 2px 0 rgba(0,0,0,.05);
  --shadow-md:            0 4px 12px 0 rgba(0,0,0,.08);
  --shadow-lg:            0 8px 24px 0 rgba(0,0,0,.10);
  --radius-sm:            8px;
  --radius-md:            12px;
}

html.dark {
  --color-bg:             #0f172a;
  --color-chrome:         #1e293b;
  --color-surface:        #1e293b;
  --color-surface-raised: #1e293b;
  --color-border:         #334155;
  --color-border-subtle:  #1e293b;
  --color-text-primary:   #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-tertiary:  #64748b;
  --shadow-sm:            0 1px 2px 0 rgba(0,0,0,.20);
  --shadow-md:            0 4px 12px 0 rgba(0,0,0,.30);
  --shadow-lg:            0 8px 24px 0 rgba(0,0,0,.40);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--color-bg);
  color: var(--color-text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ============================================================
   APP LAYOUT — sidebar + content
   ============================================================ */
.app {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: var(--color-chrome);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: sticky;
  top: 0;
  overflow: visible;
  z-index: 100;
}

html.dark .sidebar {
  background: #1e293b;
  border-right-color: rgba(255,255,255,0.06);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.375rem 1.25rem 1.25rem;
  border-bottom: 1px solid #e2e8f0;
}

html.dark .sidebar-brand {
  border-bottom-color: rgba(255,255,255,0.07);
}

.brand-mark {
  width: 34px;
  height: 34px;
  background: #2563eb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.688rem;
  font-weight: 800;
  color: white;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name {
  font-size: 0.813rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

html.dark .brand-name {
  color: #f1f5f9;
}

.brand-sub {
  font-size: 0.688rem;
  color: #64748b;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav {
  flex: 1;
  padding: 0.875rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  overflow-y: auto;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.563rem 0.75rem;
  border-radius: 8px;
  color: #64748b;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
  position: relative;
}

.sidebar-nav a svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  opacity: 0.7;
}

.sidebar-nav a:hover {
  background: rgba(0,0,0,0.04);
  color: #0f172a;
}

.sidebar-nav a:hover svg {
  opacity: 1;
}

.sidebar-nav a.active {
  background: #eff6ff;
  color: #2563eb;
}

.sidebar-nav a.active svg {
  opacity: 1;
}

.sidebar-nav a.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: #2563eb;
  border-radius: 0 2px 2px 0;
}

html.dark .sidebar-nav a              { color: #94a3b8; }
html.dark .sidebar-nav a svg          { opacity: 0.8; }
html.dark .sidebar-nav a:hover        { background: rgba(255,255,255,0.06); color: #cbd5e1; }
html.dark .sidebar-nav a.active       { background: rgba(37,99,235,0.18); color: #60a5fa; }
html.dark .sidebar-nav a.active::before { background: #3b82f6; }

/* ============================================================
   CONTENT AREA
   ============================================================ */
.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
}

/* ============================================================
   GLOBAL COMPONENT STYLES
   ============================================================ */
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: var(--color-surface);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.stat-card.warning { border-top-color: #ea580c; }
.stat-card.success { border-top-color: #059669; }
.stat-card.danger  { border-top-color: #dc2626; }
.stat-card.info    { border-top-color: var(--color-primary); }

.stat-label {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: #ea580c;
}

.stat-card.success .stat-value {
  color: #059669;
}

.stat-card.danger .stat-value {
  color: #dc2626;
}

.stat-card.info .stat-value {
  color: #2563eb;
}

.card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.25rem;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  padding-left: 0.75rem;
  border-bottom: 1px solid var(--color-border);
  border-left: 3px solid var(--color-primary);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--color-border-subtle);
  color: var(--color-text-primary);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--color-primary-light);
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: #d1fae5;
  color: #065f46;
}

.badge.warning {
  background: #fed7aa;
  color: #92400e;
}

.badge.danger {
  background: #fecaca;
  color: #991b1b;
}

.badge.info {
  background: #dbeafe;
  color: #1e40af;
}

.badge.increasing {
  background: #d1fae5;
  color: #065f46;
}

.badge.decreasing {
  background: #fecaca;
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: #fecaca;
  color: #991b1b;
}

.badge.medium {
  background: #fed7aa;
  color: #92400e;
}

.badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-secondary);
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 1rem;
  border-radius: var(--radius-sm);
  margin: 1rem 0;
  font-size: 0.938rem;
}

/* ============================================================
   DARK MODE — structural overrides needed to beat scoped
   component styles (global token cascade loses to scoped
   selectors with higher specificity)
   ============================================================ */
html.dark .card,
html.dark .stat-card {
  background: #1e293b;
  border-color: #334155;
}

html.dark .stat-card         { border-top-color: var(--color-primary); }
html.dark .stat-card.warning { border-top-color: #ea580c; }
html.dark .stat-card.success { border-top-color: #059669; }
html.dark .stat-card.danger  { border-top-color: #dc2626; }

html.dark .card-title {
  color: #f1f5f9;
}

html.dark .card-header {
  border-color: #334155;
}

html.dark .stat-label {
  color: #94a3b8;
}

html.dark .stat-value {
  color: #f1f5f9;
}

/* FilterBar */
html.dark .filter-group label {
  color: #94a3b8;
}

html.dark .filter-select {
  background: #0f172a;
  color: #e2e8f0;
  border-color: #475569;
}

html.dark .filter-select:hover {
  border-color: #64748b;
}

html.dark .reset-filters-btn {
  background: #1e293b;
  border-color: #334155;
  color: #64748b;
}

/* Restocking — scorecard cards */
html.dark .scorecard {
  background: #1e293b;
  border-color: #334155;
}

html.dark .scorecard-label {
  color: #94a3b8;
}

html.dark .scorecard-value {
  color: #f1f5f9;
}

/* Restocking — budget row and controls */
html.dark .budget-row {
  background: #1e293b;
  box-shadow: none;
}

html.dark .budget-label {
  color: #94a3b8;
}

html.dark .budget-input {
  background: #0f172a;
  color: #e2e8f0;
  border-color: #475569;
}

html.dark .currency-symbol {
  color: #94a3b8;
}

html.dark .summary-bar {
  color: #94a3b8;
}

html.dark .summary-item strong {
  color: #f1f5f9;
}

html.dark .summary-divider {
  color: #475569;
}

html.dark .clear-btn {
  background: #334155;
  color: #94a3b8;
}

html.dark .clear-btn:hover {
  background: #475569;
}

/* Restocking — table */
html.dark .restocking-table th {
  background: #1e293b;
  color: #94a3b8;
  border-color: #334155;
}

html.dark .restocking-table td {
  color: #cbd5e1;
  border-color: #334155;
}

html.dark .restocking-table tr:hover {
  background: #1e293b;
}

html.dark .empty-state {
  background: #1e293b;
  color: #94a3b8;
}

/* Input and select elements globally */
html.dark input[type="number"],
html.dark input[type="text"],
html.dark select {
  background: #0f172a;
  color: #e2e8f0;
  border-color: #475569;
}

/* Dashboard — SVG fills */
html.dark .donut-center-label {
  fill: #94a3b8;
}

html.dark .donut-center-value {
  fill: #f1f5f9;
}

/* Dashboard */
html.dark .kpi-card {
  background: #1e293b;
  border-color: #334155;
}

html.dark .kpi-label,
html.dark .kpi-goal,
html.dark .header-meta,
html.dark .section-title,
html.dark .legend-item,
html.dark .legend-item-compact,
html.dark .health-metric-label,
html.dark .h-bar-label,
html.dark .line-bar-label,
html.dark .no-data,
html.dark .no-tasks {
  color: #94a3b8;
}

html.dark .kpi-value,
html.dark .health-metric-value,
html.dark .task-text {
  color: #f1f5f9;
}

html.dark .kpi-progress-bar,
html.dark .h-bar-container {
  background: #334155;
}

html.dark .line-y-axis {
  color: #64748b;
  border-color: #334155;
}

html.dark .line-bar.empty-bar {
  background: #334155;
}

html.dark .line-bar.empty-bar:hover {
  background: #475569;
}

html.dark .clickable-row:hover {
  background: #1e3a5f !important;
}


/* Inventory */
html.dark .search-input {
  background: #0f172a;
  border-color: #475569;
  color: #e2e8f0;
}

html.dark .search-input:focus {
  background: #1e293b;
  border-color: #3b82f6;
}

html.dark .search-input::placeholder {
  color: #475569;
}

html.dark .clear-search:hover {
  background: #334155;
  color: #94a3b8;
}

/* Orders */
html.dark .items-dropdown {
  background: #1e293b;
  border-color: #334155;
}

html.dark .item-entry {
  border-color: #334155;
}

html.dark .item-name {
  color: #e2e8f0;
}

html.dark .item-meta {
  color: #94a3b8;
}

/* Demand */
html.dark .trend-card {
  background: #1e293b;
  border-color: #334155;
}

html.dark .increasing-card .trend-icon {
  background: #064e3b;
}

html.dark .stable-card .trend-icon {
  background: #1e3a5f;
}

html.dark .decreasing-card .trend-icon {
  background: #7f1d1d;
}

html.dark .trend-label {
  color: #94a3b8;
}

html.dark .trend-count {
  color: #f1f5f9;
}

html.dark .trend-item {
  background: #0f172a;
  border-color: #334155;
}

html.dark .trend-item:hover {
  background: #1e293b;
}

html.dark .more-items {
  color: #64748b;
}

/* Reports */
html.dark .reports-table th {
  background: #1e293b;
  color: #94a3b8;
  border-color: #334155;
}

html.dark .reports-table td {
  border-color: #334155;
}

html.dark .reports-table tr:hover {
  background: #1e293b;
}

html.dark .bar-label {
  color: #94a3b8;
}

html.dark .stat-meta {
  color: #94a3b8;
}

/* Spending */
html.dark .category-name {
  color: #e2e8f0;
}

html.dark .category-bar-container {
  background: #334155;
}

html.dark .transactions-table thead {
  background: #1e293b;
}

html.dark .transactions-table th {
  color: #94a3b8;
  border-color: #334155;
}

html.dark .transactions-table td {
  border-color: #334155;
}

html.dark .transactions-table tbody tr:hover {
  background: #1e293b;
}

html.dark .transactions-table tbody tr.clickable-row:hover {
  background: #1e3a5f;
}

html.dark .transaction-id,
html.dark .transaction-vendor,
html.dark .transaction-date {
  color: #94a3b8;
}

html.dark .transaction-description,
html.dark .transaction-amount {
  color: #e2e8f0;
}

html.dark .y-axis {
  color: #64748b;
  border-color: #334155;
}

html.dark .legend-item {
  color: #94a3b8;
}

/* Spending — fix near-invisible border on stat cards */
html.dark .revenue-card,
html.dark .profit-card {
  background: #1e293b;
}

/* Nav controls — dark mode toggle, language switcher, profile menu */
html.dark .dark-mode-toggle {
  color: #94a3b8;
  border-color: rgba(255,255,255,0.1);
}

html.dark .dark-mode-toggle:hover {
  color: #e2e8f0;
  border-color: rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.06);
}

html.dark .language-button,
html.dark .profile-button {
  background: rgba(255,255,255,0.06);
  border-color: rgba(255,255,255,0.1);
  color: #cbd5e1;
}

html.dark .language-button:hover,
html.dark .profile-button:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.2);
}

html.dark .profile-name {
  color: #e2e8f0;
}

html.dark .language-switcher .dropdown-menu,
html.dark .profile-menu .dropdown-menu {
  background: #1e293b;
  border-color: #334155;
}

html.dark .dropdown-header {
  background: #0f172a;
}

html.dark .user-name {
  color: #f1f5f9;
}

html.dark .user-email {
  color: #94a3b8;
}

html.dark .dropdown-divider {
  background: #334155;
}

html.dark .dropdown-item {
  color: #cbd5e1;
}

html.dark .dropdown-item:hover {
  background: #334155;
}

html.dark .dropdown-item.active {
  background: #1e3a5f;
  color: #60a5fa;
}
</style>
