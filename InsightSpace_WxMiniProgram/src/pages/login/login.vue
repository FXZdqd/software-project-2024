<script setup lang="ts">
import { postLoginWxMinAPI, postRegisterWxMinAPI } from '@/services/user'
import { ref } from 'vue';

import { useUserStore } from '@/stores'
const UserStore = useUserStore()

const isRegister = ref(false)
const loginData = ref({
  username: '',
  password: '',
  is_admin: false,
})
const registerData = ref({
  username: '',
  password: '',
  rePassword: '',
  is_admin: false,
})

//校验表单
/* const rules = {
  username: {
    rules: [{
      required: true,
      errorMessage: '请输入用户名',
      trigger: 'blur'
    }, {
      minLength: 5,
      maxlength: 16,
      errorMessage: '用户名长度在 {minLength} 到 {maxLength} 字符之间',
      trigger: 'blur'
    }]
  },
  passowrd: {
    rules: [{
      required: true,
      errorMessage: '请输入密码',
      trigger: 'blur'
    }, {
      minLength: 5,
      maxlength: 16,
      errorMessage: '密码长度在 {minLength} 到 {maxLength} 字符之间',
      trigger: 'blur'
    }]
  }
} */

//登录
const login = async () => {
  //console.log(loginData.value);

  let result = await postLoginWxMinAPI(loginData.value);
  if (result.value === 0) {

    console.log('登陆成功');
    //把用户数据存在pinia中
    UserStore.setProfile(loginData.value);
    //跳转首页

  } else if (result.value === 1) {
    console.log('该用户不存在');

  } else if (result.value === 2) {
    console.log('用户名/密码/权限错误');

  } else if (result.value === 3) {
    console.log('该用户已被封禁');

  }
}

const register = async () => {
  let result = await postRegisterWxMinAPI(registerData.value);
  if (result.value === 0) {
    console.log('注册成功');
    //回到登录页
    isRegister.value = false;
  }else if(result.value === 1){

  }
}

const clearRegisterData = () => {
  registerData.value = {
    username: '',
    password: '',
    rePassword: '',
    is_admin: false,
  }
}

</script>

<template>
  <view class="viewport">
    <view class="logo">
      <image src="@/static/images/logo.png"></image>
    </view>
    <!-- 注册表单 -->
    <view class="register" v-if="isRegister">
      <uni-forms :modelValue="registerData">
        <uni-forms-item label="用户名" name="username">
          <uni-easyinput type="text" v-model="registerData.username" placeholder="请输入用户名" />
        </uni-forms-item>
        <uni-forms-item label="密码" name="password">
          <uni-easyinput type="password" v-model="registerData.password" placeholder="请输入密码" />
        </uni-forms-item>
        <uni-forms-item label="确认密码" name="rePassword">
          <uni-easyinput type="password" v-model="registerData.rePassword" placeholder="请再次输入密码" />
        </uni-forms-item>
        <button @click="register" style="background-color:#d4e4ff">注册</button>
        <view class="shift" :hover-start-time="1" @click="isRegister = false; clearRegisterData()">
          <text>← 返回</text>
        </view>
      </uni-forms>
    </view>

    <!-- 登录表单 -->
    <view class="login" v-else>
      <uni-forms :modelValue="loginData">
        <uni-forms-item label="用户名" name="username">
          <uni-easyinput type="text" v-model="loginData.username" placeholder="请输入用户名" />
        </uni-forms-item>
        <uni-forms-item label="密码" name="password">
          <uni-easyinput type="password" v-model="loginData.password" placeholder="请输入密码" />
        </uni-forms-item>
        <button @click="login" style="background-color:#d4e4ff">登录</button>
        <view class="shift" @click="isRegister = true; clearRegisterData();">
          <text>
            还没有账号？ 去注册 →
          </text>
        </view>
      </uni-forms>
    </view>

    <view class="tips">登录/注册即视为你同意《服务条款》和《灵询隐私协议》</view>
  </view>



</template>

<style lang="scss">
page {
  height: 100%;
}

.viewport {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20rpx 40rpx;
}

.logo {
  flex: 1;
  text-align: center;

  image {
    width: 330rpx;
    height: 330rpx;
    margin-top: 10vh;
  }
}

/* .button {
  color: #94bcff;
} */

.login {
  display: flex;
  flex-direction: column;
  height: 60vh;
  padding: 40rpx 20rpx 20rpx;

  .input {
    width: 100%;
    height: 80rpx;
    font-size: 28rpx;
    border-radius: 72rpx;
    border: 1px solid #ddd;
    padding-left: 30rpx;
    margin-bottom: 20rpx;
  }

  .button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 80rpx;
    font-size: 28rpx;
    border-radius: 72rpx;
    color: #fff;

    .icon {
      font-size: 40rpx;
      margin-right: 6rpx;
    }
  }

  .extra {
    flex: 1;
    padding: 70rpx 70rpx 0;

    .caption {
      width: 440rpx;
      line-height: 1;
      border-top: 1rpx solid #ddd;
      font-size: 26rpx;
      color: #999;
      position: relative;

      text {
        transform: translate(-40%);
        background-color: #fff;
        position: absolute;
        top: -12rpx;
        left: 50%;
      }
    }

    .options {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 70rpx;

      button {
        padding: 0;
        background-color: transparent;
      }
    }

    .icon {
      font-size: 24rpx;
      color: #444;
      display: flex;
      flex-direction: column;
      align-items: center;

      &::before {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 80rpx;
        height: 80rpx;
        margin-bottom: 6rpx;
        font-size: 40rpx;
        border: 1rpx solid #444;
        border-radius: 50%;
      }
    }

    .icon-weixin::before {
      border-color: #06c05f;
      color: #06c05f;
    }
  }
}

.register {
  display: flex;
  flex-direction: column;
  height: 60vh;
  padding: 40rpx 20rpx 20rpx;
}

.tips {
  position: absolute;
  bottom: 80rpx;
  left: 20rpx;
  right: 20rpx;
  font-size: 22rpx;
  color: #999;
  text-align: center;
}

.shift {
  margin-top: 10px;
  text-align: center;
  color: #999;
  font-size: 30rpx;

  text:hover {
    color: aqua;
  }
}
</style>@/services/user
