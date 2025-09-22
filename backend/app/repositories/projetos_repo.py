"""
Repositório para operações de projetos no MongoDB.
"""
import logging
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from ..models.projeto import ProjetoCreate, ProjetoUpdate, ProjetoInDB
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


class ProjetosRepository:
    """Repositório para operações de projetos"""
    
    def __init__(self):
        self.collection_name = "projetos"
    
    async def get_collection(self):
        """Retorna a coleção de projetos"""
        database = await get_database()
        return database[self.collection_name]
    
    async def create_projeto(self, projeto_data: ProjetoCreate) -> ProjetoInDB:
        """
        Cria um novo projeto no banco de dados.
        
        Args:
            projeto_data: Dados do projeto a ser criado
            
        Returns:
            ProjetoInDB: Projeto criado com ID e timestamps
        """
        try:
            collection = await self.get_collection()
            
            # Converte para dict e adiciona timestamps
            projeto_dict = projeto_data.model_dump()
            projeto_dict["created_at"] = datetime.now()
            projeto_dict["updated_at"] = datetime.now()
            
            # Remove campos None para economizar espaço
            projeto_dict = {k: v for k, v in projeto_dict.items() if v is not None}
            
            result = await collection.insert_one(projeto_dict)
            
            # Busca o projeto criado
            created_projeto = await collection.find_one({"_id": result.inserted_id})
            
            if created_projeto:
                return ProjetoInDB(**created_projeto)
            else:
                raise Exception("Erro ao criar projeto: não foi possível recuperar dados após inserção")
                
        except Exception as e:
            logger.error(f"Erro ao criar projeto: {str(e)}")
            raise Exception(f"Erro ao criar projeto: {str(e)}")
    
    async def get_projeto_by_id(self, projeto_id: str) -> Optional[ProjetoInDB]:
        """
        Busca um projeto pelo ID.
        
        Args:
            projeto_id: ID do projeto
            
        Returns:
            ProjetoInDB ou None se não encontrado
        """
        try:
            if not ObjectId.is_valid(projeto_id):
                return None
            
            collection = await self.get_collection()
            projeto = await collection.find_one({"_id": ObjectId(projeto_id)})
            
            if projeto:
                return ProjetoInDB(**projeto)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar projeto por ID {projeto_id}: {str(e)}")
            return None
    
    async def get_all_projetos(self, skip: int = 0, limit: int = 100) -> List[ProjetoInDB]:
        """
        Lista todos os projetos com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Limite de registros por página
            
        Returns:
            Lista de ProjetoInDB
        """
        try:
            collection = await self.get_collection()
            cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
            projetos = []
            
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao listar projetos: {str(e)}")
            return []
    
    async def update_projeto(self, projeto_id: str, projeto_data: ProjetoUpdate) -> Optional[ProjetoInDB]:
        """
        Atualiza um projeto existente.
        
        Args:
            projeto_id: ID do projeto
            projeto_data: Dados para atualização
            
        Returns:
            ProjetoInDB atualizado ou None se não encontrado
        """
        try:
            if not ObjectId.is_valid(projeto_id):
                return None
            
            collection = await self.get_collection()
            
            # Remove campos None e adiciona timestamp de atualização
            update_data = projeto_data.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.now()
            
            # Remove campos None
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not update_data:
                return await self.get_projeto_by_id(projeto_id)
            
            result = await collection.update_one(
                {"_id": ObjectId(projeto_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_projeto_by_id(projeto_id)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar projeto {projeto_id}: {str(e)}")
            return None
    
    async def delete_projeto(self, projeto_id: str) -> bool:
        """
        Remove um projeto do banco de dados.
        
        Args:
            projeto_id: ID do projeto
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            if not ObjectId.is_valid(projeto_id):
                return False
            
            collection = await self.get_collection()
            result = await collection.delete_one({"_id": ObjectId(projeto_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar projeto {projeto_id}: {str(e)}")
            return False
    
    async def count_projetos(self) -> int:
        """
        Conta o total de projetos no banco.
        
        Returns:
            Número total de projetos
        """
        try:
            collection = await self.get_collection()
            return await collection.count_documents({})
        except Exception as e:
            logger.error(f"Erro ao contar projetos: {str(e)}")
            return 0
    
    async def search_projetos(self, query: str, skip: int = 0, limit: int = 100) -> List[ProjetoInDB]:
        """
        Busca projetos por texto.
        
        Args:
            query: Termo de busca
            skip: Número de registros para pular
            limit: Limite de registros por página
            
        Returns:
            Lista de projetos encontrados
        """
        try:
            collection = await self.get_collection()
            search_filter = {
                "$or": [
                    {"nome_completo": {"$regex": query, "$options": "i"}},
                    {"contato": {"$regex": query, "$options": "i"}},
                    {"tipologia": {"$regex": query, "$options": "i"}},
                    {"estilo_arquitetonico": {"$regex": query, "$options": "i"}},
                    {"desejos_expectativas": {"$regex": query, "$options": "i"}}
                ]
            }
            
            cursor = collection.find(search_filter).skip(skip).limit(limit).sort("created_at", -1)
            projetos = []
            
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao buscar projetos: {str(e)}")
            return []


# Instância global do repositório
projetos_repo = ProjetosRepository()
