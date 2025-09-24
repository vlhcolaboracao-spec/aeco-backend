"""
Router para operações CRUD de Projetos.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query, Path
import logging

from ..models.projeto import (
    Projeto, 
    ProjetoCreate, 
    ProjetoUpdate, 
    ProjetoResponse, 
    ProjetoListResponse
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
    """Busca projeto por ID"""
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


@router.get("/codigo/{cod_projeto}", response_model=ProjetoResponse)
async def buscar_projeto_por_codigo(cod_projeto: str):
    """Busca projeto por código"""
    try:
        projeto = await projetos_repo.get_projeto_by_cod_projeto(cod_projeto)
        
        if not projeto:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com código {cod_projeto} não encontrado"
            )
        
        return ProjetoResponse(
            success=True,
            message="Projeto encontrado",
            projeto=projeto
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar projeto por código {cod_projeto}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar projeto: {str(e)}"
        )


@router.get("/cliente/{cliente_id}", response_model=ProjetoListResponse)
async def buscar_projetos_por_cliente(
    cliente_id: str,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros")
):
    """Busca projetos por cliente"""
    try:
        projetos = await projetos_repo.get_projetos_by_cliente_id(cliente_id)
        
        # Aplica paginação
        total = len(projetos)
        projetos_paginados = projetos[skip:skip + limit]
        
        return ProjetoListResponse(
            success=True,
            message=f"Encontrados {len(projetos_paginados)} projetos para o cliente",
            projetos=projetos_paginados,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar projetos do cliente {cliente_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar projetos: {str(e)}"
        )


@router.get("/terreno/{terreno_id}", response_model=ProjetoListResponse)
async def buscar_projetos_por_terreno(
    terreno_id: str,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros")
):
    """Busca projetos por terreno"""
    try:
        projetos = await projetos_repo.get_projetos_by_terreno_id(terreno_id)
        
        # Aplica paginação
        total = len(projetos)
        projetos_paginados = projetos[skip:skip + limit]
        
        return ProjetoListResponse(
            success=True,
            message=f"Encontrados {len(projetos_paginados)} projetos para o terreno",
            projetos=projetos_paginados,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar projetos do terreno {terreno_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar projetos: {str(e)}"
        )


@router.get("/", response_model=ProjetoListResponse)
async def listar_projetos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: str = Query(None, description="Termo de busca")
):
    """Lista todos os projetos com paginação e busca opcional"""
    try:
        if search:
            projetos = await projetos_repo.search_projetos(search, skip=skip, limit=limit)
            total = len(projetos)  # Para busca, o total pode não ser preciso
        else:
            projetos = await projetos_repo.get_all_projetos(skip=skip, limit=limit)
            total = await projetos_repo.count_projetos()
        
        return ProjetoListResponse(
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


@router.delete("/{projeto_id}", response_model=ProjetoResponse)
async def deletar_projeto(projeto_id: str):
    """Deleta um projeto (soft delete)"""
    try:
        success = await projetos_repo.delete_projeto(projeto_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com ID {projeto_id} não encontrado"
            )
        
        return ProjetoResponse(
            success=True,
            message="Projeto deletado com sucesso"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar projeto {projeto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao deletar projeto: {str(e)}"
        )


@router.get("/{projeto_id}/completo", response_model=dict)
async def buscar_projeto_completo(projeto_id: str):
    """Busca projeto com dados relacionados (cliente, terreno, parâmetros)"""
    try:
        dados_completos = await projetos_repo.get_projeto_com_dados_completos(projeto_id)
        
        if not dados_completos:
            raise HTTPException(
                status_code=404,
                detail=f"Projeto com ID {projeto_id} não encontrado"
            )
        
        return {
            "success": True,
            "message": "Projeto encontrado com dados relacionados",
            **dados_completos
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar projeto completo {projeto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar projeto completo: {str(e)}"
        )


# === ENDPOINTS PARA FORMULÁRIOS WEB ===

@router.get("/clientes/disponiveis", response_model=dict)
async def listar_clientes_disponiveis():
    """Lista clientes disponíveis para associação a projetos"""
    try:
        from ..repositories.clientes_repo import clientes_repo
        
        clientes = await clientes_repo.get_all_clientes(skip=0, limit=1000)
        
        # Formata dados para select/dropdown
        clientes_formatados = []
        for cliente in clientes:
            clientes_formatados.append({
                "id": str(cliente.id),
                "nome": cliente.nome_completo_razao_social,
                "cpf_cnpj": cliente.cpf_cnpj,
                "tipo": "Pessoa Jurídica" if cliente.cpf_cnpj and len(cliente.cpf_cnpj) > 11 else "Pessoa Física"
            })
        
        return {
            "success": True,
            "message": f"Encontrados {len(clientes_formatados)} clientes",
            "clientes": clientes_formatados
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar clientes disponíveis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar clientes: {str(e)}"
        )


@router.get("/terrenos/disponiveis", response_model=dict)
async def listar_terrenos_disponiveis():
    """Lista terrenos disponíveis para associação a projetos"""
    try:
        from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
        
        terrenos = await formulario_terrenos_repo.get_all_terrenos(skip=0, limit=1000)
        
        # Formata dados para select/dropdown
        terrenos_formatados = []
        for terreno in terrenos:
            terrenos_formatados.append({
                "id": str(terreno.id),
                "cod_projeto": terreno.cod_projeto,
                "matricula": terreno.matricula,
                "endereco": f"{terreno.logradouro}, {terreno.numero} - {terreno.bairro}",
                "zona": terreno.zona,
                "tipologia": terreno.tipologia
            })
        
        return {
            "success": True,
            "message": f"Encontrados {len(terrenos_formatados)} terrenos",
            "terrenos": terrenos_formatados
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar terrenos disponíveis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao listar terrenos: {str(e)}"
        )


@router.get("/validacao/zona/{zona}", response_model=dict)
async def validar_dependencias_por_zona(zona: str):
    """Valida dependências de campos baseadas na zona urbana"""
    try:
        from ..services.validacao_zone_service import validacao_zone_service
        
        dependencias = validacao_zone_service.get_dependencias_por_zona(zona)
        
        return {
            "success": True,
            "message": f"Dependências obtidas para zona {zona}",
            **dependencias
        }
        
    except Exception as e:
        logger.error(f"Erro ao validar dependências da zona {zona}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao validar zona: {str(e)}"
        )


@router.get("/validacao/natureza/{natureza}", response_model=dict)
async def validar_campos_por_natureza(natureza: str):
    """Valida campos baseados na natureza do empreendimento"""
    try:
        from ..services.validacao_zone_service import validacao_zone_service
        
        validacao = validacao_zone_service.validate_campos_por_natureza(natureza, {})
        
        return {
            "success": True,
            "message": f"Validação obtida para natureza {natureza}",
            **validacao
        }
        
    except Exception as e:
        logger.error(f"Erro ao validar campos da natureza {natureza}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao validar natureza: {str(e)}"
        )


@router.get("/validacao/combinacao/{zona}/{natureza}", response_model=dict)
async def validar_combinacao_zona_natureza(zona: str, natureza: str):
    """Valida campos condicionais baseados na combinação zona + natureza"""
    try:
        from ..services.validacao_zone_service import validacao_zone_service
        
        condicionais = validacao_zone_service.get_campos_condicionais_por_zona_e_natureza(zona, natureza)
        
        return {
            "success": True,
            "message": f"Campos condicionais obtidos para {zona} + {natureza}",
            **condicionais
        }
        
    except Exception as e:
        logger.error(f"Erro ao validar combinação {zona}+{natureza}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao validar combinação: {str(e)}"
        )


@router.get("/consulta/clientes", response_model=dict)
async def consultar_clientes(
    q: str = Query("", description="Termo de busca"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros")
):
    """Consulta clientes com busca por texto e paginação"""
    try:
        from ..repositories.clientes_repo import clientes_repo
        
        if q:
            # Busca por texto
            clientes = await clientes_repo.search_clientes(q, skip=skip, limit=limit)
            total = len(clientes)  # Para busca, o total pode não ser preciso
        else:
            # Lista todos com paginação
            clientes = await clientes_repo.get_all_clientes(skip=skip, limit=limit)
            total = await clientes_repo.count_clientes()
        
        # Formata dados para seleção
        clientes_formatados = []
        for cliente in clientes:
            clientes_formatados.append({
                "id": str(cliente.id),
                "nome": cliente.nome_completo_razao_social,
                "cpf_cnpj": cliente.cpf_cnpj,
                "tipo": "Pessoa Jurídica" if cliente.cpf_cnpj and len(cliente.cpf_cnpj) > 11 else "Pessoa Física",
                "endereco": f"{cliente.logradouro or ''}, {cliente.numero or ''}, {cliente.bairro or ''}, {cliente.cidade or ''} - {cliente.estado or ''}".strip(", "),
                "contato": cliente.telefone_principal or cliente.email or ""
            })
        
        return {
            "success": True,
            "message": f"Encontrados {len(clientes_formatados)} clientes",
            "clientes": clientes_formatados,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total,
                "has_more": skip + limit < total
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao consultar clientes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao consultar clientes: {str(e)}"
        )


@router.get("/consulta/terrenos", response_model=dict)
async def consultar_terrenos(
    q: str = Query("", description="Termo de busca"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros")
):
    """Consulta terrenos com busca por texto e paginação"""
    try:
        from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
        
        if q:
            # Busca por texto (implementar search_terrenos se necessário)
            terrenos = await formulario_terrenos_repo.get_all_terrenos(skip=skip, limit=limit)
            # Filtrar por termo de busca
            terrenos = [t for t in terrenos if q.lower() in t.matricula.lower() or q.lower() in t.bairro.lower()]
            total = len(terrenos)
        else:
            # Lista todos com paginação
            terrenos = await formulario_terrenos_repo.get_all_terrenos(skip=skip, limit=limit)
            total = await formulario_terrenos_repo.count_terrenos()
        
        # Formata dados para seleção
        terrenos_formatados = []
        for terreno in terrenos:
            terrenos_formatados.append({
                "id": str(terreno.id),
                "cod_projeto": terreno.cod_projeto,
                "matricula": terreno.matricula,
                "endereco": f"{terreno.logradouro}, {terreno.numero} - {terreno.bairro}",
                "zona": terreno.zona,
                "area": terreno.area,
                "municipio": terreno.municipio,
                "estado": terreno.estado
            })
        
        return {
            "success": True,
            "message": f"Encontrados {len(terrenos_formatados)} terrenos",
            "terrenos": terrenos_formatados,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total,
                "has_more": skip + limit < total
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao consultar terrenos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao consultar terrenos: {str(e)}"
        )