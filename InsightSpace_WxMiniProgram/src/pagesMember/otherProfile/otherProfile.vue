<script setup lang="ts">
import { useUserStore } from '@/stores'
import { ref } from 'vue'
import { getFollowQAPI } from '@/services/question'
import {
  getAvatarAPI,
  getQuestionAskedByUserAPI,
  getQuestionAnsweredByUserAPI,
  getUserAPI,
} from '@/services/user'
import { onMounted } from 'vue'
import type { ProfileDetail } from '@/types/user'
import { onLoad, onShow } from '@dcloudio/uni-app'
const UserStore = useUserStore()

const FollowQ = ref<any[]>([])
const AskQ = ref<any[]>([])
const AnsQ = ref<any[]>([])

//获取会员信息
const userStore = useUserStore()
const otherUsername = uni.getStorageSync('otherUsername')
// 获取屏幕边界到安全区域距离
const { safeAreaInsets } = uni.getSystemInfoSync()
const current = ref(0)
const onClickItem = (e) => {
  if (current.value !== e.currentIndex) {
    current.value = e.currentIndex
    if (current.value == 2) {
      getFollowQ()
    } else if (current.value == 0) {
      getQuestionAskedByUser()
    } else if (current.value == 1) {
      getQuestionAnsweredByUser()
    }
  }
}

const profile = ref<ProfileDetail>({
  username: otherUsername,
  phone: 0,
  is_admin: false,
  is_banned: false,
  reports: 0,
  gender: '',
  grade: '',
  department: ''
})
const getUserProfileData = async () => {
  try {
    const res = await getUserAPI({ username: otherUsername })
    profile.value = res;
    console.log('用户信息为', profile.value);
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}
getUserProfileData()

const scrollTop = ref(0)

const items = ['ta的提问', 'ta的回答', 'ta的关注']

const getFollowQ = async () => {
  try {
    const response = await getFollowQAPI({ username: otherUsername })
    if (Array.isArray(response)) {
      FollowQ.value = response.map((question) => ({
        ...question,
      }))
    } else {
      FollowQ.value = []
    }
    console.log(FollowQ.value)
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}
const getQuestionAskedByUser = async () => {
  try {
    const response = await getQuestionAskedByUserAPI({ username: otherUsername })
    if (Array.isArray(response)) {
      AskQ.value = response.map((question) => ({
        ...question,
      }))
    } else {
      AskQ.value = []
    }
    console.log(AskQ.value)
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}
const getQuestionAnsweredByUser = async () => {
  try {
    const response = await getQuestionAnsweredByUserAPI({ username: otherUsername })
    if (Array.isArray(response)) {
      AnsQ.value = response.map((question) => ({
        ...question,
      }))
    } else {
      AnsQ.value = []
    }
    console.log(AnsQ.value)
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}

const viewInfo = (index: any) => {
  // 将 q_id 存储在本地存储中
  uni.setStorageSync('q_id', index)
  // 跳转详情页
  uni.navigateTo({ url: '/pages/detail/detail' })
}
function formatDate(dateString: any) {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
var photo = ref('')
const isphoto = ref(false)
const getAvatar = async () => {
  let data = await getAvatarAPI({ username: otherUsername })
  if (data.value == 0) {
    isphoto.value = true
    photo.value = 'http://39.109.126.173:39001/api' + data.url
  }
}
getAvatar()

onShow(async () => {
  getFollowQ
  getAvatar
  getQuestionAskedByUser
  getQuestionAnsweredByUser
  console.log('onshow被调用了')
})
</script>

<template>
  <view class="viewport" @click="getAvatar">
    <image class="background-image" src="/static/images/my_bg.jpg" mode="aspectFill" />
    <!-- 个人资料 -->
    <view class="profile" :style="{ paddingTop: safeAreaInsets!.top + 'px' }">
      <view class="overview">
        <image class="avatar" mode="aspectFill" :src="isphoto ? photo : '../../../static/images/avatar1.png'"></image>
        <view class="meta">
          <view class="nickname">{{ otherUsername }}</view>
          <view class="grade">{{ profile.grade }}级</view>
          <view class="department">{{ profile.department }}</view>
        </view>
      </view>


    </view>
    <!-- 分割线 -->
    <!-- <view class="uni-divider" /> -->

    <view class="down">
      <!-- <uni-section class="section"> -->
      <view class="uni-divider" />
      <view class="uni-padding-wrap uni-common-mt">
        <uni-segmented-control :current="current" :values="items" style-type="text" @clickItem="onClickItem" />
      </view>
      <view class="uni-divider" />
      <view class="container">
        <scroll-view class="scroll-view-container" :scroll-y="true" :scroll-top="scrollTop">
          <view class="content">
            <view v-if="current === 0">
              <view class="content-text">
                <div v-for="question in AskQ" :key="question.q_id" @click="viewInfo(question.q_id)">
                  <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
                    <text class="limit-lines">{{ question.content }}</text>
                  </uni-card>
                </div>
              </view>
            </view>
            <view v-if="current === 1">
              <view class="content-text">
                <div v-for="question in AnsQ" :key="question.q_id" @click="viewInfo(question.q_id)">
                  <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
                    <text class="limit-lines">{{ question.content }}</text>
                  </uni-card>
                </div>
              </view>
            </view>
            <view v-if="current === 2">
              <view class="content-text">
                <div v-for="question in FollowQ" :key="question.q_id" @click="viewInfo(question.q_id)">
                  <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
                    <text class="limit-lines">{{ question.content }}</text>
                  </uni-card>
                </div>
              </view>
            </view>

            <view class="bottom">没有更多内容</view>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<style lang="scss">
page {
  height: 100%;
  background-color: #ffffff;
}

.viewport {
  position: sticky;
  width: 100%;
  height: 100%;
}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.uni-common-mt {
  margin-top: 0px;
  padding-top: 0px;
  background-color: #ffffff;
}

.uni-padding-wrap {
  // width: 750rpx;
  padding: 0px 0px;
}

.scroll-view-container {
  height: 450px;
  border: 1px solid #ccc;
  overflow-y: auto;
}

.top {
  overflow: hidden;
}

/* 用户信息 */
.profile {
  margin-top: 100rpx;
  margin-bottom: 20rpx;
  position: relative;

  .overview {
    display: flex;
    height: 170rpx;
    padding: 0 36rpx;
  }

  .avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: #eee;
  }

  .gray {
    filter: grayscale(100%);
  }

  .meta {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    line-height: 30rpx;
    padding: 16rpx 0;
    margin-left: 20rpx;
    bottom: 0;
  }

  .nickname {
    max-width: 350rpx;
    margin-bottom: 35rpx;
    font-size: 50rpx;
    white-space: nowrap;
  }

  .grade {
    margin-bottom: 5rpx;
  }

  .extra {
    display: flex;
    font-size: 20rpx;
  }

  .tips {
    font-size: 22rpx;
  }

  .settings {
    position: absolute;
    bottom: 0;
    right: 40rpx;
    font-size: 30rpx;
  }
}

.uni-divider {
  width: 100%;
  height: 7px;
  background-color: #d6d6d6;
  //margin: 10px 0;
  //margin-top: px;
  overflow: visible;
}

.icon {
  right: 45rpx;
  width: 50rpx;
  height: 50rpx;
}

.down {
  opacity: 0.8;
  background-color: #ffffff;
}

.content {
  opacity: 1;
  //margin-top: 30rpx;

  justify-content: center;
  align-items: center;
  height: 100%;
  //overflow-y: stroll;
}

.bottom {
  text-align: center;
  margin-top: 5px;
  margin-bottom: 25px;
  color: #b7b7b7;
}

.limit-lines {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 2;
}
</style>
