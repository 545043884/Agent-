# 智能扫地机器人客服 Agent

基于 ReAct 架构的智能客服系统，专为扫地机器人售后场景设计。Agent 能够自主调用多种工具，结合用户私有知识库与外部数据，回答问题并生成个性化使用报告。

## 功能特性

- **知识库问答**：从向量数据库检索产品手册、故障排除、保养指南等内容
- **天气感知**：获取用户所在城市天气，提供针对性保养建议
- **个性化报告**：结合用户历史使用记录，自动生成月度使用报告
- **流式输出**：逐字流式返回回答，提升交互体验
- **中间件机制**：支持工具调用监控、日志记录、动态提示词注入

## 技术栈

| 组件 | 技术 |
|------|------|
| 大模型 | 通义千问 `qwen3-max`（阿里云 DashScope） |
| Embedding | `text-embedding-v1`（DashScope） |
| Agent 框架 | LangChain ReAct Agent |
| 向量数据库 | ChromaDB |
| 前端界面 | Streamlit |

## 项目结构

```
Agen项目/
├── app.py                  # Streamlit 前端入口
├── agent/
│   ├── react_agent.py      # ReAct Agent 核心逻辑
│   └── tools/
│       ├── agent_tootls.py # 工具集（RAG/天气/用户信息/报告）
│       └── middleware.py   # 中间件（监控/日志/提示词注入）
├── rag/
│   ├── rag_service.py      # RAG 检索服务
│   └── vector_store.py     # 向量库封装
├── utils/                  # 工具函数（配置/日志/路径/提示词加载）
├── config/                 # 配置文件（agent/rag/chroma 参数）
├── prompts/                # 提示词模板
└── data/                   # 知识库原始文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件：

```
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 启动应用

```bash
streamlit run app.py
```

## 示例问答

- `扫地机器人吸力不足怎么办？`
- `我所在城市的天气适合开窗清扫吗？`
- `帮我生成上个月的使用报告`
