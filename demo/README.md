# 提示词生成系统

基于 AI 工作流文档开发的 Web 应用，帮助用户通过填写表单的方式生成高质量提示词。

## 功能特性

### 核心功能
- **帮助用户完善思考** - 引导式表单帮助用户系统性地组织思路
- **结构化提示词** - 生成格式规范、层次分明的提示词

### 四大页面
1. **首页** - 任务诊断决策树，AI 工具推荐导航
2. **最小公式** - 通过 5 个要素快速生成简单提示词
3. **提示词模版** - 管理和使用提示词模板，支持搜索和复制
4. **复杂提示词** - 8步法流程深度构建高质量提示词

### 全局功能
- **提示词技巧** - 常驻右下角的技巧面板，支持缩放
- **复盘检查清单** - 提示词复制后弹出，5 个问题帮助反思改进

## 技术栈

- **前端**: Vite + Vue 3 + Element Plus + TypeScript + Pinia + Vue Router + Axios
- **后端**: Flask (Python) + SQLAlchemy
- **数据库**: SQLite (开发环境) / MySQL (生产环境)

## 快速开始

### 后端启动

```bash
cd demo/backend

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python run.py
```

后端默认运行在 `http://localhost:5000`

### 前端启动

```bash
cd demo/frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

前端默认运行在 `http://localhost:3000`

## 项目结构

```
demo/
├── backend/                # Flask 后端
│   ├── app/
│   │   ├── __init__.py     # Flask 应用初始化
│   │   ├── models.py       # 数据库模型
│   │   │   └── routes/     # API 路由
│   │       ├── categories.py  # 分类和产品导航API
│   │       ├── prompts.py     # 提示词生成API
│   │       ├── templates.py   # 模板管理API
│   │       └── tips.py        # 提示词技巧API
│   ├── requirements.txt    # Python 依赖
│   ├── run.py              # 应用入口
│   └── .env                # 环境变量配置
│
└── frontend/               # Vue 3 前端
    ├── src/
    │   ├── api/            # API 请求封装
    │   ├── components/     # Vue 组件
    │   │   ├── PromptTips.vue     # 提示词技巧面板
    │   │   └── ReviewDialog.vue   # 复盘检查清单弹窗
    │   ├── router/         # 路由配置
    │   ├── stores/         # Pinia 状态管理
    │   ├── styles/         # 全局样式
    │   ├── views/          # 页面组件
    │   │   ├── HomeView.vue         # 首页
    │   │   ├── MinimalFormula.vue   # 最小公式页面
    │   │   ├── TemplateList.vue     # 模板列表页面
    │   │   └── ComplexPrompt.vue    # 复杂提示词页面
    │   ├── App.vue         # 根组件
    │   └── main.ts         # 应用入口
    │
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

## 核心功能说明

### 1. 首页（任务诊断决策树）
- 三个按钮引导用户选择合适的提示词生成方式
- 展示 AI 产品导航（对话、编程、图像、效率工具、智能体）
- 每个产品包含名称、推荐理由、价格、标签等信息

### 2. 最小公式
公式结构：
```
## 角色
作为 [领域专家]

## 背景
必须避免 [禁忌项],优先考虑 [关键要素]

## 任务
实现 [具体目标],要求 [量化标准],最终输出服务于 [目标用户]

## 限制
[最多3条,量化优先,如"100字内""3个要点"]

## 输出
1. 以 Markdown 形式输出
2. 输出结果必须包含 [参考资料]
3. 输出风格 [犀利、凝练、有力]
4. 展示至少两种备选方案及其淘汰理由
```

### 3. 8步法复杂提示词
1. 明确问题与上下文
2. 自选必要角色
3. 连续提问，直到 95% 理解
4. 先跑一个具体情境
5. 根据表现迭代
6. 让"红队"挑刺
7. 直到抽到 SSR
8. 抽象成可扩展的提示模板

### 4. 复盘检查清单（全局功能）
复制提示词后弹出，5 个反思问题：
1. 预期达到的效果？
2. 如何评价（验证）这次生成的结果？
3. 是否有明显错误答案？你怎么处理的？
4. 生成的内容和你的预期不符，我是如何调整优化的？
5. 我为什么这么写提示词？

### 5. 提示词技巧（全局功能）
常驻右下角的技巧面板，包含：
- 清晰定义角色的技巧
- 提供具体背景的技巧
- 明确输出格式的技巧
- 提供示例的技巧
- 使用限制条件的技巧

## 数据库设计

系统支持 SQLite（开发）和 MySQL（生产）双数据库架构。

核心数据表：
- `categories` - 产品分类表
- `products` - AI 产品表
- `prompt_templates` - 提示词模板表
- `prompt_usage_logs` - 提示词使用日志
- `review_records` - 复盘记录表
- `prompt_tips` - 提示词技巧表

完整的数据库设计请查看 `Design/数据库设计文档.md`

## 配置说明

### 后端配置（.env）

```env
# 数据库类型: sqlite 或 mysql
DB_TYPE=sqlite

# MySQL 配置（如果使用 MySQL）
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=prompt_strategy
```

## 部署说明

### 生产环境建议使用 MySQL

1. 在 `.env` 中设置 `DB_TYPE=mysql`
2. 配置 MySQL 连接信息
3. 在 MySQL 中创建数据库：
```sql
CREATE DATABASE prompt_strategy CHARACTER SET utf8mb4;
```

### 前端构建

```bash
cd frontend
npm run build
```

构建后的文件在 `dist/` 目录，可以部署到任何静态文件服务器。

### Vercel 部署

本项目支持 Vercel 一键部署：

1. 将前后端代码推送到 GitHub
2. 在 Vercel 中导入项目
3. 配置环境变量（.env 中的变量）
4. 部署

## 开发计划

- [x] 基础项目架构
- [x] 前后端基础功能
- [x] 四个页面实现
- [x] 全局功能（技巧面板 + 复盘检查清单）
- [x] 数据库设计和连接
- [ ] API 测试和优化
- [ ] UI/UX 优化
- [ ] 移动端适配
- [ ] 单元测试和集成测试
- [ ] 生产环境部署优化

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
