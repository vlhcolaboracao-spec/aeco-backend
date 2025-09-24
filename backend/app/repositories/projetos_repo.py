"""
Repository para operações CRUD de Projetos no MongoDB.
"""
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ..models.projeto import (
    ProjetoCreate, 
    ProjetoUpdate, 
    ProjetoInDB
)
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
            from datetime import datetime
            projeto_dict["created_at"] = projeto_dict["updated_at"] = datetime.now()
            
            # Gera código do projeto se não fornecido
            if not projeto_dict.get("cod_projeto"):
                from ..utils.codigo_projeto import gerar_codigo_projeto_unico
                projeto_dict["cod_projeto"] = await gerar_codigo_projeto_unico()
            
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
    
    async def get_projeto_by_cod_projeto(self, cod_projeto: str) -> Optional[ProjetoInDB]:
        """Busca projeto por código do projeto"""
        try:
            collection = await self.get_collection()
            
            # Normaliza o código (remove formatação se houver)
            codigo_normalizado = cod_projeto.replace('-', '').upper()
            
            projeto = await collection.find_one({"cod_projeto": codigo_normalizado})
            
            if projeto:
                return ProjetoInDB(**projeto)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar projeto por código {cod_projeto}: {e}")
            raise
    
    async def get_projetos_by_cliente_id(self, cliente_id: str) -> List[ProjetoInDB]:
        """Busca projetos por ID do cliente"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(cliente_id):
                return []
            
            cursor = collection.find({"cliente_id": ObjectId(cliente_id)}).sort("created_at", -1)
            projetos = []
            
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao buscar projetos do cliente {cliente_id}: {e}")
            raise
    
    async def get_projetos_by_terreno_id(self, terreno_id: str) -> List[ProjetoInDB]:
        """Busca projetos por ID do terreno"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(terreno_id):
                return []
            
            cursor = collection.find({"terreno_id": ObjectId(terreno_id)}).sort("created_at", -1)
            projetos = []
            
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao buscar projetos do terreno {terreno_id}: {e}")
            raise
    
    async def get_all_projetos(self, skip: int = 0, limit: int = 100) -> List[ProjetoInDB]:
        """Lista todos os projetos com paginação"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find({"status": "ativo"}).skip(skip).limit(limit).sort("created_at", -1)
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
            
            from datetime import datetime
            update_data["updated_at"] = datetime.now()
            
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
        """Soft delete do projeto (marca como inativo)"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(projeto_id):
                return False
            
            from datetime import datetime
            result = await collection.update_one(
                {"_id": ObjectId(projeto_id)},
                {"$set": {"status": "inativo", "updated_at": datetime.now()}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar projeto {projeto_id}: {e}")
            raise
    
    async def count_projetos(self) -> int:
        """Conta o total de projetos ativos"""
        try:
            collection = await self.get_collection()
            return await collection.count_documents({"status": "ativo"})
            
        except Exception as e:
            logger.error(f"Erro ao contar projetos: {e}")
            raise
    
    async def search_projetos(self, query: str, skip: int = 0, limit: int = 100) -> List[ProjetoInDB]:
        """Busca projetos por texto (nome, código, descrição)"""
        try:
            collection = await self.get_collection()
            
            # Cria índice de texto se não existir
            await collection.create_index([
                ("nome_projeto", "text"),
                ("cod_projeto", "text"),
                ("descricao", "text")
            ])
            
            # Busca por texto
            search_filter = {"$text": {"$search": query}, "status": "ativo"}
            cursor = collection.find(search_filter).skip(skip).limit(limit).sort("created_at", -1)
            
            projetos = []
            async for projeto in cursor:
                projetos.append(ProjetoInDB(**projeto))
            
            return projetos
            
        except Exception as e:
            logger.error(f"Erro ao buscar projetos: {e}")
            raise
    
    async def get_projeto_com_dados_completos(self, projeto_id: str) -> Optional[dict]:
        """Busca projeto com dados relacionados (cliente, terreno, parâmetros)"""
        try:
            projeto = await self.get_projeto_by_id(projeto_id)
            if not projeto:
                return None
            
            resultado = {"projeto": projeto.dict()}
            
            # Busca dados do cliente se associado
            if projeto.cliente_id:
                try:
                    from ..repositories.clientes_repo import clientes_repo
                    cliente = await clientes_repo.get_cliente_by_id(projeto.cliente_id)
                    if cliente:
                        resultado["cliente"] = cliente.dict()
                except Exception as e:
                    logger.warning(f"Erro ao buscar cliente {projeto.cliente_id}: {e}")
            
            # Busca dados do terreno se associado
            if projeto.terreno_id:
                try:
                    from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
                    terreno = await formulario_terrenos_repo.get_terreno_by_id(projeto.terreno_id)
                    if terreno:
                        resultado["terreno"] = terreno.dict()
                        
                        # Busca parâmetros urbanísticos
                        try:
                            from ..repositories.parametros_urbanisticos_repo import parametros_urbanisticos_repo
                            parametros = await parametros_urbanisticos_repo.get_parametros_by_terreno_id(projeto.terreno_id)
                            if parametros:
                                resultado["parametros_urbanisticos"] = parametros.dict()
                        except Exception as e:
                            logger.warning(f"Erro ao buscar parâmetros do terreno {projeto.terreno_id}: {e}")
                except Exception as e:
                    logger.warning(f"Erro ao buscar terreno {projeto.terreno_id}: {e}")
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao buscar projeto completo {projeto_id}: {e}")
            raise


# Instância global do repository
projetos_repo = ProjetosRepository()