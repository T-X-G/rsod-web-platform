<template>
  <div class="profile-page">
    <div class="page-header">
      <h1 class="page-title">个人中心</h1>
      <p class="page-subtitle">管理你的账户信息和使用统计</p>
    </div>

    <div class="profile-content">
      <div class="welcome-card">
        <div class="welcome-content">
          <div class="user-avatar-wrapper">
            <el-avatar size="96">
              <img
                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                alt="用户头像"
              />
            </el-avatar>
            <div class="status-indicator online"></div>
          </div>
          <div class="user-info">
            <h2 class="user-name">你好，示例用户</h2>
            <p class="user-role">普通用户 · 已使用 12 天</p>
            <el-button
              size="small"
              type="primary"
              plain
              class="edit-btn"
            >
              <el-icon><Edit /></el-icon>
              编辑资料
            </el-button>
          </div>
        </div>
      </div>

      <div class="stats-section">
        <h3 class="section-title">检测统计概览</h3>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">总检测次数</span>
              <el-icon class="stat-trend up"><ArrowUp /></el-icon>
            </div>
            <div class="stat-value-wrapper">
              <span class="stat-value">128</span>
              <span class="stat-change">+12%</span>
            </div>
            <div class="stat-chart">
              <div class="chart-bar" style="height: 60%"></div>
              <div class="chart-bar" style="height: 75%"></div>
              <div class="chart-bar" style="height: 55%"></div>
              <div class="chart-bar" style="height: 90%"></div>
              <div class="chart-bar" style="height: 100%"></div>
              <div class="chart-bar" style="height: 85%"></div>
              <div class="chart-bar active" style="height: 88%"></div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">累计检测目标</span>
              <el-icon class="stat-trend up"><ArrowUp /></el-icon>
            </div>
            <div class="stat-value-wrapper">
              <span class="stat-value">892</span>
              <span class="stat-change">+8%</span>
            </div>
            <div class="stat-chart">
              <div class="chart-bar" style="height: 45%"></div>
              <div class="chart-bar" style="height: 60%"></div>
              <div class="chart-bar" style="height: 70%"></div>
              <div class="chart-bar" style="height: 55%"></div>
              <div class="chart-bar" style="height: 80%"></div>
              <div class="chart-bar" style="height: 75%"></div>
              <div class="chart-bar active" style="height: 92%"></div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">检测成功率</span>
              <el-icon class="stat-trend up"><ArrowUp /></el-icon>
            </div>
            <div class="stat-value-wrapper">
              <span class="stat-value">98.5%</span>
              <span class="stat-change">+2.3%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 98.5%"></div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">平均检测时长</span>
              <el-icon class="stat-trend down"><ArrowDown /></el-icon>
            </div>
            <div class="stat-value-wrapper">
              <span class="stat-value">2.3s</span>
              <span class="stat-change">-0.5s</span>
            </div>
            <div class="stat-chart">
              <div class="chart-bar" style="height: 90%"></div>
              <div class="chart-bar" style="height: 85%"></div>
              <div class="chart-bar" style="height: 80%"></div>
              <div class="chart-bar" style="height: 75%"></div>
              <div class="chart-bar" style="height: 70%"></div>
              <div class="chart-bar" style="height: 65%"></div>
              <div class="chart-bar active" style="height: 60%"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="details-section">
        <div class="detail-card">
          <h4 class="card-title">账户信息</h4>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">用户名</span>
              <span class="info-value">example_user</span>
            </div>
            <div class="info-item">
              <span class="info-label">邮箱</span>
              <span class="info-value">user@example.com</span>
            </div>
            <div class="info-item">
              <span class="info-label">注册时间</span>
              <span class="info-value">2024-01-15</span>
            </div>
            <div class="info-item">
              <span class="info-label">最后登录</span>
              <span class="info-value">2024-01-27 14:30</span>
            </div>
          </div>
        </div>

        <div class="detail-card">
          <h4 class="card-title">偏好设置</h4>
          <div class="preference-list">
            <div class="preference-item">
              <span class="preference-label">深色模式</span>
              <el-switch v-model="darkMode" active-color="#2563EB" inactive-color="#D1D5DB" />
            </div>
            <div class="preference-item">
              <span class="preference-label">自动检测</span>
              <el-switch v-model="autoDetect" active-color="#2563EB" inactive-color="#D1D5DB" />
            </div>
            <div class="preference-item">
              <span class="preference-label">通知提醒</span>
              <el-switch v-model="notifications" active-color="#2563EB" inactive-color="#D1D5DB" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { Edit, ArrowUp, ArrowDown } from "@element-plus/icons-vue";

const darkMode = ref(false);
const autoDetect = ref(true);
const notifications = ref(true);
</script>

<style scoped>
.profile-page {
  width: 100%;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.welcome-card {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-lg);
}

.welcome-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.user-avatar-wrapper {
  position: relative;
}

.user-avatar-wrapper .el-avatar {
  border: 4px solid rgba(255, 255, 255, 0.3);
}

.status-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid white;
}

.status-indicator.online {
  background-color: var(--success-color);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: var(--text-2xl);
  font-weight: 600;
  color: white;
  margin-bottom: var(--spacing-xs);
}

.user-role {
  font-size: var(--text-sm);
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: var(--spacing-md);
}

.edit-btn {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.edit-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.stats-section {
  margin-top: var(--spacing-lg);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
}

.stat-card {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.stat-label {
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-trend {
  font-size: var(--text-xs);
}

.stat-trend.up {
  color: var(--success-color);
}

.stat-trend.down {
  color: var(--error-color);
}

.stat-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-primary);
}

.stat-change {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--success-color);
  padding: 2px 6px;
  background-color: var(--success-light);
  border-radius: var(--radius-sm);
}

.stat-chart {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  height: 40px;
}

.chart-bar {
  flex: 1;
  background-color: var(--border-color);
  border-radius: var(--radius-sm);
  transition: height var(--transition-normal);
}

.chart-bar.active {
  background-color: var(--primary-color);
}

.progress-bar {
  height: 8px;
  background-color: var(--bg-secondary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  border-radius: 4px;
}

.details-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.detail-card {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.card-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.info-value {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.preference-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preference-label {
  font-size: var(--text-sm);
  color: var(--text-primary);
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .details-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
  }
  
  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-value {
    font-size: var(--text-2xl);
  }
}
</style>
