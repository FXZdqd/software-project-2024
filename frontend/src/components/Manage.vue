<!-- AdminPanel.vue -->
<template>
  <div id="admin-panel">
    <header>
      <div class="logo">
        <img src="../assets/logo.svg" alt="Logo" />
      </div>
      <nav>
        <ul>
          <li v-for="(item, index) in navItems" :key="index" :class="{'active': currentItem === item}" @click="setCurrentItem(item)">{{ item }}</li>
        </ul>
      </nav>
    </header>
    <div class="content">
      <Q v-if="currentItem === '问题管理'">问题管理内容</Q>
      <div v-if="currentItem === '用户管理'">用户管理内容</div>
      <div v-if="currentItem === '模型管理'">模型管理内容</div>
      <div v-if="currentItem === '休闲一刻'">休闲一刻内容</div>
    </div>
  </div>
</template>

<script>
import Q from './Q.vue';
export default {
  name: 'AdminPanel',
  data() {
    return {
      currentItem: '问题管理',
      navItems: ['问题管理', '用户管理', '模型管理', '休闲一刻'],
    };
  },
  methods: {
    setCurrentItem(item) {
      this.currentItem = item;
    }
  },
  components: {
   Q
  }
};
</script>

<style scoped>
#admin-panel {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #F4F7FA;
  color: #333;
  min-height: 100vh;
  width: 100vw;
}

header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 20px;
  gap: 20px;
}

.logo img {
  width: 250px; /* 适当调整大小以保持视觉平衡 */
  height: 250px;
}

nav ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  gap: 15px;
}

nav ul li {
  margin: 0 10px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  border-radius: 5px;
  background-color: #E1E5EB;
  color: #555;
  font-weight: 500; /* 增加字体权重提升可读性 */
}

nav ul li:hover, nav ul li.active {
  background-color: #007BFF;
  color: #FFF;
}

.content {
  text-align: left;
  max-width: 90%;
  margin: 5px auto; /* 减小上边距，使content部分更接近顶部 */
  background-color: #FFF;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    align-items: flex-start;
  }
  nav ul {
    margin-left: 0;
    padding-top: 10px;
  }
  .content {
    max-width: 100%;
  }
}
</style>

