<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo-icon">
          <el-icon :size="40" color="#27ae60"><Picture /></el-icon>
        </div>
        <h1 class="login-title">钢材表面缺陷智能检测平台</h1>
        <p class="login-subtitle">专业钢材检测 · 精准缺陷识别</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item class="form-actions">
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          <router-link to="/forgot-password" class="forgot-password">忘记密码?</router-link>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" class="login-btn" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-link">
        <span>还没有账号？</span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { Picture, User, Lock } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

const router = useRouter();

const loginForm = reactive({
  username: "",
  password: "",
  remember: false,
});

const loginRules = {
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 3, max: 20, message: "用户名长度在3到20个字符", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, max: 30, message: "密码长度在6到30个字符", trigger: "blur" },
  ],
};

const loginFormRef = ref(null);

const handleLogin = () => {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      console.log("登录请求:", loginForm);
      localStorage.setItem("token", "mock-token");
      router.push("/detection");
    }
  });
};
</script>

<style scoped>
/* 修改点：添加星空背景效果 */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 修改点：蓝紫色渐变星空背景 */
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 30%, #0f3460 60%, #533483 100%);
  position: relative;
  overflow: hidden;
}

/* 修改点：添加星星效果 */
.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.8), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.5), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.6), transparent),
    radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.4), transparent),
    radial-gradient(1px 1px at 160px 120px, rgba(255,255,255,0.7), transparent),
    radial-gradient(2px 2px at 200px 50px, rgba(255,255,255,0.5), transparent),
    radial-gradient(1px 1px at 250px 160px, rgba(255,255,255,0.6), transparent),
    radial-gradient(2px 2px at 300px 90px, rgba(255,255,255,0.4), transparent),
    radial-gradient(1px 1px at 350px 200px, rgba(255,255,255,0.7), transparent),
    radial-gradient(2px 2px at 400px 150px, rgba(255,255,255,0.5), transparent),
    radial-gradient(1px 1px at 450px 300px, rgba(255,255,255,0.6), transparent),
    radial-gradient(2px 2px at 500px 200px, rgba(255,255,255,0.4), transparent);
  background-repeat: repeat;
  background-size: 500px 350px;
  animation: twinkle 8s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

/* 修改点：玻璃拟态卡片样式 */
.login-card {
  width: 100%;
  max-width: 420px;
  padding: 48px 40px;
  /* 修改点：玻璃拟态效果 - 半透明背景 + backdrop-filter模糊 */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  /* 修改点：轻微发光阴影 */
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 0 60px rgba(118, 75, 162, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.15);
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.logo-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  /* 修改点：logo图标玻璃拟态效果 */
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* 修改点：标题样式 - 白色粗体 */
.login-title {
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* 修改点：副标题样式 - 浅粉色 */
.login-subtitle {
  font-size: 14px;
  color: rgba(255, 182, 193, 0.8);
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
}

.login-form {
  margin-bottom: 28px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* 修改点：记住我复选框样式 */
.form-actions .el-checkbox__label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
}

.forgot-password {
  font-size: 13px;
  /* 修改点：链接颜色为浅粉色 */
  color: rgba(255, 182, 193, 0.9);
  cursor: pointer;
}

.forgot-password:hover {
  text-decoration: underline;
  color: #ffb6c1;
}

/* 修改点：登录按钮样式 - 白色圆角、无生硬边框、hover效果 */
.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  /* 修改点：白色按钮背景 */
  background: rgba(255, 255, 255, 0.95);
  color: #2d3748;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.login-btn:hover {
  /* 修改点：hover时亮度变化 */
  background: #ffffff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.login-btn:active {
  transform: translateY(0);
}

.register-link {
  text-align: center;
  font-size: 14px;
  /* 修改点：文字颜色为白色/浅粉色 */
  color: rgba(255, 255, 255, 0.7);
}

.register-link a {
  /* 修改点：注册链接颜色为浅粉色 */
  color: rgba(255, 182, 193, 0.9);
  margin-left: 4px;
  cursor: pointer;
}

.register-link a:hover {
  text-decoration: underline;
  color: #ffb6c1;
}

/* 修改点：输入框样式 - 半透明边框、hover/聚焦发光效果 */
.login-form :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 182, 193, 0.5);
  box-shadow: 0 0 15px rgba(255, 182, 193, 0.2);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(255, 182, 193, 0.8);
  box-shadow: 0 0 20px rgba(255, 182, 193, 0.3);
}

.login-form :deep(.el-input__inner) {
  color: #ffffff;
  background: transparent;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.5);
}

.login-form :deep(.el-input__prefix) {
  color: rgba(255, 182, 193, 0.8);
}

/* 修改点：复选框样式 */
.login-form :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background: rgba(255, 182, 193, 0.8);
  border-color: rgba(255, 182, 193, 0.8);
}

.login-form :deep(.el-checkbox__inner) {
  border-color: rgba(255, 255, 255, 0.3);
}
</style>