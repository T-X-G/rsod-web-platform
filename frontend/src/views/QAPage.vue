<template>
  <div class="qa-page">
    <div>
      <h1>AI 智能问答</h1>
      <p>关于遥感目标检测的任何问题，都可以问我</p>
    </div>

    <div class="chat-container">
      <div ref="messagesContainer" class="chat-messages">
        <div 
          v-for="(msg, idx) in messages" 
          :key="idx" 
          :class="['message', { 'user-message': msg.role === 'user' }]"
        >
          <div :class="['avatar', { 'user-avatar': msg.role === 'user' }]">
            <el-icon v-if="msg.role === 'user'"><User /></el-icon>
            <el-icon v-else><ChatDotRound /></el-icon>
          </div>
          <div :class="['message-bubble', { 'user-bubble': msg.role === 'user' }]">
            {{ msg.content }}
          </div>
        </div>
        
        <div v-if="sending" class="message">
          <div class="avatar">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="message-bubble">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <el-input 
          v-model="question" 
          placeholder="请输入你的问题..." 
          :rows="3"
          @keyup.enter="send"
        />
        <el-button type="primary" :loading="sending" @click="send">
          <el-icon><ArrowRight /></el-icon>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { User, ChatDotRound, ArrowRight } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { sendMessage } from "../api/qa";

const question = ref("");
const sending = ref(false);
const messages = ref([]);
const messagesContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const send = async () => {
  if (!question.value.trim() || sending.value) return;
  
  const userMsg = { role: "user", content: question.value.trim() };
  messages.value.push(userMsg);
  question.value = "";
  sending.value = true;
  await scrollToBottom();

  try {
    const res = await sendMessage({
      messages: [...messages.value],
      conversation_id: null,
      user_id: localStorage.getItem("user_id") || "default_user"
    });
    
    if (res.success && res.data) {
      messages.value = res.data.messages;
    } else {
      throw new Error(res.message || "发送失败");
    }
  } catch (e) {
    messages.value.pop();
    ElMessage.error(e.message || "发送失败，请检查后端服务是否启动");
  } finally {
    sending.value = false;
    await scrollToBottom();
  }
};

onMounted(() => {
  messages.value = [{
    role: "assistant",
    content: "你好！我是遥感目标检测AI助手。请问有什么我可以帮助你的吗？"
  }];
  scrollToBottom();
});
</script>

<style scoped>
.qa-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.qa-page > div:first-child {
  margin-bottom: 20px;
}

.qa-page > div:first-child h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.qa-page > div:first-child p {
  font-size: 14px;
  color: #666;
}

.chat-container {
  flex: 1;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  display: flex;
  margin-bottom: 15px;
}

.message.user-message {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #aa3bff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.user-avatar {
  background: #60a5fa;
  margin-right: 0;
  margin-left: 12px;
}

.message-bubble {
  background: #f4f3ec;
  padding: 12px 16px;
  border-radius: 0 12px 12px 12px;
  max-width: 70%;
  line-height: 1.6;
  font-size: 14px;
}

.user-bubble {
  background: rgba(170, 59, 255, 0.1);
  border-radius: 12px 0 12px 12px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #999;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

.chat-input {
  padding: 20px;
  border-top: 1px solid #e5e4e7;
  display: flex;
  gap: 12px;
}

.chat-input .el-input {
  flex: 1;
}

.chat-input .el-button {
  width: 100px;
}

@keyframes typing {
  0%, 80%, 100% { opacity: 0.5; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}
</style>