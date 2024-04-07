<script setup lang="ts">
import { createQAPI } from '@/services/question'
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores'
import Editor from './components/editor.vue'
const UserStore = useUserStore()

const createQdata = ref({
  title: '',
  content: '',
  username: UserStore.profile.username
})

const rule = () =>{
  if(createQdata.value.content == ''){
    uni.showToast({
      icon: 'none',
      title: '内容不能为空'
    });
  }
  else if(createQdata.value.title == ''){
    uni.showToast({
      icon: 'none',
      title: '标题不能为空'
    });
  }else{
    addQ();
  }
}

const addQ = async () => {
  let result = await createQAPI(createQdata.value);
  if (result.value === 0) {
    console.log('发布成功');
    clearCreateQData();
    //跳转首页
    uni.switchTab({ url: '/pages/index/index' });
    uni.showToast({
      title: '发布成功'
    });
  }else if(result.value === 1){

  }
}

const clearCreateQData = () => {
  createQdata.value = {
    title: '',
    content: '',
    username: UserStore.profile.username
  }
}
</script>


<template>
  <!-- <Editor /> -->
  <button class="mini-btn" style="background-color:#d4e4ff" size="default" @click="rule">发布</button>
  <uni-section title="提问标题" subTitle="不超过255字符" type="line" padding>
    <uni-easyinput class="uni-mt-5" trim="all" v-model="createQdata.title" placeholder="请输入标题"></uni-easyinput>
  </uni-section>
  <uni-section title="提问内容" subTitle="不超过 4294967295 字符" type="line" padding>
    <uni-easyinput type="textarea" autoHeight v-model="createQdata.content" placeholder="请输入提问内容" focus></uni-easyinput>
  </uni-section>

</template>

<style scoped></style>
