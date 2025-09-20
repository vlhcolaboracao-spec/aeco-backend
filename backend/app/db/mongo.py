"""
Conexão e configuração do MongoDB.
"""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """Classe para gerenciar conexão com MongoDB"""
    
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    """Conecta ao MongoDB usando as configurações do .env"""
    try:
        MongoDB.client = AsyncIOMotorClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=5000  # 5 segundos timeout
        )
        MongoDB.database = MongoDB.client[settings.mongo_db]
        
        # Testa a conexão
        await MongoDB.client.admin.command('ping')
        logger.info(f"Conectado ao MongoDB: {settings.mongo_db}")
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Erro ao conectar no MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Fecha a conexão com MongoDB"""
    if MongoDB.client:
        MongoDB.client.close()
        logger.info("Conexão MongoDB fechada")


async def get_database() -> AsyncIOMotorDatabase:
    """Retorna a instância do banco de dados"""
    if MongoDB.database is None:
        raise Exception("MongoDB não foi inicializado. Chame connect_to_mongo() primeiro.")
    return MongoDB.database


async def ping_mongo() -> bool:
    """Verifica se o MongoDB está acessível"""
    try:
        # Se já temos uma conexão, usa ela
        if MongoDB.client is not None:
            await MongoDB.client.admin.command('ping')
            return True
        
        # Se não temos conexão, cria uma temporária para teste
        temp_client = AsyncIOMotorClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=5000
        )
        await temp_client.admin.command('ping')
        temp_client.close()
        return True
        
    except Exception as e:
        logger.error(f"Erro no ping do MongoDB: {e}")
        return False
