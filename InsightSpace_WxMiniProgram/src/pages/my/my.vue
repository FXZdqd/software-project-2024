<script setup lang="ts">
import { useUserStore } from '@/stores'

const UserStore = useUserStore()
</script>

<template>
  <view class="my">
    <view>会员信息：{{ UserStore.profile }}</view>
    <button
      @tap="
        UserStore.setProfile({
          nickname: '黑马先锋',
        })
      "
      size="mini"
      plain
      type="primary"
    >
      保存用户信息
    </button>
    <button @tap="UserStore.clearProfile()" size="mini" plain type="warn">清理用户信息</button>
  </view>
</template>

<style lang="scss">
//
</style>
