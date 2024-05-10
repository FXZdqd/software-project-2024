<template>
  <h6>
    增加、封禁用户 <br />
    为无法通过系统自动认证的新用户创建账号。管理员根据用户的行为判断是否应该进行封禁操作。
  </h6>
  <el-button-group style="padding-bottom: 1%">
    <el-button
      type="danger"
      :plain="!this.change"
      @click="
        () => {
          this.tableData = this.users;
          this.change = true;
        }
      "
      >封禁<el-icon><delete></delete></el-icon>
    </el-button>
    <el-button
      type="primary"
      :plain="this.change"
      @click="
        () => {
          this.tableData = this.tableData2;
          this.change = false;
        }
      "
      >创建<el-icon><CirclePlus></CirclePlus></el-icon></el-button
  ></el-button-group>
  <el-input
    type="text"
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
    @clear="handleClear"
    @keyup.enter="handleSearch"
  ></el-input>

  <el-table
    :data="
      tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)
    "
  >
    <el-table-column prop="username" label="用户名" width="180">
    </el-table-column>
    <el-table-column prop="phone" label="邮箱/手机号" width="180">
    </el-table-column>
    <el-table-column
      prop="username"
      label="api"
      width="180"
      v-if="this.change === false"
    >
    </el-table-column>
    <!--el-table-column prop="address" label="注册时间"> </el-table-column-->
    <el-table-column label="操作">
      <template v-slot="scope">
        <el-button type="danger" @click.stop="banuser(scope.row.username)"
          >封禁<el-icon><delete></delete></el-icon>
        </el-button>
      </template>
      <!--template v-else-if="this.change === false" v-if="this.change === true">
        <el-button type="primary"
          >增加<el-icon><CirclePlus></CirclePlus></el-icon>
        </el-button>
      </template-->
    </el-table-column>
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
      :total="tableData.length"
    >
    </el-pagination>
  </div>
</template>

<script>
import { getAllUser, banUser } from "@/api/request";

export default {
  data() {
    return {
      searchText: "",
      change: true,
      tableData: [],
      users: [],
      tableData2: [],
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 8, // 每页的数据条数
    };
  },

  async mounted() {
    try {
      const response = await getAllUser();
      console.log(response.data.allUsers);
      if (Array.isArray(response.data.allUsers)) {
        this.users = response.data.allUsers.map((user) => ({
          ...user,
        }));
        this.total = this.users.length;
        this.tableData = this.users;
      } else {
        ElNotification({
          title: "错误",
          message: "获取问题列表失败",
          type: "error",
        });
        this.users = [];
      }
    } catch (error) {
      console.error("There was an error fetching the users:", error);
      //}
    }
  },
  methods: {
    handleSearch() {
      alert("搜索内容：", this.searchText);
    },
    //每页条数改变时触发 选择一页显示多少行
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.currentPage = 1;
      this.pageSize = val;
    },
    //当前页改变时触发 跳转其他页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
    },
    handleSearch: async () => {
      // searchText.value = val;function
      //alert("搜索内容：", searchText.value); /?
      try {
        console.log("执行查询操作，关键字：", searchText.value);
        //api
      } catch (error) {
        console.error("There was an error searching the questions:", error);
      }
    },
    handleClear: async () => {
      const response = await getAllUser();
      if (Array.isArray(response.data)) {
        users.value = response.data.map((user) => ({
          ...user,
        }));
        total.value = users.value.length;
        // console.log(questions.value.length, total.value)
      } else {
        ElNotification({
          title: "错误",
          message: "获取问题列表失败",
          type: "error",
        });
        users.value = [];
      }
    },
    banuser: async (username) => {
      const response = await banUser(username);
      if (response.data.value === 0) {
        const response = await getAllUser();
        if (Array.isArray(response.data)) {
          users.value = response.data.map((user) => ({
            ...user,
          }));
          total.value = users.value.length;
          // console.log(questions.value.length, total.value)
        } else {
          users.value = [];
        }
      }
    },
  },
};
</script>

<style>
.selected {
  background-color: #00ff00; /* 设置选中时的背景色 */
  color: #ffffff; /* 设置选中时的文字颜色 */
  /* 可以根据需求设置其他样式 */
}
</style>
