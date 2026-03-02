"""
智谱 AI 适配器
"""
from typing import List, Dict, Optional
from zhipuai import ZhipuAI
from .base_adapter import LLMAdapter
from ...utils.logger import logger


class ZhipuAdapter(LLMAdapter):
    """智谱 AI 适配器"""

    def __init__(self, api_key: str, model: str = "glm-4"):
        """
        初始化智谱 AI 适配器

        Args:
            api_key: 智谱 AI API Key
            model: 模型名称，如 'glm-4', 'glm-3-turbo'
        """
        self.client = ZhipuAI(api_key=api_key)
        self.model = model
        logger.info(f"智谱 AI 适配器初始化成功，模型: {model}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        对话接口

        Args:
            messages: 消息列表，格式 [{'role': 'user', 'content': '...'}]
            temperature: 温度参数，控制随机性
            max_tokens: 最大 token 数

        Returns:
            模型回复文本
        """
        try:
            logger.info(f"调用智谱 AI，模型: {self.model}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            content = response.choices[0].message.content

            logger.info(f"智谱 AI 响应成功，长度: {len(content)}")

            return content

        except Exception as e:
            logger.error(f"智谱 AI 调用失败: {e}")
            raise

    def generate_code(
        self,
        prompt: str,
        language: str = "python",
        **kwargs
    ) -> str:
        """
        生成代码

        Args:
            prompt: 提示词
            language: 编程语言

        Returns:
            生成的代码
        """
        system_prompt = f"""你是一个专业的量化交易策略开发者。请根据用户的需求生成 {language} 代码。

要求：
1. 代码必须符合语法规范
2. 包含必要的注释
3. 使用标准的数据结构
4. 考虑异常处理"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        return self.chat(messages, **kwargs)

    def analyze_strategy(
        self,
        strategy_code: str,
        **kwargs
    ) -> Dict:
        """
        分析策略代码

        Args:
            strategy_code: 策略代码

        Returns:
            分析结果
        """
        prompt = f"""请分析以下量化交易策略代码，识别潜在风险和改进建议：

```python
{strategy_code}
```

请从以下几个方面分析：
1. 策略逻辑是否合理
2. 是否存在风险点
3. 代码质量如何
4. 改进建议"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.chat(messages, **kwargs)

        return {
            "analysis": response,
            "model": self.model
        }
