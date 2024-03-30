<template>
  <div class="questions-container">
    <el-row type="flex" justify="center">
      <el-col :span="18">
        <h1>问题列表</h1>
        <el-collapse v-model="activeNames" @change="handleCollapseChange">
          <el-collapse-item
              v-for="question in questions"
              :key="question.id"
              :name="`question-${question.id}`">
            <template #title>
              <div class="question-title">
                {{ question.title }}
                <el-tag size="small">{{ formatDate(question.date) }}</el-tag>
                <el-link icon="el-icon-view" @click.stop :underline="false">{{ question.views }} 浏览</el-link>
                <el-button
                    type="text"
                    @click.stop="likeQuestion(question.id)"
                    icon="el-icon-thumb">
                  {{ question.likes }}
                </el-button>
              </div>
            </template>
            {{ question.content }}
            <el-button
                size="mini"
                class="delete-btn"
                @click.stop="deleteQuestion(question.id)"
                type="danger">
              删除问题
            </el-button>
          </el-collapse-item>
        </el-collapse>
      </el-col>
    </el-row>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElContainer, ElHeader, ElMain, ElCollapse, ElCollapseItem, ElTag, ElLink, ElButton, ElNotification } from 'element-plus';

const questions = ref([]);
const activeNames = ref([]);

onMounted(async () => {
  try {
    const response = await axios.post('http://39.109.126.173:39000/api/getAllQuestion');
    if (Array.isArray(response.data.allQuestion)) {
      questions.value = response.data.allQuestion.map(question => ({
        ...question,
      }));
    } else {
      ElNotification({
        title: '错误',
        message: '获取问题列表失败',
        type: 'error',
      });
      questions.value = [];
    }
  } catch (error) {
    console.error("There was an error fetching the questions:", error);
  }
});

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function handleCollapseChange(val) {
  activeNames.value = val;
}

function likeQuestion(id) {
  console.log(`Like question ${id}. (Not implemented)`);
}

function deleteQuestion(id) {
  console.log(`Delete question ${id}. (Not implemented)`);
}
</script>

<style scoped>
.questions-container {
  margin: 20px;
}

.el-col {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  border-radius: 4px;
}

.question-title {
  display: flex;
  align-items: center;
  font-size: 16px; /* 调整字体大小使标题更突出 */
}

.delete-btn {
  margin-top: 12px;
}

.h1 {
  text-align: left; /* 标题左对齐 */
  margin-bottom: 20px; /* 增加标题下的空白间距 */
}
</style>