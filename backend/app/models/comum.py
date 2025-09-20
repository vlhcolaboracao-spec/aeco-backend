"""
Modelos Pydantic comuns para a aplicação.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """Modelo base para respostas da API"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Modelo para resposta do endpoint /health"""
    status: str
    mongo: bool
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
