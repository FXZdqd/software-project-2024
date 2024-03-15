<script setup lang="ts">
const { safeAreaInsets } = uni.getSystemInfoSync()
</script>

<template>
  <!-- 搜索条 -->
  <view class="search">
    <text class="icon-search">搜索问题关键字</text>
    <text class="icon-scan"></text>
  </view>
</template>

<style lang="scss">
.search {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10rpx 0 26rpx;
  height: 64rpx;
  margin: 25rpx 20rpx;
  color: #fff;
  font-size: 28rpx;
  border-radius: 32rpx;
  background-color: rgba(255, 255, 255, 0.5);
}
.icon-search {
  &::before {
    margin-right: 10rpx;
  }
}
.icon-scan {
  font-size: 30rpx;
  padding: 20rpx;
}
</style>
