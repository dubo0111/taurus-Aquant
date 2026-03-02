"""
FastAPI Agent 路由
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

router = APIRouter(prefix="/api/agent", tags=["Agent"])


class ChatRequest(BaseModel):
    """对话请求"""
    message: str
    history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    """对话响应"""
    response: str
    model: str


class StrategyGenerateRequest(BaseModel):
    """策略生成请求"""
    description: str


class StrategyGenerateResponse(BaseModel):
    """策略生成响应"""
    code: str
    description: str
    model: str


class StrategyAnalyzeRequest(BaseModel):
    """策略分析请求"""
    code: str


class StrategyAnalyzeResponse(BaseModel):
    """策略分析响应"""
    analysis: str
    model: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI 对话接口"""
    try:
        from src.agent.agent_service import get_agent

        agent = get_agent()

        # 构建消息
        messages = []
        if request.history:
            messages.extend(request.history)
        messages.append({"role": "user", "content": request.message})

        # 调用 Agent
        response = agent.chat(messages)

        return ChatResponse(
            response=response,
            model=agent.model
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-strategy", response_model=StrategyGenerateResponse)
async def generate_strategy(request: StrategyGenerateRequest):
    """生成策略代码"""
    try:
        from src.agent.agent_service import get_agent

        agent = get_agent()
        result = agent.generate_strategy(request.description)

        return StrategyGenerateResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-strategy", response_model=StrategyAnalyzeResponse)
async def analyze_strategy(request: StrategyAnalyzeRequest):
    """分析策略风险"""
    try:
        from src.agent.agent_service import get_agent

        agent = get_agent()
        result = agent.analyze_strategy(request.code)

        return StrategyAnalyzeResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indicator/{indicator_name}")
async def explain_indicator(indicator_name: str):
    """解释技术指标"""
    try:
        from src.agent.agent_service import get_agent

        agent = get_agent()
        explanation = agent.explain_indicator(indicator_name)

        return {
            "indicator": indicator_name,
            "explanation": explanation,
            "model": agent.model
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
