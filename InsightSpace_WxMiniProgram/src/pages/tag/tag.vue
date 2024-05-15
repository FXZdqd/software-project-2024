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
// 使用 setup 函数初始化数据
import { ref } from 'vue'
import { getTAGQAPI } from '@/services/question'
// 获取 tag
let tag = uni.getStorageSync('tag_name')
// 获取问题列表
const questions = ref([])
console.log('tag_name:', tag)
const getTags = async () => {
    try {
        const res = await getTAGQAPI({
            tag_name: tag,
            sort_questions_by: 'likes',
            sort_questions_order: 'asc',
            sort_answers_by: 'likes',
            sort_answers_order: 'asc',
        })
        console.log('res:', res)
        let q = res.questions
        console.log('questions:', q)
        if (Array.isArray(q)) {
            questions.value = q.map((question) => ({
                ...question,
            }))
            console.log('this:', questions.value)
        } else {
            console.log('不是数组')
            questions.value = []
        }
    } catch (error) {
        console.error('There was an error fetching the questions:', error)
    }
}
getTags()

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
    uni.setStorageSync('q_id', index);
    // 跳转详情页
    uni.navigateTo({ url: '/pages/detail/detail' });
}
</script>

<style lang>

</style>
