## 项目简介

​    **北航“灵询”问答平台**

​    **灵询**：“灵”字，象征着敏锐与智慧，如同北航学子们敏锐的思维和求知的渴望；“询”字，则代表着询问与探寻，体现了平台致力于解答疑惑、探索真理的初衷。

​    **InsightSpace**：结合了“Insight”（洞察）和“Space”（空间）两个词，既体现了“灵询”平台的问答和探索性质，又寓意着北航作为航空航天学府的广阔视野和无限可能。

  

### 技术栈

- 前端框架：[uni-app](https://uniapp.dcloud.net.cn/) (Vue3 + TS + Setup)
- 状态管理：[pinia](https://pinia.vuejs.org/zh/)
- 组件库：[uni-ui](https://uniapp.dcloud.net.cn/component/uniui/uni-ui.html)

## 运行程序

1. 安装依赖

```shell
# npm
npm i --registry=https://registry.npmmirror.com

# pnpm
pnpm i --registry=https://registry.npmmirror.com
```

2. 运行程序

```shell
# 微信小程序端
npm run dev:mp-weixin
```

3. 微信开发者工具导入 `/dist/dev/mp-weixin` 目录

### 工程结构解析

```
├── .husky                     # Git Hooks
├── .vscode                    # VS Code 插件 + 设置
├── dist                       # 打包文件夹（可删除重新打包）
├─components
├─composables
├─pages
│  ├─dialogue
│  ├─index
│  │  └─components
│  ├─login
│  └─my
├─services
├─static
│  ├─images
│  └─tabs
├─stores
│  └─modules
├─styles
├─types
├─utils
├── .editorconfig              # editorconfig 配置
├── .eslintrc.cjs              # eslint 配置
├── .prettierrc.json           # prettier 配置
├── .gitignore                 # git 忽略文件
├── index.html                 # H5 端首页
├── package.json               # package.json 依赖
├── tsconfig.json              # typescript 配置
└── vite.config.ts             # vite 配置
```
