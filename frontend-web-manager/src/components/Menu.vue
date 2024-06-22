<template>
  <div class="menu">
    <el-menu
      default-active="0"
      class="el-menu-vertical-demo"
      background-color="#0c4b8a"
      text-color="white"
      active-text-color="#ffd04b"
      text-decoration="none"
    >
      <template v-for="(item, index) in menuList" :key="index">
        <router-link :to="item.path" v-if="!item.children" :key="index">
          <el-menu-item :index="index + ''">
            <el-icon><component :is="item.icon"></component></el-icon>
            <span style="text-decoration: none">{{ item.name }}</span>
          </el-menu-item>
        </router-link>
        <el-sub-menu :index="index + ''" v-else>
          <router-link
            v-for="(sub, subIndex) in item.children"
            :to="item.path + '/' + sub.path"
            :key="subIndex"
            :index="sub.index"
          >
            <el-menu-item :index="index + '-' + subIndex">
              <el-icon><component :is="sub.icon"></component></el-icon>
              <span>{{ sub.name }}</span>
            </el-menu-item>
          </router-link>
        </el-sub-menu>
      </template>
    </el-menu>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
//import { RouteRecordRaw } from "vue-router";
import {
  QuestionFilled,
  User,
  MagicStick,
  UserFilled,
} from "@element-plus/icons-vue";

export default defineComponent({
  name: "Menu",
  components: {
    UserFilled,
    QuestionFilled,
    User,
    MagicStick,
  },
  data() {
    return {
      menuList: [], // as RouteRecordRaw[],
    };
  },
  mounted() {
    let routes = this.$router.options.routes;
    this.menuList = routes[2].children;
  },
});
</script>

<style scoped>
.menu {
  display: grid;
  height: 100%;
  .el-menu-vertical-demo {
    border-right: none;
    text-decoration: none;
  }
}
.router-link-active {
  text-decoration: none;
}
a {
  text-decoration: none;
}
.el-menu-item:hover {
  background-color: #1a5a97;
  text-decoration: none;
}
.el-menu-item {
  text-decoration: none;
}
.el-sub-menu .el-menu-item {
  background-color: #0e507c;
  text-decoration: none;
}
.el-menu.el-menu--horizontal {
  border: none;
  border-bottom: none;
  text-decoration: none;
}

.el-menu-item,
.el-sub-menu__title {
  font-size: 14px; /* 菜单字体大小 */
  font-weight: bold; /* 字体加粗 */
  text-decoration: none;
}

.el-icon {
  vertical-align: middle;
  margin-right: 8px;
  text-decoration: none;
}

.el-sub-menu__title {
  background-color: #0c4b8a;
  text-decoration: none;
}
</style>
