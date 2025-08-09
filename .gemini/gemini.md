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
-   在后续生成代码时，请采用<script>在前，<template>在后的方式。

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
- 请把输入的请求内容在完成或取消后记录在gemini.md中，并标记执行结果
- [DONE] take a break
- [DONE] 页面中，stockList的checkbox组缺省为all选项，dataPeriod组缺省是1y，reportrange组缺省是today。
- [DONE] so cool!
- [DONE] 页面中‘股票列表’选项的选中使用事件方式处理，当选中all时，其他项被取消选中，并隐藏下面的表格。
- [DONE] 在页面的左右栏中间增加一条divider
- [DONE] 下面一栏分为左右两栏，左栏中的内容是由多个‘标题’加‘内容’的空间组成；左栏中第一项的标题为“股票列表”，内容是四个checkbox组件，分别是：持仓列表、自选列表、自定义列表、全部列表，在checkbox内容下是一个按钮“添加”和，按钮下面是一个表格，表格有四列：序号、名称、代码、持有；第二项的标题为“数据期间”，内容是四个checkbox组件：三个月、半年、一年、两年；第三项的标题为“报告范围”，内容是五个checkbox组件：最近一天、最近三天、最近一个月、最近三个月、全部。右边栏分为上下两栏，上栏仅有一个标题：算法和参数设置；下栏先保留，后续会有多个重复的子组件组合展示。
- [DONE] 输入框他太长，占60%空间就好
- [DONE] 页面分上下两栏，上面一栏中使用el-description组件显示一个名称为‘标题’的输入框
- [DONE] 在跟返回按钮同行的最右侧增加一个‘提交’按钮
- [DONE] 在TrendArgument.vue增加一个返回按钮，用于返回前一页面
- [DONE] 如果发现你创建或修改的文件被修改，请使用修改后内容，因为我也在调整内容。
- [DONE] @signal/src/views/Analysis下新增TrendArgument.vue文件，用于设置计算参数，通过组件TrendArgumentTable中的‘新增’按钮跳转过去。因此需要增加相应的路由信息，路由放在一级菜单‘数据分析’下
- [DONE] 调整下表格个栏的大小，标识：40，名称：120，更新日期：160，操作：120，其他都是‘备注’的空间
- [DONE] TrendArgumentTable表格加上外框显示
- [DONE] 不是这样的，‘计算参数’和‘计算结果’两个分栏都在同一个ContentWrap卡片中，分栏使用divider分隔，名称作为标题，靠左显示
- [DONE] Trend.vue的页面内容放置在ContentWrap卡片组件内
- [DONE] 请记得gemini.md中的agent指令要求
- [DONE] @signal/src/views/Analysis/components/TrendTable.vue 文件改名为TrendArgumentTable.vue
- [DONE] 组件显示在‘计算参数’栏范围内
- [DONE] 很好，在@signal/src/views/Analysis下增加一个子目录：components，其中增加一个用于Trend.vue的表格组件，表格用于展示所有计算参数项内容。表格栏包括如下字段：标识、名称、备注、更新日期、操作。其他表格栏‘操作’中放置两个按钮：详情、删除。表格的上方有一个按钮：新增。在Trend.vue中点击‘查看’按钮显示此组件；显示组件后，‘查看’按钮名称改为‘收起’，此时再点击隐藏此组件，如此反复。
- [DONE] 两个按钮紧跟下拉框右边
- [DONE] 下拉框占用空间太长了，只要宽带的三分之一就行
- [DONE] 提交和查看两个按钮在下拉选择框的右侧
- [DONE] 在文件中引如element-ui-plus组件
- [DONE] 在‘技术参数’的栏目中，增加一个下拉选择框，其后跟两个按钮：提交，查看
- [DONE] @signal/src/views/Analysis/Trend.vue中按行分为两个栏目：‘计算参数’和‘计算结果’，增加标题和分栏
- [DONE] signal应用中，在'数据分析'下增加一个子菜单，叫做'趋势计算'，同时在@signal/src/views/Analysis/下增加相应的vue页面文件。
- [DONE] gemini.md中的agent指令需要执行
- [DONE] @signal/src/router/index.ts,修改一级菜单名称'信息分析'为'数据分析'
- [DONE] 在app应用中的data模块，刚新增了get_code()函数和对应的router接口，调整此函数，不再支持模糊查询，相应地调整前端中‘自选列表’中的接口和内容，不需要使用AutoComplete组件。如果没有找到对应的股票或指数的代码，提示找不到即可。
- [DONE] 在app应用中，增加一个agent路由文件，并添加一个支持SSE的API，名字叫做report
- [DONE] 在signal应用中，将‘信息分析’菜单调整为一级目录，并包含同名二级/、菜单
- [DONE] 在后续生成代码时，请采用<script>在前，<template>在后的方式。
- [DONE] 解决了SSE连接在SPA页面切换和关闭时无法正确断开的问题。前端通过onUnmounted钩子关闭连接，后端通过try...finally确保断开连接时正确记录日志。
- [DONE] 重构了SSE实现，通过引入ConnectionManager和用户认证，支持向不同用户推送独立的、个性化的消息。
- [DONE] 解决了SSE连接由于EventSource无法发送Header而导致的422认证失败问题，修改为通过Query参数传递token。
- [DONE] 为`app/database/data/stock.py`中所有`download_`函数创建了集成测试 (`app/test/test_stock_data.py`)。
- [DONE] 在`app/calc/technical.py`中实现了一个`get_ma_trend`函数，用于判断移动平均线的趋势。
- [DONE] 为`get_ma_trend`函数创建了测试用例 (`app/test/test_technical.py`)。