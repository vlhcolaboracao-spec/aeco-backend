"""
Repositório para operações CRUD de Clientes.
"""
from typing import List, Optional
from datetime import datetime
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..models.clientes import ClienteCreate, ClienteUpdate, ClienteInDB
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


class ClientesRepository:
    """Repositório para operações de clientes"""
    
    def __init__(self):
        self.collection_name = "clientes"
    
    async def get_collection(self) -> AsyncIOMotorDatabase:
        """Obtém a coleção de clientes"""
        db = await get_database()
        return db[self.collection_name]
    
    async def create_cliente(self, cliente_data: ClienteCreate) -> ClienteInDB:
        """Cria um novo cliente"""
        try:
            collection = await self.get_collection()
            
            # Converte para dict e adiciona timestamps
            cliente_dict = cliente_data.model_dump()
            cliente_dict["created_at"] = datetime.now()
            cliente_dict["updated_at"] = datetime.now()
            
            # Insere no banco
            result = await collection.insert_one(cliente_dict)
            
            # Busca o cliente criado
            cliente_criado = await collection.find_one({"_id": result.inserted_id})
            
            return ClienteInDB(**cliente_criado)
            
        except Exception as e:
            logger.error(f"Erro ao criar cliente: {e}")
            raise
    
    async def get_cliente_by_id(self, cliente_id: str) -> Optional[ClienteInDB]:
        """Busca um cliente por ID"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(cliente_id):
                return None
            
            cliente = await collection.find_one({"_id": ObjectId(cliente_id)})
            
            if not cliente:
                return None
            
            return ClienteInDB(**cliente)
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente {cliente_id}: {e}")
            raise
    
    async def get_cliente_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[ClienteInDB]:
        """Busca um cliente por CPF/CNPJ"""
        try:
            collection = await self.get_collection()
            
            # Remove formatação do CPF/CNPJ para busca
            cpf_cnpj_clean = ''.join(filter(str.isdigit, cpf_cnpj))
            
            cliente = await collection.find_one({"cpf_cnpj": cpf_cnpj_clean})
            
            if not cliente:
                return None
            
            return ClienteInDB(**cliente)
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por CPF/CNPJ {cpf_cnpj}: {e}")
            raise
    
    async def get_all_clientes(self, skip: int = 0, limit: int = 100) -> List[ClienteInDB]:
        """Lista todos os clientes com paginação"""
        try:
            collection = await self.get_collection()
            
            cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
            clientes = []
            
            async for cliente in cursor:
                clientes.append(ClienteInDB(**cliente))
            
            return clientes
            
        except Exception as e:
            logger.error(f"Erro ao listar clientes: {e}")
            raise
    
    async def search_clientes(self, search_term: str, skip: int = 0, limit: int = 100) -> List[ClienteInDB]:
        """Busca clientes por termo"""
        try:
            collection = await self.get_collection()
            
            # Busca em múltiplos campos
            query = {
                "$or": [
                    {"nome_completo_razao_social": {"$regex": search_term, "$options": "i"}},
                    {"cpf_cnpj": {"$regex": search_term}},
                    {"email": {"$regex": search_term, "$options": "i"}},
                    {"telefone_principal": {"$regex": search_term}},
                    {"telefone_secundario": {"$regex": search_term}},
                    {"cidade": {"$regex": search_term, "$options": "i"}},
                    {"bairro": {"$regex": search_term, "$options": "i"}}
                ]
            }
            
            cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
            clientes = []
            
            async for cliente in cursor:
                clientes.append(ClienteInDB(**cliente))
            
            return clientes
            
        except Exception as e:
            logger.error(f"Erro ao buscar clientes: {e}")
            raise
    
    async def update_cliente(self, cliente_id: str, cliente_data: ClienteUpdate) -> Optional[ClienteInDB]:
        """Atualiza um cliente existente"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(cliente_id):
                return None
            
            # Remove campos None e adiciona timestamp de atualização
            update_data = cliente_data.model_dump(exclude_unset=True)
            if update_data:
                update_data["updated_at"] = datetime.now()
                
                result = await collection.update_one(
                    {"_id": ObjectId(cliente_id)},
                    {"$set": update_data}
                )
                
                if result.modified_count == 0:
                    return None
            
            # Busca o cliente atualizado
            return await self.get_cliente_by_id(cliente_id)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar cliente {cliente_id}: {e}")
            raise
    
    async def delete_cliente(self, cliente_id: str) -> bool:
        """Deleta um cliente"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(cliente_id):
                return False
            
            result = await collection.delete_one({"_id": ObjectId(cliente_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar cliente {cliente_id}: {e}")
            raise
    
    async def count_clientes(self) -> int:
        """Conta o total de clientes"""
        try:
            collection = await self.get_collection()
            return await collection.count_documents({})
            
        except Exception as e:
            logger.error(f"Erro ao contar clientes: {e}")
            raise


# Instância global do repositório
clientes_repo = ClientesRepository()
