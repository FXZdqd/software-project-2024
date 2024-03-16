<script setup lang="ts">
import { ref } from 'vue'
const catelist = ref([
  { name: '课程', img: '../../../static/images/课程.png' },
  { name: '科研', img: '../../../static/images/研究.png' },
  { name: '竞赛', img: '../../../static/images/科技竞赛.png' },
  { name: '升学', img: '../../../static/images/升学求学.png' },
  { name: '其他', img: '../../../static/images/其他.png' },
])
</script>

<template>
  <view class="category">
    <navigator
      class="category-item"
      hover-class="none"
      url="/pages/index/index"
      v-for="item in catelist"
      :key="item.name"
    >
      <image class="icon" :src="item.img"></image>
      <text class="text">{{ item.name }}</text>
    </navigator>
  </view>
</template>

<style lang="scss">
/* 前台类目 */
.category {
  margin: 20rpx 0 0;
  padding: 10rpx 0;
  display: flex;
  flex-wrap: wrap;
  min-height: 160rpx;

  .category-item {
    width: 150rpx;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;

    .icon {
      width: 60rpx;
      height: 60rpx;
    }
    .text {
      font-size: 26rpx;
      color: #666;
    }
  }
}
</style>
