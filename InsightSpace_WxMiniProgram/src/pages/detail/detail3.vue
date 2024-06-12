<template>
  <view>
    <!-- 问题发布者头像和名称 -->
    <view class="user-info">
      <image v-if="question.url !== null" class="avatar" :src="'http://39.109.126.173:39001/api' + question.url"
        @tap="toggleSee(question.username)" />
      <image v-else class="avatar" src="@/static/images/avatar1.png" @tap="toggleSee(question.username)" />
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
        <image v-if="question.username !== name" class="report-icon" src="/static/images/report1.png"
          @tap="toggleReportQ">
        </image>
        <image v-else class="report-icon" src="/static/images/delete.png" @tap="toggleDeleteQ">
        </image>
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
          <img v-if="answer.url !== null" class="avatar" :src="'http://39.109.126.173:39001/api' + answer.url"
            @tap="toggleSee(answer.username)" />
          <img v-else class="avatar" src="@/static/images/avatar1.png" @tap="toggleSee(answer.username)" />
          <text class="username">{{ answer.username }}</text>
        </view>
        <text>{{ answer.content }}</text>
        <!-- 点赞和踩按钮 -->
        <view class="like-dislike">
          <icon>
            <image class="likeA-icon" :src="likeIconSrcA"
              @tap="toggleLikeA(answer.a_id, answer.is_liked, answer.username, index)">
            </image>
            <image v-if="answer.username !== name" class="reportA-icon" src="/static/images/report1.png"
              @tap="toggleReportA(answer.a_id)">
            </image>
            <image v-else class="reportA-icon" src="/static/images/delete.png" @tap="toggleDeleteA(answer.a_id)">
            </image>
          </icon>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
// 使用 setup 函数初始化数据
import { ref, onMounted } from 'vue'
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
  delQAPI,
  delAAPI,
} from '@/services/question'
import { useUserStore } from '@/stores'
import { deleteUserAPI } from '@/services/user'
const popup = ref(null)
const name = ref('')
// 获取 q_id
let qid = uni.getStorageSync('q_id')
console.log('q_id:', qid)
const question = ref({
  title: '',
  content: '',
  username: '',
  date: '',
  answers: [null],
  tags: [null],
  url: '',
  is_liked: Boolean,
  is_followed: Boolean,
})
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
  if (res.url == 'null') question.value.url = ''
  else question.value.url = res.url
  question.value.date = formatDate(res.date)
  question.value.answers = res.answers
  question.value.is_liked = res.is_liked
  question.value.is_followed = res.is_followed
  question.value.tags = res.tags
  name.value = UserStore.profile.username
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
const likeIconSrcA = ref('/static/images/like.png')
const followIconSrc = ref('/static/images/follow.png')
const reportIconSrc = ref('/static/images/report1.png')
const toggleSee = (name) => {
  uni.setStorageSync('otherUsername', name)
  uni.navigateTo({ url: '/pagesMember/otherProfile/otherProfile' })
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
const flag = ref(false)
const toggleLikeA = (id, is_liked, name, index) => {
  console.log('处理回答id的点赞功能:', id)
  if (flag.value) {
    if (is_liked) {
      //取消点赞
      unlikeA(id, name)
      question.value.answers[index].is_liked = false
      console.log(
        'answers数组第',
        index,
        '个元素的is_liked属性变为:',
        question.value.answers[index].is_liked,
      )
    } else {
      //点赞
      likeA(id, name)
      question.value.answers[index].is_liked = true
      console.log(
        'answers数组第',
        index,
        '个元素的is_liked属性变为:',
        question.value.answers[index].is_liked,
      )
    }
    flag.value = false
  } else {
    if (is_liked) {
      //点赞
      likeA(id, name)
      question.value.answers[index].is_liked = true
      console.log(
        'answers数组第',
        index,
        '个元素的is_liked属性变为:',
        question.value.answers[index].is_liked,
      )
    } else {
      //取消点赞
      unlikeA(id, name)
      question.value.answers[index].is_liked = false
      console.log(
        'answers数组第',
        index,
        '个元素的is_liked属性变为:',
        question.value.answers[index].is_liked,
      )
    }
    flag.value = true
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
const delQ = async () => {
  const res = await delQAPI({ q_id: qid })
  console.log(res)
}
const delA = async (id) => {
  const res = await delAAPI({ a_id: id })
  console.log(res)
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

const likeA = async (id, username) => {
  const res = await likeAAPI({ a_id: id, username: username })
  console.log(res)
}
const unlikeA = async (id, username) => {
  const res = await unlikeAAPI({ a_id: id, username: username })
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
const toggleDeleteA = (id) => {
  uni.showModal({
    title: '删除',
    content: '确定要删除吗？',
    success: function (res) {
      if (res.confirm) {
        console.log('用户点击确定')
        delA(id)
      } else if (res.cancel) {
        console.log('用户点击取消')
      }
    },
  })
}
const toggleDeleteQ = () => {
  uni.showModal({
    title: '删除',
    content: '确定要删除吗？',
    success: function (res) {
      if (res.confirm) {
        console.log('用户点击确定')
        delQ()
      } else if (res.cancel) {
        console.log('用户点击取消')
      }
    },
  })
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
              reportA(id)
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
  margin-left: 260px;
}

.reportA-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
  margin-left: 13px;
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
