"""
Router para health check da aplicação.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from ..models.comum import HealthResponse
from ..db.mongo import ping_mongo
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de health check que verifica:
    - Status da aplicação
    - Conectividade com MongoDB
    """
    try:
        # Testa conexão com MongoDB
        mongo_status = await ping_mongo()
        
        # Determina status geral
        overall_status = "ok" if mongo_status else "degraded"
        
        response = HealthResponse(
            status=overall_status,
            mongo=mongo_status,
            timestamp=datetime.now()
        )
        
        logger.info(f"Health check - Status: {overall_status}, MongoDB: {mongo_status}")
        return response
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no health check: {str(e)}"
        )
