<script setup lang="ts">
// 获取屏幕边界到安全区域距离
import { ref } from 'vue'
import { getKeywordQAPI } from '@/services/question'
const { safeAreaInsets } = uni.getSystemInfoSync()
const key = ref('')
const confirm = (value: any) => {
  console.log(value)
  let valstr = value.value
  console.log(valstr)
  searchkeyword(valstr)
}
const searchkeyword = async (keyword: string) => {
  // 调用搜索接口
  const res = await getKeywordQAPI({
    keyword: keyword,
    sort_questions_by: 'likes',
    sort_questions_order: 'asc',
    sort_answers_by: 'likes',
    sort_answers_order: 'asc',
  })
  console.log(res)

}
// const clicksearch = () => {
//   uni.navigateTo({ url: '/pages/search/search' });
// }
</script>

<template>
  <view class="navbar" :style="{ paddingTop: safeAreaInsets?.top + 'px' }">
    <!-- logo文字 -->
    <view class="logo">
      <image class="logo-image" src="@/static/images/logo.png"></image>
      <text class="logo-text">灵询问答 · 智慧领航</text>
    </view>
    <!-- 搜索条 -->
    <view class="search">
      <uni-search-bar v-model="key" radius="100" @confirm="confirm" placeholder="请输入搜索内容" clear-button="always">
      </uni-search-bar>
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

  .search {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 10rpx 0 26rpx;
    height: 64rpx;
    margin: 20rpx 20rpx;
    color: #0b0b0b;
    font-size: 28rpx;
    border-radius: 32rpx;
    background-color: rgba(255, 255, 255, 0.5);
  }

  .icon-search {
    &::before {
      margin-right: 10rpx;
    }
  }
}
</style>
