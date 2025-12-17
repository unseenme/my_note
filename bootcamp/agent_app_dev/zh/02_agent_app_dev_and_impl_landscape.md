# Agent 应用开发与落地全景

## 目录

01. 智能体（Agent）定义
02. 智能体系统（Agentic System）的架构划分
03. 智能体系统（Agentic System）组成模块
04. 国内外有哪些 Agent 平台、框架、产品
05. 总结

---

## 01. 智能体（Agent）定义

### 智能体（Agent）的现状定义

* **现状：** 从学术界到产业界，大模型领域仍处于快速发展阶段，**还没有明确具体的共识**。任何一个非单次大模型调用的系统，都有可能被其开发者称为“Agent”。

* **OpenAI 的 AGI 五级分类：**
    * Level 1: Conversational AI (仅限于语言对话，能力有限)
    * Level 2: Reasoners (在专业领域能够独立推理，不需外部工具)
    * Level 3: Agents (能长时间自主行动执行任务)
    * Level 4: Innovators (产生新思路，推动科技突破)
    * Level 5: Organizers (能管理协调整个组织)

* **前 OpenAI 研究副总裁 翁荔（Lilian Weng）的定义：**
    $$Agent = \text{大模型} + \text{记忆} + \text{主动规划} + \text{工具使用}$$
    
* **LangChain 作者 Horrison 的定义：**
    > Agent 是一个使用 **LLM 决定应用程序控制流**的系统。
    >
    > *“This fits my technical definition, but not the common perception of what an agent should be capable of. It’s hard to define exactly what an agent is!”*

### “Agentic”：渐进的智能属性

* **吴恩达 & Horrison 观点：** 不必拘泥于“是否属于 Agent”，而应关注其具备 **“agentic”（渐进的智能属性）** 的程度。
* 形容词 **“agentic”** 更能包容这个蓬勃发展的领域中各种形态的系统。
* 类似于自动驾驶汽车的 L1-L4 分级，一个 Agentic System 的智能程度可以有不同等级，**取决于 LLM 对系统行为的决策权重**。

---

## 02. 智能体系统（Agentic System）的架构划分

从架构上看，Agentic System 可以分为两大类系统：

| 类型 | 工作流 (Workflow) | 自主智能体 (Autonomous Agent) |
| :--- | :--- | :--- |
| **特点** | 通过预定义代码路径编排 LLM 和工具 | LLM 动态控制决策和工具使用，自主规划任务 |
| **侧重** | 流程固定和可预测性 | 灵活性与自我决策 |
| **适用场景** | 任务明确、步骤可预定义的场景 | 任务步骤难以预知、需长期自主规划的场景 |

**注意事项：**

* 有些场景（如聊天对话）可能完全不需要 Agentic System。
* 对很多场景，通过 **RAG（检索增强生成）和 Prompt 优化**可能已足够。
* **增加系统复杂度往往伴随延迟和成本，需权衡利弊！**

---

## 03. 智能体系统（Agentic System）组成模块

### 3.1 基础构建模块：增强型 LLM

* 智能体系统的基础是具备**检索、工具使用和记忆能力**的增强型 LLM。
* **建议：** 复杂应用使用的模型能力都是基于 API，一定要搞清楚大模型接口逻辑。开发时建议优先直接使用 API，只在必要时借助高级框架。

### 3.2 工作流（Workflow）的常见模式

工作流侧重流程固定和可预测性，通过预定义代码路径编排 LLM 和工具。

#### 🔹 提示链 (Prompt Chaining)
* **模式：** 按顺序拆分任务，每一步由 LLM 生成内容。可以在任意中间步骤添加程序检查（“gate”）以确保过程按计划执行。
* **场景示例：** 先生成市场营销文案，再将其翻译；编写提纲、检验提纲、再根据提纲写完整文档。

#### 🔹 路由 (Routing)
* **模式：** 根据输入分类，分配给专门的后续任务/流程/工具。
* **场景示例：**
    * 不同类型的客户服务请求（常见问题、退款、技术支持）进入不同的后续流程。
    * 将简单问题路由给较小模型，困难问题路由给更强大模型，以优化成本与速度。

#### 🔹 并行 (Parallelization)
* **模式：** 同时执行多个任务，然后将它们的输出聚合在一起。
* **主要变体：**
    * **分段 (Sectioning)：** 将任务划分为可以并行运行的独立子任务。
    * **投票 (Voting)：** 对同一任务进行多次执行，获得多样化输出，以进行对比或投票。
* **场景示例：**
    * （分段）并行内容审核与主任务处理。
    * （投票）多个提示从不同角度评估某段内容是否不当。

#### 🔹 协调者-工作者 (Orchestrator-Workers)
* **模式：**
    * **协调者**（通常是 LLM）拆解任务。
    * **工作者**（可以是其他 LLM 或工具）专注子任务。
* **场景示例：**
    * 多文件代码修改：每次都需要对多个文件进行复杂改动的编程产品。
    * 多源信息搜索分析：在多源信息中搜索并分析可能相关的信息。

#### 🔹 评估-优化循环 (Evaluator-Optimizer)
* **模式：**
    * 一个 LLM 生成输出。
    * 另一个 LLM（评估者）进行反馈和优化。
    * **反复循环**直到达到终止条件。
* **场景示例：**
    * 文学翻译润色：评估者指出初稿的不足并给出改进意见。
    * 复杂搜索任务的多轮优化：评估者判断是否需要进一步搜索。

### 3.3 自主智能体（Autonomous Agent）

自主智能体适用于**开放性问题**，即当任务步骤数量难以预知或无法预先固定时。

* **执行环境反馈：** 执行过程中获取环境真实反馈（例如工具调用的结果或代码执行情况）。
* **人工干预：** 支持人工检查点干预（可在检查点或遇到阻碍时暂停，等待人类反馈）。
* **终止条件：** 设置终止条件（通常在任务完成时终止，也常设置停止条件如最大迭代次数）。

#### 关键组件

在基于 LLM 的自主智能体系统中，LLM 充当智能体的大脑，需结合以下关键组件：

1.  **规划模块 (Planning)**
    * 子目标拆解：将复杂任务分解为可管理的子目标。
    * 反思优化：通过自我评估改进执行策略。

2.  **记忆系统 (Memory)**
    * 短期记忆 (上下文)。
    * 长期记忆（外部存储）。

3.  **工具使用 (Tool Use)**
    * 获取预训练模型外的实时信息与功能扩展（调用外部 API）。

---

## 04. 国内外有哪些 Agent 平台、框架、产品

### 智能体系统构建框架

| 类型 | 框架/平台 | 特点 |
| :--- | :--- | :--- |
| **全代码框架** | LangChain & LangGraph | 开源，全代码 |
| | LlamaIndex | 开源，全代码 |
| **低代码平台** | 毕昇 BISHENG | Apache 2.0 开源，专注企业级场景 |
| | Dify | 开源 |
| | Coze | Apache 2.0 开源 |
| | FastGPT | 开源 |

### 低代码 Workflow 产品设计的思考

1.  **独立、完备的流程编排框架：**
    * 不简单是一个被 bot 调用的工具。
    * 不需要划分出 chatflow 和 workflow。

2.  **Human in the loop 特性：**
    * 中间过程支持灵活的输入/输出和多样化的人机交互。
    * 复杂业务场景需要人类与 AI 进行协作：人类也能参与执行过程的判断和决策。

3.  **节点之间是否支持成环？**
    * 核心在于 workflow 执行引擎抽象出来后，到底是一个 **DAG（有向无环图）还是状态机**？
    * **结论：** 根据形式语言与自动机理论，支持成环能够覆盖更多范围的场景。

### Agent 产品示例

* ChatGPT DeepResearch
* Manus
* 扣子空间
* 毕昇灵思
* AutoGLM 沉思

---

## 05. 总结

### 5.1 智能体定义

* 大模型领域发展很快，关于 Agent 的定义还没有一个统一的说法。
* 与其讨论某个产品是不是属于 Agent，不如讨论它在多大程度上具有 **agentic 属性**。

### 5.2 Agentic System 划分

从架构上可以划分为：
* **自主智能体 (Autonomous Agent)**
* **工作流 (Workflow)**

### 5.3 自主智能体

自主智能体适用于开放性问题，即当任务步骤数量难以预知或无法预先固定时。
* **规划模块：** 帮助 Agents 更好地理解任务结构和目标，以及在此基础上如何分配资源和优化决策。
* **记忆系统：** 长期记忆 & 短期记忆。
* **工具使用：** 调用外部 API，以获取模型权重中缺少的额外信息。

### 5.4 工作流模块

* 包含**提示链、路由、并行、协调者—工作者、评估—优化循环**等模式。
* **设计原则：** 应避免盲目追求过度复杂性。针对具体任务，**从简单方案出发**，再根据性能与需求逐步优化。

---

## 推荐阅读 & 参考资料

* OpenAI API 文档：`https://platform.openai.com/docs/guides/function-calling`
* lilian weng：《LLM Powered Autonomous Agents》：`https://lilianweng.github.io/posts/2023-06-23-agent/`
* Langchain：《What is an AI agent?》：`https://blog.langchain.dev/what-is-an-agent/`
* Anthropic：《Building effective agents》：`https://www.anthropic.com/research/building-effective-agents`

**相关框架 & 平台：**

* langchain：`https://www.langchain.com/`
* llamaindex：`https://www.llamaindex.ai/`
* 毕昇 BISHENG：`https://bisheng.ai.com/`
* Dify：`https://cloud.dify.ai/`
* Coze：`https://www.coze.cn/`