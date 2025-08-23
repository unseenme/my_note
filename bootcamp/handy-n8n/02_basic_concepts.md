# n8n Basic Concepts

## Trigger Nodes
Trigger nodes are used to start workflows in n8n.

- **Manual Trigger**: Starts a workflow manually from the editor.
- **Schedule Trigger**: Executes workflows on a predefined schedule (e.g., cron jobs).
- **Webhook Trigger**: Starts a workflow when an incoming HTTP request is received.
- **Chat Trigger**: Initiates workflows based on chat interactions (e.g., chatbots).

## Core Nodes
Core nodes are essential for workflow logic and data handling.

- **Data Transformation**: Modify or restructure incoming data for further processing.
- **Control Flow**: Direct workflow execution paths (e.g., IF, Switch, Merge).
- **HTTP Request**: Send HTTP requests to external APIs or services.

## Code in n8n
n8n allows dynamic logic using built-in scripting.

- **Expressions**: Use JavaScript within double curly braces `{{ }}` to access and manipulate data dynamically.
- **Code Node**: Execute custom JavaScript or TypeScript for complex logic and transformations.
