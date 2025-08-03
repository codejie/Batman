# Batman 项目概览

本项目是一个名为 "Batman" 的全栈金融数据分析和可视化平台。它由两部分组成：
- app: 用 Python 编写的后端 API 服务，基于FastAP实现；
- signal：用 Vue.js 编写的前端用户界面 应用，使用了vite编译，element-plus的UI组件库。

## 后端: `app`

`app` 是一个基于 FastAPI 框架构建的高性能异步 API 服务。它负责处理核心业务逻辑、数据处理、用户认证和数据库交互。

### 主要技术栈

-   **Web 框架**: FastAPI
-   **服务器**: Uvicorn
-   **数据库 ORM**: SQLAlchemy
-   **数据处理**: Pandas
-   **金融技术分析**: TA-Lib
-   **任务调度**: APScheduler
-   **缓存**: Redis
-   **认证**: JWT (JSON Web Tokens)

### 核心功能

-   提供 RESTful API 用于金融数据（如股票、基金）的增删改查。
-   集成 `TA-Lib` 库，提供多种技术分析指标计算的 API。
-   通过 `APScheduler` 管理定时任务，例如定期获取和更新金融数据。
-   使用 JWT 进行安全的用户身份验证和授权。
-   通过 SQLAlchemy ORM 与关系型数据库进行交互，管理用户和金融数据。

### 如何运行

在 `app` 目录下, 首先通过 `pip` 安装依赖:

```bash
pip install -r requirements.txt
```

然后使用 `uvicorn` 启动应用:

```bash
uvicorn app.main:app --reload
```

## 前端: `signal`

`signal` 是一个现代化的单页应用 (SPA)，作为项目的用户交互界面。它负责数据的可视化展示、用户操作和与后端 API 的通信。

### 主要技术栈

-   **核心框架**: Vue.js 3
-   **构建工具**: Vite
-   **编程语言**: TypeScript
-   **UI 组件库**: Element Plus
-   **状态管理**: Pinia
-   **路由**: Vue Router
-   **HTTP 请求**: Axios
-   **CSS 框架**: UnoCSS
-   **数据可视化**: ECharts

### 核心功能

-   一个美观且响应式的用户仪表盘，用于展示个人持仓和市场数据。
-   使用 `ECharts` 绘制专业的 K 线图和其他金融图表。
-   提供用户登录、注册以及个人信息管理功能。
-   与后端 `app` 服务进行数据交互，动态展示实时和历史金融数据。
-   实现了基于路由的前端权限控制。

### 如何运行

在 `signal` 目录下, 首先通过 `npm` 或 `pnpm` 安装依赖:

```bash
npm install
# or
pnpm install
```

然后启动开发服务器:

```bash
npm run dev
```

## 架构

本项目采用经典的前后端分离架构。

-   `signal` (前端) 负责用户界面和交互，通过 HTTP 请求 (使用 Axios) 调用后端 API。
-   `app` (后端) 负责处理业务逻辑和数据，并将结果以 JSON 格式返回给前端。

这种架构使得前后端可以独立开发、测试和部署。

## 部署
### Docker
本项目支持Docker构建和部署。
- `signal`
```bash
    =\docker build -t batman:signal -f .\deploy\dockerfile.signal .
````
- `app`
```bash
    docker build -t batman:app -f .\deploy\dockerfile.app .
```

### Docker Compose
本项目支持使用Docker Compose部署。
```bash
    docker compose -f .\deploy\docker-compose-service.yml up -d
```

## Gemini Agent Instructions

- 将输入的需求内容都记录在gemini.md中
- [DONE] 在app应用中的data模块，刚新增了get_code()函数和对应的router接口，调整此函数，不再支持模糊查询，相应地调整前端中‘自选列表’中的接口和内容，不需要使用AutoComplete组件。如果没有找到对应的股票或指数的代码，提示找不到即可。
- 请把输入的请求内容在完成或取消后记录在gemini.md中，并标记执行结果
- [DONE] 在app应用中，增加一个agent路由文件，并添加一个支持SSE的API，名字叫做report
- [DONE] 在signal应用中，将‘信息分析’菜单调整为一级目录，并包含同名二级/、菜单
- [DONE] 在后续生成代码时，请采用<script>在前，<template>在后的方式。
- [DONE] 解决了SSE连接在SPA页面切换和关闭时无法正确断开的问题。前端通过onUnmounted钩子关闭连接，后端通过try...finally确保断开连接时正确记录日志。
- [DONE] 重构了SSE实现，通过引入ConnectionManager和用户认证，支持向不同用户推送独立的、个性化的消息。
- [DONE] 解决了SSE连接由于EventSource无法发送Header而导致的422认证失败问题，修改为通过Query参数传递token。