"""
Repository para operações CRUD de Formulário de Terrenos de Projetos no MongoDB.
"""
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ..models.formulario_terrenos_projetos import (
    FormularioTerrenosProjetosCreate, 
    FormularioTerrenosProjetosUpdate, 
    FormularioTerrenosProjetosInDB
)
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


class FormularioTerrenosRepository:
    """Repository para gerenciar terrenos no MongoDB"""
    
    def __init__(self):
        self.collection_name = "formulario_terrenos_projetos"
    
    async def get_collection(self):
        """Retorna a coleção de terrenos"""
        db = await get_database()
        return db[self.collection_name]
    
    async def create_terreno(self, terreno_data: FormularioTerrenosProjetosCreate) -> FormularioTerrenosProjetosInDB:
        """Cria um novo terreno e calcula automaticamente os parâmetros urbanísticos"""
        try:
            collection = await self.get_collection()
            
            # Converte para dict e adiciona timestamps
            terreno_dict = terreno_data.dict()
            from datetime import datetime
            terreno_dict["created_at"] = terreno_dict["updated_at"] = datetime.now()
            
            result = await collection.insert_one(terreno_dict)
            
            # Busca o terreno criado
            created_terreno = await collection.find_one({"_id": result.inserted_id})
            terreno_obj = FormularioTerrenosProjetosInDB(**created_terreno)
            
            # Calcula automaticamente os parâmetros urbanísticos
            try:
                await self._calcular_parametros_urbanisticos(terreno_obj)
            except Exception as calc_error:
                logger.warning(f"Erro ao calcular parâmetros urbanísticos para terreno {terreno_obj.id}: {calc_error}")
                # Não falha o cadastro do terreno se houver erro no cálculo dos parâmetros
            
            return terreno_obj
            
        except Exception as e:
            logger.error(f"Erro ao criar terreno: {e}")
            raise
    
    async def _calcular_parametros_urbanisticos(self, terreno: FormularioTerrenosProjetosInDB):
        """Calcula e salva os parâmetros urbanísticos para um terreno"""
        try:
            # Importa aqui para evitar import circular
            from ..models.parametros_urbanisticos import ParametrosUrbanisticosCreate, DadosCalculoParametros
            from ..repositories.parametros_urbanisticos_repo import parametros_urbanisticos_repo
            from ..services.parametros_urbanisticos_service import parametros_service
            
            # Prepara dados para cálculo
            dados_calculo = DadosCalculoParametros(
                zona=terreno.zona,
                tipologia=terreno.tipologia,
                municipio=terreno.municipio
            )
            
            # Calcula todos os parâmetros
            parametros_calculados = await parametros_service.calcular_todos_parametros(dados_calculo)
            
            # Cria o documento de parâmetros urbanísticos
            parametros_data = ParametrosUrbanisticosCreate(
                terreno_id=terreno.id,
                municipio=terreno.municipio,
                legislacao="LC_108_2009_ALTERADA_LC_415_2023",
                **parametros_calculados
            )
            
            # Salva no banco
            await parametros_urbanisticos_repo.create_parametros(parametros_data)
            
            logger.info(f"Parâmetros urbanísticos calculados e salvos para terreno {terreno.id}")
            
        except Exception as e:
            logger.error(f"Erro ao calcular parâmetros urbanísticos: {e}")
            raise
    
    async def get_terreno_by_id(self, terreno_id: str) -> Optional[FormularioTerrenosProjetosInDB]:
        """Busca terreno por ID"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(terreno_id):
                return None
            
            terreno = await collection.find_one({"_id": ObjectId(terreno_id)})
            
            if terreno:
                return FormularioTerrenosProjetosInDB(**terreno)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar terreno {terreno_id}: {e}")
            raise
    
    async def get_all_terrenos(self, skip: int = 0, limit: int = 100) -> List[FormularioTerrenosProjetosInDB]:
        """Lista todos os terrenos com paginação"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
            terrenos = []
            
            async for terreno in cursor:
                terrenos.append(FormularioTerrenosProjetosInDB(**terreno))
            
            return terrenos
            
        except Exception as e:
            logger.error(f"Erro ao listar terrenos: {e}")
            raise
    
    async def update_terreno(self, terreno_id: str, terreno_data: FormularioTerrenosProjetosUpdate) -> Optional[FormularioTerrenosProjetosInDB]:
        """Atualiza um terreno"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(terreno_id):
                return None
            
            # Remove campos None do update
            update_data = {k: v for k, v in terreno_data.dict().items() if v is not None}
            
            if not update_data:
                # Se não há dados para atualizar, busca o terreno atual
                return await self.get_terreno_by_id(terreno_id)
            
            update_data["updated_at"] = update_data.get("updated_at")
            
            result = await collection.update_one(
                {"_id": ObjectId(terreno_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_terreno_by_id(terreno_id)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar terreno {terreno_id}: {e}")
            raise
    
    async def delete_terreno(self, terreno_id: str) -> bool:
        """Deleta um terreno"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(terreno_id):
                return False
            
            result = await collection.delete_one({"_id": ObjectId(terreno_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar terreno {terreno_id}: {e}")
            raise
    
    async def count_terrenos(self) -> int:
        """Conta o total de terrenos"""
        try:
            collection = await self.get_collection()
            return await collection.count_documents({})
            
        except Exception as e:
            logger.error(f"Erro ao contar terrenos: {e}")
            raise
    
    async def search_terrenos(self, query: str, skip: int = 0, limit: int = 100) -> List[FormularioTerrenosProjetosInDB]:
        """Busca terrenos por texto (matrícula, município, bairro)"""
        try:
            collection = await self.get_collection()
            
            # Cria índice de texto se não existir
            await collection.create_index([
                ("matricula", "text"),
                ("municipio", "text"),
                ("bairro", "text"),
                ("logradouro", "text")
            ])
            
            # Busca por texto
            search_filter = {"$text": {"$search": query}}
            cursor = collection.find(search_filter).skip(skip).limit(limit).sort("created_at", -1)
            
            terrenos = []
            async for terreno in cursor:
                terrenos.append(FormularioTerrenosProjetosInDB(**terreno))
            
            return terrenos
            
        except Exception as e:
            logger.error(f"Erro ao buscar terrenos: {e}")
            raise


# Instância global do repository
formulario_terrenos_repo = FormularioTerrenosRepository()
