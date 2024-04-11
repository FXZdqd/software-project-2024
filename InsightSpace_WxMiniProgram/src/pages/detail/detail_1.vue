<script setup lang="ts">
import { ref } from 'vue'
</script>

<template>
    <view class="uni-flex uni-column">
        <view class="flex-item flex-item-V uni-bg-red">A</view>
        <view class="flex-item flex-item-V uni-bg-green">B</view>
        <view class="flex-item flex-item-V uni-bg-blue">C</view>
    </view>
</template>

<style>
.flex-item-V {
    width: 100%;
    height: 150rpx;
    text-align: center;
    line-height: 150rpx;
}
</style>
