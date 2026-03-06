# Changelog

所有项目的显著变更都将记录在此文件中。

格式基于[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 初始版本开发中

## [1.0.0] - 2024-XX-XX

### Added
- ✨ 初始版本发布
- 📄 文档上传功能（支持PDF、DOCX、MD、TXT）
- 🔍 智能文档搜索（基于RAG技术）
- 💬 AI对话功能，带来源引用
- 🎭 多种AI角色模板（技术、HR、产品）
- 📜 对话历史管理
- 👍 对话反馈功能
- 🐳 Docker Compose一键部署
- 🖥️ 本地开发支持

### 技术栈
- **后端**: FastAPI + Python 3.11 + SQLAlchemy
- **前端**: React 19 + TypeScript + Vite + Ant Design
- **向量数据库**: ChromaDB
- **LLM**: OpenAI API / 阿里云百炼兼容

### 文档
- 完整的README文档
- API文档（Swagger UI）
- 部署指南
- 开发文档

---

## 版本发布说明

### 版本号规则

版本格式：主版本号.次版本号.修订号

- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 标签约定

- `v1.0.0` - 正式版本
- `v1.0.0-alpha.1` - 内测版本
- `v1.0.0-beta.1` - 公测版本
- `v1.0.0-rc.1` - 候选版本
