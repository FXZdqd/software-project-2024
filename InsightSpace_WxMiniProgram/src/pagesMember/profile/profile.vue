<script setup lang="ts">
import { getUserProfileAPI, getAvatarAPI, resetPasswordAPI } from '@/services/user'
import type { ProfileDetail } from '@/types/user'
import { onLoad } from '@dcloudio/uni-app'
import { ref } from 'vue'
import { useUserStore } from '@/stores'

const userStore = useUserStore()

// 获取屏幕边界到安全区域距离
const { safeAreaInsets } = uni.getSystemInfoSync()

var photo = ref('')
const getAvatar = async () => {
  let data = await getAvatarAPI({ username: userStore.profile.username });
  if (data.value == 0) {
    photo.value = data.base64;
  }
}
getAvatar();
const isProfile = ref(true)
// 获取个人信息
const profile = ref<ProfileDetail>()
const getUserProfileData = async () => {
  const res = await getUserProfileAPI({ username: userStore.profile.username })
  profile.value = res.result
}

onLoad(() => {
  getUserProfileData()
})

const rePwdData = ref({
  username: userStore.profile.username,
  new_password: '',
  new_password_re: '',
})
const repwd = async () => {
  isProfile.value = false;
  const res = await resetPasswordAPI(rePwdData.value);
  console.log(rePwdData.value);

  if (res.value == 0) {
    userStore.clearProfile();
    uni.reLaunch({ url: '/pages/login/login' });
    uni.showToast({
      title: '修改密码成功'
    });
  }
  console.log(res.value);


}

</script>

<template>
  <view class="viewport">
    <!-- 导航栏 -->
    <view class="navbar" :style="{ paddingTop: safeAreaInsets?.top + 'px' }">
      <navigator open-type="navigateBack" class="back icon-left" hover-class="none"></navigator>
      <view class="title">个人信息</view>
    </view>
    <!-- 头像 -->
    <view class="avatar">
      <view class="avatar-content">
        <image class="image" :src="'data:image/jpeg;base64,' + photo" mode="aspectFill" />
        <text class="text">点击修改头像</text>
      </view>
    </view>
    <!-- 表单 -->
    <view class="form" v-if="isProfile">
      <!-- 表单内容 -->
      <view class="form-content">
        <view class="form-item">
          <text class="label">用户名</text>
          <!-- <text class="account">{{ profile?.username }}</text> -->
          <text class="account">{{ userStore.profile.username }}</text>
        </view>
        <!-- <view class="form-item">
          <text class="label">昵称</text>
          <input class="input" type="text" placeholder="请填写昵称" :value="profile?.nickname" />
        </view> -->
        <view class="form-item">
          <text class="label">性别</text>
          <radio-group>
            <label class="radio">
              <radio value="男" color="#27ba9b" :checked="profile?.gender === '男'" />
              男
            </label>
            <label class="radio">
              <radio value="女" color="#27ba9b" :checked="profile?.gender === '女'" />
              女
            </label>
          </radio-group>
        </view>
        <view class="form-item">
          <text class="label">出生日期</text>
          <picker class="picker" mode="date" :value="profile?.birthday" start="1900-01-01" :end="new Date()">
            <view v-if="profile?.birthday">{{ profile?.birthday }}</view>
            <view class="placeholder" v-else>请选择日期</view>
          </picker>
        </view>
        <view class="form-item">
          <text class="label">城市</text>
          <picker class="picker" :value="profile?.fullLocation?.split(' ')" mode="region">
            <view v-if="profile?.fullLocation">{{ profile.fullLocation }}</view>
            <view class="placeholder" v-else>请选择城市</view>
          </picker>
        </view>
        <view class="form-item">
          <text class="label">职业</text>
          <input class="input" type="text" placeholder="请填写职业" :value="profile?.profession" />
        </view>
      </view>
      <view class="form">
        <view class="form-content">
          <view class="form-item" @click="isProfile = false">
            <view class="label">修改密码</view>
          </view>
        </view>
      </view>
      <!-- 提交按钮 -->
      <button class="form-button">保存</button>
    </view>
    <view class="form" v-else>
      <view class="form-content">
        <view class="form-item">
          <text class="label">原密码</text>
          <input class="input" :password="true" placeholder="请填写原密码" />
        </view>
        <view class="form-item">
          <text class="label">新密码</text>
          <input class="input" :password="true" placeholder="请填写新密码" v-model="rePwdData.new_password" />
        </view>
        <view class="form-item">
          <text class="label">确认新密码</text>
          <input class="input" :password="true" placeholder="请再次填写新密码" v-model="rePwdData.new_password_re" />
        </view>

      </view>
      <button class="form-button" @click="repwd()">提交</button>
      <button class="form-button" @click="isProfile = true">返回</button>
    </view>
  </view>
</template>

<style lang="scss">
page {
  background-color: #f4f4f4;
}

.viewport {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-size: auto 420rpx;
  background-repeat: no-repeat;
  background-color: #9bcdff;
}

// 导航栏
.navbar {
  position: relative;

  .title {
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: 500;
    color: #fff;
  }

  .back {
    position: absolute;
    height: 40px;
    width: 40px;
    left: 0;
    font-size: 20px;
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

// 头像
.avatar {
  text-align: center;
  width: 100%;
  height: 260rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .image {
    width: 160rpx;
    height: 160rpx;
    border-radius: 50%;
    background-color: #eee;
  }

  .text {
    display: block;
    padding-top: 20rpx;
    line-height: 1;
    font-size: 26rpx;
    color: #fff;
  }
}

// 表单
.form {
  background-color: #f4f4f4;

  &-content {
    margin: 20rpx 20rpx 0;
    padding: 0 20rpx;
    border-radius: 10rpx;
    background-color: #fff;
  }

  &-item {
    display: flex;
    height: 96rpx;
    line-height: 46rpx;
    padding: 25rpx 10rpx;
    background-color: #fff;
    font-size: 28rpx;
    border-bottom: 1rpx solid #ddd;

    &:last-child {
      border: none;
    }

    .label {
      width: 180rpx;
      color: #333;
    }

    .account {
      color: #666;
    }

    .input {
      flex: 1;
      display: block;
      height: 46rpx;
    }

    .radio {
      margin-right: 20rpx;
    }

    .picker {
      flex: 1;
    }

    .placeholder {
      color: #808080;
    }
  }

  &-button {
    height: 80rpx;
    text-align: center;
    line-height: 80rpx;
    margin: 30rpx 20rpx;
    color: #fff;
    border-radius: 80rpx;
    font-size: 30rpx;
    background-color: #9bcdff;
  }
}
</style>