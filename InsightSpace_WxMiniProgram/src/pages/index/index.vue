<script setup lang="ts">
import CustomNavBar from './components/CustomNavBar.vue'
import CategoryPanel from './components/CategoryPanel.vue'
import { getAllQAPI } from '@/services/question'
import { ref, onMounted } from 'vue'
const questions = ref<any[]>([])
onMounted(
  async () => {
    try {
      const response = await getAllQAPI()
      if (Array.isArray(response)) {
        questions.value = response.map((question) => ({
          ...question
        }))

      } else {
        questions.value = []
      }
    } catch (error) {
      console.error('There was an error fetching the questions:', error)
    }
  } //setInterval(, 5000)
)


function formatDate(dateString) {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const viewInfo = (index: any) => {
  // 将 q_id 存储在本地存储中
  uni.setStorageSync('q_id', index);
  // 跳转详情页
  uni.navigateTo({ url: '/pages/detail/detail' });
}
/*
const questionlist = ref<{ allQuestion: any[] }>({
  allQuestion: [],
})
const getall = async () => {
  const res = await getAllQAPI()
  questionlist.value = res as { allQuestion: any[] }
  console.log(questionlist.value)
  if (res.value === 0) {
    console.log('获取主界面问题成功')
    console.log(res.value)
    console.log(questionlist.value)
  } else {
    console.log('获取主界面问题失败')
  }
}
getall()
*/
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
    <div v-for="question in questions" :key="question.q_id" @click="viewInfo(question.q_id)">
      <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
        <text>{{ question.content }}</text>
      </uni-card>
    </div>
  </view>
</template>

<style lang="scss">
.banner,
.banner image {
  width: 450px;
  height: 180px;
}
</style>
