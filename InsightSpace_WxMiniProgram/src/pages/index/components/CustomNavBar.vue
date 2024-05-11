<script setup lang="ts">
// 获取屏幕边界到安全区域距离
import { ref } from 'vue'
const { safeAreaInsets } = uni.getSystemInfoSync()
const key = ref('')
const confirm = (value: any) => {
  console.log(value)
  let valstr = value.value
  console.log(valstr)
  uni.setStorageSync('valstr', valstr)
  uni.navigateTo({ url: '/pages/search/search' })
  //searchkeyword(valstr)
}

const sort = ref(0)
const range = ref([
  { value: 0, text: "默认排序" },
  { value: 1, text: "按点赞量" },
  { value: 2, text: "按最新发布" },
  { value: 3, text: "按浏览量" },
  { value: 4, text: "按相关度" },
])

const change = (e:any) => {
  console.log("e:", e);
  uni.setStorageSync('sort', e)
}
</script>

<template>
  <view class="navbar" :style="{ paddingTop: safeAreaInsets?.top + 'px' }">
    <!-- logo文字 -->
    <view class="logo">
      <image class="logo-image" src="@/static/images/logo.png"></image>
      <text class="logo-text">灵询问答 · 智慧领航</text>
    </view>
    <!-- 搜索条 -->
    <view class="search-and-select">
      <uni-search-bar v-model="key" radius="100" @confirm="confirm" placeholder="请输入搜索内容" clearButton="auto"
        cancelButton="none" class="search-bar"></uni-search-bar>
      <!-- 排序选择器 -->
      <uni-data-select v-model="sort" :localdata="range" @change="change" :clear="false"
        class="data-select"></uni-data-select>
    </view>
  </view>
</template>

<style lang="scss">
/* 自定义导航条 */
.navbar {
  background-image: url(@/static/images/navigate.png);
  background-size: cover;
  position: relative;
  display: flex;
  flex-direction: column;
  padding-top: 20px;

  .logo {
    display: flex;
    align-items: center;
    height: 64rpx;
    padding-left: 30rpx;
    padding-top: 20rpx;

    .logo-image {
      width: 90rpx;
      height: 80rpx;
    }

    .logo-text {
      flex: 1;
      line-height: 28rpx;
      color: #0b0b0b;
      margin: 2rpx 0 0 20rpx;
      padding-left: 20rpx;
      border-left: 1rpx solid #0b0b0b;
      font-size: 26rpx;
    }
  }

  .search-and-select {
    display: flex;
    width: 100%;
  }

  .search-bar {
    width: 68%;
  }

  .data-select {
    width: 28%;
    margin-top: 12px;
  }
}
</style>
