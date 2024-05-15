<template>
  <view>
    <!-- 问题发布者头像和名称 -->
    <view class="user-info">
      <image class="avatar" src="../../../static/images/avatar0.png"></image>
      <text class="username">{{ question.username }}</text>
      <text class="qdate">{{ question.date }}</text>
    </view>

    <!-- 问题内容 -->
    <view class="qtitle">
      <text>{{ question.title }}</text>
    </view>

    <!--标签-->
    <view class="row">
      <view class="col" v-for="(tag, index) in question.tags" :key="index">
        <uni-tag class="tag" :inverted="true" :text="tagname(tag)" :type="getTagType(tag)" />
      </view>
    </view>

    <b></b>
    <!-- 问题内容 -->
    <view class="qcontent">
      <text>{{ question.content }}</text>
      <icon>
        <image class="report-icon" src="/static/images/report1.png" @tap="toggleReportQ"></image>
        <image class="like-icon" :src="likeIconSrc" @tap="toggleLikeQ"></image>
        <image class="follow-icon" :src="followIconSrc" @tap="togglefollow"></image>
      </icon>
    </view>

    <b></b>
    <view>
      <button class="button" type="primary" plain="true" @click="handleAnswer">
        <text class="button-text">去回答</text>
      </button>
    </view>
    <view>
      <!-- 普通弹窗 -->
      <uni-popup class="pop" ref="popup" background-color="#fff" type="bottom">
        <view class="popup-content"><text class="text">我的回答</text>
          <uni-forms-item>
            <uni-easyinput type="textarea" v-model="myanswer" placeholder="请输入您的回答" />
          </uni-forms-item>
          <button type="primary" plain="true" @click="handlegoAnswer">发布</button>
        </view>
      </uni-popup>
    </view>
    <b></b>
    <!-- 回答区域 -->
    <view class="answer-section">
      <view v-for="(answer, index) in question.answers" :key="index" class="answer">
        <!-- 回答者头像和名称 -->
        <view class="user-info">
          <image class="avatar" src="../../../static/images/avatar1.png"></image>
          <text class="username">{{ answer.username }}</text>
        </view>
        <text>{{ answer.content }}</text>
        <!-- 点赞和踩按钮 -->
        <view class="like-dislike">
          <icon>
            <image class="reportA-icon" src="/static/images/report1.png" @tap="toggleReportA(answer.a_id - 1)">
            </image>
            <image class="likeA-icon" :src="answer.is_liked ? '/static/images/liked.png' : '/static/images/like.png'"
              @tap="toggleLikeA(answer.a_id - 1)">
            </image>
          </icon>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
// 使用 setup 函数初始化数据
import { ref } from 'vue'
import {
  getQAPI,
  followAPI,
  unfollowAPI,
  likeQAPI,
  unlikeQAPI,
  likeAAPI,
  unlikeAAPI,
  reportQAPI,
  reportAAPI,
  goAnswerAPI,
} from '@/services/question'
import { useUserStore } from '@/stores'
const popup = ref(null)
const handleAnswer = () => {
  popup.value.open()
}
const handlegoAnswer = () => {
  goAnswer()
  popup.value.close()
}
const myanswer = ref('')
const UserStore = useUserStore()
const goAnswer = async () => {
  const res = await goAnswerAPI({
    q_id: qid,
    content: myanswer.value,
    username: UserStore.profile.username,
  })
  console.log(res)
}
// 获取 q_id
let qid = uni.getStorageSync('q_id')
console.log('q_id:', qid)
const question = ref({
  title: '',
  content: '',
  username: '',
  date: '',
  answers: [],
  tags: [],
  is_liked: Boolean,
  is_followed: Boolean,
})
const getTagType = (tag) => {
  if (tag === 'course') {
    return 'primary'
  } else if (tag === 'research') {
    return 'success'
  } else if (tag === 'further_study') {
    return 'warning'
  } else if (tag === 'competition') {
    return 'error'
  } else {
    return 'default'
  }
}
const tagname = (tag) => {
  if (tag === 'course') {
    return '课程'
  } else if (tag === 'research') {
    return '科研'
  } else if (tag === 'further_study') {
    return '升学'
  } else if (tag === 'competition') {
    return '竞赛'
  } else {
    return '其他'
  }
}
const getDetails = async () => {
  const res = await getQAPI({ q_id: qid, username: UserStore.profile.username })
  question.value.title = res.title
  question.value.content = res.content
  question.value.username = res.username
  question.value.date = formatDate(res.date)
  question.value.answers = res.answers
  question.value.is_liked = res.is_liked
  question.value.is_followed = res.is_followed
  question.value.tags = res.tags
  console.log(question.value)

  if (question.value.is_liked) {
    console.log('已点赞')
    likeIconSrc.value = '/static/images/liked.png'
  } else {
    console.log('未点赞')
    likeIconSrc.value = '/static/images/like.png'
  }
  if (question.value.is_followed) {
    console.log('已收藏')
    followIconSrc.value = '/static/images/followed.png'
  } else {
    console.log('未收藏')
    followIconSrc.value = '/static/images/follow.png'
  }
}
getDetails()

const likeIconSrc = ref('/static/images/like.png')
const followIconSrc = ref('/static/images/follow.png')
const reportIconSrc = ref('/static/images/report1.png')
const reportIconSrcA = [5]
for (let i = 0; i < question.value.answers.length; i++) {
  reportIconSrcA.push('/static/images/report1.png')
}
const likeIconSrcA = [5]
for (let i = 0; i < question.value.answers.length; i++) {
  likeIconSrcA.push('/static/images/like.png')
}
const toggleLikeQ = () => {
  console.log('1', question.value.is_liked)
  if (question.value.is_liked) {
    //取消点赞
    unlikeQ()
    question.value.is_liked = false
  } else {
    //点赞
    likeQ()
    question.value.is_liked = true
  }
  likeIconSrc.value = question.value.is_liked
    ? '/static/images/liked.png'
    : '/static/images/like.png'
  console.log('2', likeIconSrc.value)
}

const toggleLikeA = (id) => {
  console.log('处理回答id的点赞功能:', id)
  if (question.value.answers[id].is_liked) {
    //取消点赞
    unlikeA(id + 1)
    question.value.answers[id].is_liked = false
  } else {
    //点赞
    likeA(id + 1)
    question.value.answers[id].is_liked = true
  }
}

const togglefollow = () => {
  console.log(question.value.is_followed)
  if (question.value.is_followed) {
    console.log('取消关注')
    unfollowQ()
    question.value.is_followed = false
  } else {
    followQ()
    question.value.is_followed = true
  }
  followIconSrc.value = question.value.is_followed
    ? '/static/images/followed.png'
    : '/static/images/follow.png'
  console.log(followIconSrc.value)
}
const likeQ = async () => {
  console.log('执行点赞')
  const res = await likeQAPI({ q_id: qid, username: UserStore.profile.username })
  console.log(res)
}
const unlikeQ = async () => {
  console.log('取消点赞')
  const res = await unlikeQAPI({ q_id: qid, username: UserStore.profile.username })
  console.log(res)
}

const likeA = async (id) => {
  const res = await likeAAPI({ a_id: id, username: UserStore.profile.username })
  console.log(res)
}
const unlikeA = async (id) => {
  const res = await unlikeAAPI({ a_id: id, username: UserStore.profile.username })
  console.log(res)
}
const followQ = async () => {
  const res = await followAPI({ q_id: qid, username: UserStore.profile.username })
  console.log(res)
}
const unfollowQ = async () => {
  const res = await unfollowAPI({ q_id: qid, username: UserStore.profile.username })
  console.log(res)
}
const reportQ = async () => {
  const res = await reportQAPI({ q_id: qid })
  console.log(res)
}
const reportA = async (id) => {
  const res = await reportAAPI({ a_id: id })
  console.log(res)
}

const toggleReportQ = () => {
  //弹出一个dialog
  uni.showModal({
    title: '举报',
    content: '确定要举报吗？',
    success: function (res) {
      if (res.confirm) {
        //弹出一个表单，用户填写举报理由，输入框至少两行
        uni.showModal({
          title: '举报理由',
          content: '',
          editable: true,
          success: function (res) {
            if (res.confirm) {
              console.log('用户提交了举报理由：', res.content)
              reportQ()
              uni.showToast({
                icon: 'success',
                title: '举报成功',
              })
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

const toggleReportA = (id) => {
  //弹出一个dialog
  uni.showModal({
    title: '举报',
    content: '确定要举报吗？',
    success: function (res) {
      if (res.confirm) {
        //弹出一个表单，用户填写举报理由，输入框至少两行
        uni.showModal({
          title: '举报理由',
          content: '',
          editable: true,
          success: function (res) {
            if (res.confirm) {
              //用户点击确定，提交举报理由
              console.log('用户提交了举报理由：', res.content)
              reportA(id + 1)
              uni.showToast({
                icon: 'success',
                title: '举报成功',
              })
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

.pop {
  height: 400px;
}

.follow-icon {
  width: 25px;
  height: 25px;
  margin-right: 2px;
}

.like-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
}

.likeA-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
  margin-left: 13px;
}

.reportA-icon {
  width: 25px;
  height: 25px;
  margin-left: 260px;
}

.report-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
  margin-left: 200px;
}

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
  text-align: left;
}

.qtitle {
  font-weight: bold;
  font-size: 21px;
  margin-left: 5%;
  position: relative;
}

.qcontent {
  font-size: 16px;
  margin-left: 5%;
  position: relative;
  right: 10px;
}

.qdate {
  font-size: 10px;
  margin-left: 150px;
}

.tag {
  width: 30px;
  height: 7px;
}

.row {
  display: flex;
  width: 35%;
  margin-top: 5px;
  margin-bottom: 10px;
  margin-left: 5px;
}

.col {
  flex: 1;
}
</style>
