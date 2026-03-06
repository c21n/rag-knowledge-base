# 企业 RAG 知识库系统

[![Docker](https://img.shields.io/badge/Docker-就绪-blue)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-blue)](https://reactjs.org/)
[![License](https://img.shields.io/badge/许可证-MIT-yellow.svg)](LICENSE)

基于 RAG（检索增强生成）技术的智能文档助手。上传文档、提问问题，获得带有来源引用的 AI 驱动答案。

## 功能特性

- **文档上传**: 支持 PDF、DOCX、MD、TXT 文件格式
- **智能处理**: 自动文本分块和 Embedding 生成
- **语义搜索**: 基于 ChromaDB 的向量检索
- **AI 问答**: 带有来源引用的上下文答案
- **角色模板**: 多种 AI 角色（技术、HR、产品）
- **对话历史**: 支持反馈的持久化聊天记录
- **现代界面**: 基于 Ant Design 的 React 界面
- **Docker 部署**: 一键 Docker Compose 部署

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端      │────▶│   后端      │────▶│  ChromaDB   │
│  (React)    │     │  (FastAPI)  │     │ (向量数据库) │
│   :80       │◀────│   :8000     │◀────│   :8001     │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   SQLite    │
                     │  (元数据)    │
                     └─────────────┘
```

- **前端**: React 19 + TypeScript + Vite + Ant Design
- **后端**: FastAPI + Python 3.11 + SQLAlchemy
- **向量数据库**: ChromaDB 语义搜索
- **LLM**: OpenAI / 阿里云百炼 API（通义千问）
- **数据库**: SQLite 存储元数据和对话历史

## 环境要求

- Docker 20.10 或更高版本
- Docker Compose 2.0 或更高版本
- 最低 4GB 内存（推荐 8GB）
- OpenAI 或阿里云百炼 API 密钥

## 快速开始

### 1. 克隆仓库

```bash
git clone <仓库地址>
cd rag-knowledge-base
```

### 2. 运行安装脚本

**Linux/Mac:**
```bash
./scripts/setup.sh
```

**Windows:**
```powershell
.\scripts\setup.ps1
```

### 3. 配置 API 密钥

编辑 `.env` 文件并添加你的 API 密钥：

```bash
# 必需：添加你的 API 密钥
OPENAI_API_KEY=你的_openai_api密钥
# 或
API_KEY=你的_阿里云百炼_api密钥
```

### 4. 启动应用

```bash
docker-compose up -d
```

### 5. 访问应用

- **前端界面**: http://localhost
- **API 文档**: http://localhost:8000/docs

---

## 🖥️ 本地部署（不使用 Docker）

如果你不想使用 Docker，可以直接在本地运行前后端服务。

### 环境要求

- Python 3.11+
- Node.js 20+
- npm 或 yarn

### 1. 配置后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

**后端 .env 配置示例：**

```env
# API 配置（阿里云百炼 - 通义千问）
OPENAI_API_KEY=你的_api密钥
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_EMBEDDING_MODEL=text-embedding-v1

# 数据库
DATABASE_URL=sqlite:///./data/app.db

# ChromaDB
CHROMA_PERSIST_DIR=./data/chroma

# 文件上传
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# Embedding 模型
EMBEDDING_MODEL=text-embedding-v1
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### 2. 启动后端服务

```bash
# 在 backend 目录下，确保虚拟环境已激活
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动

### 3. 配置前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量（可选）
# 创建 .env.local 文件
echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local
```

### 4. 启动前端服务

```bash
# 在 frontend 目录下
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 5. 访问应用

- **前端界面**: http://localhost:5173
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health

### 本地部署目录结构

```
rag-knowledge-base/
├── backend/
│   ├── src/              # 后端源代码
│   ├── data/             # 数据库和上传文件
│   │   ├── app.db        # SQLite 数据库
│   │   ├── chroma/       # ChromaDB 向量数据
│   │   └── uploads/      # 上传的文档
│   └── .env              # 后端环境配置
├── frontend/
│   ├── src/              # 前端源代码
│   ├── node_modules/     # 前端依赖
│   └── .env.local        # 前端环境配置（可选）
└── README.md
```

### 停止服务

```bash
# 停止后端（在终端按 Ctrl+C）
# 停止前端（在另一个终端按 Ctrl+C）

# 退出虚拟环境（如果需要）
deactivate
```

---

## 配置说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 必需* |
| `API_KEY` | 阿里云百炼 API 密钥 | 必需* |
| `DATABASE_URL` | SQLite 数据库路径 | `sqlite:///./data/app.db` |
| `CHROMA_HOST` | ChromaDB 主机名 | `chromadb` |
| `UPLOAD_DIR` | 文档上传目录 | `./uploads` |
| `MAX_FILE_SIZE` | 最大文件大小 | `10485760` (10MB) |
| `EMBEDDING_MODEL` | Embedding 模型 | `text-embedding-v1` |
| `LLM_MODEL` | LLM 模型 | `qwen-max` |

*至少需要提供一个 LLM API 密钥

## API 接口

### 核心接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/chat` | 提交问题并获得答案 |
| GET | `/api/chat/history/{session_id}` | 获取对话历史 |
| POST | `/api/chat/feedback` | 提交反馈 |

### 文档管理

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/documents` | 列出所有文档 |
| POST | `/api/documents` | 上传文档 |
| DELETE | `/api/documents/{id}` | 删除文档 |

## 开发环境

### 后端开发

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

开发服务器将在 http://localhost:5173 启动

## 故障排除

### "连接被拒绝" 错误
- 确保 Docker 正在运行
- 检查端口 80、8000 或 8001 是否已被占用

### "API 密钥错误"
- 验证 `.env` 中已设置 `OPENAI_API_KEY` 或 `API_KEY`
- 重启服务：`docker-compose restart`

### "端口已被占用"
- 修改 `docker-compose.yml` 中的端口映射

## 项目结构

```
.
├── backend/              # FastAPI 后端
├── frontend/             # React 前端
├── scripts/              # 安装脚本
├── docker-compose.yml    # Docker Compose 配置
├── .env.example          # 环境变量模板
└── README.md             # 本文件
```

## Docker 命令

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止所有服务
docker-compose down

# 重新构建镜像
docker-compose build --no-cache
```

## 许可证

MIT 许可证

## 支持

如有问题和疑问：
1. 查看故障排除部分
2. 访问 http://localhost:8000/docs 查看 API 文档
3. 查看日志：`docker-compose logs`
