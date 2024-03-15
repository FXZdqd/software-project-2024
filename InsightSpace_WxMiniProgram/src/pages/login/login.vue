<script setup lang="ts">
import { postLoginWxMinAPI } from '@/services/login'
import { onLoad } from '@dcloudio/uni-app';
import { ref } from 'vue';

/* let code = ''
onLoad(async () => {
  const res = await wx.login()
  code = res.code
})

//获取用户手机号
const onGetphonenumber: UniHelper.ButtonOnGetphonenumber = async (ev) => {
  const encryptedData = ev.detail!.encryptedData!
  const iv = ev.detail!.iv!
  const res = await postLoginWxMinAPI({
    code,
    encryptedData,
    iv,
  })
  console.log(res);
} */
import { useUserStore } from '@/stores'
const UserStore = useUserStore()

const loginData = ref({
  username: '',
  password: '',
  is_admin: false,
})

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

const submit = async () => {
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

</script>

<template>
  <view class="viewport">
    <view class="logo">
      <image src="@/static/images/logo.png"></image>
    </view>
    <view class="login">
      <!-- 账号密码登录 -->
      <view class="login">
        <uni-forms :modelValue="loginData">
          <uni-forms-item label="用户名" name="username">
            <uni-easyinput type="text" v-model="loginData.username" placeholder="请输入用户名" />
          </uni-forms-item>
          <uni-forms-item label="密码" name="password">
            <uni-easyinput type="password" v-model="loginData.password" placeholder="请输入密码" />
          </uni-forms-item>
          <button @click="submit">Submit</button>
        </uni-forms>
      </view>
      <view class="tips">登录/注册即视为你同意《服务条款》和《灵询隐私协议》</view>
    </view>
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

  .phone {
    //background-color: #28bb9c;
    background-color: rgba(0, 162, 255, 0.758);
  }

  .wechat {
    background-color: #06c05f;
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

.tips {
  position: absolute;
  bottom: 80rpx;
  left: 20rpx;
  right: 20rpx;
  font-size: 22rpx;
  color: #999;
  text-align: center;
}
</style>
