"""
Repository para operações CRUD de Parâmetros Urbanísticos no MongoDB.
"""
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ..models.parametros_urbanisticos import (
    ParametrosUrbanisticosCreate, 
    ParametrosUrbanisticosUpdate, 
    ParametrosUrbanisticosInDB
)
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


class ParametrosUrbanisticosRepository:
    """Repository para gerenciar parâmetros urbanísticos no MongoDB"""
    
    def __init__(self):
        self.collection_name = "param_urb_terrenos"
    
    async def get_collection(self):
        """Retorna a coleção de parâmetros urbanísticos"""
        db = await get_database()
        return db[self.collection_name]
    
    async def create_parametros(self, parametros_data: ParametrosUrbanisticosCreate) -> ParametrosUrbanisticosInDB:
        """Cria novos parâmetros urbanísticos"""
        try:
            collection = await self.get_collection()
            
            # Converte para dict e adiciona timestamps
            parametros_dict = parametros_data.dict()
            from datetime import datetime
            parametros_dict["created_at"] = parametros_dict["updated_at"] = datetime.now()
            
            result = await collection.insert_one(parametros_dict)
            
            # Busca os parâmetros criados
            created_parametros = await collection.find_one({"_id": result.inserted_id})
            return ParametrosUrbanisticosInDB(**created_parametros)
            
        except Exception as e:
            logger.error(f"Erro ao criar parâmetros urbanísticos: {e}")
            raise
    
    async def get_parametros_by_terreno_id(self, terreno_id: str) -> Optional[ParametrosUrbanisticosInDB]:
        """Busca parâmetros por ID do terreno"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(terreno_id):
                return None
            
            parametros = await collection.find_one({
                "terreno_id": ObjectId(terreno_id),
                "status": "ativo"
            })
            
            if parametros:
                return ParametrosUrbanisticosInDB(**parametros)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar parâmetros para terreno {terreno_id}: {e}")
            raise
    
    async def get_parametros_by_id(self, parametros_id: str) -> Optional[ParametrosUrbanisticosInDB]:
        """Busca parâmetros por ID próprio"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(parametros_id):
                return None
            
            parametros = await collection.find_one({"_id": ObjectId(parametros_id)})
            
            if parametros:
                return ParametrosUrbanisticosInDB(**parametros)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar parâmetros {parametros_id}: {e}")
            raise
    
    async def get_all_parametros(self, skip: int = 0, limit: int = 100) -> List[ParametrosUrbanisticosInDB]:
        """Lista todos os parâmetros com paginação"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find({"status": "ativo"}).skip(skip).limit(limit).sort("created_at", -1)
            parametros = []
            
            async for param in cursor:
                parametros.append(ParametrosUrbanisticosInDB(**param))
            
            return parametros
            
        except Exception as e:
            logger.error(f"Erro ao listar parâmetros: {e}")
            raise
    
    async def update_parametros(self, parametros_id: str, parametros_data: ParametrosUrbanisticosUpdate) -> Optional[ParametrosUrbanisticosInDB]:
        """Atualiza parâmetros urbanísticos"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(parametros_id):
                return None
            
            # Remove campos None do update
            update_data = {k: v for k, v in parametros_data.dict().items() if v is not None}
            
            if not update_data:
                # Se não há dados para atualizar, busca os parâmetros atuais
                return await self.get_parametros_by_id(parametros_id)
            
            from datetime import datetime
            update_data["updated_at"] = datetime.now()
            
            result = await collection.update_one(
                {"_id": ObjectId(parametros_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_parametros_by_id(parametros_id)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar parâmetros {parametros_id}: {e}")
            raise
    
    async def delete_parametros(self, parametros_id: str) -> bool:
        """Soft delete dos parâmetros (marca como inativo)"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(parametros_id):
                return False
            
            from datetime import datetime
            result = await collection.update_one(
                {"_id": ObjectId(parametros_id)},
                {"$set": {"status": "inativo", "updated_at": datetime.now()}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar parâmetros {parametros_id}: {e}")
            raise
    
    async def count_parametros(self) -> int:
        """Conta o total de parâmetros ativos"""
        try:
            collection = await self.get_collection()
            return await collection.count_documents({"status": "ativo"})
            
        except Exception as e:
            logger.error(f"Erro ao contar parâmetros: {e}")
            raise
    
    async def search_parametros_by_municipio(self, municipio: str, skip: int = 0, limit: int = 100) -> List[ParametrosUrbanisticosInDB]:
        """Busca parâmetros por município"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find({
                "municipio": municipio.upper(),
                "status": "ativo"
            }).skip(skip).limit(limit).sort("created_at", -1)
            
            parametros = []
            async for param in cursor:
                parametros.append(ParametrosUrbanisticosInDB(**param))
            
            return parametros
            
        except Exception as e:
            logger.error(f"Erro ao buscar parâmetros por município {municipio}: {e}")
            raise
    
    async def get_parametros_by_zona(self, zona: str, skip: int = 0, limit: int = 100) -> List[ParametrosUrbanisticosInDB]:
        """Busca parâmetros por zona (através do terreno relacionado)"""
        try:
            collection = await self.get_collection()
            
            # Agregação para buscar parâmetros de terrenos com zona específica
            pipeline = [
                {
                    "$lookup": {
                        "from": "formulario_terrenos_projetos",
                        "localField": "terreno_id",
                        "foreignField": "_id",
                        "as": "terreno"
                    }
                },
                {
                    "$match": {
                        "terreno.zona": zona.upper(),
                        "status": "ativo"
                    }
                },
                {
                    "$sort": {"created_at": -1}
                },
                {
                    "$skip": skip
                },
                {
                    "$limit": limit
                }
            ]
            
            parametros = []
            async for doc in collection.aggregate(pipeline):
                parametros.append(ParametrosUrbanisticosInDB(**doc))
            
            return parametros
            
        except Exception as e:
            logger.error(f"Erro ao buscar parâmetros por zona {zona}: {e}")
            raise
    
    async def recalcular_parametros(self, terreno_id: str, dados_calculo) -> Optional[ParametrosUrbanisticosInDB]:
        """
        Recalcula parâmetros para um terreno existente
        """
        try:
            # Primeiro, busca os parâmetros existentes
            parametros_existentes = await self.get_parametros_by_terreno_id(terreno_id)
            
            if not parametros_existentes:
                return None
            
            # Importa o service aqui para evitar import circular
            from ..services.parametros_urbanisticos_service import parametros_service
            
            # Calcula novos parâmetros
            novos_parametros = await parametros_service.calcular_todos_parametros(dados_calculo)
            
            # Atualiza apenas os campos de parâmetros
            update_data = ParametrosUrbanisticosUpdate(**novos_parametros)
            
            return await self.update_parametros(str(parametros_existentes.id), update_data)
            
        except Exception as e:
            logger.error(f"Erro ao recalcular parâmetros para terreno {terreno_id}: {e}")
            raise


# Instância global do repository
parametros_urbanisticos_repo = ParametrosUrbanisticosRepository()
