"""
Aplicação principal FastAPI do sistema AECO.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db.mongo import connect_to_mongo, close_mongo_connection
from .routers import health, projetos

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação:
    - Conecta ao MongoDB na inicialização
    - Fecha conexões na finalização
    """
    # Startup
    logger.info("Iniciando aplicação AECO...")
    try:
        await connect_to_mongo()
        logger.info("Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar aplicação: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Finalizando aplicação...")
    await close_mongo_connection()
    logger.info("Aplicação finalizada.")


# Criação da aplicação FastAPI
app = FastAPI(
    title="Sistema AECO - Backend API",
    description="API REST para sistema AECO com FastAPI e MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos routers
app.include_router(health.router)
app.include_router(projetos.router)


@app.get("/")
async def root():
    """Endpoint raiz com informações básicas da API"""
    return {
        "message": "Sistema AECO - Backend API",
        "version": "1.0.0",
        "environment": settings.app_env,
        "docs_url": "/docs",
        "health_check": "/health"
    }


@app.get("/info")
async def app_info():
    """Informações detalhadas da aplicação"""
    return {
        "app_name": "Sistema AECO",
        "version": "1.0.0",
        "environment": settings.app_env,
        "port": settings.app_port,
        "mongo_db": settings.mongo_db,
        "api_base_url": settings.api_base_url
    }
