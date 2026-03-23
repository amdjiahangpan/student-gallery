# 南邮寒假大作战 — AMD ROCm

[English](./README.md)

## 活动信息

| 字段 | 详情 |
|------|------|
| **活动名称** | 南京邮电大学寒假大作战 — AMD ROCm |
| **赛题主题** | 基于 ROCm 的大语言模型应用开发 |
| **提交截止** | 2026 年 3 月 19 日 |
| **现场答辩** | 2026 年 3 月 22 日 |
| **地点** | 南京邮电大学 |
| **平台** | aup-learning-cloud — AMD GPU 集群（JupyterHub） |

## 背景介绍

AMD ROCm 是开源 GPU 计算平台，支持在 AMD 硬件上运行高性能 AI 任务。本次比赛要求学生在基于 ROCm 的集群环境中构建可交互的 LLM 智能应用。

**参考资料：**
- ROCm 官方文档：https://rocm.docs.amd.com/
- ROCm GitHub：https://github.com/ROCm/ROCm
- AMD CES 2025 发布：https://www.amd.com/zh-cn/newsroom/press-releases/2025-1-6-amd-announces-expanded-consumer-and-commercial-ai-.html
- AMD CES 2026 发布：https://www.amd.com/zh-cn/newsroom/press-releases/2026-1-5-amd-expands-ai-leadership-across-client-graphics-.html

## 赛题：大语言模型应用开发

**目标：** 构建一个可交互的智能应用系统（如问答助手、聊天机器人），基于集群 ROCm 环境运行。

### 开发环境

| 组件 | 详情 |
|------|------|
| **平台** | 远程 JupyterHub（Python 3.12+），通过 aup-learning-cloud 访问 |
| **Ollama API 地址** | `open-webui-ollama.open-webui:11434` |
| **可用模型** | `qwen3-coder:30b`、`gpt-oss:20b` |
| **上下文窗口** | 32K tokens |
| **推荐交互方式** | `ipywidgets`（在 Notebook 内原生交互） |
| **API 文档** | https://ollama.readthedocs.io/api/ |

### 推荐主题

#### 主题 1：领域知识问答助手（RAG 方向）
构建面向特定领域（如校规、专业课程、编程文档）的问答系统。
- **基础：** 多轮对话、记忆机制、异步/流式 API、中英文支持
- **进阶：** 完整 RAG 链路（文档解析 → 向量检索 → 增强生成）、来源标注

#### 主题 2：文本智能分析与报告助手（数据处理方向）
利用大模型对文本进行结构化提取与深度分析。
- **基础：** 摘要、情感分析、关键词提取；格式化 Markdown 报告输出
- **进阶：** 批量处理流水线（多线程/异步）、多文本对比分析报告

#### 主题 3：代码辅助编程专家（工程应用方向）
构建面向初学者的代码解释与调试助手。
- **基础：** 代码逐段说明、常见错误分析，支持 Python（Java/C++ 可选）
- **进阶：** 自动生成项目脚手架和测试用例、代码风格检查与重构建议

#### 主题 4：交互式叙事与逻辑分析（创意与逻辑方向）
基于对话引导使用 LLM 生成故事续写，并监控故事逻辑一致性。
- **基础：** 多轮续写、故事类型选择（科幻/悬疑/奇幻）、基本结构检查
- **进阶：** 一致性检测（角色/场景状态表）、三幕式结构打分

### 技术要求

- **Prompt Engineering：** 必须在文档中展示提示词迭代过程（约束、Few-shot、思维链）
- **集群资源利用：** 必须通过代码展示对集群内网 Ollama API 的调用
- **错误处理：** 必须处理 API 超时、空输入，以及上下文超长（32K）问题，至少实现以下一种方案：
  - 分段滚动处理（Chunking & Sliding Window）
  - 级联摘要生成（Recursive Summarization）
  - 动态截断与提示词压缩（Truncation & Prompt Compression）

## 奖项设置

| 奖项 | 名额 | 奖品 |
|------|------|------|
| 一等奖 | 1 队 | PYNQ Z2 开发板 × 1 + AMD 定制 T恤 × 2 + AMD 定制折叠背包 × 1 |
| 二等奖 | 2 队 | Spartan Edge FPGA 开发板 × 1 + AMD 定制帽子 × 2 + AMD 定制折叠背包 × 1 |
| 三等奖 | 4 队 | AMD 定制马克杯 × 2 + AMD 定制折叠背包 × 1 |
| 优秀奖 | 10 队 | AMD 定制折叠背包 × 2 |
| 参与奖 | 全体参赛者 | 《可定制计算》书籍 × 1（先到先得） |

## 学习资料

- DataWhale：https://www.datawhale.cn/
- DataWhale GitHub：https://github.com/datawhalechina
- AMD ModelScope 社区：https://modelscope.cn/brand/view/AMDCommunity

## 参赛作品

> 学生通过 Pull Request 提交作品，详见 [CONTRIBUTING_ZH.md](../../CONTRIBUTING_ZH.md)。

| 文件夹 | 团队 | 项目 |
|--------|------|------|
| _（作品合并后显示）_ | — | — |

## 如何体验所有案例

1. 打开 aup-learning-cloud → 选择 **Basic GPU Environment**
2. Git URL 填入：`https://github.com/amdjiahangpan/aup-learning-cloud-case-hub`
3. 启动后进入 `cases/2026-03-njupt-winter-battle/`
4. 打开任意作品文件夹，运行 `main.ipynb`
