<template>
  <el-input
    type="text"
    prefix-icon="Search"
    v-model="searchText"
    placeholder="请输入关键词，按Enter键搜索"
    style="
      width: 350px;
      cursor: pointer;
      padding-bottom: 10px;
      padding-left: 3%;
    "
    clearable
    @clear="handleClear"
    @keyup.enter="handleSearch"
  ></el-input>
  <!--el-button type="primary" @click="$emit('searchClick')">搜索</el-button>
  <el-alert>{{ searchText }}</el-alert-->
  <div class="questions-container">
    <el-table
      :data="
        questions.slice((currentPage - 1) * pageSize, currentPage * pageSize)
      "
      style="width: 100%"
      max-height="400"
      stripe
      @filter-change="filtchange"
      ><el-table-column type="expand" look="浏览详情">
        <template v-slot="props">
          <el-form class="demo-table-expand">
            <el-form-item
              label="问题内容："
              style="padding-left: 20px; font-weight: bolder"
              ><!--span slot="label"><span style="color: #f56c6c;font-size: 14px;"> * </span-->
              <span>{{ props.row.content }}</span>
            </el-form-item>
            <el-form-item label="回答：" style="padding-left: 20px">
              <span>{{ props.row.answer }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="问题标题"
        ><template v-slot="scope">{{
          scope.row.title
        }}</template></el-table-column
      >
      <el-table-column label="时间">
        <template v-slot="scope">{{
          formatDate(scope.row.date)
        }}</template></el-table-column
      >
      <el-table-column label="提问者">
        <template v-slot="scope">{{
          scope.row.username
        }}</template></el-table-column
      >
      <el-table-column
        label="Tag"
        :filters="[
          { text: 'course', value: 'course' },
          { text: 'research', value: 'research' },
          { text: 'further_study', value: 'further_study' },
          { text: 'competition', value: 'competition' },
          { text: 'other', value: 'other' },
        ]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template v-slot="scope">
          <el-tag
            v-for="(val, key) in scope.row.tags"
            :key="key"
            :type="tagMap(val)"
            round
            >{{ val }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作">
        <el-button @click.stop="deleteQuestion(props.row.q_id)" type="danger">
          删除问题<el-icon><delete></delete></el-icon> </el-button
      ></el-table-column>
      <!--el-link icon="el-icon-view" @click.stop :underline="false"<el-tag size="small">
            ><template v-slot="scope">{{ scope.row.views }} 浏览</template></el-link
          >@keyup.enter="handle"
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
import { ref, onMounted } from "vue";
import axios from "axios";
import { ElButton, ElNotification } from "element-plus";
// import type { ,TagProps  } from "element-plus";
import {
  getAllQuestions,
  delQuestion,
  GetQuesByKeyword,
  GetQuesByTag,
} from "@/api/request";
const questions = ref([]);
const activeNames = ref([]);
const searchText = ref("");
const currentPage = ref(1); // 当前页码
const total = ref(0); // 总条数
const pageSize = ref(8); // 每页的数据条数

onMounted(
  async () => {
    try {
      const response = await getAllQuestions();
      console.log(response.data);
      if (Array.isArray(response.data)) {
        questions.value = response.data.map((question) => ({
          ...question,
        }));
        total.value = questions.value.length;
        // console.log(questions.value.length, total.value)
      } else {
        ElNotification({
          title: "错误",
          message: "获取问题列表失败",
          type: "error",
        });
        questions.value = [];
      }
    } catch (error) {
      console.error("There was an error fetching the questions:", error);
    }
  } //setInterval(, 5000)
);

function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function handleCollapseChange(val) {
  activeNames.value = val;
}

function likeQuestion(id) {
  console.log(`Like question ${id}. (Not implemented)`);
}

const deleteQuestion = async (id) => {
  try {
    const response = await delQuestion(id);
    if (response.data.value === 0) {
      console.log(`Delete question ${id}. (Not implemented)`);
      const response = await getAllQuestions();
      if (Array.isArray(response.data)) {
        questions.value = response.data.map((question) => ({
          ...question,
        }));
        total.value = questions.value.length;
        // console.log(questions.value.length, total.value)
      } else {
        ElNotification({
          title: "错误",
          message: "获取问题列表失败",
          type: "error",
        });
        questions.value = [];
      }
    } else {
      console.log(response.data);
    }
  } catch (error) {
    console.error("There was an error deleting the questions:", error);
  }
};
function handleSizeChange(val) {
  console.log(`每页 ${val} 条`);
  currentPage.value = 1;
  pageSize.value = val;
}
//每页条数改变时触发 选择一页显示多少行

//当前页改变时触发 跳转其他页
function handleCurrentChange(val) {
  console.log(`当前页: ${val}`);
  currentPage.value = val;
}
const handleSearch = async () => {
  // searchText.value = val;function
  //alert("搜索内容：", searchText.value); /?
  try {
    console.log("执行查询操作，关键字：", searchText.value);
    const response = await GetQuesByKeyword(searchText.value);
    console.log(response.data);
    if (Array.isArray(response.data)) {
      questions.value = response.data.map((question) => ({
        ...question,
      }));
      total.value = questions.value.length;
      // console.log(questions.value.length, total.value)
    } else {
      ElNotification({
        title: "错误",
        message: "获取问题列表失败",
        type: "error",
      });
      questions.value = [];
    } //api
  } catch (error) {
    console.error("There was an error searching the questions:", error);
  }
};
const handleClear = async () => {
  const response = await getAllQuestions();
  if (Array.isArray(response.data)) {
    questions.value = response.data.map((question) => ({
      ...question,
    }));
    total.value = questions.value.length;
    // console.log(questions.value.length, total.value)
  } else {
    ElNotification({
      title: "错误",
      message: "获取问题列表失败",
      type: "error",
    });
    questions.value = [];
  }
};

const filtchange = async (filters) => {
  // searchText.value = val;function
  //alert("搜索内容：", searchText.value); /?
  console.log(filters[String(Object.keys(filters))]);
  // const response = await GetQuesByTag(filters[String(Object.keys(filters))]);
  // total.value = response.data.length; //this.$refs.table;
  // if (filters.category.length > 0) {
  //   _this.status = filters.category[0];
  // } else {
  //   _this.status = undefined;
  // }
};

const filterTag = (value, row) => {
  for (var i = 0; i < row.tags.length; i++) {
    if (row.tags[i] === value) {
      return true;
    }
  }
};
const tagMap = (tag) => {
  //???
  if (tag === "course") {
    return "success";
  } else if (tag === "reseach") {
    return "primary";
  } else if (tag === "further_study") {
    return "info";
  } else if (tag === "competition") {
    return "warning";
  } else if (tag === "other") {
    return "danger";
  }
};
</script>

<style scoped>
.questions-container {
  margin: 3px;
  overflow: auto;
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
<!-- {
  "title": "test",
  "content": " ",
  "username": "zjk1"
} -->
