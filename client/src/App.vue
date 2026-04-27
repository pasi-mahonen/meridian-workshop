<template>
  <div class="app">
    <header class="top-nav">
      <div class="nav-container">
        <div class="logo">
          <h1>{{ t('nav.companyName') }}</h1>
          <span class="subtitle">{{ t('nav.subtitle') }}</span>
        </div>
        <nav class="nav-tabs">
          <router-link to="/" :class="{ active: $route.path === '/' }">
            {{ t('nav.overview') }}
          </router-link>
          <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }">
            {{ t('nav.inventory') }}
          </router-link>
          <router-link to="/orders" :class="{ active: $route.path === '/orders' }">
            {{ t('nav.orders') }}
          </router-link>
          <router-link to="/spending" :class="{ active: $route.path === '/spending' }">
            {{ t('nav.finance') }}
          </router-link>
          <router-link to="/demand" :class="{ active: $route.path === '/demand' }">
            {{ t('nav.demandForecast') }}
          </router-link>
          <router-link to="/reports" :class="{ active: $route.path === '/reports' }">
            {{ t('nav.reports') }}
          </router-link>
          <router-link to="/restocking" :class="{ active: $route.path === '/restocking' }">
            {{ t('nav.restocking') }}
          </router-link>
        </nav>
        <LanguageSwitcher />
        <DarkModeToggle />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </header>
    <FilterBar />
    <main class="main-content">
      <router-view />
    </main>

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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-nav {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 2rem;
  height: 70px;
}

.nav-container > .nav-tabs {
  margin-left: auto;
  margin-right: 1rem;
}

.nav-container > .language-switcher {
  margin-right: 1rem;
}

.logo {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.logo h1 {
  font-size: 1.375rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.subtitle {
  font-size: 0.813rem;
  color: #64748b;
  font-weight: 400;
  padding-left: 0.75rem;
  border-left: 1px solid #e2e8f0;
}

.nav-tabs {
  display: flex;
  gap: 0.25rem;
}

.nav-tabs a {
  padding: 0.625rem 1.25rem;
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.938rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-tabs a:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.nav-tabs a.active {
  color: #2563eb;
  background: #eff6ff;
}

.nav-tabs a.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #2563eb;
}

.main-content {
  flex: 1;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: #64748b;
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.25rem;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #0f172a;
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
  background: white;
  border-radius: 10px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.25rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
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
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: 6px;
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
  color: #64748b;
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.938rem;
}

/* Dark mode overrides */
html.dark body {
  background: #0f172a;
  color: #e2e8f0;
}

html.dark .top-nav {
  background: #1e293b;
  border-color: #334155;
}

html.dark .card,
html.dark .stat-card {
  background: #1e293b;
  border-color: #334155;
}

html.dark .card-title {
  color: #f1f5f9;
}

html.dark .card-header {
  border-color: #334155;
}

html.dark table thead {
  background: #1e293b;
}

html.dark th {
  color: #94a3b8;
}

html.dark td {
  color: #cbd5e1;
  border-color: #1e293b;
}

html.dark tbody tr:hover {
  background: #1e293b;
}

html.dark .nav-tabs a {
  color: #94a3b8;
}

html.dark .nav-tabs a.active {
  color: #60a5fa;
  background: #1e3a5f;
}

html.dark .logo h1 {
  color: #f1f5f9;
}

html.dark .subtitle {
  color: #94a3b8;
}

html.dark .page-header h2 {
  color: #f1f5f9;
}

html.dark .page-header p {
  color: #94a3b8;
}

/* FilterBar */
html.dark .filters-bar {
  background: #1e293b;
  border-color: #334155;
}

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

html.dark .task-input {
  border-color: #475569;
  background: #0f172a;
  color: #e2e8f0;
}

html.dark .task-item {
  background: #0f172a;
  border-color: #334155;
}

html.dark .task-item:hover {
  background: #1e293b;
  border-color: #475569;
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

html.dark .stat-card {
  background: #1e293b;
}

html.dark .stat-label {
  color: #94a3b8;
}

html.dark .stat-value {
  color: #f1f5f9;
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
  border-color: #334155;
}

html.dark .dark-mode-toggle:hover {
  color: #e2e8f0;
  border-color: #475569;
  background: #1e293b;
}

html.dark .language-button,
html.dark .profile-button {
  background: #1e293b;
  border-color: #334155;
  color: #cbd5e1;
}

html.dark .language-button:hover,
html.dark .profile-button:hover {
  background: #334155;
  border-color: #475569;
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
