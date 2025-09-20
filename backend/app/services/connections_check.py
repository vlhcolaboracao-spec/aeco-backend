"""
Serviços para verificação de conexões do sistema.
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any
from datetime import datetime

from ..config import settings
from ..db.mongo import ping_mongo

logger = logging.getLogger(__name__)


async def check_mongo_connection() -> Dict[str, Any]:
    """
    Verifica a conexão com MongoDB
    
    Returns:
        Dict com status e detalhes da conexão
    """
    try:
        start_time = datetime.now()
        is_connected = await ping_mongo()
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds() * 1000
        
        return {
            "status": "OK" if is_connected else "FAIL",
            "connected": is_connected,
            "response_time_ms": round(response_time, 2),
            "message": "Conexão com MongoDB estabelecida" if is_connected else "Falha na conexão com MongoDB",
            "mongo_uri": settings.mongo_uri.replace(settings.mongo_uri.split("@")[0].split("://")[1], "***") if "@" in settings.mongo_uri else settings.mongo_uri,
            "mongo_db": settings.mongo_db
        }
        
    except Exception as e:
        logger.error(f"Erro ao verificar MongoDB: {e}")
        return {
            "status": "FAIL",
            "connected": False,
            "response_time_ms": None,
            "message": f"Erro na verificação: {str(e)}",
            "mongo_uri": settings.mongo_uri.replace(settings.mongo_uri.split("@")[0].split("://")[1], "***") if "@" in settings.mongo_uri else settings.mongo_uri,
            "mongo_db": settings.mongo_db
        }


async def check_api_health() -> Dict[str, Any]:
    """
    Verifica se a API está respondendo
    
    Returns:
        Dict com status e detalhes da API
    """
    try:
        start_time = datetime.now()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.api_base_url}/health",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                data = await response.json()
                
                return {
                    "status": "OK" if response.status == 200 else "FAIL",
                    "http_status": response.status,
                    "response_time_ms": round(response_time, 2),
                    "message": "API respondendo corretamente" if response.status == 200 else f"API retornou status {response.status}",
                    "api_url": settings.api_base_url,
                    "health_data": data
                }
                
    except asyncio.TimeoutError:
        return {
            "status": "FAIL",
            "http_status": None,
            "response_time_ms": None,
            "message": "Timeout na requisição para a API",
            "api_url": settings.api_base_url,
            "health_data": None
        }
    except Exception as e:
        logger.error(f"Erro ao verificar API: {e}")
        return {
            "status": "FAIL",
            "http_status": None,
            "response_time_ms": None,
            "message": f"Erro na verificação: {str(e)}",
            "api_url": settings.api_base_url,
            "health_data": None
        }


async def run_full_connections_check() -> Dict[str, Any]:
    """
    Executa verificação completa de todas as conexões
    
    Returns:
        Dict com resultados de todas as verificações
    """
    logger.info("Iniciando verificação completa de conexões...")
    
    # Executa verificações em paralelo
    mongo_result, api_result = await asyncio.gather(
        check_mongo_connection(),
        check_api_health(),
        return_exceptions=True
    )
    
    # Trata exceções
    if isinstance(mongo_result, Exception):
        mongo_result = {
            "status": "FAIL",
            "connected": False,
            "message": f"Exceção: {str(mongo_result)}"
        }
    
    if isinstance(api_result, Exception):
        api_result = {
            "status": "FAIL",
            "http_status": None,
            "message": f"Exceção: {str(api_result)}"
        }
    
    # Determina status geral
    all_ok = (
        mongo_result.get("status") == "OK" and 
        api_result.get("status") == "OK"
    )
    
    return {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "OK" if all_ok else "FAIL",
        "mongo": mongo_result,
        "api": api_result,
        "summary": {
            "total_checks": 2,
            "passed": sum([
                1 for result in [mongo_result, api_result] 
                if result.get("status") == "OK"
            ]),
            "failed": sum([
                1 for result in [mongo_result, api_result] 
                if result.get("status") != "OK"
            ])
        }
    }
