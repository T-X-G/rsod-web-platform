<template>
  <div class="qa-page">
    <div class="page-header">
      <h1 class="page-title">AI 智能问答</h1>
      <p class="page-subtitle">关于钢材表面缺陷检测的任何问题，都可以问我</p>
    </div>

    <div class="chat-container">
      <div class="chat-messages">
        <div class="message ai-message">
          <div class="message-avatar">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="message-content">
            你好！我是钢材表面缺陷检测AI助手。我可以帮你解答关于裂纹、夹杂物、斑点、麻面、轧入氧化皮、划痕等缺陷检测的相关问题，也可以为你提供检测结果的详细分析。
          </div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="question"
          placeholder="请输入你的问题..."
          :rows="3"
        />
        <el-button type="primary" class="send-btn" :loading="sending">
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const question = ref("");
const sending = ref(false);
</script>

<style scoped lang="scss">
.qa-page {
  width: 100%;
  height: calc(100vh - 64px - 48px);
  display: flex;
  flex-direction: column;

  .page-header {
    margin-bottom: var(--spacing-lg);

    .page-title {
      font-size: var(--text-3xl);
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: var(--spacing-xs);
    }

    .page-subtitle {
      font-size: var(--text-base);
      color: var(--text-secondary);
    }
  }

  .chat-container {
    flex: 1;
    background-color: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    overflow: hidden;

    .chat-messages {
      flex: 1;
      padding: var(--spacing-lg);
      overflow-y: auto;

      .message {
        display: flex;
        margin-bottom: var(--spacing-lg);

        .message-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-right: var(--spacing-md);
          flex-shrink: 0;
          box-shadow: var(--shadow-sm);
        }

        .message-content {
          background-color: var(--bg-secondary);
          padding: var(--spacing-md);
          border-radius: 0 var(--radius-lg) var(--radius-lg) var(--radius-lg);
          max-width: 70%;
          line-height: 1.7;
          font-size: var(--text-sm);
          color: var(--text-primary);
        }

        &.user-message {
          flex-direction: row-reverse;

          .message-avatar {
            margin-right: 0;
            margin-left: var(--spacing-md);
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
          }

          .message-content {
            background-color: var(--primary-light);
            color: var(--text-primary);
            border-radius: var(--radius-lg) 0 var(--radius-lg) var(--radius-lg);
          }
        }
      }
    }

    .chat-input {
      padding: var(--spacing-lg);
      border-top: 1px solid var(--border-light);
      display: flex;
      gap: var(--spacing-md);
      background-color: var(--bg-secondary);

      :deep(.el-textarea__inner) {
        border-radius: var(--radius-md);
        border-color: var(--border-color);
        padding: var(--spacing-md);
        font-size: var(--text-sm);
      }

      .send-btn {
        width: 100px;
        height: auto;
        border-radius: var(--radius-md);
        background-color: var(--primary-color);
        border-color: var(--primary-color);
        font-weight: 500;
      }

      .send-btn:hover {
        background-color: var(--primary-dark);
        border-color: var(--primary-dark);
      }
    }
  }
}

@media (max-width: 768px) {
  .qa-page {
    height: calc(100vh - 64px - 32px);
  }

  .chat-container .chat-messages .message .message-content {
    max-width: 85%;
  }

  .chat-input {
    padding: var(--spacing-md) !important;
  }

  .send-btn {
    width: 80px !important;
  }
}
</style>