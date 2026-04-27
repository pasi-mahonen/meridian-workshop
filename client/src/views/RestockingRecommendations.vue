<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div class="budget-row">
      <div class="budget-input-group">
        <label class="budget-label">{{ t('restocking.budgetLabel') }}</label>
        <div class="budget-field">
          <span class="currency-symbol">{{ currentCurrency === 'JPY' ? '¥' : '$' }}</span>
          <input
            v-model.number="budgetInput"
            type="number"
            min="0"
            step="1000"
            class="budget-input"
            :placeholder="t('restocking.budgetPlaceholder')"
            @keyup.enter="applyBudget"
          />
        </div>
        <button class="apply-btn" @click="applyBudget">{{ t('restocking.applyBudget') }}</button>
        <button v-if="budget > 0" class="clear-btn" @click="clearBudget">✕</button>
      </div>
      <div v-if="!loading && !error" class="summary-bar">
        <span class="summary-item">
          <strong>{{ items.length }}</strong> {{ t('restocking.itemsRecommended') }}
        </span>
        <span class="summary-divider">·</span>
        <span class="summary-item">
          {{ t('restocking.totalCost') }}: <strong>{{ formatCurrency(totalCost) }}</strong>
        </span>
        <span v-if="budget > 0" class="summary-divider">·</span>
        <span v-if="budget > 0" class="summary-item budget-tag">
          {{ t('restocking.budgetLabel') }}: {{ formatCurrency(budget) }}
        </span>
      </div>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="items.length === 0" class="empty-state">{{ t('restocking.noneFound') }}</div>
    <div v-else class="card">
      <div class="table-container">
        <table class="restocking-table">
          <thead>
            <tr>
              <th>{{ t('restocking.table.sku') }}</th>
              <th>{{ t('restocking.table.name') }}</th>
              <th>{{ t('restocking.table.warehouse') }}</th>
              <th class="num">{{ t('restocking.table.stock') }}</th>
              <th class="num">{{ t('restocking.table.reorderPoint') }}</th>
              <th class="num">{{ t('restocking.table.forecast') }}</th>
              <th class="num">{{ t('restocking.table.toOrder') }}</th>
              <th class="num">{{ t('restocking.table.unitCost') }}</th>
              <th class="num">{{ t('restocking.table.estCost') }}</th>
              <th>{{ t('restocking.table.trend') }}</th>
              <th>{{ t('restocking.table.priority') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.sku + item.warehouse">
              <td><strong>{{ item.sku }}</strong></td>
              <td>{{ item.name }}</td>
              <td>{{ item.warehouse }}</td>
              <td class="num" :class="{ 'low-stock': item.quantity_on_hand < item.reorder_point }">
                {{ item.quantity_on_hand }}
              </td>
              <td class="num">{{ item.reorder_point }}</td>
              <td class="num">{{ item.forecasted_demand }}</td>
              <td class="num order-qty">{{ item.units_needed }}</td>
              <td class="num">{{ formatCurrency(item.unit_cost) }}</td>
              <td class="num">{{ formatCurrency(item.estimated_cost) }}</td>
              <td><span :class="getTrendClass(item.trend)">{{ t(`trends.${item.trend}`) }}</span></td>
              <td><span :class="getPriorityClass(item.priority_score)">{{ getPriorityLabel(item.priority_score) }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'RestockingRecommendations',
  setup() {
    const { t, currentCurrency } = useI18n()
    const { getCurrentFilters, selectedLocation, selectedCategory } = useFilters()

    const loading = ref(true)
    const error = ref(null)
    const items = ref([])
    const budgetInput = ref(null)
    const budget = ref(0)

    const totalCost = computed(() =>
      items.value.reduce((sum, item) => sum + item.estimated_cost, 0)
    )

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        items.value = await api.getRestocking({
          ...getCurrentFilters(),
          budget: budget.value
        })
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const applyBudget = () => {
      budget.value = budgetInput.value || 0
      loadData()
    }

    const clearBudget = () => {
      budgetInput.value = null
      budget.value = 0
      loadData()
    }

    watch([selectedLocation, selectedCategory], loadData)
    onMounted(loadData)

    const formatCurrency = (value) =>
      Number(value).toLocaleString('en-US', {
        style: 'currency',
        currency: currentCurrency.value,
        maximumFractionDigits: 2
      })

    const getTrendClass = (trend) => ({
      'badge success': trend === 'increasing',
      'badge warning': trend === 'stable',
      'badge neutral': trend === 'decreasing'
    })

    const getPriorityClass = (score) => ({
      'badge danger': score >= 4,
      'badge warning': score === 2 || score === 3,
      'badge neutral': score <= 1
    })

    const getPriorityLabel = (score) => {
      if (score >= 4) return t('priority.high')
      if (score >= 2) return t('priority.medium')
      return t('priority.low')
    }

    return {
      t,
      currentCurrency,
      loading,
      error,
      items,
      budgetInput,
      budget,
      totalCost,
      applyBudget,
      clearBudget,
      formatCurrency,
      getTrendClass,
      getPriorityClass,
      getPriorityLabel
    }
  }
}
</script>

<style scoped>
.restocking {
  padding: 0;
}

.budget-row {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: white;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
}

.budget-input-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.budget-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.budget-field {
  position: relative;
  display: flex;
  align-items: center;
}

.currency-symbol {
  position: absolute;
  left: 10px;
  color: #64748b;
  font-size: 0.875rem;
  pointer-events: none;
}

.budget-input {
  padding: 0.5rem 0.75rem 0.5rem 1.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  width: 160px;
  outline: none;
  transition: border-color 0.15s;
}

.budget-input:focus {
  border-color: #3b82f6;
}

.apply-btn {
  padding: 0.5rem 1.25rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.apply-btn:hover { background: #2563eb; }

.clear-btn {
  padding: 0.5rem 0.75rem;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  cursor: pointer;
}

.clear-btn:hover { background: #e2e8f0; }

.summary-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #64748b;
}

.summary-item strong { color: #0f172a; }
.summary-divider { color: #cbd5e1; }

.budget-tag {
  background: #eff6ff;
  color: #1d4ed8;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.table-container { overflow-x: auto; }

.restocking-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.restocking-table th {
  background: #f8fafc;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.restocking-table th.num,
.restocking-table td.num { text-align: right; }

.restocking-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  color: #374151;
}

.restocking-table tr:hover { background: #f8fafc; }

.low-stock { color: #dc2626; font-weight: 600; }
.order-qty { color: #1d4ed8; font-weight: 600; }

.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.success { background: #dcfce7; color: #166534; }
.badge.warning { background: #fef3c7; color: #92400e; }
.badge.danger  { background: #fee2e2; color: #991b1b; }
.badge.neutral { background: #f1f5f9; color: #475569; }

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.error {
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
}
</style>
