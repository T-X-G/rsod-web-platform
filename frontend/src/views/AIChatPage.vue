<template>
  <DashboardLayout>
    <div class="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <!-- Header -->
      <div>
        <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <span>工作台</span>
          <span class="text-gray-600">›</span>
          <span class="text-primary">AI 问答</span>
        </div>
        <h1 class="text-2xl font-bold text-white mb-2">AI 智能问答</h1>
        <p class="text-gray-400">关于钢材表面缺陷检测的任何问题，都可以问我</p>
      </div>

      <!-- Chat Container -->
      <div class="flex-1 glass-card p-6 flex flex-col overflow-hidden">
        <!-- Messages Area -->
        <div
          class="flex-1 overflow-y-auto space-y-6 mb-4 scrollbar-tech"
          ref="messagesContainer"
        >
          <!-- Welcome Message -->
          <div v-if="messages.length === 1" class="py-12 text-center">
            <div
              class="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/20 flex items-center justify-center"
            >
              <svg
                class="w-8 h-8 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
          </div>

          <!-- Messages -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="[
              'flex gap-4',
              message.role === 'user' ? 'flex-row-reverse' : '',
            ]"
          >
            <!-- Avatar -->
            <div
              :class="[
                'w-10 h-10 min-w-[40px] rounded-xl flex-shrink-0 flex items-center justify-center',
                message.role === 'user'
                  ? 'bg-gradient-to-br from-primary to-cyan-400'
                  : 'bg-primary/20 border border-primary/30',
              ]"
            >
              <svg
                v-if="message.role === 'assistant'"
                class="w-5 h-5 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
              <svg
                v-else
                class="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>

            <!-- Message Content -->
            <div
              :class="[
                'max-w-[70%] rounded-2xl px-5 py-3',
                message.role === 'user'
                  ? 'bg-primary/20 text-white rounded-tr-none border border-primary/30'
                  : 'bg-white/5 text-gray-300 rounded-tl-none border border-primary/10',
              ]"
            >
              <p class="text-sm leading-relaxed whitespace-pre-wrap">
                {{ message.content }}
              </p>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex gap-4">
            <div
              class="w-10 h-10 min-w-[40px] rounded-xl bg-primary/20 border border-primary/30 flex-shrink-0 flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
            <div
              class="bg-white/5 border border-primary/10 rounded-2xl rounded-tl-none px-5 py-3"
            >
              <div class="flex gap-1">
                <div
                  class="w-2 h-2 bg-primary rounded-full animate-bounce"
                  style="animation-delay: 0ms"
                ></div>
                <div
                  class="w-2 h-2 bg-primary rounded-full animate-bounce"
                  style="animation-delay: 150ms"
                ></div>
                <div
                  class="w-2 h-2 bg-primary rounded-full animate-bounce"
                  style="animation-delay: 300ms"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="py-3 border-t border-primary/10">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-xs text-gray-400">快捷提问:</span>
            <button
              v-for="question in quickQuestions"
              :key="question"
              @click="sendMessage(question)"
              class="px-3 py-1.5 bg-primary/20 text-primary text-xs rounded-full hover:bg-primary/30 border border-primary/30 transition-all"
            >
              {{ question }}
            </button>
          </div>
        </div>

        <!-- Input Area -->
        <div class="flex items-center gap-3 pt-3 border-t border-primary/10">
          <div class="flex-1 relative">
            <input
              v-model="inputMessage"
              type="text"
              placeholder="请输入您的问题..."
              class="w-full px-4 py-3 bg-white/5 border border-primary/20 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:bg-primary/5 transition-all"
              @keydown.enter="handleSend"
            />
          </div>
          <button
            @click="handleSend"
            :disabled="!inputMessage.trim() || isTyping"
            class="px-6 py-3 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-medium hover:shadow-lg hover:shadow-primary/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            发送
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14 5l7 7m0 0l-7 7m7-7H3"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import DashboardLayout from "../layouts/DashboardLayout.vue";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const inputMessage = ref("");
const isTyping = ref(false);
const conversationId = ref<number | null>(null);
const messagesContainer = ref<HTMLElement | null>(null);

const messages = ref<Message[]>([
  {
    role: "assistant",
    content:
      "你好！我是钢材表面缺陷检测AI助手。我可以帮你解答关于裂纹、夹杂物、斑点、麻面、轧入氧化皮、划痕等缺陷检测的相关问题，也可以为你提供检测结果的详细分析。",
  },
]);

const quickQuestions = [
  "什么是裂纹缺陷？",
  "如何提高检测精度？",
  "检测支持哪些图片格式？",
  "缺陷分类标准是什么？",
];

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = async (content: string) => {
  if (!content.trim()) return;

  messages.value.push({
    role: "user",
    content: content.trim(),
  });

  inputMessage.value = "";
  await scrollToBottom();

  isTyping.value = true;

  try {
    const payload = {
      messages: messages.value.map((m) => ({
        role: m.role,
        content: m.content,
      })),
      conversation_id: conversationId.value,
      user_id: localStorage.getItem("user_id") || "default_user",
    };

    const res = await fetch("/qa/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await res.json();

    if (json.success && json.data) {
      conversationId.value = json.data.conversation_id;
      messages.value.push({
        role: "assistant",
        content: json.data.response,
      });
    } else {
      messages.value.push({
        role: "assistant",
        content: "抱歉，AI 服务暂时不可用：" + (json.message || "未知错误"),
      });
    }
  } catch {
    messages.value.push({
      role: "assistant",
      content: "网络错误，请检查后端服务是否运行。",
    });
  }

  isTyping.value = false;
  await scrollToBottom();
};

const handleSend = () => {
  sendMessage(inputMessage.value);
};
</script>
