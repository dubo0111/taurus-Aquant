"""
智谱 AI Agent 服务
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from zhipuai import ZhipuAI

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.logger import logger
from src.utils.config import settings


class ZhipuAgent:
    """智谱 AI Agent"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化智谱 AI Agent

        Args:
            api_key: 智谱 AI API Key
            model: 模型名称
        """
        self.api_key = api_key or settings.ZHIPU_API_KEY
        self.model = model or settings.ZHIPU_MODEL

        if not self.api_key:
            raise ValueError("ZHIPU_API_KEY 未配置")

        self.client = ZhipuAI(api_key=self.api_key)
        logger.info(f"智谱 AI Agent 初始化成功，模型: {self.model}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        对话接口

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            模型回复
        """
        try:
            logger.info(f"调用智谱 AI，模型: {self.model}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content
            logger.info(f"智谱 AI 响应成功，长度: {len(content)}")

            return content

        except Exception as e:
            logger.error(f"智谱 AI 调用失败: {e}")
            raise

    def generate_strategy(self, description: str) -> Dict:
        """
        生成交易策略代码

        Args:
            description: 策略描述

        Returns:
            包含代码和说明的字典
        """
        prompt = f"""你是一个专业的量化交易策略开发者。请根据用户需求生成 Python 策略代码。

用户需求：{description}

要求：
1. 代码必须符合 Python 语法规范
2. 包含必要的注释
3. 使用标准的数据结构（pandas DataFrame）
4. 策略类名以 Strategy 结尾
5. 实现 generate_signals 方法，返回包含 'date' 和 'signal' 列的 DataFrame
   - signal = 1 表示买入
   - signal = -1 表示卖出
   - signal = 0 表示持有

请直接输出代码，不要有多余的解释。"""

        messages = [
            {"role": "system", "content": "你是一个专业的量化交易策略开发者"},
            {"role": "user", "content": prompt}
        ]

        code = self.chat(messages, temperature=0.3)

        return {
            "code": code,
            "description": description,
            "model": self.model
        }

    def analyze_strategy(self, strategy_code: str) -> Dict:
        """
        分析策略风险

        Args:
            strategy_code: 策略代码

        Returns:
            风险分析结果
        """
        prompt = f"""请分析以下量化交易策略代码的风险点和改进建议：

```python
{strategy_code}
```

请从以下几个方面分析：
1. **策略逻辑风险**：策略逻辑是否合理，是否存在明显漏洞
2. **过拟合风险**：是否容易过拟合历史数据
3. **风险控制**：是否有止损、仓位控制等风控措施
4. **代码质量**：代码是否存在 Bug 或潜在问题
5. **改进建议**：具体的优化建议

请用清晰的格式输出。"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        analysis = self.chat(messages, temperature=0.5)

        return {
            "analysis": analysis,
            "model": self.model
        }

    def explain_indicator(self, indicator_name: str) -> str:
        """
        解释技术指标

        Args:
            indicator_name: 指标名称

        Returns:
            指标说明
        """
        prompt = f"""请解释技术指标：{indicator_name}

请包含：
1. 指标的计算方法
2. 指标的使用方法
3. 指标的优缺点
4. 适用场景

请用简洁清晰的语言说明。"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        explanation = self.chat(messages)
        return explanation

    def generate_trading_plan(self, market_condition: str) -> str:
        """
        生成交易计划

        Args:
            market_condition: 市场情况描述

        Returns:
            交易计划
        """
        prompt = f"""基于以下市场情况，生成一个交易计划：

{market_condition}

请包含：
1. 市场分析
2. 交易策略
3. 风险控制
4. 资金管理
5. 止损止盈设置

请给出具体的可执行建议。"""

        messages = [
            {"role": "system", "content": "你是一个专业的量化交易分析师"},
            {"role": "user", "content": prompt}
        ]

        plan = self.chat(messages, temperature=0.6)
        return plan


# 全局 Agent 实例
_agent = None


def get_agent() -> ZhipuAgent:
    """获取全局 Agent 实例"""
    global _agent
    if _agent is None:
        _agent = ZhipuAgent()
    return _agent
