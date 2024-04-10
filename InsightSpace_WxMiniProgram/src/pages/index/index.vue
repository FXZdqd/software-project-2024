<script setup lang="ts">
import CustomNavBar from './components/CustomNavBar.vue'
import CategoryPanel from './components/CategoryPanel.vue'
import { getAllQAPI } from '@/services/question'
import { ref } from 'vue'
interface AllQuestionData {
  allQuestion: []
}

// 假设 API 返回的数据类型为 unknown
const questionlist = ref<AllQuestionData>({
  allQuestion: [],
})

const getall = async () => {
  try {
    // 假设 getAllQAPI() 函数返回的数据类型为 unknown
    const res = await getAllQAPI()

    // 使用类型保护来判断数据类型
    if (isValidAllQuestionData(res)) {
      questionlist.value = res
      console.log(questionlist.value)
    } else {
      console.error('Invalid data format')
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    // 处理错误
  }
}
getall()

// 自定义类型保护函数，判断是否符合 AllQuestionData 类型
function isValidAllQuestionData(data: any): data is AllQuestionData {
  return typeof data === 'object' && Array.isArray(data.allQuestion)
}

const viewInfo = (index: any) => {
  //跳转详情页
  uni.navigateTo({ url: `/pages/detail/detail?q_id=${index}` })
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
    <div v-for="question in questionlist.allQuestion" :key="question.q_id" @click="viewInfo(question.q_id)">
      <uni-card :title="question.title" :sub-title="question.username" :extra="question.date">
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
