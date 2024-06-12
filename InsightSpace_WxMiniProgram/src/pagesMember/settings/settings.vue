<script setup lang="ts">
import { useUserStore } from '@/stores'
import { deleteUserAPI } from '@/services/user';
import { ref } from 'vue';
const userStore = useUserStore()
// 退出登录
const onLogout = () => {
  uni.showModal({
    content: '是否退出登录？',
    success: (res) => {
      if (res.confirm) {
        // 清理用户信息
        userStore.clearProfile()
        // 返回登录页
        uni.reLaunch({ url: '/pages/login/login' });
      }
    },
  })
}

const deleteUserData = ref({
  username: userStore.profile.username,
  password: ''
})

const cancel = async () => {
  uni.showModal({
    title: '注销账号',
    content: '一经注销，账号所有信息将被清空，无法恢复',
    success: async (res) => {
      if (res.confirm) {
        uni.showModal({
          title: '请输入密码',
          editable: true,
          success: async (res1) => {
            if (res1.content == userStore.profile.password) {
              const res2 = await deleteUserAPI({ username: userStore.profile.username })
              console.log(res2.message);
              // 清理用户信息
              userStore.clearProfile()
              // 返回登录页
              uni.reLaunch({ url: '/pages/login/login' });
              uni.showToast({
                title: '注销成功'
              });
            } else {
              uni.showToast({
                icon: 'error',
                title: '密码错误'
              });
            }
          },
        })
      }
    },
  })
}

</script>

<template>
  <view class="viewport">
    <!-- 列表1 -->
    <view class="list">
      <navigator url="/pagesMember/myProfile/myProfile" hover-class="none" class="item arrow">
        我的信息
      </navigator>
    </view>

    <!-- 列表2 -->
    <view class="list">
      <button hover-class="none" class="item arrow" open-type="openSetting">授权管理</button>
      <button hover-class="none" class="item arrow" open-type="feedback">问题反馈</button>
      <button hover-class="none" class="item arrow" open-type="contact">联系我们</button>
    </view>
    <!-- 列表3 -->
    <view class="list">
      <navigator hover-class="none" class="item arrow" url="/pagesMember/introduction/introduction">关于《灵询》</navigator>
    </view>
    <!-- 操作按钮 -->
    <view class="action">
      <view class="button" @click="onLogout">退出登录</view>
    </view>
    <view class="action">
      <view class="button" @click="cancel">注销账号</view>
    </view>
  </view>
</template>

<style lang="scss">
page {
  background-color: #f4f4f4;
}

.viewport {
  padding: 20rpx;
}

/* 列表 */
.list {
  padding: 0 20rpx;
  background-color: #fff;
  margin-bottom: 20rpx;
  border-radius: 10rpx;

  .item {
    line-height: 90rpx;
    padding-left: 10rpx;
    font-size: 30rpx;
    color: #333;
    border-top: 1rpx solid #ddd;
    position: relative;
    text-align: left;
    border-radius: 0;
    background-color: #fff;

    &::after {
      width: auto;
      height: auto;
      left: auto;
      border: none;
    }

    &:first-child {
      border: none;
    }

    &::after {
      right: 5rpx;
    }
  }

  .arrow::after {
    content: '\e6c2';
    position: absolute;
    top: 50%;
    color: #ccc;
    font-family: 'erabbit' !important;
    font-size: 32rpx;
    transform: translateY(-50%);
  }
}

.action {
  text-align: center;
  line-height: 90rpx;
  margin-top: 40rpx;
  font-size: 32rpx;
  color: #333;

  .button {
    background-color: #fff;
    margin-bottom: 20rpx;
    border-radius: 10rpx;
  }
}
</style>