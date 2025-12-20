import os
from typing import Dict, List, Tuple
from openai import OpenAI

class BaseModel:
    def __init__(self, api_key: str = '') -> None:
        self.api_key = api_key

    def chat(self, prompt: str, history: List[Dict[str, str]], system_prompt: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        基础聊天接口
        
        Args:
            prompt: 用户输入
            history: 对话历史
            system_prompt: 系统提示
            
        Returns:
            (模型响应, 更新后的对话历史)
        """
        pass

    
class Siliconflow(BaseModel):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.siliconflow.cn/v1")

    def chat(self, prompt: str, history: List[Dict[str, str]] = [], system_prompt: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        与 Siliconflow API 进行聊天
        
        Args:
            prompt: 用户输入
            history: 对话历史
            system_prompt: 系统提示
            
        Returns:
            (模型响应, 更新后的对话历史)
        """
        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."}
        ]
        
        # 添加历史消息
        if history:
            messages.extend(history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": prompt})

        # 调用 API
        response = self.client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B-Instruct-2507",
            messages=messages,
            temperature=0.6,
            max_tokens=2000,
        )

        model_response = response.choices[0].message.content
        
        # 更新对话历史
        updated_history = messages.copy()
        updated_history.append({"role": "assistant", "content": model_response})

        return model_response, updated_history


class BaiduAIStudio(BaseModel):
    def __init__(self):
        """
        Initialize the Baidu-AI Studio client.
        Retrieves the API key from the environment variable 'AI_STUDIO_API_KEY'.
        """
        # Fetch the API key from environment variables
        self.api_key = os.getenv("AI_STUDIO_API_KEY")
        if not self.api_key:
            raise ValueError("Environment variable 'AI_STUDIO_API_KEY' is not set.")
            
        # Initialize the OpenAI client with Baidu's specific base_url
        self.client = OpenAI(
            api_key=self.api_key, 
            base_url="https://aistudio.baidu.com/llm/lmapi/v3"
        )

    def chat(self, prompt: str, history: List[Dict[str, str]] = None, system_prompt: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        Chat with the Baidu-AI Studio LLM API (ERNIE).
        
        Args:
            prompt: User input string.
            history: List of previous message dictionaries.
            system_prompt: System role description.
            
        Returns:
            Tuple containing (model_response, updated_conversation_history).
        """
        # Initialize history if None to avoid mutable default argument issues
        if history is None:
            history = []

        # Construct the message list starting with the system prompt
        messages = [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."}
        ]
        
        # Append existing conversation history
        messages.extend(history)
        
        # Append the current user prompt
        messages.append({"role": "user", "content": prompt})

        # Call the API using the specified ERNIE model
        response = self.client.chat.completions.create(
            model="ernie-3.5-8k",
            messages=messages,
            temperature=0.6,
            max_tokens=2000,
        )

        # Extract the content from the response
        model_response = response.choices[0].message.content
        
        # Create a copy of the messages and append the assistant's response for the updated history
        updated_history = messages.copy()
        # Note: We usually exclude the system prompt from the history 
        # if the next call prepends it again, but for consistency with your 
        # Siliconflow example, we return the full list used in the prompt + assistant reply.
        updated_history.append({"role": "assistant", "content": model_response})

        return model_response, updated_history


if __name__ == "__main__":
    llm = Siliconflow(api_key="your api key")
    prompt = "你好"
    response, history = llm.chat(prompt)
    print("Response:", response)
    print("History:", history)
