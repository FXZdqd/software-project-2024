<script setup lang="ts">
import {
  getAvatarAPI, resetPasswordAPI, setAvatarAPI,
  reUsernameAPI, getUserAPI, setUserInfoAPI,
  getQuestionAskedByUserAPI,
} from '@/services/user'
import type { ProfileDetail } from '@/types/user'
import { onLoad } from '@dcloudio/uni-app'
import { ref } from 'vue'
import { useUserStore } from '@/stores'
import { onMounted } from 'vue'

const userStore = useUserStore()

// 获取屏幕边界到安全区域距离
const { safeAreaInsets } = uni.getSystemInfoSync()

var photo = ref('')
const isphoto = ref(false)
const getAvatar = async () => {
  let data = await getAvatarAPI({ username: userStore.profile.username });
  if (data.value == 0) {
    isphoto.value = true
    photo.value = 'http://39.109.126.173:39001/api' + data.url;
    console.log(photo);

  } else {
    console.log('获取头像失败');
  }
}
getAvatar();

let filePath = ''
const setAvatar = async () => {
  try {
    uni.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        filePath = res.tempFilePaths[0];
        uni.uploadFile({
          url: 'http://39.109.126.173:39001/api/setAvatar',
          filePath: filePath,
          name: 'photo',
          formData: {
            'username': userStore.profile.username
          },
          success: (uploadFileRes) => {
            console.log(filePath);
            console.log('上传成功:', uploadFileRes.data);
            uni.showToast({
              title: '头像上传成功'
            });
            getAvatar();
          },
          fail: (err) => {
            console.error('上传失败:', err);
          }
        });
      }
    })
  } catch (error) {
    console.error('图片选择失败', error);
  }
}


const isProfile = ref(true)
const isRePwd = ref(false)
// 获取个人信息
const profile = ref<ProfileDetail>({
  username: userStore.profile.username,
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
    const res = await getUserAPI({ username: userStore.profile.username })
    profile.value = res;
    console.log('用户信息为', profile.value);
  } catch (error) {
    console.error('There was an error fetching the questions:', error)
  }
}
getUserProfileData()
onLoad(() => {
  getUserProfileData()
  getAvatar()

})
onMounted(
  getUserProfileData
)

const setUserInfo = async () => {
  const setUSerInfoData = ref({
    username: userStore.profile.username,
    gender: profile.value.gender,
    grade: profile.value.grade,
    department: profile.value.department
  })
  //console.log(setUSerInfoData.value);
  //console.log(profile.value);
  const res = await setUserInfoAPI(setUSerInfoData.value);
  console.log(res.message);
  getUserProfileData
  //console.log('用户的新设置为：', profile.value);
  uni.navigateBack();
  uni.showToast({
    title: '信息设置成功'
  });
}
const onGenderChange: UniHelper.RadioGroupOnChange = (ev) => {
  profile.value.gender = ev.detail.value
}


const rePwdData = ref({
  username: userStore.profile.username,
  old_password: '',
  new_password: '',
  new_password_re: '',
})
const clearRePwdData = () => {
  rePwdData.value = {
    username: userStore.profile.username,
    old_password: '',
    new_password: '',
    new_password_re: '',
  }
}
const repwd = async () => {
  isProfile.value = false;
  const res = await resetPasswordAPI(rePwdData.value);
  console.log(res.value);
  if (res.value == 0) {
    userStore.clearProfile();
    uni.reLaunch({ url: '/pages/login/login' });
    uni.showToast({
      title: '密码修改成功'
    });
  } else if (res.value == 1) {

  } else if (res.value == 2) {
    uni.showToast({
      icon: 'error',
      title: '两次密码不一致'
    });
    clearRePwdData()
  } else if (res.value == 3) {

  } else if (res.value == 4) {
    uni.showToast({
      icon: 'error',
      title: '旧密码错误'
    });
    clearRePwdData()
  }
}

const reUsernameData = ref({
  old_username: userStore.profile.username,
  new_username: ''
})
const clearReUsernameData = () => {
  reUsernameData.value = {
    old_username: userStore.profile.username,
    new_username: ''
  }
}
const loginData = ref(userStore.profile)
const reUsername = async () => {
  let res = await reUsernameAPI(reUsernameData.value)
  console.log(res.value);

  if (res.value == 0) {
    uni.navigateBack();
    uni.showToast({
      title: '修改成功'
    });
    loginData.value.username = reUsernameData.value.new_username;
    userStore.setProfile(loginData.value);

  } else if (res.value == 2) {
    uni.showToast({
      icon: 'error',
      title: '该用户已存在'
    });
    clearReUsernameData();
  } else if (res.value == 3) {
    uni.showToast({
      icon: 'error',
      title: '与旧用户名相同！'
    });
    clearReUsernameData();
  }
}


const years = ref(Array.from({ length: new Date().getFullYear() - 2010 + 1 }, (_, i) => (2010 + i).toString()));
const onYearChange: UniHelper.RegionPickerOnChange = (ev) => {
  profile.value.grade = years.value[ev.detail.value]
  console.log('设置年级', profile.value.grade);
}


const departments = ref([
  '01 材料科学与工程学院',
  '02 电子信息工程学院',
  '03 自动化科学与电气工程学院',
  '04 能源与动力工程学院',
  '05 航空科学与工程学院',
  '06 计算机学院',
  '07 机械工程及自动化学院',
  '08 经济管理学院',
  '09 数学科学学院',
  '10 生物医学与工程学院',
  '11 人文社会科学学院',
  '12 外国语学院',
  '13 交通科学与工程学院',
  '14 可靠性与系统工程学院',
  '15 宇航学院',
  '16 飞行学院',
  '17 仪器科学与光电工程学院',
  '18 北京学院',
  '19 物理学院',
  '20 法学院',
  '21 软件学院',
  '23 未来空天技术学院/高等理工学院',
  '24 中法工程师学院',
  '25 国际学院',
  '26 新媒体艺术与设计学院',
  '27 化学学院',
  '28 马克思主义学院',
  '29 人文与社会科学高等研究院',
  '30 空间与环境学院',
  '31 无人机系统研究院',
  '32 航空发动机研究院',
  '35 国际通用工程学院',
  '37 北航学院',
  '38 医学科学与工程学院',
  '39 网络空间安全学院',
  '41 集成电路科学与工程学院',
  '42 人工智能研究院',
  '43 前沿科学技术创新研究院',
])
const onDepartmentChange: UniHelper.RegionPickerOnChange = (ev) => {
  profile.value.department = departments.value[ev.detail.value]
  console.log('设置院系：', profile.value.department);
}

</script>

<template>
  <view class="viewport">
    <!-- 导航栏 -->
    <view class="navbar" :style="{ paddingTop: safeAreaInsets?.top + 'px' }">
      <navigator open-type="navigateBack" class="back icon-left" hover-class="none"></navigator>
      <view class="title">个人信息</view>
    </view>
    <!-- 头像 -->
    <view class="avatar">
      <view class="avatar-content" v-if="isphoto">
        <image class="image" :src="photo" mode="aspectFill" />
        <view class="text" @click="setAvatar()">点击修改头像</view>
      </view>
      <view class="avatar-content" @click="setAvatar()" v-else>
        <image class="image" src="../../../static/images/avatar1.png" mode="aspectFill" />
        <view class="text">点击修改头像</view>
      </view>
    </view>
    <!-- 表单 -->
    <view class="form" v-if="isProfile">
      <!-- 表单内容 -->
      <view class="form-content">
        <view class="form-item">
          <text class="label">用户名</text>
          <text class="account">{{ userStore.profile.username }}</text>
        </view>
        <view class="form-item">
          <text class="label">性别</text>
          <radio-group @change="onGenderChange">
            <label class="radio">
              <radio value="男" color="#9bcdff" :checked="profile.gender === '男'" />
              男
            </label>
            <label class="radio">
              <radio value="女" color="#9bcdff" :checked="profile.gender === '女'" />
              女
            </label>
          </radio-group>
        </view>
        <view class="form-item">
          <text class="label">年级</text>
          <!-- <input class="input" type="text" placeholder="请填写年级" v-model="profile.grade" /> -->
          <picker mode="selector" :range="years" :value="profile?.grade" @change="onYearChange">
            <view v-if="profile?.grade">{{ profile.grade }}</view>
            <view class="placeholder" v-else>请选择年级</view>
          </picker>

        </view>
        <view class="form-item">
          <text class="label">院系</text>
          <!-- <input class="input" type="text" placeholder="请填写院系" v-model="profile.department" /> -->
          <picker class="picker" :value="profile?.department" mode="selector" :range="departments"
            @change="onDepartmentChange">
            <view v-if="profile?.department">{{ profile.department }}</view>
            <view class="placeholder" v-else>请选择院系</view>
          </picker>

        </view>
      </view>
      <view class="form">
        <view class="form-content">
          <view class="form-item" @click="isProfile = false; isRePwd = false">
            <view class="label">修改用户名</view>
          </view>
          <view class="form-item" @click="isProfile = false; isRePwd = true">
            <view class="label">修改密码</view>
          </view>
        </view>
      </view>
      <!-- 提交按钮 -->
      <button class="form-button" @click="setUserInfo()">保存</button>
    </view>
    <view class="form" v-else-if="isRePwd">
      <view class="form-content">
        <view class="form-item">
          <text class="label">原密码</text>
          <input class="input" :password="true" placeholder="请填写原密码" v-model="rePwdData.old_password" />
        </view>
        <view class="form-item">
          <text class="label">新密码</text>
          <input class="input" :password="true" placeholder="请填写新密码" v-model="rePwdData.new_password" />
        </view>
        <view class="form-item">
          <text class="label">确认新密码</text>
          <input class="input" :password="true" placeholder="请再次填写新密码" v-model="rePwdData.new_password_re" />
        </view>

      </view>
      <button class="form-button" @click="repwd()">提交</button>
      <button class="form-button" @click="isProfile = true">返回</button>
    </view>
    <view class="form" v-else>
      <view class="form-content">
        <view class="form-item">
          <text class="label">新用户名</text>
          <input class="input" placeholder="请填写新用户名" v-model="reUsernameData.new_username" />
        </view>
      </view>
      <button class="form-button" @click="reUsername()">提交</button>
      <button class="form-button" @click="isProfile = true">返回</button>
    </view>
  </view>
</template>

<style lang="scss">
page {
  background-color: #f4f4f4;
}

.viewport {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-size: auto 420rpx;
  background-repeat: no-repeat;
  background-color: #9bcdff;
}

// 导航栏
.navbar {
  position: relative;

  .title {
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: 500;
    color: #fff;
  }

  .back {
    position: absolute;
    height: 40px;
    width: 40px;
    left: 0;
    font-size: 20px;
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

// 头像
.avatar {
  text-align: center;
  width: 100%;
  height: 260rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .image {
    width: 160rpx;
    height: 160rpx;
    border-radius: 50%;
    background-color: #eee;
  }

  .text {
    display: block;
    padding-top: 20rpx;
    line-height: 1;
    font-size: 26rpx;
    color: #fff;

  }
}

// 表单
.form {
  background-color: #f4f4f4;

  &-content {
    margin: 20rpx 20rpx 0;
    padding: 0 20rpx;
    border-radius: 10rpx;
    background-color: #fff;
  }

  &-item {
    display: flex;
    height: 96rpx;
    line-height: 46rpx;
    padding: 25rpx 10rpx;
    background-color: #fff;
    font-size: 28rpx;
    border-bottom: 1rpx solid #ddd;

    &:last-child {
      border: none;
    }

    .label {
      width: 180rpx;
      color: #333;
    }

    .account {
      color: #666;
    }

    .input {
      flex: 1;
      display: block;
      height: 46rpx;
    }

    .radio {
      margin-right: 20rpx;
    }

    .picker {
      flex: 1;
    }

    .placeholder {
      color: #808080;
    }
  }

  &-button {
    height: 80rpx;
    text-align: center;
    line-height: 80rpx;
    margin: 30rpx 20rpx;
    color: #fff;
    border-radius: 80rpx;
    font-size: 30rpx;
    background-color: #9bcdff;
  }
}
</style>