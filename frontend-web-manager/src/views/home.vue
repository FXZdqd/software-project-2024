<template>
  <div class="dashboard">
    <el-container>
      <el-aside>
        <el-header style="height: fit-content"><Header /></el-header>
        <Menu />
      </el-aside>
      <el-container>
        <el-main><router-view /></el-main>
        <el-footer
          ><Footer class="navbar-fixed-bottom" />
          <h6 style="align-items: center">
            Frontend-Web-Manager 2024
          </h6></el-footer
        >
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import Menu from "../components/Menu.vue";
export default {
  components: { Footer, Menu, Header },
};
</script>
<style scoped>
.dashboard {
  display: flex;
  width: 100vw;
  height: 100vh;
}

.el-aside {
  display: flex;
  flex-direction: column;
  width: 150px;
  background-color: #333; /* 侧边栏背景色 */
  color: white;
}

.el-header {
  flex-shrink: 0; /* 防止头部压缩 */
  background-color: #409eff; /* 头部背景色 */
  color: white;
}

/* 调整Menu组件的样式以适应新布局 */
Menu {
  height: 90%;
}

.el-main {
  flex: 1; /* 主内容区占据剩余空间 */
  background-color: #f2f2f2;
}

.el-footer {
  flex-shrink: 0;
  width: 100%;
  height: min-content;
  background-color: #409eff;
  color: white;
  text-align: center;
}
</style>
