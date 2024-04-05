<template>
  <h1>
    增加、封禁用户 <br />
    为无法通过系统自动认证的新用户创建账号。管理员根据用户的行为判断是否应该进行封禁操作。
  </h1>
  <el-input
    type="text"
    prefix-icon="Search"
    v-model="searchText"
    placeholder="请输入,Enter键搜索"
    style="width: 270px; cursor: pointer"
    @keyup.enter="handleSearch"
  ></el-input>
  <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)">
    <el-table-column prop="date" label="用户名" width="180"> </el-table-column>
    <el-table-column prop="name" label="邮箱" width="180"> </el-table-column>
    <el-table-column prop="address" label="注册时间"> </el-table-column>
    <el-table-column prop="operate" label="操作">
      <template v-slot="scope" v-if="name === '第一页'">
        <el-button type="danger" v-model="scope.row.Id" size="mini"
          >封禁
          <el-icon><delete></delete></el-icon>
        </el-button>
      </template>
      <template v-slot="scope" v-else-if="name === '第二页'">
        <el-button type="primary" v-model="scope.row.Id" size="mini">增加 </el-button>
      </template>
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
export default {
  data() {
    return {
      searchText: '',
      tableData: [
        //在<el-tabel>标签里的 :data的值是tabelData，表示表格的数据都在tabelData中，所以是这个写法。
        {
          date: '2016-05-02',
          name: '第一页',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-02',
          name: '第一页',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-02',
          name: '第er页',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-02',
          name: '第er页',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-02',
          name: '第一页',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-02',
          name: '第一页',
          address: '上海市普陀区金沙江路 1518 弄'
        }
      ],
      currentPage: 1, // 当前页码
      total: 20, // 总条数
      pageSize: 2 // 每页的数据条数
    }
  },
  methods: {
    handleSearch() {
      alert('搜索内容：', this.searchText)
    },
    //每页条数改变时触发 选择一页显示多少行
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.currentPage = 1
      this.pageSize = val
    },
    //当前页改变时触发 跳转其他页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.currentPage = val
    }
  }
}
</script>

<style></style>
