"""
Configurações da aplicação carregadas via variáveis de ambiente.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do arquivo .env"""
    
    # Configurações da aplicação
    app_env: str = "dev"
    app_port: int = 8000
    api_base_url: str = "http://127.0.0.1:8000"
    
    # Configurações do MongoDB
    mongodb_username: str = "leandro"
    mongodb_password: str = "Leandro123."
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    database_name: str = "dev"
    
    @property
    def mongo_uri(self) -> str:
        """Constrói a URI do MongoDB a partir das variáveis separadas"""
        return f"mongodb://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/?authSource=admin"
    
    @property
    def mongo_db(self) -> str:
        """Retorna o nome do banco de dados"""
        return self.database_name
    
    # Configurações de logging
    log_level: str = "INFO"
    
    # Configurações do Frontend
    frontend_mode: str = "jinja"  # "static" ou "jinja"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


# Instância global das configurações
settings = Settings()
