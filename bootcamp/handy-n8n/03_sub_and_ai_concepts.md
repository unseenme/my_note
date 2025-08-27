# Sub-workflows and AI Concepts

## Sub-workflows
Manage modular workflows using **Execute Workflow** and **Execute Sub-workflow Trigger** nodes. Sub-workflows allow for microservice-like structure and help mitigate memory issues. They do **not** count against your plan’s execution or active workflow limits.  
**Steps**:
1. **Create sub-workflow**  
   - New workflow or convert nodes from parent workflow.  
   - Define input data mode: *fields*, *JSON example*, or *accept all data*.  
2. **Call sub-workflow**  
   - Use **Execute Sub-workflow** node in the parent workflow.  
   - Pass required input items, then save.  
   - Use “View sub-execution” link to trace executions between parent and sub-workflow.  

## Error Handling
Use an **Error Workflow** to manage failures gracefully.
- Create a separate workflow starting with an **Error Trigger** as the first node.  
- In your main workflow’s settings, assign this error workflow.  
- Optionally use the **Stop And Error** node to trigger it manually.  

Error workflows receive different context depending on whether the failure occurred in a trigger or later node (e.g. `trigger{}` vs. `execution{}` payload differences).  

## Cluster Nodes
In n8n, **Cluster nodes** are used within the AI/Advanced AI context—they include specialized sub-nodes such as vector stores, memory managers, retrievers, and tools.  

## Memory Nodes
### Simple Memory Node
- Enables persistence of chat history within a workflow.
- Configurable parameters:
  - **Session Key**: key to store memory.
  - **Context Window Length**: number of previous interactions to retain.  
- **Limitations**:
  - Not compatible with queue mode—memory may not stay consistent across workers.  
  - For sub-nodes, expressions always resolve against the **first input item**.  
- **Common Issues**:
  - Multiple Simple Memory nodes share memory unless different session IDs are used.  
  - If `sessionId` is missing (common error), ensure it's present in Chat trigger output or manage it manually.  

### Chat Memory Manager Node
Provides more advanced in-workflow manipulation of chat memory:
- **Operations**: Get Many Messages, Insert Messages, Delete Messages.  
- In Insert mode, choose between **Insert** or **Override All** existing messages.  
- Delete mode supports removing last N or all messages.  
- Allows injecting messages with specific types (AI, System, User).  

## RAG (Retrieval-Augmented Generation)
### Overview
RAG enhances AI responses by grounding them in external, domain-specific content via vector stores.  

### Steps:
1. **Insert documents into vector store**:  
   - Use nodes: **Vector Store** (e.g. Simple Vector Store) with *Insert Documents* operation.  
   - Choose an embedding model.  
   - Use a **Default Data Loader** to split content (by character, Markdown/html chunks, tokens).  
   - Optional: add metadata for filtering.  
2. **Querying**:
   - **Via Agent**:  
     - Add AI Agent node, attach vector store as a tool, define limits and metadata.  
     - Use same embedding model.  
   - **Directly**:  
     - Use vector store node with *Get Many* operation. Set query, limit, whether to include metadata.  

**Pro‑tip**: Use a vector store question-answer tool first to fetch relevant chunks before calling expensive models.  

## Content Upload
Covered under RAG workflows:
- Use data fetching nodes (e.g., File read, HTTP).
- Insert documents into vector store via **Vector Store** node.  
- Split content using **Default Data Loader**.  

## Content Retrieval
Two main methods:
- **Agent-based**: AI Agent with vector store tool + embedding model.  
- **Direct retrieval**: Vector store node with *Get Many* operation.  

## Tools
In Advanced AI context, “Tools” are external services integrated via nodes:
- Example: **MCP Client Tool**—connect to an external MCP server, expose tools to AI Agent. Parameters:
  - SSE endpoint, authentication method.
  - Tools to include/exclude for the Agent.  

Other tools available as sub-nodes include SearXNG, Wikipedia, Wolfram|Alpha, Vector Store QA Tool, Call n8n Workflow Tool, etc.  

## MCP (Model Context Protocol)
The **MCP Client Tool** node allows integration with external MCP servers:
- Use to let AI agents call external tools.
- Configurable fields: SSE endpoint, authentication (Bearer or header), and selective exposure of tools.  
