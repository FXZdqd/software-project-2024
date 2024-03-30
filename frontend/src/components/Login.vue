<template>
    <div class="container">
      <rain></rain>
      <img class="logo-svg" src="../assets/bz.svg" alt="Logo" />
      <div class="spacer"></div>
      <div class="login-container">
        <h2 style="display: flex; justify-content: center; align-items: center;">管理员登录</h2>
        <div class="spacer"></div>
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="username">用户名:</label>
            <input type="text" id="username" v-model="username" class="text-input" />
          </div>
          <div class="form-group">
            <label for="password">密码:</label>
            <input type="password" id="password" v-model="password" class="text-input" />
          </div>
          <button type="submit" class="login-button">登录</button>
        </form>
        <!-- 自定义模态框 -->
        <transition name="fade">
          <div v-if="showModal" class="modal-overlay">
            <div class="modal">
              <template v-if="errorCode === 1">
                <h3>登录失败</h3>
                <p>用户不存在，请重试</p>
              </template>
              <template v-else-if="errorCode === 2">
                <h3>登录失败</h3>
                <p>用户名，密码，或权限错误，请重试</p>
              </template>
              <template v-else-if="errorCode === 3">
                <h3>登录失败</h3>
                <p>用户被封禁，请联系管理员</p>
              </template>
              <template v-else>
                <p>未知错误，错误码: {{ errorCode }}</p>
              </template>
              <button @click="closeModal" class="modal-button">关闭</button>
            </div>
          </div>
        </transition>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Rain from "./Rain.vue";

const router = useRouter();
const username = ref('');
const password = ref('');
const showModal = ref(false);
const errorCode = ref(0);

const login = async () => {
  try {
    const response = await axios.post('http://39.109.126.173:39000/api/login', {
      username: username.value,
      password: password.value,
      is_admin: true
    });
    errorCode.value = response.data.value;
    if (errorCode.value === 0) {
      router.push('/Manage');
    } else {
      showModal.value = true;
    }
  } catch (error) {
    console.error('登录失败:', error.response.data.message);
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<style scoped>
.logo-svg {
  width: 850px;
  height: 850px;
  display: block;
  margin: auto;
  z-index: 3;
}

.spacer{
  margin-top: 20px;
}
.login-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 350px;
  width:400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #fff; /* 设置内层 div 的背景色为白色 */
  z-index: 1;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 50px;
  display: flex;
  align-items: center;
}

label {
  font-weight: bold;
  width: 80px; /* 调整标签的宽度，使其对齐 */
}

.text-input {
  flex: 1; /* 让文本输入框填充剩余的空间 */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-right: 20px;
}

.login-button {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0056b3;
}

/* 自定义模态框样式 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.modal h3 {
  margin-top: 0;
}

.modal-button {
  margin-top: 10px;
  padding: 8px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.modal-button:hover {
  background-color: #0056b3;
}
</style>
