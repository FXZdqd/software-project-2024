<script setup lang="ts">
import CustomNavBar from './components/CustomNavBar.vue'
import CategoryPanel from './components/CategoryPanel.vue'
</script>

<template>
  <CustomNavBar />
  <swiper class="banner">
    <swiper-item>
      <image src="@/static/images/ad1.png"></image>
    </swiper-item>
  </swiper>
  <CategoryPanel />
  <view class="index">
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
    <uni-card
      title="问题"
      sub-title="标签"
      extra="2024-3-15"
      thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    >
      <text>内容内容内容内容内容内容内容内容内容内容</text>
    </uni-card>
  </view>
</template>

<style lang="scss">
.banner,
.banner image {
  width: 450px;
  height: 180px;
}
</style>
