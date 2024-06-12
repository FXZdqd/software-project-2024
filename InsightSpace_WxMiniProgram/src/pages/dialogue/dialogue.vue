<template>
  <view class="container">
    <text>请扫描二维码开启ai问答</text>
    <image src="@/static/images/gzh.png" class="qrcode"></image>
  </view>
</template>

<script lang="ts" setup>
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
