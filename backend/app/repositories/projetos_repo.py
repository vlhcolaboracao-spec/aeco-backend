"""
Repository para operações CRUD de Projetos no MongoDB.
"""
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ..models.projeto import ProjetoCreate, ProjetoUpdate, ProjetoInDB
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


class ProjetosRepository:
    """Repository para gerenciar projetos no MongoDB"""
    
    def __init__(self):
        self.collection_name = "projetos"
    
    async def get_collection(self):
        """Retorna a coleção de projetos"""
        db = await get_database()
        return db[self.collection_name]
    
    async def create_projeto(self, projeto_data: ProjetoCreate) -> ProjetoInDB:
        """Cria um novo projeto"""
        try:
            collection = await self.get_collection()
            
            # Converte para dict e adiciona timestamps
            projeto_dict = projeto_data.dict()
            projeto_dict["created_at"] = projeto_dict["updated_at"] = projeto_dict.get("created_at")
            
            result = await collection.insert_one(projeto_dict)
            
            # Busca o projeto criado
            created_projeto = await collection.find_one({"_id": result.inserted_id})
            return ProjetoInDB(**created_projeto)
            
        except Exception as e:
            logger.error(f"Erro ao criar projeto: {e}")
            raise
    
    async def get_projeto_by_id(self, projeto_id: str) -> Optional[ProjetoInDB]:
        """Busca projeto por ID"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(projeto_id):
                return None
            
            projeto = await collection.find_one({"_id": ObjectId(projeto_id)})
            
            if projeto:
                return ProjetoInDB(**projeto)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar projeto {projeto_id}: {e}")
            raise
    
    async def get_all_projetos(self, skip: int = 0, limit: int = 100) -> List[ProjetoInDB]:
        """Lista todos os projetos com paginação"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
            projetos = []
            
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao listar projetos: {e}")
            raise
    
    async def update_projeto(self, projeto_id: str, projeto_data: ProjetoUpdate) -> Optional[ProjetoInDB]:
        """Atualiza um projeto"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(projeto_id):
                return None
            
            # Remove campos None do update
            update_data = {k: v for k, v in projeto_data.dict().items() if v is not None}
            
            if not update_data:
                # Se não há dados para atualizar, busca o projeto atual
                return await self.get_projeto_by_id(projeto_id)
            
            update_data["updated_at"] = update_data.get("updated_at")
            
            result = await collection.update_one(
                {"_id": ObjectId(projeto_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_projeto_by_id(projeto_id)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar projeto {projeto_id}: {e}")
            raise
    
    async def delete_projeto(self, projeto_id: str) -> bool:
        """Deleta um projeto"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(projeto_id):
                return False
            
            result = await collection.delete_one({"_id": ObjectId(projeto_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar projeto {projeto_id}: {e}")
            raise
    
    async def count_projetos(self) -> int:
        """Conta o total de projetos"""
        try:
            collection = await self.get_collection()
            return await collection.count_documents({})
            
        except Exception as e:
            logger.error(f"Erro ao contar projetos: {e}")
            raise


# Instância global do repository
projetos_repo = ProjetosRepository()
