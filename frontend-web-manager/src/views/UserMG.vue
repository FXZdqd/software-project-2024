<template>
  <el-button-group style="padding-bottom: 1%">
    <el-button
      type="danger"
      :plain="!change"
      @click="
        () => {
          tableData = users;
          change = true;
        }
      "
      >封禁<el-icon><delete></delete></el-icon>
    </el-button>
    <el-button
      type="primary"
      :plain="change"
      @click="
        () => {
          tableData = tableData2;
          change = false;
        }
      "
      >创建<el-icon><CirclePlus></CirclePlus></el-icon></el-button
  ></el-button-group>
  <el-input
    prefix-icon="Search"
    v-model="searchText"
    placeholder="请输入用户名关键词，按Enter键搜索"
    style="
      width: 350px;
      cursor: pointer;

      position: fixed;
      left: 40%;
    "
    clearable
    @clear="handleClear(users)"
    @keyup.enter="handleSearch(searchText)"
  ></el-input>

  <el-table
    :data="
      tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)
    "
    style="width: 100%"
    max-height="400"
    stripe
  >
    <el-table-column prop="username" label="用户名" width="100">
    </el-table-column>
    <el-table-column width="50">
      <template v-slot="scope">
        <el-icon v-if="scope.row.gender === `女`"><Female></Female></el-icon>
        <el-icon v-else-if="scope.row.gender === `男`"><Male></Male></el-icon>
      </template>
    </el-table-column>
    <el-table-column width="80"
      ><template v-slot="scope"
        ><el-tag v-if="scope.row.is_admin">管理员</el-tag></template
      ></el-table-column
    >
    <el-table-column prop="department" label="学院"></el-table-column>
    <el-table-column prop="grade" label="年级"></el-table-column>
    <el-table-column prop="phone" label="邮箱/手机号"> </el-table-column>
    <el-table-column prop="username" label="api" v-if="change === false">
    </el-table-column>
    <!--el-table-column prop="address" label="注册时间"> </el-table-column-->
    <el-table-column prop="reports" label="被举报次数"></el-table-column>
    <el-table-column fixed="right" label="操作">
      <template v-slot="scope">
        <template v-if="change === false">
          <el-button type="primary"
            >增加<el-icon><CirclePlus></CirclePlus></el-icon>
          </el-button>
        </template>
        <template v-else>
          <el-button
            v-if="!scope.row.is_admin"
            :disabled="scope.row.is_banned"
            :type="scope.row.is_banned ? '' : 'danger'"
            @click.stop="banuser(scope.row.username)"
            >{{ scope.row.is_banned ? "已被" : "" }}封禁<el-icon
              v-if="!scope.row.is_banned"
              style="margin-left: 1px"
              ><delete
            /></el-icon>
          </el-button> </template
      ></template>
    </el-table-column>
  </el-table>
  <!-- 分页器 -->
  <div class="block" style="margin-top: 15px; max-width: 10px">
    <el-pagination
      align="center"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[1, 5, 10, 20]"
      :page-size="pageSize"
      layout=" sizes, prev, pager, next, total,jumper"
      :total="tableData.length"
    >
    </el-pagination>
  </div>
</template>

<script setup>
import { getAllUserByReport, banUser, searchUser } from "@/api/request";
import axios from "axios";
import { ref, onMounted } from "vue";
import { ElMessageBox } from "element-plus";
const users = ref([]);
const tableData = ref([]);
const total = ref(0);
const searchText = ref("");
const change = ref(true);
const tableData2 = ref([
  { username: "为无法通过系统自动认证的新用户创建账号。" },
]);
const currentPage = ref(1);
const pageSize = ref(7);

onMounted(async () => {
  // console.log(this.text);
  try {
    const response = await getAllUserByReport();
    console.log(response.data.users);
    if (Array.isArray(response.data.users)) {
      users.value = response.data.users.map((user) => ({
        ...user,
      }));
      total.value = users.value.length;
      tableData.value = users.value;
    } // else {
    //   ElNotification({
    //     title: "错误",
    //     message: "获取问题列表失败",
    //     type: "error",
    //   });
    //   this.users = [];
    // }
  } catch (error) {
    console.error("There was an error fetching the users:", error);
    //}
  }
});
//每页条数改变时触发 选择一页显示多少行
function handleSizeChange(val) {
  console.log(`每页 ${val} 条`);
  currentPage.value = 1;
  pageSize.value = val;
}
//当前页改变时触发 跳转其他页
function handleCurrentChange(val) {
  console.log(`当前页: ${val}`);
  currentPage.value = val;
}
const handleSearch = async (searchText) => {
  // searchText.value = val;functionsearchText
  //alert("搜索内容：", searchText.value); /?

  // console.log(response.data); // var text = document.getElementById("searchText").value;
  // searchText.addEventListener("keyup", (event) => {
  //   console.log(event.keyCode);
  // });
  console.log("执行查询操作，关键字：", searchText);
  try {
    // this.search(searchText).then((result) => (res = result));
    const response = await searchUser(searchText);
    console.log(response.data);

    if (Array.isArray(response.data.users)) {
      users.value = response.data.users.map((user) => ({
        ...user,
      }));
      total.value = users.value.length;
      tableData.value = users.value;
    } else {
      tableData.value = [];
    }
  } catch (error) {
    console.error("There was an error searching the users:", error);
  }
};
const handleClear = async () => {
  const response = await getAllUserByReport();
  console.log(response.data.users);
  if (Array.isArray(response.data.users)) {
    users.value = response.data.users.map((user) => ({
      ...user,
    }));
    total.value = users.value.length;
    tableData.value = users.value;
  }
};
const banuser = async (username) => {
  ElMessageBox.confirm("确认封禁用户？", "Warning", {
    confirmButtonText: "封禁",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      const response = await banUser(username);
      console.log(response.data);
      // this.$forceUpdate();
      const response1 = await getAllUserByReport();
      console.log(response1.data.users);
      if (Array.isArray(response1.data.users)) {
        users.value = response1.data.users.map((user) => ({
          ...user,
        }));
        total.value = users.value.length;
        tableData.value = users.value;
      }
    })
    .catch(() => {});
};
</script>

<style>
.selected {
  background-color: #00ff00; /* 设置选中时的背景色 */
  color: #ffffff; /* 设置选中时的文字颜色 */
  /* 可以根据需求设置其他样式 */
}
</style>
