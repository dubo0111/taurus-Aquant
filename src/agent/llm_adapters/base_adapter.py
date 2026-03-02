"""
LLM 适配器基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict


class LLMAdapter(ABC):
    """LLM 适配器抽象基类"""

    @abstractmethod
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
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            模型回复文本
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
