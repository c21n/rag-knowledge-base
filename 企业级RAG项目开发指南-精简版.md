# 企业级RAG项目开发指南（精简版）

> **项目名称**: 企业智能知识库问答系统（Enterprise Intelligent Document Assistant）  
> **目标**: 打造可写入简历的企业级项目，匹配AI辅助开发职位  
> **预计周期**: 4周  
> **难度**: ⭐⭐⭐（中级）

---

## 📋 目录

1. [项目概述与定位](#一项目概述与定位)
2. [核心功能设计](#二核心功能设计)
3. [技术架构](#三技术架构)
4. [详细开发路线图](#四详细开发路线图)
5. [技术栈与依赖](#五技术栈与依赖)

---

## 一、项目概述与定位

### 1.1 项目背景

基于对6个AI辅助开发职位的分析，发现以下高需求技能：
- ✅ RAG（检索增强生成）系统开发 - 出现率83%
- ✅ AI编程工具使用（Cursor/Copilot） - 出现率100%
- ✅ Prompt工程 - 出现率67%
- ✅ 全栈开发能力 - 出现率83%
- ✅ LangChain框架 - 出现率50%

本项目一次性覆盖以上所有技能点。

### 1.2 项目定位

**一句话描述**:  帮助企业员工快速检索内部文档，通过自然语言提问获取精准答案，并标注答案来源的企业级知识库系统。

**核心价值**:
- 解决企业内部文档分散、检索困难的问题
- 提供可溯源的AI问答（不是黑盒回答）
- 支持多角色场景（技术支持/HR/产品）

### 1.3 目标用户场景

| 场景 | 用户提问示例 | 系统回答 |
|------|-------------|----------|
| 技术支持 | "如何配置数据库连接池？" | 从《技术手册》第3章找到配置步骤 |
| 新人入职 | "请假流程是什么？" | 从《员工手册》找到HR流程图 |
| 产品咨询 | "这个功能在哪个版本上线的？" | 从《CHANGELOG》找到版本记录 |

---

## 二、核心功能设计

### 2.1 功能架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户交互层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   对话界面    │  │  文档管理    │  │  系统配置    │      │
│  │  (React)     │  │   (上传/删除) │  │ (Prompt模板) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      API网关层 (FastAPI)                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  /api/chat  │ │ /api/upload │ │/api/history │           │
│  │   问答接口   │ │  上传接口    │ │  历史记录   │           │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
└─────────┼───────────────┼───────────────┼──────────────────┘
          │               │               │
          └───────────────┼───────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    核心业务逻辑层 (LangChain)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 RAG Pipeline                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │ Document │→ │  Text    │→ │ Vector   │         │   │
│  │  │  Loader  │  │ Splitter │  │  Store   │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  │       ↑                                    ↓       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │ Answer   │← │   LLM    │← │ Retriever│         │   │
│  │  │ Generator│  │          │  │          │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │
          ├──────────────┬──────────────┬──────────────┐
          │              │              │              │
┌─────────▼────┐  ┌─────▼──────┐  ┌────▼─────┐  ┌─────▼──────┐
│ Vector DB    │  │   LLM      │  │ File     │  │  SQL       │
│ (ChromaDB)   │  │ (OpenAI/   │  │ Storage  │  │ Database   │
│ - Embeddings │  │  Claude)   │  │ (Local)  │  │ (SQLite/   │
│ - Metadata   │  │ - Chat     │  │          │  │  PostgreSQL)│
└──────────────┘  │ - Embedding│  │          │  │            │
                  └────────────┘  └──────────┘  └────────────┘
```

### 2.2 功能模块详解

#### 模块1：文档智能解析与索引系统

**功能描述**:
- 支持多格式文档上传（PDF、DOCX、MD、TXT）
- 自动提取文本内容
- 智能分块（Chunking）策略
- 生成向量嵌入并存储

**技术要点**:
```python
# 分块策略配置
TEXT_SPLITTER_CONFIG = {
    "chunk_size": 500,        # 每块500字符
    "chunk_overlap": 50,      # 重叠50字符，保证上下文连贯
    "separators": ["\n\n", "\n", "。", "；", " ", ""]  # 优先按段落分割
}
```

**核心代码结构**:
```python
class DocumentProcessor:
    def load_document(self, file_path: str) -> List[Document]:
        """加载PDF/Word/Markdown文档"""
        pass
    
    def split_text(self, documents: List[Document]) -> List[Document]:
        """文本分块处理"""
        pass
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """生成向量嵌入"""
        pass
```

#### 模块2：智能问答引擎（RAG核心）

**功能描述**:
- 接收用户自然语言提问
- 向量检索相似文档片段（Top-K）
- 构建Prompt上下文
- 调用LLM生成答案
- 返回答案+来源引用

**RAG流程**:
```
用户提问 → 向量化 → 相似度检索（Top 5） → 上下文组装 → LLM生成 → 返回答案
```

**核心代码结构**:
```python
class RAGChain:
    def __init__(self, vector_store, llm, prompt_template):
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        self.llm = llm
        self.prompt = prompt_template
    
    def query(self, question: str) -> dict:
        # 1. 检索相关文档
        docs = self.retriever.get_relevant_documents(question)
        
        # 2. 构建上下文
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # 3. 生成答案
        response = self.llm.generate(context, question)
        
        # 4. 返回答案和来源
        return {
            "answer": response,
            "sources": [doc.metadata for doc in docs]
        }
```

#### 模块3：Prompt模板管理系统

**功能描述**:
- 预设多种角色场景Prompt
- 支持动态切换角色
- 可自定义Prompt模板
- 支持多轮对话上下文

**预设角色模板**:

**角色A：技术支持专员**
```
你是一位经验丰富的技术支持工程师。请根据以下技术文档内容，
回答用户问题。如果文档中没有相关信息，请明确告知。

相关文档内容：
{context}

用户问题：{question}

请用中文回答，并在回答末尾列出引用的文档来源。
```

**角色B：HR助手**
```
你是一位专业的人力资源顾问。请根据公司员工手册内容，
回答员工关于公司制度、福利、流程的咨询。

相关制度文档：
{context}

员工咨询：{question}

请用友好、专业的语气回答，并注明依据的制度条款。
```

**角色C：产品顾问**
```
你是一位产品专家。请根据产品文档，回答用户关于产品功能、
使用方法的问题。

产品文档内容：
{context}

用户问题：{question}

请清晰、简洁地回答，并推荐相关功能模块。
```

#### 模块4：对话历史与反馈系统

**功能描述**:
- 保存对话记录到数据库
- 支持查看历史会话
- 用户可对答案点赞/点踩
- 收集反馈用于后续优化

**数据模型**:
```python
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True)  # 会话ID
    question = Column(Text)                   # 用户问题
    answer = Column(Text)                     # 系统回答
    sources = Column(JSON)                    # 引用来源
    role = Column(String)                     # 使用的角色模板
    feedback = Column(Integer)                # 1=点赞, -1=点踩, 0=未评价
    created_at = Column(DateTime)
```

#### 模块5：系统管理后台

**功能描述**:
- 文档库管理（查看/删除/更新）
- Prompt模板编辑
- 系统配置（API密钥、模型参数）
- 使用统计（问答次数、满意度）

---

## 三、技术架构

### 3.1 架构设计原则

1. **模块化设计**: 每个功能模块独立，便于测试和维护
2. **可扩展性**: 支持切换不同LLM和向量数据库
3. **可配置性**: 关键参数通过配置文件管理
4. **容器化**: 支持Docker一键部署

### 3.2 分层架构

```
┌─────────────────────────────────────┐
│           Presentation Layer         │
│  (React + TypeScript + TailwindCSS)  │
│  - 组件化UI设计                       │
│  - 状态管理 (Zustand/Redux)          │
│  - HTTP客户端 (Axios)                │
├─────────────────────────────────────┤
│            API Gateway Layer         │
│  (FastAPI + Uvicorn)                 │
│  - RESTful API设计                   │
│  - 请求验证 (Pydantic)               │
│  - 错误处理机制                      │
│  - CORS配置                          │
├─────────────────────────────────────┤
│           Business Logic Layer       │
│  (LangChain + Custom Logic)          │
│  - RAG流程编排                       │
│  - Prompt管理                        │
│  - 文档处理                          │
├─────────────────────────────────────┤
│           Data Access Layer          │
│  - Vector DB (ChromaDB)              │
│  - SQL DB (SQLite/PostgreSQL)        │
│  - File Storage (Local/S3)           │
├─────────────────────────────────────┤
│         External Services            │
│  - OpenAI API / Claude API           │
│  - Embedding Models                  │
└─────────────────────────────────────┘
```

### 3.3 数据流图

```
┌─────────────┐     上传      ┌──────────────┐
│   用户      │──────────────→│  文档处理器   │
│  (前端)     │               │  (后端)      │
└─────────────┘               └──────┬───────┘
                                     │
                                     ↓解析
                              ┌──────────────┐
                              │  文本分块    │
                              └──────┬───────┘
                                     │
                                     ↓向量化
                              ┌──────────────┐
                              │  Embedding   │
                              │   Model      │
                              └──────┬───────┘
                                     │
                                     ↓存储
                              ┌──────────────┐
                              │  ChromaDB    │
                              │  (向量库)    │
                              └──────────────┘

┌─────────────┐     提问      ┌──────────────┐     检索    ┌──────────────┐
│   用户      │──────────────→│   RAG引擎    │───────────→│  ChromaDB    │
│  (前端)     │               │  (LangChain) │            │  (Top-K检索) │
│             │←──────────────│              │←───────────│              │
│             │   答案+来源    └──────┬───────┘            └──────────────┘
└─────────────┘                      │
                                     │ 生成
                                     ↓
                              ┌──────────────┐
                              │  LLM Model   │
                              │ (GPT-4/Claude)│
                              └──────────────┘
```

---

## 四、详细开发路线图

### Week 1: 基础架构搭建（第1-7天）

#### Day 1-2: 项目初始化与环境配置

**任务清单**:
- [ ] 使用Cursor创建项目目录结构
- [ ] 初始化Python虚拟环境
- [ ] 安装核心依赖（FastAPI、LangChain等）
- [ ] 配置Git仓库，创建README.md
- [ ] 设计项目目录结构

**项目目录结构**:
```
enterprise-rag-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── chat.py      # 对话接口
│   │   │   │   ├── documents.py # 文档管理接口
│   │   │   │   └── config.py    # 配置接口
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── exceptions.py    # 异常处理
│   │   │   └── logging.py       # 日志配置
│   │   ├── models/
│   │   │   ├── schemas.py       # Pydantic模型
│   │   │   └── database.py      # SQLAlchemy模型
│   │   ├── services/
│   │   │   ├── rag_service.py   # RAG核心服务
│   │   │   ├── document_service.py
│   │   │   └── llm_service.py
│   │   └── utils/
│   │       ├── document_loader.py
│   │       └── text_splitter.py
│   ├── uploads/                 # 上传文件存储
│   ├── chroma_db/               # 向量数据库
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/          # React组件
│   │   ├── pages/               # 页面
│   │   ├── services/            # API调用
│   │   ├── store/               # 状态管理
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

**Cursor提示词示例**:
```
请帮我创建一个FastAPI项目的基础结构，包含：
1. main.py作为入口，配置CORS和路由
2. api/routes目录存放路由模块
3. models/schemas.py定义Pydantic模型
4. core/config.py读取环境变量配置
5. 使用python-dotenv管理配置
```

#### Day 3-4: 数据库设计与配置

**任务清单**:
- [ ] 设计数据库模型（文档、对话、配置表）
- [ ] 配置SQLAlchemy和Alembic迁移
- [ ] 实现基础CRUD操作
- [ ] 初始化ChromaDB向量数据库

**核心代码**:
```python
# models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String)  # pdf, docx, md, txt
    file_size = Column(Integer)
    total_chunks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(JSON)  # 存储来源文档信息
    role = Column(String, default="default")
    feedback = Column(Integer, default=0)  # 1=like, -1=dislike
    created_at = Column(DateTime, default=datetime.utcnow)

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    system_prompt = Column(Text, nullable=False)
    context_template = Column(Text)
    is_default = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Day 5-7: 文档上传与解析

**任务清单**:
- [ ] 实现文件上传API（支持PDF、Word、Markdown）
- [ ] 集成文档解析库（PyPDF2、python-docx）
- [ ] 实现文本提取功能
- [ ] 编写文档处理服务
- [ ] 测试上传流程

**核心代码**:
```python
# utils/document_loader.py
from typing import List
from langchain.schema import Document
import PyPDF2
import docx
import markdown
from pathlib import Path

class DocumentLoader:
    """文档加载器，支持PDF、Word、Markdown、TXT"""
    
    @staticmethod
    def load_pdf(file_path: str) -> str:
        """加载PDF文件"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def load_docx(file_path: str) -> str:
        """加载Word文档"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    @staticmethod
    def load_markdown(file_path: str) -> str:
        """加载Markdown文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def load_txt(file_path: str) -> str:
        """加载纯文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @classmethod
    def load(cls, file_path: str) -> Document:
        """根据文件类型自动选择加载器"""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        loaders = {
            '.pdf': cls.load_pdf,
            '.docx': cls.load_docx,
            '.md': cls.load_markdown,
            '.txt': cls.load_txt
        }
        
        if extension not in loaders:
            raise ValueError(f"不支持的文件格式: {extension}")
        
        text = loaders[extension](file_path)
        
        return Document(
            page_content=text,
            metadata={
                "source": file_path,
                "filename": path.name,
                "type": extension
            }
        )
```

---

### Week 2: RAG核心实现（第8-14天）

#### Day 8-10: 向量数据库与文本分块

**任务清单**:
- [ ] 实现文本分块策略
- [ ] 集成ChromaDB
- [ ] 实现文档向量化存储
- [ ] 配置Embedding模型（OpenAI/text-embedding-ada-002）

**核心代码**:
```python
# utils/text_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

class SmartTextSplitter:
    """智能文本分块器"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", "；", " ", ""]
    
    def split(self, documents: List[Document]) -> List[Document]:
        """分割文档"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False
        )
        
        chunks = text_splitter.split_documents(documents)
        
        # 为每个chunk添加序号和父文档信息
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_index": i,
                "chunk_size": len(chunk.page_content)
            })
        
        return chunks
```

```python
# services/document_service.py
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from typing import List
import chromadb

class DocumentService:
    """文档服务，处理文档的存储和检索"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        
        # 初始化ChromaDB客户端
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def add_documents(self, documents: List[Document], collection_name: str = "documents"):
        """添加文档到向量数据库"""
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )
        vectorstore.persist()
        return len(documents)
    
    def get_retriever(self, collection_name: str = "documents", search_k: int = 5):
        """获取检索器"""
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )
        return vectorstore.as_retriever(search_kwargs={"k": search_k})
```

#### Day 11-12: RAG流程编排（LangChain）

**任务清单**:
- [ ] 设计RAG Chain流程
- [ ] 实现检索-生成流程
- [ ] 集成LLM（OpenAI GPT-4/Claude）
- [ ] 实现答案格式化输出

**核心代码**:
```python
# services/rag_service.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

class RAGService:
    """RAG服务，处理问答逻辑"""
    
    def __init__(self, document_service, llm_model: str = "gpt-4"):
        self.document_service = document_service
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0.7)
        
        # 默认Prompt模板
        self.default_prompt = PromptTemplate.from_template("""
        你是一位专业的助手。请根据以下文档内容回答用户问题。
        如果文档中没有相关信息，请明确告知你不知道。
        
        相关文档内容：
        {context}
        
        用户问题：{question}
        
        请用中文回答，并在回答末尾列出引用的文档来源。
        """)
    
    def format_docs(self, docs):
        """格式化文档，用于Prompt构建"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(f"[文档{i}] {doc.page_content}")
        return "\n\n".join(formatted)
    
    def create_chain(self, prompt_template: PromptTemplate = None):
        """创建RAG Chain"""
        retriever = self.document_service.get_retriever()
        prompt = prompt_template or self.default_prompt
        
        # 构建Chain
        chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def query(self, question: str, prompt_template: PromptTemplate = None) -> dict:
        """执行问答"""
        retriever = self.document_service.get_retriever()
        
        # 获取相关文档
        docs = retriever.get_relevant_documents(question)
        
        # 创建Chain并执行
        chain = self.create_chain(prompt_template)
        answer = chain.invoke(question)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",  # 前200字符
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        }
```

#### Day 13-14: API接口开发

**任务清单**:
- [ ] 实现/chat问答接口
- [ ] 实现/documents文档管理接口
- [ ] 实现/config配置接口
- [ ] 添加请求验证和错误处理
- [ ] 测试所有API

**核心代码**:
```python
# api/routes/chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from services.rag_service import RAGService
from models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    role: Optional[str] = "default"
    
class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[dict]
    session_id: str

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """问答接口"""
    try:
        result = rag_service.query(
            question=request.question,
            role=request.role
        )
        
        # 保存对话记录
        conversation_id = await save_conversation(
            session_id=request.session_id,
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
            role=request.role
        )
        
        return ChatResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
            session_id=request.session_id or conversation_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """获取对话历史"""
    history = await get_conversation_history(session_id)
    return {"history": history}
```

---

### Week 3: 前端与优化（第15-21天）

#### Day 15-17: React前端界面开发

**任务清单**:
- [ ] 初始化React项目（Vite + TypeScript）
- [ ] 安装UI组件库（Ant Design / TailwindCSS）
- [ ] 开发对话界面组件（ChatUI）
- [ ] 开发文档上传组件
- [ ] 实现API调用服务

**核心组件结构**:
```typescript
// frontend/src/components/ChatInterface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, List, Avatar, Typography, Spin } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

interface Source {
  content: string;
  metadata: {
    filename: string;
    chunk_index: number;
  };
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // 调用后端API
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container" style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* 消息列表 */}
      <List
        className="message-list"
        style={{ flex: 1, overflow: 'auto', padding: '20px' }}
        dataSource={messages}
        renderItem={(msg) => (
          <List.Item
            style={{
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            <div
              style={{
                maxWidth: '70%',
                padding: '12px 16px',
                borderRadius: '12px',
                background: msg.role === 'user' ? '#1890ff' : '#f0f0f0',
                color: msg.role === 'user' ? '#fff' : '#000'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
                <Avatar
                  icon={msg.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
                  style={{ marginRight: '8px' }}
                />
                <Typography.Text strong>
                  {msg.role === 'user' ? '我' : 'AI助手'}
                </Typography.Text>
              </div>
              
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              
              {/* 显示来源 */}
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #d9d9d9' }}>
                  <Typography.Text type="secondary" style={{ fontSize: '12px' }}>
                    参考来源：
                    {msg.sources.map((source, idx) => (
                      <span key={idx} style={{ marginLeft: '8px' }}>
                        {source.metadata.filename}
                      </span>
                    ))}
                  </Typography.Text>
                </div>
              )}
            </div>
          </List.Item>
        )}
      />
      
      <div ref={messagesEndRef} />

      {/* 输入框 */}
      <div style={{ padding: '20px', borderTop: '1px solid #d9d9d9' }}>
        <Input.TextArea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="请输入您的问题..."
          autoSize={{ minRows: 2, maxRows: 4 }}
          onPressEnter={(e) => {
            if (!e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSend}
          loading={loading}
          style={{ marginTop: '12px', float: 'right' }}
        >
          发送
        </Button>
      </div>
    </div>
  );
};

export default ChatInterface;
```

#### Day 18-19: Prompt模板系统实现

**任务清单**:
- [ ] 创建Prompt模板管理界面
- [ ] 实现角色切换功能
- [ ] 支持自定义Prompt编辑
- [ ] 测试不同角色的回答效果

#### Day 20-21: 答案溯源与引用高亮

**任务清单**:
- [ ] 优化来源展示方式
- [ ] 实现引用内容高亮
- [ ] 添加点击跳转原文功能
- [ ] 美化UI展示效果

---

### Week 4: 完善与部署（第22-28天）

#### Day 22-24: 对话历史与反馈系统

**任务清单**:
- [ ] 实现对话历史列表
- [ ] 添加点赞/点踩功能
-- [ ] 实现会话管理（新建/删除会话）
- [ ] 优化数据库查询性能

#### Day 25-26: 性能优化

**任务清单**:
- [ ] 实现Redis缓存热门问题
- [ ] 优化向量检索速度
- [ ] 添加请求限流
- [ ] 优化前端加载速度

**缓存策略**:
```python
# 缓存常见问题，减少LLM调用
from functools import lru_cache
import hashlib

class QueryCache:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.local_cache = {}
    
    def get_cache_key(self, question: str) -> str:
        """生成缓存key"""
        return hashlib.md5(question.encode()).hexdigest()
    
    def get(self, question: str):
        """获取缓存结果"""
        key = self.get_cache_key(question)
        # 先查本地缓存
        if key in self.local_cache:
            return self.local_cache[key]
        # 再查Redis
        if self.redis:
            result = self.redis.get(key)
            if result:
                return json.loads(result)
        return None
    
    def set(self, question: str, answer: dict, expire: int = 3600):
        """设置缓存"""
        key = self.get_cache_key(question)
        self.local_cache[key] = answer
        if self.redis:
            self.redis.setex(key, expire, json.dumps(answer))
```

#### Day 27-28: 文档编写与部署

**任务清单**:
- [ ] 编写详细README.md
- [ ] 编写API文档
- [ ] 创建Dockerfile
- [ ] 编写docker-compose.yml
- [ ] 部署到个人服务器或云平台
- [ ] 录制演示视频/GIF

**README.md模板**:
```markdown
# 企业智能知识库问答系统

## 🎯 项目简介
基于RAG（检索增强生成）技术的企业级文档问答系统，支持员工通过自然语言查询内部技术文档。

## ✨ 核心功能
- 📄 多格式文档上传（PDF/Word/Markdown）
- 💬 智能问答，答案带引用来源
- 🎭 多角色Prompt模板（技术支持/HR/产品）
- 📝 对话历史管理
- 👍 用户反馈收集

## 🛠 技术栈
- 后端：Python + FastAPI + LangChain
- 前端：React + TypeScript + Ant Design
- 向量数据库：ChromaDB
- LLM：OpenAI GPT-4 / Claude
- 部署：Docker + Docker Compose

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- OpenAI API Key

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourname/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入你的OpenAI API Key
```

3. 启动服务（Docker方式）
```bash
docker-compose up -d
```

4. 访问系统
- 前端：http://localhost:3000
- 后端API文档：http://localhost:8000/docs

## 📊 项目亮点

### 1. AI工具提效
- 使用Cursor完成70%后端代码开发
- 使用Claude设计系统架构
- 使用GitHub Copilot辅助日常编码

### 2. RAG系统优化
- 智能文本分块策略（重叠50字符保证上下文）
- Top-K相似度检索（K=5）
- 答案溯源（精确到文档段落）

### 3. Prompt工程实践
- 设计3种角色模板（技术支持/HR/产品）
- 支持上下文记忆的多轮对话
- 可配置的Prompt管理系统

## 📈 性能指标
- 平均响应时间：<2秒
- 答案准确率：85%+
- 支持并发：50+用户

## 🎥 Demo演示
![Demo GIF](docs/demo.gif)

## 📝 API文档
详见 [API文档](docs/api.md)

## 🤝 贡献指南
欢迎提交Issue和PR！

## 📄 License
MIT License
```

---

## 五、技术栈与依赖

### 5.1 后端依赖

**requirements.txt**:
```
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# LangChain生态
langchain==0.1.0
langchain-openai==0.0.5
langchain-community==0.0.10

# 向量数据库
chromadb==0.4.15

# 数据库
sqlalchemy==2.0.23
alembic==1.12.1
aiosqlite==0.19.0

# 文档处理
pypdf2==3.0.1
python-docx==1.1.0
python-markdown==3.5.1

# 工具
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2

# 开发工具
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
```

### 5.2 前端依赖

**package.json**:
```json
{
  "name": "rag-assistant-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-markdown": "^9.0.1",
    "axios": "^1.6.2",
    "antd": "^5.12.0",
    "@ant-design/icons": "^5.2.6",
    "zustand": "^4.4.7",
    "react-router-dom": "^6.20.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6"
  }
}
```

### 5.3 Docker配置

**Dockerfile (Backend)**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile (Frontend)**:
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./app.db
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/chroma_db:/app/chroma_db
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

---

## 相关文档

- [AI工具使用指南及进阶](./企业级RAG项目-AI工具与进阶指南.md)
- [简历模板与面试准备](./企业级RAG项目-简历与面试指南.md)

---

**文档版本**: 1.0  
**最后更新**: 2026-03-03
