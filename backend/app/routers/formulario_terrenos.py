"""
Router para operações CRUD de Formulário de Terrenos de Projetos.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
import logging

from ..models.formulario_terrenos_projetos import (
    FormularioTerrenosProjetos, 
    FormularioTerrenosProjetosCreate, 
    FormularioTerrenosProjetosUpdate, 
    FormularioTerrenosProjetosResponse, 
    FormularioTerrenosProjetosListResponse
)
from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/formulario-terrenos-projetos", tags=["formulario-terrenos-projetos"])


@router.post("/", response_model=FormularioTerrenosProjetosResponse, status_code=201)
async def criar_terreno(terreno_data: FormularioTerrenosProjetosCreate):
    """Cria um novo terreno de projeto"""
    try:
        terreno = await formulario_terrenos_repo.create_terreno(terreno_data)
        
        return FormularioTerrenosProjetosResponse(
            success=True,
            message="Terreno criado com sucesso",
            terreno=terreno
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar terreno: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar terreno: {str(e)}"
        )


@router.get("/{terreno_id}", response_model=FormularioTerrenosProjetosResponse)
async def buscar_terreno(terreno_id: str):
    """Busca um terreno por ID"""
    try:
        terreno = await formulario_terrenos_repo.get_terreno_by_id(terreno_id)
        
        if not terreno:
            raise HTTPException(
                status_code=404,
                detail=f"Terreno com ID {terreno_id} não encontrado"
            )
        
        return FormularioTerrenosProjetosResponse(
            success=True,
            message="Terreno encontrado",
            terreno=terreno
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar terreno: {str(e)}"
        )


@router.get("/", response_model=FormularioTerrenosProjetosListResponse)
async def listar_terrenos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: str = Query(None, description="Termo de busca")
):
    """Lista todos os terrenos com paginação e busca opcional"""
    try:
        if search:
            terrenos = await formulario_terrenos_repo.search_terrenos(search, skip=skip, limit=limit)
            total = len(terrenos)  # Para busca, o total pode não ser preciso
        else:
            terrenos = await formulario_terrenos_repo.get_all_terrenos(skip=skip, limit=limit)
            total = await formulario_terrenos_repo.count_terrenos()
        
        return FormularioTerrenosProjetosListResponse(
            success=True,
            message=f"Encontrados {len(terrenos)} terrenos",
            terrenos=terrenos,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar terrenos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar terrenos: {str(e)}"
        )


@router.put("/{terreno_id}", response_model=FormularioTerrenosProjetosResponse)
async def atualizar_terreno(terreno_id: str, terreno_data: FormularioTerrenosProjetosUpdate):
    """Atualiza um terreno existente"""
    try:
        terreno = await formulario_terrenos_repo.update_terreno(terreno_id, terreno_data)
        
        if not terreno:
            raise HTTPException(
                status_code=404,
                detail=f"Terreno com ID {terreno_id} não encontrado"
            )
        
        return FormularioTerrenosProjetosResponse(
            success=True,
            message="Terreno atualizado com sucesso",
            terreno=terreno
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar terreno: {str(e)}"
        )


@router.delete("/{terreno_id}")
async def deletar_terreno(terreno_id: str):
    """Deleta um terreno"""
    try:
        deleted = await formulario_terrenos_repo.delete_terreno(terreno_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Terreno com ID {terreno_id} não encontrado"
            )
        
        return {
            "success": True,
            "message": f"Terreno {terreno_id} deletado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao deletar terreno: {str(e)}"
        )


@router.get("/stats/summary")
async def estatisticas_terrenos():
    """Retorna estatísticas resumidas dos terrenos"""
    try:
        total = await formulario_terrenos_repo.count_terrenos()
        
        # Busca alguns terrenos recentes para estatísticas
        terrenos_recentes = await formulario_terrenos_repo.get_all_terrenos(skip=0, limit=10)
        
        # Calcula área total
        area_total = sum(terreno.area for terreno in terrenos_recentes)
        
        # Conta por tipo de lote
        tipos_lote = {}
        for terreno in terrenos_recentes:
            tipo = terreno.tipo_lote
            tipos_lote[tipo] = tipos_lote.get(tipo, 0) + 1
        
        return {
            "success": True,
            "message": "Estatísticas calculadas com sucesso",
            "data": {
                "total_terrenos": total,
                "area_total_m2": round(area_total, 2),
                "tipos_lote": tipos_lote,
                "terrenos_recentes": len(terrenos_recentes)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao calcular estatísticas: {str(e)}"
        )
