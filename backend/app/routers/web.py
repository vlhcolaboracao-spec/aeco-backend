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
from ..models.clientes import ClienteCreate
from ..models.projeto import ProjetoCreate
from ..repositories.formulario_terrenos_repo import formulario_terrenos_repo
from ..repositories.clientes_repo import clientes_repo
from ..repositories.projetos_repo import projetos_repo

logger = logging.getLogger(__name__)

# Configuração dos templates Jinja2
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "web", "templates"))

# Router para rotas web
router = APIRouter()

# Montar arquivos estáticos
router.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "web", "static")), name="static")


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


@router.get("/cadastro-clientes", response_class=HTMLResponse)
async def cadastro_clientes(request: Request):
    """
    Página do cadastro de clientes.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        return templates.TemplateResponse(
            "cadastro_clientes.html",
            {
                "request": request,
                "frontend_mode": frontend_mode,
                "api_base_url": settings.api_base_url
            }
        )
                
    except Exception as e:
        logger.error(f"Erro ao servir cadastro de clientes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/clientes", response_class=JSONResponse)
async def criar_cliente_web(request: Request):
    """
    Endpoint para criar cliente via formulário web.
    Retorna JSON para HTMX.
    """
    try:
        logger.info("Iniciando processamento do formulário de clientes")
        
        # Processa dados do formulário
        form_data = await request.form()
        logger.info(f"Dados do formulário recebidos: {dict(form_data)}")
        
        # Extrai dados básicos (converte strings vazias para None)
        nome_completo_razao_social = form_data.get("nome_completo_razao_social") or None
        cpf_cnpj = form_data.get("cpf_cnpj") or None
        rg_inscricao_estadual = form_data.get("rg_inscricao_estadual") or None
        data_nascimento_fundacao_str = form_data.get("data_nascimento_fundacao") or None
        telefone_principal = form_data.get("telefone_principal") or None
        telefone_secundario = form_data.get("telefone_secundario") or None
        email = form_data.get("email") or None
        redes_sociais = form_data.get("redes_sociais") or None
        logradouro = form_data.get("logradouro") or None
        numero = form_data.get("numero") or None
        complemento = form_data.get("complemento") or None
        bairro = form_data.get("bairro") or None
        cidade = form_data.get("cidade") or None
        estado = form_data.get("estado") or None
        cep = form_data.get("cep") or None
        pais = form_data.get("pais") or "BRASIL"
        
        # Converte data se fornecida
        data_nascimento_fundacao = None
        if data_nascimento_fundacao_str:
            from datetime import datetime
            data_nascimento_fundacao = datetime.fromisoformat(data_nascimento_fundacao_str).date()
        
        # Cria objeto de dados do cliente
        cliente_data = ClienteCreate(
            nome_completo_razao_social=nome_completo_razao_social,
            cpf_cnpj=cpf_cnpj,
            rg_inscricao_estadual=rg_inscricao_estadual,
            data_nascimento_fundacao=data_nascimento_fundacao,
            telefone_principal=telefone_principal,
            telefone_secundario=telefone_secundario,
            email=email,
            redes_sociais=redes_sociais,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep,
            pais=pais
        )
        
        logger.info(f"Tentando salvar cliente no banco: {cliente_data.dict()}")
        
        # Salva no banco
        cliente = await clientes_repo.create_cliente(cliente_data)
        
        logger.info(f"Cliente salvo com sucesso: {cliente.id}")
        
        return JSONResponse(content={
            "success": True,
            "message": "Cliente cadastrado com sucesso!",
            "cliente_id": str(cliente.id)
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar cliente via web: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro ao cadastrar cliente: {str(e)}"
            }
        )


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
        # tipologia removida - agora está no projeto
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
            # tipologia removida - agora está no projeto
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
        
        from datetime import datetime
        
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


@router.get("/clientes-list", response_class=HTMLResponse)
async def clientes_list_widget(limit: int = 10):
    """
    Widget de lista de clientes para HTMX.
    Retorna HTML com tabela de clientes.
    """
    try:
        clientes = await clientes_repo.get_all_clientes(skip=0, limit=limit)
        
        if not clientes:
            return HTMLResponse(content="""
            <div class="text-gray-500 text-sm">
                Nenhum cliente cadastrado ainda.
            </div>
            """)
        
        # HTML da tabela
        html_content = """
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Nome/Razão Social
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            CPF/CNPJ
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Cidade
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Telefone
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Criado em
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
        """
        
        for cliente in clientes:
            # Formata CPF/CNPJ
            cpf_cnpj_formatado = cliente.cpf_cnpj or '-'
            if cliente.cpf_cnpj:
                if len(cliente.cpf_cnpj) == 11:  # CPF
                    cpf_cnpj_formatado = f"{cliente.cpf_cnpj[:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:]}"
                elif len(cliente.cpf_cnpj) == 14:  # CNPJ
                    cpf_cnpj_formatado = f"{cliente.cpf_cnpj[:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:]}"
            
            nome_display = cliente.nome_completo_razao_social or 'Nome não informado'
            if len(nome_display) > 30:
                nome_display = nome_display[:30] + '...'
            
            html_content += f"""
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {nome_display}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {cpf_cnpj_formatado}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {cliente.cidade or '-'}/{cliente.estado or '-'}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {cliente.telefone_principal or '-'}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {cliente.created_at.strftime('%d/%m/%Y')}
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
        logger.error(f"Erro ao carregar lista de clientes: {e}")
        return HTMLResponse(content="""
        <div class="text-red-500 text-sm">
            Erro ao carregar lista de clientes.
        </div>
        """)


@router.get("/processos", response_class=HTMLResponse)
async def pagina_processos(request: Request):
    """
    Página de cadastro de processos Revit.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        return templates.TemplateResponse(
            "processos.html",
            {
                "request": request,
                "frontend_mode": frontend_mode,
                "api_base_url": settings.api_base_url
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar página de processos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/orquestracao", response_class=HTMLResponse)
async def pagina_orquestracao(request: Request):
    """
    Página de orquestração de processos Revit.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        return templates.TemplateResponse(
            "orquestracao.html",
            {
                "request": request,
                "frontend_mode": frontend_mode,
                "api_base_url": settings.api_base_url
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar página de orquestração: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/processos", response_class=JSONResponse)
async def criar_processo_web(request: Request):
    """
    Endpoint para criar processo via formulário web.
    Retorna JSON para HTMX.
    """
    try:
        logger.info("Iniciando processamento do formulário de processos")
        
        # Processa dados do formulário
        form_data = await request.form()
        logger.info(f"Dados do formulário recebidos: {dict(form_data)}")
        
        # Extrai dados básicos
        nome = form_data.get("nome")
        descricao = form_data.get("descricao")
        versao = form_data.get("versao")
        categoria = form_data.get("categoria")
        tipo = form_data.get("tipo")
        timeout_segundos = int(form_data.get("timeout_segundos", 300))
        tentativas_retry = int(form_data.get("tentativas_retry", 3))
        ordem_execucao = int(form_data.get("ordem_execucao", 1))
        ambiente = form_data.get("ambiente", "desenvolvimento")
        tags = form_data.get("tags", "")
        ativo = form_data.get("ativo") == "on"
        parametros_entrada = form_data.get("parametros_entrada", "{}")
        
        # Processa arquivo se fornecido
        arquivo_principal = None
        arquivo_principal_file = form_data.get("arquivo_principal")
        if arquivo_principal_file and hasattr(arquivo_principal_file, 'filename'):
            arquivo_principal = arquivo_principal_file.filename
        
        # Processa descrição do processo se for tipo textual
        descricao_processo = form_data.get("descricao_processo", "")
        
        logger.info(f"Processo criado: {nome} - {categoria} - {tipo}")
        
        # Por enquanto, apenas retorna sucesso
        # TODO: Implementar salvamento no banco de dados
        return JSONResponse(content={
            "success": True,
            "message": f"Processo '{nome}' criado com sucesso!",
            "processo": {
                "nome": nome,
                "descricao": descricao,
                "versao": versao,
                "categoria": categoria,
                "tipo": tipo,
                "ativo": ativo
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar processo: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }
        )


@router.get("/cadastro-projetos", response_class=HTMLResponse)
async def cadastro_projetos(request: Request):
    """
    Página de cadastro de projetos.
    """
    try:
        frontend_mode = getattr(settings, 'frontend_mode', 'static')
        
        if frontend_mode == "jinja":
            # Serve template Jinja2
            return templates.TemplateResponse(
                "cadastro_projetos.html",
                {
                    "request": request,
                    "frontend_mode": frontend_mode,
                    "api_base_url": settings.api_base_url
                }
            )
        else:
            # Serve HTML estático
            static_html_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "public", "cadastro_projetos.html")
            if os.path.exists(static_html_path):
                with open(static_html_path, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
            else:
                raise HTTPException(status_code=404, detail="Página não encontrada")
                
    except Exception as e:
        logger.error(f"Erro ao carregar página de cadastro de projetos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/cadastro-projetos", response_class=JSONResponse)
async def criar_projeto_web(request: Request):
    """
    Endpoint para criar projeto via formulário web.
    Retorna JSON para HTMX.
    """
    try:
        logger.info("Iniciando processamento do formulário de projetos")
        
        # Processa dados do formulário
        form_data = await request.form()
        logger.info(f"Dados do formulário recebidos: {dict(form_data)}")
        
        # Extrai dados do formulário
        projeto_data = {
            "nome_completo": form_data.get("nome_completo"),
            "contato": form_data.get("contato"),
            "estado_civil_composicao": form_data.get("estado_civil_composicao"),
            "profissao_rotina": form_data.get("profissao_rotina"),
            "tipologia": form_data.get("tipologia"),
            "ambientes_desejados": form_data.get("ambientes_desejados"),
            "prioridades": form_data.get("prioridades"),
            "estilo_arquitetonico": form_data.get("estilo_arquitetonico"),
            "materiais_interesse": form_data.get("materiais_interesse"),
            "exemplos_referencias": form_data.get("exemplos_referencias"),
            "uso_espacos_dia_dia": form_data.get("uso_espacos_dia_dia"),
            "animais_estimacao": form_data.get("animais_estimacao"),
            "necessidades_especiais": form_data.get("necessidades_especiais"),
            "frequencia_visitas": form_data.get("frequencia_visitas"),
            "orcamento_estimado": form_data.get("orcamento_estimado"),
            "fonte_recursos": form_data.get("fonte_recursos"),
            "prazo_entrega": form_data.get("prazo_entrega"),
            "solucoes_sustentaveis": form_data.get("solucoes_sustentaveis"),
            "nivel_automacao": form_data.get("nivel_automacao"),
            "desejos_expectativas": form_data.get("desejos_expectativas"),
            "restricoes": form_data.get("restricoes")
        }
        
        # Remove campos vazios
        projeto_data = {k: v for k, v in projeto_data.items() if v and v.strip()}
        
        # Valida se pelo menos um campo foi preenchido
        if not projeto_data:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Pelo menos um campo deve ser preenchido"
                }
            )
        
        # Cria modelo Pydantic
        projeto_create = ProjetoCreate(**projeto_data)
        
        # Salva no banco de dados
        projeto_criado = await projetos_repo.create_projeto(projeto_create)
        
        logger.info(f"Projeto criado com sucesso: {projeto_criado.id}")
        
        return JSONResponse(content={
            "success": True,
            "message": f"Projeto de '{projeto_criado.nome_completo or 'Cliente'}' cadastrado com sucesso!",
            "projeto": {
                "id": str(projeto_criado.id),
                "nome_completo": projeto_criado.nome_completo,
                "tipologia": projeto_criado.tipologia,
                "created_at": projeto_criado.created_at.isoformat() if projeto_criado.created_at else None
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }
        )


@router.post("/cadastrar-projeto")
async def cadastrar_projeto(
    request: Request,
    nome_projeto: str = Form(...),
    tipo_empreendimento: str = Form(...),
    natureza: str = Form(...),
    descricao: Optional[str] = Form(None),
    pavimentos: Optional[str] = Form(None),
    altura_total: Optional[str] = Form(None),
    area_construida: Optional[str] = Form(None),
    area_minima_lote: Optional[str] = Form(None),
    cliente_id: Optional[str] = Form(None),
    terreno_id: Optional[str] = Form(None),
    avenida: Optional[str] = Form(None),
    observacoes: Optional[str] = Form(None)
):
    """
    Processa o formulário de cadastro de projeto.
    """
    try:
        logger.info("=== INÍCIO DO CADASTRO DE PROJETO ===")
        logger.info(f"Dados recebidos:")
        logger.info(f"  nome_projeto: {nome_projeto}")
        logger.info(f"  tipo_empreendimento: {tipo_empreendimento}")
        logger.info(f"  natureza: {natureza}")
        logger.info(f"  cliente_id: {cliente_id}")
        logger.info(f"  terreno_id: {terreno_id}")
        logger.info(f"  pavimentos: {pavimentos}")
        logger.info(f"  altura_total: {altura_total}")
        logger.info(f"  area_construida: {area_construida}")
        logger.info(f"  avenida: {avenida}")
        # Gera código do projeto automaticamente
        logger.info("Gerando código do projeto...")
        from ..utils.codigo_projeto import gerar_codigo_projeto_unico
        cod_projeto = await gerar_codigo_projeto_unico()
        logger.info(f"Código gerado: {cod_projeto}")
        
        # Trata campos vazios e conversões
        logger.info("Tratando campos vazios...")
        
        # Converte campos numéricos
        pavimentos_int = None
        if pavimentos is not None and pavimentos != "":
            try:
                pavimentos_int = int(pavimentos)
            except (ValueError, TypeError):
                pavimentos_int = None
        
        altura_float = None
        if altura_total is not None and altura_total != "":
            try:
                altura_float = float(altura_total)
            except (ValueError, TypeError):
                altura_float = None
        
        area_construida_float = None
        if area_construida is not None and area_construida != "":
            try:
                area_construida_float = float(area_construida)
            except (ValueError, TypeError):
                area_construida_float = None
        
        area_minima_float = None
        if area_minima_lote is not None and area_minima_lote != "":
            try:
                area_minima_float = float(area_minima_lote)
            except (ValueError, TypeError):
                area_minima_float = None
        
        # Converte campos de texto para None se vazios
        descricao_clean = descricao if descricao and descricao.strip() else None
        avenida_clean = avenida if avenida and avenida.strip() else None
        observacoes_clean = observacoes if observacoes and observacoes.strip() else None
        cliente_id_clean = cliente_id if cliente_id and cliente_id.strip() else None
        terreno_id_clean = terreno_id if terreno_id and terreno_id.strip() else None
        
        logger.info(f"Campos tratados:")
        logger.info(f"  pavimentos: {pavimentos_int}")
        logger.info(f"  altura_total: {altura_float}")
        logger.info(f"  area_construida: {area_construida_float}")
        logger.info(f"  cliente_id: {cliente_id_clean}")
        logger.info(f"  terreno_id: {terreno_id_clean}")
        
        # Cria o projeto
        logger.info("Criando objeto ProjetoCreate...")
        projeto_data = ProjetoCreate(
            cod_projeto=cod_projeto,
            nome_projeto=nome_projeto,
            tipo_empreendimento=tipo_empreendimento,
            natureza=natureza,
            descricao=descricao_clean,
            pavimentos=pavimentos_int,
            altura_total=altura_float,
            area_construida=area_construida_float,
            area_minima_lote=area_minima_float,
            cliente_id=cliente_id_clean,
            terreno_id=terreno_id_clean,
            avenida=avenida_clean,
            observacoes=observacoes_clean
        )
        logger.info("Objeto ProjetoCreate criado com sucesso!")
        
        projeto_criado = await projetos_repo.create_projeto(projeto_data)
        
        # Se um terreno foi associado, recalcula os parâmetros urbanísticos
        if terreno_id:
            try:
                terreno = await formulario_terrenos_repo.get_terreno_by_id(terreno_id)
                if terreno:
                    # Atualiza o terreno com o projeto_id
                    await formulario_terrenos_repo.update_terreno(terreno_id, {"projeto_id": str(projeto_criado.id)})
                    
                    # Recalcula parâmetros urbanísticos
                    await formulario_terrenos_repo._calcular_parametros_urbanisticos(terreno)
                    logger.info(f"Parâmetros urbanísticos recalculados para terreno {terreno_id}")
            except Exception as e:
                logger.warning(f"Erro ao recalcular parâmetros para terreno {terreno_id}: {e}")
        
        return JSONResponse(content={
            "success": True,
            "message": "Projeto cadastrado com sucesso!",
            "data": {
                "id": str(projeto_criado.id),
                "cod_projeto": projeto_criado.cod_projeto,
                "nome_projeto": projeto_criado.nome_projeto,
                "tipo_empreendimento": projeto_criado.tipo_empreendimento,
                "created_at": projeto_criado.created_at.isoformat() if projeto_criado.created_at else None
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }
        )