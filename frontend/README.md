# RAG Knowledge Base - Frontend

企业RAG知识库系统的前端应用，基于React 19 + TypeScript + Vite + Ant Design构建。

## 技术栈

- **框架**: React 19
- **语言**: TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design 6.x
- **HTTP客户端**: Axios
- **代码规范**: ESLint + TypeScript ESLint

## 功能特性

- 📄 **文档管理**: 上传、查看、删除PDF/DOCX/MD/TXT文件
- 💬 **智能对话**: 基于RAG技术的AI问答，带来源引用
- 🎭 **角色模板**: 支持技术、HR、产品等多种AI角色
- 📜 **对话历史**: 持久化聊天记录，支持反馈
- 🎨 **现代UI**: 响应式设计，支持暗黑模式

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

开发服务器将在 http://localhost:5173 启动

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist/` 目录

### 代码检查

```bash
npm run lint
```

## 环境配置

创建 `.env.local` 文件配置环境变量：

```env
# API基础URL
VITE_API_BASE_URL=http://localhost:8000
```

## 项目结构

```
frontend/
├── src/
│   ├── components/     # 可复用组件
│   ├── hooks/          # 自定义React Hooks
│   ├── layouts/        # 布局组件
│   ├── pages/          # 页面组件
│   ├── services/       # API服务
│   ├── types/          # TypeScript类型定义
│   ├── utils/          # 工具函数
│   ├── App.tsx         # 应用根组件
│   └── main.tsx        # 应用入口
├── public/             # 静态资源
├── index.html          # HTML模板
├── package.json        # 项目配置
├── tsconfig.json       # TypeScript配置
└── vite.config.ts      # Vite配置
```

## API集成

前端通过Axios与后端API通信，主要接口包括：

- **文档管理**: `/api/documents`
- **对话接口**: `/api/chat`
- **角色管理**: `/api/roles`
- **健康检查**: `/api/health`

详细API文档见后端Swagger UI: http://localhost:8000/docs

## 开发规范

### 代码风格

- 使用TypeScript严格模式
- 组件使用函数式组件 + Hooks
- 使用Ant Design组件库保持UI一致性
- 遵循ESLint规则

### 提交规范

提交信息格式：`<type>(<scope>): <subject>`

- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 相关链接

- [后端API文档](../backend/README.md)
- [主项目README](../README.md)

## License

[MIT](../LICENSE)
