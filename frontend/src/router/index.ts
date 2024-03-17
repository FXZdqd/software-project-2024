// src/router/index.ts

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Login from '../components/Login.vue';
import Manage from "../components/Manage.vue";
const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Login', // 将登录页面命名为 Login
        component: Login,
    },
    {
        path: '/Manage',
        name: 'Manage',
        component: Manage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
