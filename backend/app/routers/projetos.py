"""
Router para operações CRUD de Projetos.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
import logging

from ..models.projeto import (
    Projeto, ProjetoCreate, ProjetoUpdate, 
    ProjetoResponse, ProjetosListResponse
)
from ..repositories.projetos_repo import projetos_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projetos", tags=["projetos"])


@router.post("/", response_model=ProjetoResponse, status_code=201)
async def criar_projeto(projeto_data: ProjetoCreate):
    """Cria um novo projeto"""
    try:
        projeto = await projetos_repo.create_projeto(projeto_data)
        
        return ProjetoResponse(
            success=True,
            message="Projeto criado com sucesso",
            projeto=projeto
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar projeto: {str(e)}"
        )


@router.get("/{projeto_id}", response_model=ProjetoResponse)
async def buscar_projeto(projeto_id: str):
    """Busca um projeto por ID"""
    try:
        projeto = await projetos_repo.get_projeto_by_id(projeto_id)
        
        if not projeto:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com ID {projeto_id} não encontrado"
            )
        
        return ProjetoResponse(
            success=True,
            message="Projeto encontrado",
            projeto=projeto
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar projeto {projeto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar projeto: {str(e)}"
        )


@router.get("/", response_model=ProjetosListResponse)
async def listar_projetos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros")
):
    """Lista todos os projetos com paginação"""
    try:
        projetos = await projetos_repo.get_all_projetos(skip=skip, limit=limit)
        total = await projetos_repo.count_projetos()
        
        return ProjetosListResponse(
            success=True,
            message=f"Encontrados {len(projetos)} projetos",
            projetos=projetos,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar projetos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar projetos: {str(e)}"
        )


@router.put("/{projeto_id}", response_model=ProjetoResponse)
async def atualizar_projeto(projeto_id: str, projeto_data: ProjetoUpdate):
    """Atualiza um projeto existente"""
    try:
        projeto = await projetos_repo.update_projeto(projeto_id, projeto_data)
        
        if not projeto:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com ID {projeto_id} não encontrado"
            )
        
        return ProjetoResponse(
            success=True,
            message="Projeto atualizado com sucesso",
            projeto=projeto
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar projeto {projeto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar projeto: {str(e)}"
        )


@router.delete("/{projeto_id}")
async def deletar_projeto(projeto_id: str):
    """Deleta um projeto"""
    try:
        deleted = await projetos_repo.delete_projeto(projeto_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com ID {projeto_id} não encontrado"
            )
        
        return {
            "success": True,
            "message": f"Projeto {projeto_id} deletado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar projeto {projeto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao deletar projeto: {str(e)}"
        )
