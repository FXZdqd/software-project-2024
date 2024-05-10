<template>
  <view>
    <!-- 问题发布者头像和名称 -->
    <view class="user-info">
      <image class="avatar" src="../../../static/images/avatar0.png"></image>
      <text class="username">{{ question.username }}</text>
      <text class="qdate">{{ question.date }}</text>
    </view>

    <!-- 问题内容 -->

    <text class="qtitle">{{ question.title }}</text>
    <b></b>
    <!-- 问题内容 -->
    <view class="qcontent">
      <text>{{ question.content }}</text>
      <button class="follow-btn">+关注</button>
      <icon>
        <image class="like-icon" :src="likeIconSrc" @tap="toggleLike"></image>
        <image class="report-icon" src="../../../static/images/report.png" @tap="toggleReport"></image>
      </icon>
    </view>

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
          <icon>
            <image class="like-icon" :src="likeIconSrc" @tap="toggleLike"></image>
            <image class="report-icon" src="../../../static/images/report.png" @tap="toggleReport"></image>
          </icon>
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
const likeIconSrc = ref('/static/images/like.png')
const toggleLike = () => {
  isLiked.value = !isLiked.value
  console.log(isLiked.value)
  likeIconSrc.value = isLiked.value ? '/static/images/liked.png' : '/static/images/like.png'
  console.log(likeIconSrc.value)
}

const toggleReport = () => {
  //弹出一个dialog
  uni.showModal({
    title: '举报',
    content: '确定要举报吗？',
    success: function (res) {
      if (res.confirm) {
        //弹出一个表单，用户填写举报理由，输入框至少两行
        uni.showModal({
          title: '举报理由',
          content: '请填写举报理由',
          editable: true,
          success: function (res) {
            if (res.confirm) {
              //用户点击确定，提交举报理由
              console.log('用户提交了举报理由：', res.content)
            } else if (res.cancel) {
              console.log('用户点击取消')
            }
          },
        })
        console.log('用户点击确定')
      } else if (res.cancel) {
        console.log('用户点击取消')
      }
    },
  })
}

// 假设的多条回答数据
const answers = ref([
  { content: '回答内容1ghdhyibfcedaszxcvnhjjknjmvcdzer', username: '用户名1' },
  { content: '回答内容2rzxrcgvhbjnmwserdrtfghbnjmvcdzxcvbnm', username: '用户名2' },
  { content: '回答内容3dxtfcgvhbjnnjhbvgyzretrftyguiytretgvhbjnmvcdzxcvbnm', username: '用户名3' },
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
  width: 25px;
  height: 25px;
  margin-right: 10px;
  margin-left: 270px;
}

.report-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
  margin-left: 12px;
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
  font-size: 10px;
  margin-left: 150px;
}

.follow-btn {
  width: 16%;
  height: 1%;
  margin-right: 6%;

  text-align: auto;
  font-size: 12px;
  background-color: #eef5a7;
  /* 按钮背景色 */
  color: #070707;
  /* 按钮文字颜色 */
  padding: 1px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
