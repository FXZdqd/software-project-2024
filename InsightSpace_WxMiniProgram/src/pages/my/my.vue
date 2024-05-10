<script setup lang="ts">
import { useUserStore } from '@/stores'
import { ref } from 'vue'
const UserStore = useUserStore()

// 获取屏幕边界到安全区域距离
const { safeAreaInsets } = uni.getSystemInfoSync()
const current = ref(0)
const onClickItem = (e) => {
  if (current.value !== e.currentIndex) {
    current.value = e.currentIndex
  }
}
const items = ['我的提问', '我的回答', '我的关注']
//获取会员信息
const userStore = useUserStore()
</script>

<template>
  <scroll-view class="viewport" scroll-y enable-back-to-top>
    <image class="background-image" src="/static/images/my_bg.jpg" mode="aspectFill" />
    <!-- 个人资料 -->
    <view class="profile" :style="{ paddingTop: safeAreaInsets!.top + 'px' }">
      <!-- 情况1：已登录 -->
      <view class="overview">
        <navigator url="/pagesMember/profile/profile" hover-class="none">
          <image class="avatar" mode="aspectFill" :src="userStore.profile.avator"></image>
        </navigator>
        <view class="meta">
          <view class="nickname">{{ UserStore.profile.username }}</view>
          
        </view>
      </view>

      <navigator class="settings" url="/pagesMember/settings/settings" hover-class="none">
        <image class="icon" src="/static/images/set.png" mode="aspectFill" />
        <text class="settings-text">设置</text>
      </navigator>
    </view>
    <!-- 分割线 -->  
    <view class="uni-divider"></view> 

    <view class="down">
      <uni-section>
        <!-- <view class="uni-padding-wrap uni-common-mt"> -->
          <uni-segmented-control :current="current" :values="items" style-type=text @clickItem="onClickItem" />
        <!-- </view> -->
        <view class="content">
          <view v-if="current === 0"><text class="content-text">我的提问</text></view>
          <view v-if="current === 1"><text class="content-text">我的回答</text></view>
          <view v-if="current === 2"><text class="content-text">我的关注</text></view>
        </view>
      </uni-section>
    </view>


  </scroll-view>
</template>

<style lang="scss">
page {
  height: 100%;
  overflow: hidden;
  background-color: #f7f7f8;
}

.viewport {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;

}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

/* 用户信息 */
.profile {
  margin-top: 100rpx;
  margin-bottom: 30rpx;
  position: relative;

  .overview {
    display: flex;
    height: 170rpx;
    padding: 0 36rpx;
  }

  .avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: #eee;
  }

  .gray {
    filter: grayscale(100%);
  }

  .meta {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    line-height: 30rpx;
    padding: 16rpx 0;
    margin-left: 20rpx;
    bottom: 0;
  }

  .nickname {
    max-width: 350rpx;
    margin-bottom: 50rpx;
    font-size: 30rpx;
    white-space: nowrap;
  }

  .extra {
    display: flex;
    font-size: 20rpx;
  }

  .tips {
    font-size: 22rpx;
  }

  /* .update {
    padding: 3rpx 10rpx 1rpx;
    color: rgba(0, 0, 0, 0.8);
    border: 1rpx solid rgba(0, 0, 0, 0.8);
    margin-right: 10rpx;
    border-radius: 30rpx;
    bottom: 0;
  } */

  .settings {
    position: absolute;
    bottom: 0;
    right: 40rpx;
    font-size: 30rpx;
  }
}
.uni-divider {  
    width: 100%; 
    height: 10px;
    background-color: #046d9b;  
    //margin: 10px 0;   
}
.icon {
  right:45rpx;
  width: 50rpx;
  height: 50rpx;
}

.down {
  border-radius: 50%;

  .content {
    margin-top: 30rpx;
    justify-content: center;
    align-items: center;
    height: 1000rpx;
  }



}
</style>