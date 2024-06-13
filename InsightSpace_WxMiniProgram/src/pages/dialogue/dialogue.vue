<template>
  <view class="container" @tap="handleTap()">
    <text>请扫描二维码开启ai问答</text>
    <image src="@/static/images/gzh.png" class="qrcode"></image>

  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const qrCodeUrl = '@/static/images/gzh.png';
const handleTap = () => {

  uni.previewImage({

    urls: ['http://39.109.126.173:39001/api/media/avator/2_20240612161414.jpg'], // 预览图片的链接数组

  });
};


</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 20px;
}

.qrcode {
  width: 200px;
  height: 200px;
  margin-top: 20px;
}
</style>
