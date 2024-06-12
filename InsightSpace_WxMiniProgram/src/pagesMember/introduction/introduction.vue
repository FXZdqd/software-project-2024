<template>
  <view class="container">
    <image class="background-image" src="@/static/images/ad2.png" mode="aspectFill" />
    <!-- 标题 -->
    <view class="header">
      <text class="title">北航校园问答平台</text>
    </view>

    <!-- 特点介绍 -->
    <view class="features">
      <view class="feature">
        <view class="feature-title">快速解答</view>
        <view class="feature-text">随时解决你的疑惑</view>
      </view>
      <view class="feature">
        <view class="feature-title">多方资源</view>
        <view class="feature-text">整合学校各部门资源</view>
      </view>
      <view class="feature">
        <view class="feature-title">AI智能辅助</view>
        <view class="feature-text">借助人工智能技术</view>
      </view>
      <view class="feature">
        <view class="feature-title">交流分享</view>
        <view class="feature-text">与其他用户交流讨论</view>
      </view>
    </view>

    <!-- 使用说明 -->
    <view class="usage">
      <view class="usage-title">如何使用</view>
      <view class="usage-text">1. 提问搜索：输入问题或关键词搜索</view>
      <view class="usage-text">2. AI问答：尝试使用AI问答功能</view>
      <view class="usage-text">3. 交流互动：分享知识和经验</view>
    </view>


  </view>
</template>

<style>
.container {
  padding: 20px;
}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}


.header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-bottom: 30px;
}

.feature {
  text-align: center;
  width: 45%;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 8px;
  background-color: #ffffff;
}

.feature-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.feature-text {
  font-size: 16px;
}

.usage {
  margin-bottom: 20px;
}

.usage-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.usage-text {
  font-size: 16px;
  margin-bottom: 5px;
}

.join,
.contact {
  text-align: center;
  margin-bottom: 20px;
}

.join-title,
.contact-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.join-text,
.contact-text {
  font-size: 16px;
}
</style>
