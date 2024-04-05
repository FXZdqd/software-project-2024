<template>
  <el-input
    type="text"
    prefix-icon="Search"
    v-model="searchText"
    placeholder="请输入,Enter键搜索"
    style="width: 270px; cursor: pointer"
    @keyup.enter="handleSearch"
  ></el-input>
  <div class="questions-container">
    <el-table
      :data="questions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
      style="width: 100%"
      ><el-table-column type="expand" look="浏览详情">
        <template v-slot="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="回答：">
              <span>{{ props.row.content }}</span>
            </el-form-item>
            <el-button
              size="mini"
              class="delete-btn"
              @click.stop="deleteQuestion(props.row.q_id)"
              type="danger"
              style="float: right"
            >
              删除问题<el-icon><delete></delete></el-icon>
            </el-button>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="问题"
        ><template v-slot="scope">{{ scope.row.title }}</template></el-table-column
      >
      <el-table-column label="时间">
        <template v-slot="scope">{{ formatDate(scope.row.date) }}</template></el-table-column
      >
      <!--el-link icon="el-icon-view" @click.stop :underline="false"<el-tag size="small">
            ><template v-slot="scope">{{ scope.row.views }} 浏览</template></el-link
          >
          <el-button type="text" @click.stop="likeQuestion(questions.q_id)" icon="el-icon-thumb">
            {{ questions.likes }}
          </el-button-->
      <!--el-table-column><template slot-scope="scope">{{ questions.title }}</template></el-table-column-->
    </el-table>

    <!-- 分页器 -->
    <div class="block" style="margin-top: 15px">
      <el-pagination
        align="center"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[1, 5, 10, 20]"
        :page-size="pageSize"
        layout=" sizes, prev, pager, next, total,jumper"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElButton, ElNotification } from 'element-plus'
import {getAllQuestions,delQuestion} from "@/api/request"
const questions = ref([])
const activeNames = ref([])
const searchText = ref('')
const currentPage = ref(1) // 当前页码
const total = ref(0) // 总条数
const pageSize = ref(8) // 每页的数据条数

onMounted(
  async () => {
    try {
      const response = await getAllQuestions()
      if (Array.isArray(response.data.allQuestion)) {
        questions.value = response.data.allQuestion.map((question) => ({
          ...question
        }))
        total.value = questions.value.length
        // console.log(questions.value.length, total.value)
      } else {
        ElNotification({
          title: '错误',
          message: '获取问题列表失败',
          type: 'error'
        })
        questions.value = []
      }
    } catch (error) {
      console.error('There was an error fetching the questions:', error)
    }
  } //setInterval(, 5000)
)

function formatDate(dateString) {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

function handleCollapseChange(val) {
  activeNames.value = val
}

function likeQuestion(id) {
  console.log(`Like question ${id}. (Not implemented)`)
}

const deleteQuestion = async (id) => {
  try {
    const response = await delQuestion(id)
    if (response.data === 0) {
      console.log(`Delete question ${id}. (Not implemented)`)
      const response = await getAllQuestions()
      if (Array.isArray(response.data.allQuestion)) {
        questions.value = response.data.allQuestion.map((question) => ({
          ...question
        }))
        total.value = questions.value.length
        // console.log(questions.value.length, total.value)
      } else {
        ElNotification({
          title: '错误',
          message: '获取问题列表失败',
          type: 'error'
        })
        questions.value = []
      }
    } else {
      console.log(response.data)
    }
  } catch (error) {
    console.error('There was an error deleting the questions:', error)
  }
}
function handleSizeChange(val) {
  console.log(`每页 ${val} 条`)
  currentPage.value = 1
  pageSize.value = val
}
//每页条数改变时触发 选择一页显示多少行

//当前页改变时触发 跳转其他页
function handleCurrentChange(val) {
  console.log(`当前页: ${val}`)
  currentPage.value = val
}
const handleSearch = () => {
  alert('搜索内容：', searchText) ///?
  //api
}
</script>

<style scoped>
.questions-container {
  margin: 3px;
  overflow: hidden scroll;
  height: 450px;
}

.el-col {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.question-title {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.delete-btn {
  margin-top: 12px;
}

.h1 {
  text-align: left;
  margin-bottom: 20px;
}
</style>
