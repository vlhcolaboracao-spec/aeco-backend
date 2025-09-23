"""
Utilitários para geração de códigos de projeto únicos.
"""
import random
import string
import logging
from typing import Set
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


def gerar_codigo_projeto() -> str:
    """
    Gera um código de projeto único de 7 caracteres alfanuméricos.
    Formato: 3 letras + 4 números (ex: ABC1234)
    """
    # Caracteres permitidos
    letras = string.ascii_uppercase
    numeros = string.digits
    
    # Gera 3 letras + 4 números
    codigo = ''.join(random.choices(letras, k=3)) + ''.join(random.choices(numeros, k=4))
    
    return codigo


async def gerar_codigo_projeto_unico() -> str:
    """
    Gera um código de projeto único garantindo que não existe no banco.
    """
    max_tentativas = 100  # Evita loop infinito
    tentativas = 0
    
    while tentativas < max_tentativas:
        codigo = gerar_codigo_projeto()
        
        # Verifica se já existe no banco
        if await codigo_projeto_existe(codigo):
            tentativas += 1
            logger.warning(f"Código {codigo} já existe, tentando novamente... (tentativa {tentativas})")
            continue
        else:
            logger.info(f"Código único gerado: {codigo}")
            return codigo
    
    # Se chegou aqui, algo deu errado
    raise Exception(f"Não foi possível gerar código único após {max_tentativas} tentativas")


async def codigo_projeto_existe(codigo: str) -> bool:
    """
    Verifica se um código de projeto já existe no banco de dados.
    """
    try:
        db = await get_database()
        collection = db["formulario_terrenos_projetos"]
        
        # Busca por código existente
        resultado = await collection.find_one({"cod_projeto": codigo})
        
        return resultado is not None
        
    except Exception as e:
        logger.error(f"Erro ao verificar existência do código {codigo}: {e}")
        # Em caso de erro, assume que existe para evitar duplicatas
        return True


async def validar_codigo_projeto_unico(codigo: str) -> bool:
    """
    Valida se um código de projeto é único no sistema.
    Retorna True se único, False se já existe.
    """
    return not await codigo_projeto_existe(codigo)


def formatar_codigo_projeto(codigo: str) -> str:
    """
    Formata o código do projeto para exibição.
    Ex: ABC1234 -> ABC-1234
    """
    if len(codigo) == 7:
        return f"{codigo[:3]}-{codigo[3:]}"
    return codigo


def extrair_codigo_projeto_formatado(codigo_formatado: str) -> str:
    """
    Extrai o código do projeto removendo formatação.
    Ex: ABC-1234 -> ABC1234
    """
    return codigo_formatado.replace('-', '').upper()
