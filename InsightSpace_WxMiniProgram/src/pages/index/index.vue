<script setup lang="ts">
import CustomNavBar from './components/CustomNavBar.vue'
</script>

<template>
  <view class="index">
    <swiper class="banner">
      <swiper-item>
        <image src="@/static/images/ad1.png"></image>
      </swiper-item>
    </swiper>

    <uni-search-bar :focus="true"> </uni-search-bar>
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
  height: 200px;
}
</style>
