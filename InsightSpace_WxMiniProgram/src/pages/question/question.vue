<script setup lang="ts">
import { createQAPI } from '@/services/question'
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores'
const UserStore = useUserStore()

const createQdata = ref({
  title: '',
  content: '',
  username: UserStore.profile.username,
  tags: [],
})

const rule = () => {
  if (createQdata.value.content == '') {
    uni.showToast({
      icon: 'none',
      title: '内容不能为空',
    })
  } else if (createQdata.value.title == '') {
    uni.showToast({
      icon: 'none',
      title: '标题不能为空',
    })
  } else {
    addQ()
  }

}

const addQ = async () => {
  console.log(createQdata.value)

  let result = await createQAPI(createQdata.value)

  if (result.value === 0) {
    console.log('发布成功')
    //跳转首页
    uni.switchTab({ url: '/pages/index/index' })
    uni.showToast({
      title: '发布成功',
    })
    clearCreateQData()
  } else if (result.value === 1) {
    console.log('发布失败')
    uni.showToast({
      icon: 'none',
      title: '发布成功',
    })
  }

}

const clearCreateQData = () => {
  createQdata.value = {
    title: '',
    content: '',
    username: UserStore.profile.username,
    tags: [],
  }
}
const catelist = ref([
  { text: '课程', value: 'course' },
  { text: '科研', value: 'research' },
  { text: '竞赛', value: 'competition' },
  { text: '升学', value: 'further_study' },
  { text: '其他', value: 'other' },
])
const onTagsChange: UniHelper.CheckboxGroupOnChange = (ev) => {
  createQdata.value.tags = ev.detail.value
  console.log(createQdata.value.tags)
}
const goAI = () => {
  uni.switchTab({
    url: '/pages/dialogue/dialogue'
  });
}
</script>

<template>
  <!-- <Editor /> -->

  <uni-section title="提问标题" type="line" padding>
    <uni-easyinput class="uni-mt-5" trim="all" v-model="createQdata.title" placeholder="请输入标题"></uni-easyinput>
  </uni-section>
  <uni-section title="提问内容" type="line" padding>
    <uni-easyinput type="textarea" autoHeight v-model="createQdata.content" placeholder="请输入提问内容" focus></uni-easyinput>
  </uni-section>
  <uni-section title="请为问题选择tag" sub-title="非必选项" type="line" padding>
    <uni-data-checkbox multiple mode="tag" v-model="createQdata.tags" :localdata="catelist" @change="onTagsChange" />
  </uni-section>
  <button class="mini-btn" style="background-color: #d4e4ff" size="default" @click="rule">
    发布
  </button>
  <view class="goAI" @click="goAI()">
    需要快速回复?点击获取AI即时回复 →
  </view>
</template>

<style scoped>
.mini-btn {
  height: 80rpx;
  text-align: center;
  line-height: 80rpx;
  margin: 30rpx 20rpx;
  color: #000000;
  border-radius: 80rpx;
  font-size: 30rpx;
  background-color: #9bcdff;
}

.goAI {
  margin-top: 10px;
  text-align: center;
  color: #999;
  font-size: 30rpx;

  /* text:hover {
    color: aqua;
  } */
}
</style>
