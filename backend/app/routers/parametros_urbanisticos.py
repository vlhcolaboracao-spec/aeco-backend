"""
Router para operações CRUD de Parâmetros Urbanísticos.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query, Path, Response
from fastapi.responses import JSONResponse
import logging
from datetime import datetime, timedelta

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


# === NOVOS ENDPOINTS PARA DYNAMO/REVIT ===

@router.get("/api/parametros/projeto/{cod_projeto}", response_model=dict)
async def get_parametros_completos_projeto(
    cod_projeto: str = Path(..., description="Código do projeto (7 caracteres)"),
    response: Response = None
):
    """
    Busca TODOS os parâmetros urbanísticos de um projeto por código.
    Endpoint otimizado para Dynamo/Revit - uma única requisição retorna tudo.
    """
    try:
        # Busca terreno por código do projeto
        from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
        terreno = await formulario_terrenos_repo.get_terreno_by_cod_projeto(cod_projeto)
        
        if not terreno:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com código {cod_projeto} não encontrado"
            )
        
        # Busca parâmetros urbanísticos
        parametros = await parametros_urbanisticos_repo.get_parametros_by_terreno_id(str(terreno.id))
        
        if not parametros:
            raise HTTPException(
                status_code=404,
                detail=f"Parâmetros urbanísticos não encontrados para o projeto {cod_projeto}"
            )
        
        # Prepara resposta otimizada para Dynamo/Revit
        response_data = {
            "success": True,
            "projeto_codigo": terreno.cod_projeto,
            "terreno_id": str(terreno.id),
            "municipio": terreno.municipio,
            "zona": terreno.zona,
            "tipologia": terreno.tipologia,
            "parametros": {},
            "legislacao": parametros.legislacao,
            "data_calculo": parametros.data_calculo.isoformat(),
            "timestamp": parametros.updated_at.isoformat()
        }
        
        # Extrai valores dos parâmetros calculados
        if parametros.recuo_frontal:
            response_data["parametros"]["recuo_frontal"] = {
                "valor": parametros.recuo_frontal.valor,
                "unidade": parametros.recuo_frontal.unidade,
                "regra_aplicada": parametros.recuo_frontal.regra_aplicada,
                "erro": parametros.recuo_frontal.erro
            }
        
        if parametros.recuo_lateral:
            response_data["parametros"]["recuo_lateral"] = {
                "valor": parametros.recuo_lateral.valor,
                "unidade": parametros.recuo_lateral.unidade,
                "regra_aplicada": parametros.recuo_lateral.regra_aplicada,
                "erro": parametros.recuo_lateral.erro
            }
        
        if parametros.recuo_fundos:
            response_data["parametros"]["recuo_fundos"] = {
                "valor": parametros.recuo_fundos.valor,
                "unidade": parametros.recuo_fundos.unidade,
                "regra_aplicada": parametros.recuo_fundos.regra_aplicada,
                "erro": parametros.recuo_fundos.erro
            }
        
        if parametros.testada_minima:
            response_data["parametros"]["testada_minima"] = {
                "valor": parametros.testada_minima.valor,
                "unidade": parametros.testada_minima.unidade,
                "regra_aplicada": parametros.testada_minima.regra_aplicada,
                "erro": parametros.testada_minima.erro
            }
        
        if parametros.altura_maxima:
            response_data["parametros"]["altura_maxima"] = {
                "valor": parametros.altura_maxima.valor,
                "unidade": parametros.altura_maxima.unidade,
                "regra_aplicada": parametros.altura_maxima.regra_aplicada,
                "erro": parametros.altura_maxima.erro
            }
        
        if parametros.outorga_onerosa:
            response_data["parametros"]["outorga_onerosa"] = {
                "valor": parametros.outorga_onerosa.valor,
                "unidade": parametros.outorga_onerosa.unidade,
                "regra_aplicada": parametros.outorga_onerosa.regra_aplicada,
                "erro": parametros.outorga_onerosa.erro
            }
        
        # Adiciona headers de cache
        if response:
            response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutos
            response.headers["ETag"] = f'"{parametros.id}"'
            response.headers["Last-Modified"] = parametros.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetros completos para projeto {cod_projeto}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetros: {str(e)}"
        )


@router.get("/api/parametros/projeto/{cod_projeto}/{parametro}", response_model=dict)
async def get_parametro_especifico_projeto(
    cod_projeto: str = Path(..., description="Código do projeto (7 caracteres)"),
    parametro: str = Path(..., description="Nome do parâmetro específico"),
    response: Response = None
):
    """
    Busca um parâmetro específico de um projeto por código.
    Endpoint otimizado para Dynamo/Revit - requisição granular.
    """
    try:
        # Valida se o parâmetro é válido
        parametros_validos = [
            "recuo_frontal", "recuo_lateral", "recuo_fundos", 
            "testada_minima", "altura_maxima", "outorga_onerosa"
        ]
        
        if parametro not in parametros_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Parâmetro '{parametro}' inválido. Parâmetros válidos: {', '.join(parametros_validos)}"
            )
        
        # Busca terreno por código do projeto
        from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
        terreno = await formulario_terrenos_repo.get_terreno_by_cod_projeto(cod_projeto)
        
        if not terreno:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com código {cod_projeto} não encontrado"
            )
        
        # Busca parâmetros urbanísticos
        parametros_obj = await parametros_urbanisticos_repo.get_parametros_by_terreno_id(str(terreno.id))
        
        if not parametros_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Parâmetros urbanísticos não encontrados para o projeto {cod_projeto}"
            )
        
        # Busca o parâmetro específico
        parametro_obj = getattr(parametros_obj, parametro, None)
        
        if not parametro_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Parâmetro '{parametro}' não encontrado para o projeto {cod_projeto}"
            )
        
        # Prepara resposta otimizada
        response_data = {
            "success": True,
            "projeto_codigo": terreno.cod_projeto,
            "terreno_id": str(terreno.id),
            "parametro": parametro,
            "valor": parametro_obj.valor,
            "unidade": parametro_obj.unidade,
            "regra_aplicada": parametro_obj.regra_aplicada,
            "dependencias": parametro_obj.dependencias,
            "erro": parametro_obj.erro,
            "legislacao": parametros_obj.legislacao,
            "data_calculo": parametros_obj.data_calculo.isoformat(),
            "timestamp": parametros_obj.updated_at.isoformat()
        }
        
        # Adiciona headers de cache
        if response:
            response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutos
            response.headers["ETag"] = f'"{parametros_obj.id}-{parametro}"'
            response.headers["Last-Modified"] = parametros_obj.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar parâmetro {parametro} para projeto {cod_projeto}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar parâmetro: {str(e)}"
        )
