import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login.vue')
  },
  {
    path: '/home',
    name: '主页',
    redirect: '/home/ques_mg',
    component: () => import('../views/home.vue'),
    children: [
      {
        path: '/home/ques_mg',
        name: '问题管理',
        icon: 'QuestionFilled',
        component: () => import('@/views/QuestionMG.vue')
      },
      {
        path: '/home/user_mg',
        name: '用户管理',
        icon: 'UserFilled',
        component: () => import('@/views/UserMG.vue')
      },
      {
        path: '/home/AI_mg',
        name: '模型管理',
        icon: 'MagicStick',
        component: () => import('@/views/AIModelMG.vue')
      },
      {
        path: '/home/my',
        name: '个人中心',
        icon: 'User',
        component: () => import('@/views/Myaccount.vue')
      },

    ]
  },
]
const router = createRouter({
  // 配置为Hash模式
  history: createWebHashHistory(),
  // 配置routes
  routes,
  // 路由跳转时返回顶部
  scrollBehavior () {
    return {top: 0}
  }
})
export default router;