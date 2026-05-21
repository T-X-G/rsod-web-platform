<template>
  <div class="main-layout">
    <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <slot name="sidebar"></slot>
    </aside>

    <div class="main-container">
      <header class="header">
        <slot name="header"></slot>
      </header>

      <main class="content">
        <slot name="content"></slot>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isSidebarCollapsed = ref(false);
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-primary);
}

.sidebar {
  width: 220px;
  background-color: var(--bg-card);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-normal);
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.sidebar.collapsed {
  width: 64px;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 64px;
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.content {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
  background-color: var(--bg-primary);
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .sidebar {
    width: 64px;
  }
  
  .sidebar.collapsed {
    width: 0;
    overflow: hidden;
  }
  
  .content {
    padding: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 var(--spacing-md);
  }
  
  .content {
    padding: var(--spacing-sm);
  }
}
</style>
