<template>
  <div class="sidebar-container">
    <div class="logo-section">
      <div class="logo-icon">
        <Cpu style="color: white; font-size: 20px" />
      </div>
      <div class="logo-text">
        <div class="logo-title">钢材缺陷检测</div>
        <div class="logo-subtitle">SteelDefect AI</div>
      </div>
    </div>

    <div class="nav-menu">
      <div
        v-for="item in menuList"
        :key="item.path"
        class="nav-item"
        :class="{ active: currentPath === item.path }"
        @click="handleMenuClick(item)"
      >
        <el-icon :size="18" class="nav-icon"><component :is="item.icon" /></el-icon>
        <span class="nav-text">{{ item.name }}</span>
        <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="user-section">
        <el-avatar size="36">
          <img
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
            alt="用户头像"
          />
        </el-avatar>
        <div class="user-info">
          <div class="user-name">Lily</div>
          <div class="user-role">普通用户</div>
        </div>
      </div>
      <div class="footer-actions">
        <div class="action-item" @click="handleSettings">
          <el-icon :size="16"><Setting /></el-icon>
          <span>设置</span>
        </div>
        <div class="action-item" @click="handleLogout">
          <el-icon :size="16"><Close /></el-icon>
          <span>退出</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  Cpu,
  Picture,
  Clock,
  ChatDotRound,
  DataLine,
  User,
  Setting,
  Close,


} from "@element-plus/icons-vue";

const router = useRouter();
const route = useRoute();

const menuList = [
  {
    name: "智能检测",
    icon: Picture,
    path: "/detection",
    badge: null,
  },
  {
    name: "历史记录",
    icon: Clock,
    path: "/history",
    badge: "12",
  },
  {
    name: "AI 问答",
    icon: ChatDotRound,
    path: "/qa",
    badge: null,
  },
  {
    name: "目标库",
    icon: DataLine,
    path: "/targets",
    badge: null,
  },
  {
    name: "个人中心",
    icon: User,
    path: "/profile",
    badge: null,
  },
];

const currentPath = computed(() => route.path);

const handleMenuClick = (item) => {
  router.push(item.path);
};

const handleSettings = () => {
  router.push("/settings");
};

const handleLogout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-card);
}

.logo-section {
  height: 72px;
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
}

.logo-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-sm);
  flex-shrink: 0;
}

.logo-text {
  overflow: hidden;
}

.logo-title {
  font-size: var(--text-sm);
  font-weight: 600;
  color: white;
  line-height: 1.3;
  white-space: nowrap;
}

.logo-subtitle {
  font-size: var(--text-xs);
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
  line-height: 1.3;
  white-space: nowrap;
}

.nav-menu {
  flex: 1;
  padding: var(--spacing-md);
}

.nav-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xs);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  color: var(--text-secondary);
}

.nav-item:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  font-weight: 500;
}

.nav-item.active .nav-icon {
  color: var(--primary-color);
}

.nav-icon {
  font-size: var(--text-lg);
  margin-right: var(--spacing-md);
  color: var(--text-muted);
  flex-shrink: 0;
  transition: color var(--transition-fast);
}

.nav-item:hover .nav-icon {
  color: var(--text-secondary);
}

.nav-text {
  font-size: var(--text-sm);
  line-height: 1.4;
  flex: 1;
}

.nav-badge {
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 2px 8px;
  background-color: var(--secondary-color);
  color: white;
  border-radius: 10px;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-light);
  background-color: var(--bg-secondary);
}

.user-section {
  display: flex;
  align-items: center;
  padding-bottom: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

.user-section .el-avatar {
  margin-right: var(--spacing-sm);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: var(--text-xs);
  color: var(--text-muted);
  white-space: nowrap;
}

.footer-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-item:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .logo-text,
  .nav-text,
  .user-info,
  .action-item span {
    display: none;
  }
  
  .logo-section {
    justify-content: center;
    padding: 0;
  }
  
  .logo-icon {
    margin-right: 0;
  }
  
  .nav-item {
    justify-content: center;
    padding: var(--spacing-md) 0;
  }
  
  .nav-icon {
    margin-right: 0;
  }
  
  .sidebar-footer {
    align-items: center;
  }
  
  .user-section {
    justify-content: center;
    border-bottom: none;
    padding-bottom: 0;
    margin-bottom: 0;
  }
  
  .footer-actions {
    display: none;
  }
}
</style>
