<template>
  <div class="login-container">
    <rain></rain>
    <div class="logo-container">
      <img src="@/assets/bz.svg" alt="Logo" style="width: 100%; height: 100%" />
      <!-- 假设是一个图片logo -->
    </div>
    <div class="form">
      <h1 style="margin-top: 20%">管理员登录</h1>
      <el-card shadow="never" class="login-card">
        <el-form ref="form" :model="state.loginForm" :rules="rules">
          <el-form-item prop="username">
            <el-input
              v-model="state.loginForm.username"
              placeholder="请输入用户名"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="state.loginForm.password"
              show-password
              placeholder="请输入密码"
            />
          </el-form-item>
          <!-- <el-form-item prop="isAgree">
            <el-checkbox> 用户平台使用协议 </el-checkbox>
          </el-form-item> -->
          <el-form-item>
            <el-button style="width: 350px" type="primary" @click="login"
              >登录</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
      <!-- 自定义模态框 -->
      <transition name="fade">
        <div v-if="showModal" class="modal-overlay">
          <div class="modal">
            <template v-if="errorCode === 1">
              <p>用户不存在，请重试</p>
            </template>
            <template v-else-if="errorCode === 2">
              <p>用户名，密码，或权限错误，请重试</p>
            </template>
            <template v-else-if="errorCode === 3">
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
import { log_in } from "@/api/request";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import Rain from "./Rain.vue";
import type { FormRules } from "element-plus";
const router = useRouter();
const showModal = ref(false);
const errorCode = ref(0);

const usernameRules = (rule: any, value: string, callback: any) => {
  var module = new RegExp(/^1[2-9]\d{9}$/);
  if (value === "") {
    callback(new Error("请输入手机号/用户名"));
  } //else if (!module.test(value)) {
  // callback(new Error('格式有误'))
  // }
  callback();
};

const passwordRules = (rule: any, value: string, callback: any) => {
  var module = new RegExp(/^(?=.*\d)(?=.*[A-z])[\da-zA-Z]{6,18}$/);
  if (value === "") {
    callback(new Error("请输入密码"));
  } // else if (!module.test(value)) {
  // callback(new Error('密码必须为6-18位'))
  // }
  callback();
};

const rules = reactive<FormRules>({
  username: [{ required: true, validator: usernameRules, trigger: "blur" }],
  password: [{ required: true, validator: passwordRules, trigger: "blur" }],
});

const state = reactive({
  loginForm: {
    username: "",
    password: "",
  },
});

const login = async () => {
  try {
    console.log(state.loginForm);
    const response = await log_in(
      state.loginForm.username,
      state.loginForm.password,
      true
    );
    errorCode.value = response.data.value;
    if (errorCode.value === 0) {
      console.log("登录成功");
      await router.push("/home");
    } else {
      showModal.value = true;
    }
  } catch (error) {
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<style>
.login-container {
  align-items: stretch;
  display: flex;
  justify-content: flex-end;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.logo-container {
  width: 40%;
  margin-right: 15%;
  z-index: -1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container .form h1 {
  font-family: 优设标题;
  font-size: 56px;
  color: #333;
  margin-bottom: 50px;
}
.login-container .form {
  background-color: #ffffff; /* 更亮的背景色 */
  padding: 40px; /* 增加内边距以便于阅读 */
  border-radius: 10px; /* 更圆润的边角 */
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 6px 20px rgba(0, 0, 0, 0.1); /* 更细腻的阴影效果 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 使子元素在中心对齐 */
  z-index: 2;
  width: 30%;
  height: 100%;
}
.login-card {
  width: 100%;
}
.login-container .form .el-input {
  height: 100%;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  font-weight: bold;
}

.login-container .form .el-form-item {
  margin-top: 20px;
  height: 40px;
  width: 100%;
}

.login-container .form .el-button {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  height: 44px;
  font-weight: bold;
}

.login-container .form .el-button:focus,
.login-container .form .el-button:hover {
  border-color: #409eff;
}

.login-container .form .el-button {
  background-color: #409eff;
  color: white;
  margin-top: 10px;
  transition:
    background-color 0.3s,
    border-color 0.3s;
}

.login-container .form .el-checkbox__input.is-checked .el-checkbox__inner {
  background-color: #409eff;
  border-color: #409eff;
}

.login-container .form .el-button:active {
  background-color: #3a8ee6;
}

.login-container .form .el-checkbox {
  margin-top: 20px;
}

.login-container .form .el-button:active {
  background-color: #3a8ee6;
}
.login-container .form .el-checkbox {
  margin-top: 20px;
}

.login-container .form .el-button[type="text"] {
  color: #409eff;
  font-size: 0.875rem;
  transition: color 0.3s ease-in-out;
}

.login-container .form .el-button[type="text"]:hover {
  color: #337ab7;
}

.fade-enter-active,
.fade-leave-active {
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
  backdrop-filter: blur(5px);
}

.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  justify-content: center;
  transition: transform 0.3s ease-out;
}

.modal h3 {
  margin-top: 0;
}

.modal-button {
  margin-top: 10px;
  margin-left: 25%;
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
