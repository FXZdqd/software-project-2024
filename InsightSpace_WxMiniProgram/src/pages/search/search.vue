//新建一个空白的搜索页面
<template>
    <view class="index">
        <div v-for="question in questions" :key="question.q_id" @click="viewInfo(question.q_id)">
            <uni-card :title="question.title" :sub-title="question.username" :extra="formatDate(question.date)">
                <text>{{ question.content }}</text>
            </uni-card>
        </div>
    </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getKeywordQAPI } from '@/services/question'
const sort = ref('')
onMounted(() => {
    let str = uni.getStorageSync('valstr')
    let sor = uni.getStorageSync('sort')
    console.log('keyword:', str)
    console.log('sort:', sor)
    if(sor==0 || sor==1){
        sort.value = 'likes'
    }
    else if(sor == 2){
        sort.value = 'date'
    }
    else if(sor == 3){
        sort.value = 'views'
    }
    else if(sor == 4){
        sort.value = 'relevant'
    }
    searchkey(str,sort.value)
})

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
    // 将 q_id 存储在本地存储中
    uni.setStorageSync('q_id', index)
    // 跳转详情页
    uni.navigateTo({ url: '/pages/detail/detail' })
}
</script>

<style scoped></style>
