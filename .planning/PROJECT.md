# 企业智能知识库问答系统 (Enterprise Intelligent Document Assistant)

## What This Is

帮助企业员工快速检索内部文档，通过自然语言提问获取精准答案，并标注答案来源的企业级知识库系统。支持多格式文档上传（PDF、Word、Markdown、TXT），基于RAG技术实现智能问答。

## Core Value

解决企业内部文档分散、检索困难的问题，提供可溯源的AI问答（不是黑盒回答），支持多角色场景（技术支持/HR/产品）。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] 多格式文档上传与解析（PDF、DOCX、MD、TXT）
- [ ] 智能文本分块与向量化存储
- [ ] 基于RAG的智能问答引擎
- [ ] 答案溯源与引用展示
- [ ] 多角色Prompt模板管理（技术支持/HR/产品）
- [ ] 对话历史保存与查看
- [ ] 用户反馈收集（点赞/点踩）
- [ ] 系统管理后台
- [ ] Docker容器化部署

### Out of Scope

- 用户认证与权限管理 — 初期版本假设单企业内部使用，暂不需要复杂权限
- 多租户支持 — 初期专注单企业场景
- 实时协作编辑 — 超出知识库问答的核心定位
- 移动端App — 初期优先Web端
- 离线模式 — 依赖LLM API，暂不支持完全离线

## Context

### 项目背景
基于对6个AI辅助开发职位的分析，发现以下高需求技能：
- RAG（检索增强生成）系统开发 - 出现率83%
- AI编程工具使用（Cursor/Copilot） - 出现率100%
- Prompt工程 - 出现率67%
- 全栈开发能力 - 出现率83%
- LangChain框架 - 出现率50%

本项目一次性覆盖以上所有技能点。

### 目标用户场景
| 场景 | 用户提问示例 | 系统回答 |
|------|-------------|----------|
| 技术支持 | "如何配置数据库连接池？" | 从《技术手册》第3章找到配置步骤 |
| 新人入职 | "请假流程是什么？" | 从《员工手册》找到HR流程图 |
| 产品咨询 | "这个功能在哪个版本上线的？" | 从《CHANGELOG》找到版本记录 |

### 技术架构
- **前端**: React + TypeScript + Ant Design + TailwindCSS
- **后端**: Python + FastAPI + Uvicorn
- **RAG框架**: LangChain
- **向量数据库**: ChromaDB
- **LLM**: OpenAI GPT-4 / Claude
- **文档处理**: PyPDF2, python-docx, python-markdown
- **部署**: Docker + Docker Compose

### 预计周期
4周开发周期

## Constraints

- **Tech Stack**: Python + React — 匹配AI辅助开发职位技能要求
- **Timeline**: 4 weeks — 符合企业级项目展示需求
- **Dependencies**: OpenAI API Key — LLM调用必需
- **Performance**: <2秒平均响应时间 — 用户体验要求
- **Compatibility**: 支持50+用户并发 — 企业级要求

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 使用ChromaDB作为向量数据库 | 轻量级、易于部署、与LangChain集成良好 | — Pending |
| 采用FastAPI作为后端框架 | 现代化、高性能、自动生成API文档 | — Pending |
| 使用LangChain编排RAG流程 | 行业标准、组件丰富、易于扩展 | — Pending |
| 支持多种文档格式 | 企业文档格式多样化需求 | — Pending |
| React + Ant Design前端 | 快速开发、企业级UI组件丰富 | — Pending |

---
*Last updated: 2026-03-04 after initialization*
