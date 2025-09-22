"""
Router para operações CRUD de Parâmetros Urbanísticos.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query, Path
import logging

from ..models.parametros_urbanisticos import (
    ParametrosUrbanisticos, 
    ParametrosUrbanisticosCreate, 
    ParametrosUrbanisticosUpdate, 
    ParametrosUrbanisticosResponse, 
    ParametrosUrbanisticosListResponse,
    DadosCalculoParametros
)
from ..repositories.parametros_urbanisticos_repo import parametros_urbanisticos_repo
from ..services.parametros_urbanisticos_service import parametros_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/parametros-urbanisticos", tags=["parametros-urbanisticos"])


@router.post("/", response_model=ParametrosUrbanisticosResponse, status_code=201)
async def criar_parametros(parametros_data: ParametrosUrbanisticosCreate):
    """Cria novos parâmetros urbanísticos"""
    try:
        parametros = await parametros_urbanisticos_repo.create_parametros(parametros_data)
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos criados com sucesso",
            parametros=parametros
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar parâmetros urbanísticos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar parâmetros: {str(e)}"
        )


@router.get("/terreno/{terreno_id}", response_model=ParametrosUrbanisticosResponse)
async def get_parametros_by_terreno(
    terreno_id: str = Path(..., description="ID do terreno")
):
    """Busca parâmetros urbanísticos por ID do terreno"""
    try:
        parametros = await parametros_urbanisticos_repo.get_parametros_by_terreno_id(terreno_id)
        
        if not parametros:
            raise HTTPException(
                status_code=404,
                detail="Parâmetros urbanísticos não encontrados para este terreno"
            )
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos encontrados",
            parametros=parametros
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetros para terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetros: {str(e)}"
        )


@router.get("/{parametros_id}", response_model=ParametrosUrbanisticosResponse)
async def get_parametros_by_id(
    parametros_id: str = Path(..., description="ID dos parâmetros")
):
    """Busca parâmetros urbanísticos por ID próprio"""
    try:
        parametros = await parametros_urbanisticos_repo.get_parametros_by_id(parametros_id)
        
        if not parametros:
            raise HTTPException(
                status_code=404,
                detail="Parâmetros urbanísticos não encontrados"
            )
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos encontrados",
            parametros=parametros
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetros {parametros_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetros: {str(e)}"
        )


@router.get("/", response_model=ParametrosUrbanisticosListResponse)
async def listar_parametros(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar")
):
    """Lista todos os parâmetros urbanísticos com paginação"""
    try:
        parametros = await parametros_urbanisticos_repo.get_all_parametros(skip=skip, limit=limit)
        total = await parametros_urbanisticos_repo.count_parametros()
        
        return ParametrosUrbanisticosListResponse(
            success=True,
            message=f"Encontrados {len(parametros)} parâmetros urbanísticos",
            parametros=parametros,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar parâmetros: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar parâmetros: {str(e)}"
        )


@router.put("/{parametros_id}", response_model=ParametrosUrbanisticosResponse)
async def atualizar_parametros(
    parametros_id: str,
    parametros_data: ParametrosUrbanisticosUpdate
):
    """Atualiza parâmetros urbanísticos"""
    try:
        parametros = await parametros_urbanisticos_repo.update_parametros(parametros_id, parametros_data)
        
        if not parametros:
            raise HTTPException(
                status_code=404,
                detail="Parâmetros urbanísticos não encontrados"
            )
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos atualizados com sucesso",
            parametros=parametros
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar parâmetros {parametros_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar parâmetros: {str(e)}"
        )


@router.delete("/{parametros_id}", response_model=ParametrosUrbanisticosResponse)
async def deletar_parametros(
    parametros_id: str = Path(..., description="ID dos parâmetros")
):
    """Deleta parâmetros urbanísticos (soft delete)"""
    try:
        success = await parametros_urbanisticos_repo.delete_parametros(parametros_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Parâmetros urbanísticos não encontrados"
            )
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos deletados com sucesso"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar parâmetros {parametros_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao deletar parâmetros: {str(e)}"
        )


@router.get("/municipio/{municipio}", response_model=ParametrosUrbanisticosListResponse)
async def buscar_parametros_por_municipio(
    municipio: str = Path(..., description="Nome do município"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar")
):
    """Busca parâmetros urbanísticos por município"""
    try:
        parametros = await parametros_urbanisticos_repo.search_parametros_by_municipio(
            municipio=municipio,
            skip=skip,
            limit=limit
        )
        
        return ParametrosUrbanisticosListResponse(
            success=True,
            message=f"Encontrados {len(parametros)} parâmetros para o município {municipio}",
            parametros=parametros,
            total=len(parametros)
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetros por município {municipio}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetros: {str(e)}"
        )


@router.get("/zona/{zona}", response_model=ParametrosUrbanisticosListResponse)
async def buscar_parametros_por_zona(
    zona: str = Path(..., description="Zona urbana"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar")
):
    """Busca parâmetros urbanísticos por zona"""
    try:
        parametros = await parametros_urbanisticos_repo.get_parametros_by_zona(
            zona=zona,
            skip=skip,
            limit=limit
        )
        
        return ParametrosUrbanisticosListResponse(
            success=True,
            message=f"Encontrados {len(parametros)} parâmetros para a zona {zona}",
            parametros=parametros,
            total=len(parametros)
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetros por zona {zona}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetros: {str(e)}"
        )


@router.post("/terreno/{terreno_id}/recalcular", response_model=ParametrosUrbanisticosResponse)
async def recalcular_parametros(
    terreno_id: str = Path(..., description="ID do terreno"),
    dados_calculo: DadosCalculoParametros = None
):
    """Recalcula parâmetros urbanísticos para um terreno"""
    try:
        # Se não foram fornecidos dados de cálculo, tenta buscar do terreno
        if not dados_calculo:
            # TODO: Buscar dados do terreno para recalcular
            raise HTTPException(
                status_code=400,
                detail="Dados de cálculo necessários para recalcular parâmetros"
            )
        
        parametros = await parametros_urbanisticos_repo.recalcular_parametros(
            terreno_id=terreno_id,
            dados_calculo=dados_calculo
        )
        
        if not parametros:
            raise HTTPException(
                status_code=404,
                detail="Parâmetros urbanísticos não encontrados para este terreno"
            )
        
        return ParametrosUrbanisticosResponse(
            success=True,
            message="Parâmetros urbanísticos recalculados com sucesso",
            parametros=parametros
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao recalcular parâmetros para terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao recalcular parâmetros: {str(e)}"
        )


@router.post("/calcular", response_model=dict)
async def calcular_parametros_temporarios(dados_calculo: DadosCalculoParametros):
    """Calcula parâmetros urbanísticos temporariamente (sem salvar)"""
    try:
        parametros = await parametros_service.calcular_todos_parametros(dados_calculo)
        
        return {
            "success": True,
            "message": "Parâmetros calculados com sucesso",
            "parametros": parametros,
            "legislacao": parametros_service.legislacao
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular parâmetros temporários: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao calcular parâmetros: {str(e)}"
        )
