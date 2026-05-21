<template>
  <div class="header-container">
    <div class="header-left">
      <button class="sidebar-toggle" @click="toggleSidebar">
        <el-icon><Menu /></el-icon>
      </button>
      <div class="breadcrumbs">
        <el-icon class="breadcrumb-icon"><HomeFilled /></el-icon>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-text">{{ currentPage }}</span>
      </div>
    </div>

    <div class="header-right">
      <div class="search-box">
        <el-icon class="search-icon"><Search /></el-icon>
        <input type="text" placeholder="搜索..." class="search-input" />
      </div>

      <div class="header-actions">
        <el-tag type="success" effect="light" class="status-tag">
          <el-icon class="el-icon--left"><CircleCheck /></el-icon>
          系统正常
        </el-tag>

        <div class="action-icons">
          <button class="action-btn" @click="handleGrid">
            <el-icon><Grid /></el-icon>
          </button>
          <button class="action-btn notification-btn" @click="handleNotification">
            <el-icon><Bell /></el-icon>
            <span class="notification-badge">3</span>
          </button>
          <button class="action-btn" @click="handleHelp">
            <el-icon><HelpFilled /></el-icon>
          </button>
          <div class="user-dropdown">
            <el-avatar class="user-avatar" size="32">
              <img
                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                alt="用户头像"
              />
            </el-avatar>
            <div class="user-info">
              <div class="user-name">Lily</div>
              <div class="user-role">普通用户</div>
            </div>
            <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import {
  HomeFilled,
  Menu,
  Search,
  Grid,
  Bell,
  HelpFilled,
  ArrowDown,
  CircleCheck,
} from "@element-plus/icons-vue";

const route = useRoute();

const currentPage = computed(() => {
  const pageNames = {
    "/detection": "智能检测",
    "/history": "历史记录",
    "/qa": "AI问答",
    "/targets": "目标库",
    "/profile": "个人中心",
    "/settings": "系统设置",
  };
  return pageNames[route.path] || "工作台";
});

const toggleSidebar = () => {
  const sidebar = document.querySelector(".sidebar");
  if (sidebar) {
    sidebar.classList.toggle("collapsed");
  }
};

const handleGrid = () => {};

const handleNotification = () => {};

const handleHelp = () => {};
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.sidebar-toggle {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background-color: var(--bg-hover);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
}

.sidebar-toggle:hover {
  background-color: var(--border-color);
  color: var(--text-primary);
}

.breadcrumbs {
  display: flex;
  align-items: center;
}

.breadcrumb-icon {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.breadcrumb-separator {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: 0 4px;
}

.breadcrumb-text {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: var(--spacing-sm);
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.search-input {
  width: 200px;
  padding: var(--spacing-xs) var(--spacing-sm) var(--spacing-xs) calc(var(--spacing-lg));
  font-size: var(--text-sm);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background-color: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.search-input:focus {
  border-color: var(--primary-color);
  background-color: var(--bg-card);
  box-shadow: 0 0 0 2px var(--primary-light);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.status-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: var(--text-xs);
  font-weight: 500;
  background-color: var(--success-light);
  color: var(--success-color);
  border: none;
}

.action-icons {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background-color: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
  position: relative;
}

.action-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  font-size: 10px;
  font-weight: 600;
  background-color: var(--error-color);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
  margin-left: var(--spacing-sm);
}

.user-dropdown:hover {
  background-color: var(--bg-hover);
}

.user-avatar {
  margin-right: var(--spacing-sm);
}

.user-info {
  margin-right: 4px;
}

.user-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.user-role {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.dropdown-icon {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .search-box {
    display: none;
  }
  
  .status-tag {
    display: none;
  }
}
</style>
