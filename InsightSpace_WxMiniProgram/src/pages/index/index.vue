<script setup lang="ts">
import CustomNavBar from './components/CustomNavBar.vue'
import CategoryPanel from './components/CategoryPanel.vue'
import { getAllQAPI, addVAPI } from '@/services/question'
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
const questions = ref<any[]>([])
onShow(
  async () => {
    console.log('首页onShow被调用了')
    try {
      const response = await getAllQAPI()
      if (Array.isArray(response)) {
        questions.value = response.map((question) => ({
          ...question,
        }))
      } else {
        questions.value = []
      }
    } catch (error) {
      console.error('There was an error fetching the questions:', error)
    }
  }, //setInterval(, 5000)
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
const viewid = ref(0)
const viewInfo = (index: any) => {
  uni.setStorageSync('q_id', index)
  viewid.value = index
  addview()
  uni.navigateTo({ url: '/pages/detail/detail' })
}

const addview = async () => {
  const res = await addVAPI({ q_id: viewid.value })
  console.log(res)
}
</script>

<template>
  <CustomNavBar />

  <swiper class="banner">
    <swiper-item>
      <image src="@/static/images/ad1.png"></image>
    </swiper-item>
  </swiper>
  <CategoryPanel />
  <view class="index flex-col">
    <div v-for="question in questions" :key="question.q_id" @click="viewInfo(question.q_id)">
      <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
        <text class="limit-lines">{{ question.content }}</text>
        <uni-icons class="eyes" type="eye" size="17"><text class="viewnum">120</text></uni-icons>
        <uni-icons class="chats" type="chat" size="17"><text class="viewnum">9</text></uni-icons>
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

.limit-lines {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 2;
}

.viewnum {
  font-size: 11px;
  bottom: 10px;
}

.eyes {
  margin-left: 250px;
  margin-right: 5px;
}
</style>
