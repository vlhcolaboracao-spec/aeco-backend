"""
Router para operações CRUD de Clientes.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
import logging

from ..models.clientes import (
    Cliente, 
    ClienteCreate, 
    ClienteUpdate, 
    ClienteResponse, 
    ClienteListResponse
)
from ..repositories.clientes_repo import clientes_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=201)
async def criar_cliente(cliente_data: ClienteCreate):
    """Cria um novo cliente"""
    try:
        # Verifica se já existe cliente com o mesmo CPF/CNPJ (apenas se fornecido)
        if cliente_data.cpf_cnpj:
            cliente_existente = await clientes_repo.get_cliente_by_cpf_cnpj(cliente_data.cpf_cnpj)
            if cliente_existente:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um cliente cadastrado com este CPF/CNPJ"
                )
        
        cliente = await clientes_repo.create_cliente(cliente_data)
        
        return ClienteResponse(
            success=True,
            message="Cliente criado com sucesso",
            cliente=cliente
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar cliente: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar cliente: {str(e)}"
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def buscar_cliente(cliente_id: str):
    """Busca um cliente por ID"""
    try:
        cliente = await clientes_repo.get_cliente_by_id(cliente_id)
        
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
        
        return ClienteResponse(
            success=True,
            message="Cliente encontrado",
            cliente=cliente
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar cliente {cliente_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar cliente: {str(e)}"
        )


@router.get("/", response_model=ClienteListResponse)
async def listar_clientes(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: str = Query(None, description="Termo de busca")
):
    """Lista todos os clientes com paginação e busca opcional"""
    try:
        if search:
            clientes = await clientes_repo.search_clientes(search, skip=skip, limit=limit)
            total = len(clientes)  # Para busca, o total pode não ser preciso
        else:
            clientes = await clientes_repo.get_all_clientes(skip=skip, limit=limit)
            total = await clientes_repo.count_clientes()
        
        return ClienteListResponse(
            success=True,
            message=f"Encontrados {len(clientes)} clientes",
            clientes=clientes,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar clientes: {str(e)}"
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(cliente_id: str, cliente_data: ClienteUpdate):
    """Atualiza um cliente existente"""
    try:
        # Se está atualizando CPF/CNPJ, verifica se já existe outro cliente com o mesmo
        if cliente_data.cpf_cnpj:
            cliente_existente = await clientes_repo.get_cliente_by_cpf_cnpj(cliente_data.cpf_cnpj)
            if cliente_existente and str(cliente_existente.id) != cliente_id:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe outro cliente cadastrado com este CPF/CNPJ"
                )
        
        cliente = await clientes_repo.update_cliente(cliente_id, cliente_data)
        
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
        
        return ClienteResponse(
            success=True,
            message="Cliente atualizado com sucesso",
            cliente=cliente
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar cliente {cliente_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar cliente: {str(e)}"
        )


@router.delete("/{cliente_id}")
async def deletar_cliente(cliente_id: str):
    """Deleta um cliente"""
    try:
        deleted = await clientes_repo.delete_cliente(cliente_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
        
        return {
            "success": True,
            "message": f"Cliente {cliente_id} deletado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar cliente {cliente_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao deletar cliente: {str(e)}"
        )


@router.get("/stats/summary")
async def estatisticas_clientes():
    """Retorna estatísticas resumidas dos clientes"""
    try:
        total = await clientes_repo.count_clientes()
        
        # Busca alguns clientes recentes para estatísticas
        clientes_recentes = await clientes_repo.get_all_clientes(skip=0, limit=10)
        
        # Conta por estado
        estados = {}
        for cliente in clientes_recentes:
            if cliente.estado:
                estado = cliente.estado
                estados[estado] = estados.get(estado, 0) + 1
        
        # Conta por cidade
        cidades = {}
        for cliente in clientes_recentes:
            if cliente.cidade:
                cidade = cliente.cidade
                cidades[cidade] = cidades.get(cidade, 0) + 1
        
        return {
            "success": True,
            "message": "Estatísticas calculadas com sucesso",
            "data": {
                "total_clientes": total,
                "estados": estados,
                "cidades": cidades,
                "clientes_recentes": len(clientes_recentes)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao calcular estatísticas: {str(e)}"
        )
