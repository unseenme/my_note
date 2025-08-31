# Learning Notes: n8n Community Nodes and Custom Node Development

## 1. Community Nodes

### Overview
- Community nodes are distributed as **npm packages**, hosted on the npm registry ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
- To be recognized as a community node, the package must:
  - **Name**: Begin with `n8n-nodes-` or use a scoped format like `@scope/n8n-nodes-...` (e.g. `n8n-nodes-weather`, `@weatherPlugins/n8n-nodes-weather`) ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
  - **Keywords**: Include `n8n-community-node-package` in the `"keywords"` field of `package.json` ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
  - **n8n attribute**: Define the nodes and credentials under the `"n8n"` attribute in `package.json` (see starter node for example) ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
- **Testing and Publishing**:
  - Utilize the **linter** to verify node code quality and test locally ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
  - Publish the package to the npm registry. Then submit it for **verification by n8n**, ensuring it meets technical and UX standards (e.g., no runtime dependencies, proper documentation). n8n reserves the right to reject nodes that overlap with paid or enterprise functionality ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
- **Installation & Management**:
  - Verified community nodes can be installed using the n8n **nodes panel GUI**.
  - Alternatively, install via GUI or manually through `npm install` on self-hosted instances for both verified and unverified nodes (unverified nodes unavailable on n8n cloud) ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/installation/?utm_source=chatgpt.com)).

## 2. Custom Node Development

### 2.1 Setting Up Your Environment
- **Prerequisites**:
  - Install **Node.js (minimum v18.17.0)** and **npm**, using tools like **nvm**; also ensure **git** is installed ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/build/node-development-environment/?utm_source=chatgpt.com)).
  - Install **n8n globally** using `npm install n8n -g` to test custom nodes locally ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/build/node-development-environment/?utm_source=chatgpt.com)).
- **Editor**:
  - Recommended IDE: **Visual Studio Code** with extensions: **ESLint**, **EditorConfig**, and **Prettier** (enables real-time linter feedback while coding) ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/build/node-development-environment/?utm_source=chatgpt.com)).

### 2.2 Planning Your Node
- Establish elements such as:
  - **Node type**
  - **Development style** (declarative vs programmatic)
  - **UI design**
  - **File structure** ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).

### 2.3 Building the Node
- Follow **tutorials** for both:
  - **Declarative-style nodes** (simpler, configuration-driven)
  - **Programmatic-style nodes** (custom code logic) ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).
- Reference the **"Reference"** section to understand:
  - Node UI elements, code standards, error handling, versioning
  - File structure for base files, codex, credentials
  - HTTP request helpers, item linking, UX/verification guidelines ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).

### 2.4 Testing the Node
- **Local testing**:
  - Use the node linter and run the node locally to validate functionality ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).
  - Leverage troubleshooting tips from documentation ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).

### 2.5 Deployment
- **Submit your node** as a community node via npm and optionally for verification by n8n ([docs.n8n.io](https://docs.n8n.io/integrations/community-nodes/build-community-nodes/?utm_source=chatgpt.com)).
- For private use, install node packages locally in your environment ([docs.n8n.io](https://docs.n8n.io/integrations/creating-nodes/overview/?utm_source=chatgpt.com)).

## 3. Additional Resources & Community Insights

### Starter Template
- Use the **n8n‑nodes‑starter** GitHub template as a foundation:
  - Contains examples in `/nodes` and `/credentials`
  - Includes linter, dependencies, and workflow for building and publishing ([github.com](https://github.com/n8n-io/n8n-nodes-starter?utm_source=chatgpt.com)).

### Community Tooling Enhancements
- Recent updates note that documentation may be outdated:
  - **pnpm** is now recommended over **npm**
  - Some users report integrating **devcontainers** and custom tooling for hot reloading (e.g., `n8n-nodes-builder`) ([community.n8n.io](https://community.n8n.io/t/n8n-custom-node-dev-env-with-debug-and-hot-reload/85395?utm_source=chatgpt.com)).

### AI-related Custom Node Usage
- To enable custom nodes as AI tools, set `usableAsTool: true` in the node definition and use the environment variable `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE` to allow usage — addresses default checks restricting custom nodes as tools ([community.n8n.io](https://community.n8n.io/t/creating-a-custom-node-tool/79651?utm_source=chatgpt.com)).

##  Summary Table

| Phase             | Key Actions                                               |
|------------------|-----------------------------------------------------------|
| **Community Nodes**     | Name must start with `n8n-nodes-`; include keywords; define `n8n` field; lint & test; publish; verify for n8n; install via GUI or npm for self-hosting |
| **Development Setup**   | Use Node.js ≥18.17.0, npm, git, install n8n CLI; use VS Code with recommended extensions |
| **Plan & Build**        | Choose node type/style/UI/file structure; follow declarative/programmatic tutorials; refer to reference files and standards |
| **Test & Debug**        | Run linter; test locally; troubleshoot using official guidance |
| **Deploy & Distribute** | Publish to npm; optionally submit for verification; install as private or community node |
| **Advanced Tips**       | Use starter template; use pnpm or devcontainers for faster workflow; add AI tool support via `usableAsTool` and env var |
