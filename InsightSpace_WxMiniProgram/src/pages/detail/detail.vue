<template>
  <view>
    <!-- 问题发布者头像和名称 -->
    <view class="user-info">
      <image class="avatar" src="../../../static/images/avatar0.png"></image>
      <text class="username">{{ question.username }}</text>
    </view>

    <!-- 问题内容 -->

    <text class="qtitle">{{ question.title }}</text>
    <b></b>
    <!-- 问题内容 -->
    <view class="qcontent">
      <text>{{ question.content }}</text>
    </view>
    <b></b>
    <text class="qdate">{{ question.date }}</text>

    <!-- 回答区域 -->
    <view class="answer-section">
      <view v-for="(answer, index) in answers" :key="index" class="answer">
        <!-- 回答者头像和名称 -->
        <view class="user-info">
          <image class="avatar" src="../../../static/images/avatar1.png"></image>
          <text class="username">{{ answer.username }}</text>
        </view>
        <text>{{ answer.content }}</text>
        <!-- 点赞和踩按钮 -->
        <view class="like-dislike">
          <button @click="toggleLike">
            <image src="../../../static/images/like.png" alt="Like" />
          </button>
          <button @click="dislike">
            <image src="../../../static/images/dislike.png" alt="Dislike" />
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
// 使用 setup 函数初始化数据
import { ref, watch } from 'vue'
import { getQAPI } from '@/services/question'
// 获取 q_id
let qid = uni.getStorageSync('q_id')
console.log('q_id:', qid)
const title = ref('')
const content = ref('')
const username = ref('')
const date = ref('')
const question = ref({
  title: '',
  content: '',
  username: '',
  date: '',
})
const getDetails = async () => {
  const res = await getQAPI({ q_id: qid })
  question.value.title = res.title
  question.value.content = res.content
  question.value.username = res.username
  question.value.date = formatDate(res.date)
  console.log(question.value)
}
getDetails()

const isLiked = ref(false)

const toggleLike = () => {
  isLiked.value = !isLiked.value
}

//const likeImage = ref('@/static/images/like.png')

// 监听isLiked的变化，根据状态切换图片
//watch(isLiked, (newValue) => {
//  likeImage.value = newValue ? '@/static/images/like.png' : '@/static/images/liked.png'
//})

const dislike = () => {
  // 处理踩逻辑
}
// 假设这里有多条回答数据
const answers = ref([
  { content: '回答内容1' },
  { content: '回答内容2' },
  // 其他回答数据
])

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
</script>

<style>
/* 样式根据需要自行修改 */
.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 20px;
  margin-top: 10px;
  margin-left: 10px;
}

.username {
  font-size: 14px;
}

.question-content {
  margin-top: 10px;
}

.like-icon {
  width: 13px;
  height: 13px;
  margin-right: 10px;
}

.icon-dislikebtn {}

.icon {
  width: 30px;
  height: 30px;
}

.answer-section {
  margin-top: 20px;
}

.answer {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
}

.qtitle {
  font-weight: bold;
  font-size: 21px;
  margin-left: 5%;
}

.qcontent {
  font-size: 16px;
  margin-left: 5%;
}

.qdate {
  font-size: 12px;
  margin-left: 230px;
}
</style>
