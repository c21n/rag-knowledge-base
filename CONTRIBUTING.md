# Contributing to RAG Knowledge Base

感谢你对本项目的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果你发现了bug或有功能建议，请通过GitHub Issues提交：

1. 搜索现有issues，避免重复提交
2. 使用issue模板（如果有）
3. 提供详细的描述和复现步骤
4. 附上相关的日志或截图

### 提交代码

#### 开发环境设置

1. Fork本仓库
2. 克隆你的fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag-knowledge-base.git
   cd rag-knowledge-base
   ```
3. 添加上游仓库:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/rag-knowledge-base.git
   ```

#### 开发流程

1. 创建新分支:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行你的修改

3. 确保代码质量:
   ```bash
   # 后端
   cd backend
   pip install -r requirements.txt
   pytest
   
   # 前端
   cd frontend
   npm install
   npm run lint
   npm run build
   ```

4. 提交你的更改:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. 推送到你的fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. 创建Pull Request

### 代码规范

#### 提交信息格式

使用[Conventional Commits](https://www.conventionalcommits.org/)格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）:
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式（不影响代码运行的变动）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

示例:
```
feat(backend): add document search endpoint

Implement semantic search using ChromaDB vector store.
Supports filtering by document type and date range.

Closes #123
```

#### Python代码规范

- 遵循[PEP 8](https://pep8.org/)风格指南
- 使用类型注解
- 编写docstring（Google风格）
- 保持函数简洁（尽量不超过50行）

#### TypeScript/React代码规范

- 使用函数式组件
- 使用TypeScript严格模式
- 组件props使用接口定义
- 使用hooks进行状态管理

### 测试

- 为新功能编写测试
- 确保所有测试通过
- 保持测试覆盖率

### 文档

- 更新相关的README文件
- 为API添加文档字符串
- 更新CHANGELOG.md

## 行为准则

- 保持友善和尊重
- 接受建设性批评
- 关注社区利益

## 获取帮助

- 查看[README.md](README.md)获取基本信息
- 查看[文档](docs/)获取详细说明
- 在Discussions中提问

## 许可证

通过贡献代码，你同意你的贡献将在[MIT许可证](LICENSE)下发布。

感谢你的贡献！🎉
