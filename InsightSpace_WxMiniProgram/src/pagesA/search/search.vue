//新建一个空白的搜索页面
<template>
  <view class="uni-padding-wrap uni-common-mt">
    <uni-segmented-control :current="current" :values="items" style-type="text" @clickItem="onClickItem" />
  </view>
  <view v-if="current === 0" class="index">
    <div v-for="question in questions" :key="question.q_id" @click="viewInfo(question.q_id)">
      <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
        <text>{{ question.content }}</text>
      </uni-card>
    </div>
  </view>
  <view v-if="current === 1" class="index">
    <div v-for="user in users" :key="user.username" @click="viewUser(user.username)">
      <uni-card>
        <img v-if="user.base64 !== null" class="avatar" :src="'data:image/jpeg;base64,' + user.base64" />
        <img v-else class="avatar" src="@/static/images/avatar1.png" />
        <text class="username">{{ user.username }}</text>
      </uni-card>
    </div>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getKeywordQAPI } from '@/services/question'
import { searchUserAPI } from '@/services/user'
const sort = ref('')
const current = ref(0)
const items = ['问题', '用户']
let k = ''
onMounted(() => {
  let str = uni.getStorageSync('valstr')
  k = str
  let sor = uni.getStorageSync('sort')
  console.log('keyword:', str)
  console.log('sort:', sor)
  if (sor == 0 || sor == 1) {
    sort.value = 'likes'
  } else if (sor == 2) {
    sort.value = 'date'
  } else if (sor == 3) {
    sort.value = 'views'
  } else if (sor == 4) {
    sort.value = 'relevant'
  }
  searchkey(str, sort.value)
})
const onClickItem = (e) => {
  if (current.value !== e.currentIndex) {
    current.value = e.currentIndex
    if (current.value === 1) {
      searchUser(k)
    }
    console.log('current:', current.value)
  }
}
const questions = ref([
  {
    q_id: 0,
    title: 'string',
    content: 'string',
    date: 'string',
    likes: 0,
    views: 0,
    tags: [null],
    username: 'string',
  },
])
const users = ref([
  {
    username: 'string',
    phone: 'string',
    gender: 'string',
    grade: 'string',
    department: 'string',
    base64: 'string',
  },
])
const searchkey = async (word, sort) => {
  try {
    const response = await getKeywordQAPI({
      keyword: word,
      sort_questions_by: sort,
      sort_questions_order: 'desc',
      sort_answers_by: 'likes',
      sort_answers_order: 'desc',
    })
    console.log('res:', response)
    if (Array.isArray(response)) {
      questions.value = response.map((question) => ({
        ...question,
      }))
      console.log('this:', questions.value)
    } else {
      questions.value = []
    }
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}
const searchUser = async (word) => {
  try {
    const response = await searchUserAPI({
      keyword: word,
    })
    console.log('res:', response)
    let u = response.users
    if (Array.isArray(u)) {
      users.value = u.map((user) => ({
        ...user,
      }))
      console.log('this:', users.value)
    } else {
      users.value = []
    }
  } catch (error) {
    console.error('There was an error fetching the users information:', error)
  }
}
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
const viewInfo = (index) => {
  uni.setStorageSync('q_id', index)
  uni.navigateTo({ url: '/pagesA/detail/detail' })
}
const viewUser = (name) => {
  uni.setStorageSync('otherUsername', name)
  uni.navigateTo({ url: '/pagesMember/otherProfile/otherProfile' })
}
</script>

<style scoped>
.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background-color: #eee;
}

.username {
  margin-left: 20px;
}
</style>
