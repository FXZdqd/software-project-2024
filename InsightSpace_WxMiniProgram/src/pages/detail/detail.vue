<template>
  <view>
    <!-- 问题发布者头像和名称 -->
    <view class="user-info">
      <image class="avatar" :src="question.creator.avatar" mode="aspectFill"></image>
      <text class="username">{{ question.creator.name }}</text>
    </view>

    <!-- 问题内容 -->
    <view class="question-content">
      <text>{{ question.content }}</text>
    </view>

    <!-- 回答区域 -->
    <view class="answer-section">
      <view v-for="(answer, index) in answers" :key="index" class="answer">
        <text>{{ answer.content }}</text>
        <!-- 其他回答相关内容 -->
      </view>
    </view>

    <!-- 点赞和踩按钮 -->
    <view class="like-dislike">
      <button class="icon-btn" @click="like">
        <image class="icon" src="@/static/images/点赞前.png" mode="aspectFit"></image>
      </button>
      <button class="icon-btn" @click="dislike">
        <image class="icon" src="@/static/images/点赞.png" mode="aspectFit"></image>
      </button>
    </view>
  </view>
</template>

<script setup>
// 使用 setup 函数初始化数据
import { ref } from 'vue'

const question = {
  creator: {
    avatar: '问题发布者头像地址',
    name: '问题发布者名称',
  },
  content: '问题内容',
}
const like = () => {
  // 处理点赞逻辑
}

const dislike = () => {
  // 处理踩逻辑
}
// 假设这里有多条回答数据
const answers = ref([
  { content: '回答内容1' },
  { content: '回答内容2' },
  // 其他回答数据
])
</script>

<style>
/* 样式根据需要自行修改 */
.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
}

.question-content {
  margin-top: 10px;
}

.like-dislike {
  display: flex;
  align-items: center;
}

.icon-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
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
}
</style>
