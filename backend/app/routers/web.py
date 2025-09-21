"""
Router para servir o frontend (HTML estático e templates Jinja2).
"""
import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import logging

from ..config import settings
from ..models.formulario_terrenos_projetos import FormularioTerrenosProjetosCreate
from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo

logger = logging.getLogger(__name__)

# Configuração dos templates Jinja2
templates = Jinja2Templates(directory="backend/app/web/templates")

# Router para rotas web
router = APIRouter()

# Montar arquivos estáticos
router.mount("/static", StaticFiles(directory="backend/app/web/static"), name="static")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Página principal do dashboard.
    Serve HTML estático ou template Jinja2 baseado na configuração FRONTEND_MODE.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        if frontend_mode == "jinja":
            # Serve template Jinja2
            return templates.TemplateResponse(
                "dashboard.html",
                {
                    "request": request,
                    "frontend_mode": frontend_mode,
                    "api_base_url": settings.api_base_url
                }
            )
        else:
            # Serve HTML estático
            static_file_path = "frontend/public/index.html"
            if os.path.exists(static_file_path):
                with open(static_file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                return HTMLResponse(content=html_content)
            else:
                raise HTTPException(status_code=404, detail="Arquivo HTML estático não encontrado")
                
    except Exception as e:
        logger.error(f"Erro ao servir dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_jinja(request: Request):
    """
    Dashboard usando template Jinja2 (sempre).
    """
    try:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "frontend_mode": "jinja",
                "api_base_url": settings.api_base_url
            }
        )
    except Exception as e:
        logger.error(f"Erro ao servir dashboard Jinja: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/formulario-terrenos-projetos", response_class=HTMLResponse)
async def formulario_terrenos(request: Request):
    """
    Página do formulário de terrenos.
    Serve HTML estático ou template Jinja2 baseado na configuração FRONTEND_MODE.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        if frontend_mode == "jinja":
            # Serve template Jinja2
            return templates.TemplateResponse(
                "formulario_terrenos.html",
                {
                    "request": request,
                    "frontend_mode": frontend_mode,
                    "api_base_url": settings.api_base_url
                }
            )
        else:
            # Serve HTML estático
            static_file_path = "frontend/public/formulario_terrenos.html"
            if os.path.exists(static_file_path):
                with open(static_file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                return HTMLResponse(content=html_content)
            else:
                raise HTTPException(status_code=404, detail="Arquivo HTML estático não encontrado")
                
    except Exception as e:
        logger.error(f"Erro ao servir formulário de terrenos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/formulario-terrenos-projetos", response_class=JSONResponse)
async def criar_terreno_web(request: Request):
    """
    Endpoint para criar terreno via formulário web.
    Retorna JSON para HTMX.
    """
    try:
        from datetime import datetime
        
        logger.info("Iniciando processamento do formulário de terrenos")
        
        # Processa dados do formulário
        form_data = await request.form()
        logger.info(f"Dados do formulário recebidos: {dict(form_data)}")
        
        # Extrai dados básicos
        matricula = form_data.get("matricula")
        data_str = form_data.get("data")
        municipio = form_data.get("municipio")
        estado = form_data.get("estado")
        pais = form_data.get("pais", "BRASIL")
        bairro = form_data.get("bairro")
        logradouro = form_data.get("logradouro")
        numero = form_data.get("numero")
        cep = form_data.get("cep")
        lados_poligono = int(form_data.get("lados_poligono"))
        tipo_lote = form_data.get("tipo_lote")
        area = form_data.get("area")
        norte_verdadeiro = float(form_data.get("norte_verdadeiro"))
        zona = form_data.get("zona")
        observacoes = form_data.get("observacoes")
        
        # Converte data string para datetime
        data_obj = datetime.fromisoformat(data_str)
        
        # Processa ângulos internos
        angulos_internos = []
        for i in range(1, lados_poligono + 1):
            angulo_key = f"angulo_{i}"
            angulo_value = form_data.get(angulo_key)
            logger.info(f"Ângulo {i} ({angulo_key}): '{angulo_value}'")
            
            if angulo_value and angulo_value.strip():
                try:
                    angulo_float = float(angulo_value)
                    angulos_internos.append(angulo_float)
                except ValueError:
                    logger.error(f"Erro ao converter ângulo {i}: '{angulo_value}'")
                    raise HTTPException(status_code=400, detail=f"Ângulo {i} deve ser um número válido")
            else:
                logger.warning(f"Ângulo {i} está vazio ou nulo")
                angulos_internos.append(0.0)
        
        logger.info(f"Ângulos processados: {angulos_internos}")
        
        # Processa dimensões dos lados
        dimensoes_lados = []
        for i in range(1, lados_poligono + 1):
            tipo_key = f"dimensao_{i}_tipo"
            medida_key = f"dimensao_{i}_medida"
            tipo_value = form_data.get(tipo_key)
            medida_value = form_data.get(medida_key)
            
            logger.info(f"Dimensão {i} - Tipo: '{tipo_value}', Medida: '{medida_value}'")
            
            if not tipo_value or not medida_value:
                logger.error(f"Dimensão {i} está incompleta - Tipo: '{tipo_value}', Medida: '{medida_value}'")
                raise HTTPException(status_code=400, detail=f"Dimensão {i} deve ter tipo e medida preenchidos")
            
            try:
                medida_float = float(medida_value)
                if medida_float <= 0:
                    raise HTTPException(status_code=400, detail=f"Medida da dimensão {i} deve ser maior que zero")
                
                dimensoes_lados.append({
                    "tipo": tipo_value,
                    "medida": medida_float
                })
            except ValueError:
                logger.error(f"Erro ao converter medida da dimensão {i}: '{medida_value}'")
                raise HTTPException(status_code=400, detail=f"Medida da dimensão {i} deve ser um número válido")
        
        logger.info(f"Dimensões processadas: {dimensoes_lados}")
        
        # Cria objeto de dados do terreno
        terreno_data = FormularioTerrenosProjetosCreate(
            matricula=matricula,
            data=data_obj,
            municipio=municipio,
            estado=estado,
            pais=pais,
            bairro=bairro,
            logradouro=logradouro,
            numero=numero,
            cep=cep,
            lados_poligono=lados_poligono,
            angulos_internos=angulos_internos,
            dimensoes_lados=dimensoes_lados,
            tipo_lote=tipo_lote,
            area=area,
            norte_verdadeiro=norte_verdadeiro,
            zona=zona,
            observacoes=observacoes
        )
        
        logger.info(f"Tentando salvar terreno no banco: {terreno_data.dict()}")
        
        # Salva no banco
        terreno = await formulario_terrenos_repo.create_terreno(terreno_data)
        
        logger.info(f"Terreno salvo com sucesso: {terreno.id}")
        
        return JSONResponse(content={
            "success": True,
            "message": "Terreno cadastrado com sucesso!",
            "terreno_id": str(terreno.id)
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar terreno via web: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro ao cadastrar terreno: {str(e)}"
            }
        )


@router.get("/health-status", response_class=HTMLResponse)
async def health_status_widget():
    """
    Widget de status para HTMX.
    Retorna HTML com badges de status.
    """
    try:
        from ..db.mongo import ping_mongo
        
        # Testa conexão MongoDB
        mongo_status = await ping_mongo()
        
        # Determina status geral
        overall_status = "OK" if mongo_status else "FAIL"
        
        # HTML com badges
        html_content = f"""
        <div class="space-y-2">
            <div class="flex space-x-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {'bg-green-100 text-green-800' if overall_status == 'OK' else 'bg-red-100 text-red-800'}">
                    API: {overall_status}
                </span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {'bg-green-100 text-green-800' if mongo_status else 'bg-red-100 text-red-800'}">
                    MongoDB: {'OK' if mongo_status else 'FAIL'}
                </span>
            </div>
            <div class="text-xs text-gray-500">
                Última verificação: {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Erro no widget de status: {e}")
        return HTMLResponse(content="""
        <div class="space-y-2">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                Erro na verificação
            </span>
        </div>
        """)


@router.get("/terrenos-list", response_class=HTMLResponse)
async def terrenos_list_widget(limit: int = 10):
    """
    Widget de lista de terrenos para HTMX.
    Retorna HTML com tabela de terrenos.
    """
    try:
        terrenos = await formulario_terrenos_repo.get_all_terrenos(skip=0, limit=limit)
        
        if not terrenos:
            return HTMLResponse(content="""
            <div class="text-gray-500 text-sm">
                Nenhum terreno cadastrado ainda.
            </div>
            """)
        
        # HTML da tabela
        html_content = """
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Matrícula
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Município
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Área (m²)
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Tipo
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Criado em
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
        """
        
        for terreno in terrenos:
            html_content += f"""
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {terreno.matricula}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {terreno.municipio}/{terreno.estado}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {terreno.area:.2f}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {terreno.tipo_lote}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {terreno.created_at.strftime('%d/%m/%Y')}
                        </td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Erro ao carregar lista de terrenos: {e}")
        return HTMLResponse(content="""
        <div class="text-red-500 text-sm">
            Erro ao carregar lista de terrenos.
        </div>
        """)
