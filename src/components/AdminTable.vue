<template>
  <div class="admin-table-container">
    <!-- Controls -->
    <div class="table-controls">
      <div class="controls-left">
        <div class="items-per-page">
          <label for="pageSize">تعداد ردیف:</label>
          <select v-model.number="pageSize" id="pageSize" @change="handlePageSizeChange">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
        <div class="total-items">
          کل: {{ totalItems }} مورد
        </div>
      </div>
      <div class="controls-right">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="جستجو..." 
          class="search-input"
          @input="handleSearch"
        >
      </div>
    </div>

    <!-- Table -->
    <Loader v-if="loading" />
    <table v-else-if="paginatedData.length > 0" class="admin-table">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in paginatedData" :key="item.id">
          <td v-for="column in columns" :key="column.key">
            <span v-if="column.type === 'boolean'">
              <span v-if="item[column.key]" class="status-published">منتشر شده</span>
              <span v-else class="status-draft">پیش‌نویس</span>
            </span>
            <span v-else-if="column.type === 'date'">
              {{ formatDate(item[column.key]) }}
            </span>
            <span v-else>
              {{ getNestedValue(item, column.key) }}
            </span>
          </td>
          <td class="actions">
            <button @click="$emit('edit', item)" class="btn-edit">ویرایش</button>
            <button @click="$emit('delete', item)" class="btn-delete">حذف</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="no-data">هیچ داده‌ای یافت نشد</div>

    <!-- Pagination -->
    <div v-if="data.length > 0" class="pagination">
      <button 
        @click="previousPage" 
        :disabled="currentPage === 1"
        class="btn-pagination"
      >
        قبلی
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          :class="{ active: currentPage === page }"
          class="btn-page-number"
        >
          {{ page }}
        </button>
      </div>

      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages"
        class="btn-pagination"
      >
        بعدی
      </button>

      <div class="page-info">
        صفحه {{ currentPage }} از {{ totalPages }}
      </div>
    </div>
  </div>
</template>

<script>
import Loader from './Loader.vue';

export default {
  name: 'AdminTable',
  components: {
    Loader
  },
  props: {
    data: {
      type: Array,
      required: true
    },
    columns: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    totalItems: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 25,
      searchQuery: ''
    };
  },
  computed: {
    filteredData() {
      if (!this.searchQuery) {
        return this.data;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.data.filter(item => {
        return this.columns.some(column => {
          const value = this.getNestedValue(item, column.key);
          return value && value.toString().toLowerCase().includes(query);
        });
      });
    },
    totalPages() {
      const total = this.totalItems || this.data.length;
      return Math.ceil(total / this.pageSize);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredData.slice(start, end);
    },
    visiblePages() {
      const pages = [];
      const maxPagesToShow = 5;
      const halfWindow = Math.floor(maxPagesToShow / 2);
      
      let startPage = Math.max(1, this.currentPage - halfWindow);
      let endPage = Math.min(this.totalPages, startPage + maxPagesToShow - 1);
      
      if (endPage - startPage < maxPagesToShow - 1) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      
      return pages;
    }
  },
  watch: {
    data() {
      // Reset to first page when data changes
      this.currentPage = 1;
    }
  },
  methods: {
    getNestedValue(obj, path) {
      return path.split('.').reduce((current, key) => current && current[key], obj);
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleDateString('fa-IR');
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
    handlePageSizeChange() {
      this.currentPage = 1;
      this.$emit('pageSize-change', this.pageSize);
    },
    handleSearch() {
      this.currentPage = 1;
      this.$emit('search', this.searchQuery);
    }
  }
}
</script>

<style scoped>
.admin-table-container {
  width: 100%;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.controls-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 10px;
}

.items-per-page label {
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.items-per-page select {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 13px;
  cursor: pointer;
}

.items-per-page select:focus {
  outline: none;
  border-color: #1abc9c;
}

.total-items {
  color: #666;
  font-size: 13px;
  white-space: nowrap;
}

.controls-right {
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 13px;
  min-width: 200px;
}

.search-input:focus {
  outline: none;
  border-color: #1abc9c;
  box-shadow: 0 0 0 3px rgba(26, 188, 156, 0.1);
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 16px;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
  background: #fafafa;
  border-radius: 4px;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.admin-table th,
.admin-table td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #eee;
}

.admin-table th {
  background: #f8f9fa;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.admin-table td {
  color: #666;
  font-size: 14px;
}

.admin-table tr:hover {
  background: #f8f9fa;
}

.status-published {
  color: #27ae60;
  font-weight: bold;
}

.status-draft {
  color: #f39c12;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn-edit,
.btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-edit:hover {
  background: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(52, 152, 219, 0.3);
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(231, 76, 60, 0.3);
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  flex-wrap: wrap;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.btn-pagination,
.btn-page-number {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  color: #333;
  transition: all 0.3s ease;
  min-width: 40px;
}

.btn-pagination:hover:not(:disabled),
.btn-page-number:hover {
  border-color: #1abc9c;
  color: #1abc9c;
}

.btn-page-number.active {
  background: #1abc9c;
  color: white;
  border-color: #1abc9c;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 13px;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .table-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .controls-left,
  .controls-right {
    flex-direction: column;
    width: 100%;
  }

  .search-input {
    min-width: 100%;
  }

  .admin-table th,
  .admin-table td {
    padding: 8px 10px;
    font-size: 12px;
  }

  .actions {
    flex-direction: column;
    gap: 4px;
  }

  .btn-edit,
  .btn-delete {
    padding: 4px 8px;
    font-size: 11px;
  }

  .pagination {
    flex-direction: column;
    gap: 8px;
  }

  .page-numbers {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>