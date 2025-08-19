# Learning Notes on n8n

## Part 1: Notes after Learning the Introduction to n8n

n8n is a fair-code licensed workflow automation tool that enables users
to connect different applications and services with minimal effort. It
provides a node-based interface that allows both technical and
non-technical users to design complex workflows.

Key takeaways from the introduction: - **Open Source**: n8n is open
source with a fair-code license, making it accessible and modifiable.\
- **Workflow Automation**: It helps automate repetitive tasks by
connecting multiple applications and services.\
- **Node-Based Design**: Each function, API call, or service is
represented as a "node", making it visually intuitive.\
- **Integration**: Supports integration with hundreds of services, and
new integrations can be added via community contributions.\
- **Flexibility**: Provides the ability to extend functionality with
custom code or logic.

Overall, n8n stands out as a flexible and powerful tool for workflow
automation that balances accessibility with deep customization options.

## Part 2: Summary of My Installation Process

"""
docker volume create n8n_data

docker run -it --rm \
 --name n8n \
 -p 5678:5678 \
 -e GENERIC_TIMEZONE="Asia/Tokyo" \
 -e TZ="Asia/Tokyo" \
 -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true \
 -e N8N_RUNNERS_ENABLED=true \
 -v n8n_data:/home/node/.n8n \
 docker.n8n.io/n8nio/n8n
"""
