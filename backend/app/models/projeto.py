"""
Modelos Pydantic para Projetos.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class PyObjectId(ObjectId):
    """Classe para serializar ObjectId do MongoDB"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProjetoBase(BaseModel):
    """Modelo base para Projetos"""
    
    # Identificação do Projeto
    cod_projeto: Optional[str] = Field(None, min_length=7, max_length=7, description="Código único do projeto (7 caracteres)")
    nome_projeto: str = Field(..., min_length=1, max_length=200, description="Nome do projeto")
    
    # Relacionamentos (opcionais)
    cliente_id: Optional[str] = Field(None, description="ID do cliente proprietário (opcional)")
    terreno_id: Optional[str] = Field(None, description="ID do terreno onde será executado")
    
    # Características do Empreendimento
    tipo_empreendimento: str = Field(..., description="Tipo: Residencial, Comercial, Misto")
    natureza: str = Field(..., description="Natureza: Desmembramento, Loteamento e Condomínio")
    
    # Dados Técnicos
    pavimentos: Optional[int] = Field(None, ge=1, le=50, description="Número de pavimentos")
    altura_total: Optional[float] = Field(None, gt=0, le=200, description="Altura total em metros")
    area_construida: Optional[float] = Field(None, gt=0, description="Área construída em m²")
    area_minima_lote: Optional[float] = Field(None, gt=0, description="Área mínima do lote em m² (para loteamentos)")
    
    # Dados Especiais (para zonas específicas)
    avenida: Optional[str] = Field(None, max_length=200, description="Avenida (para zonas ZCT2/ZCT4)")
    
    # Informações Adicionais
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição do projeto")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")
    
    # Status
    status: str = Field(default="ativo", description="Status do projeto")

    @field_validator('cod_projeto')
    @classmethod
    def validate_cod_projeto(cls, v):
        """Valida código do projeto"""
        if v is None:
            return None  # Será gerado automaticamente pelo repositório
        if len(v) != 7:
            raise ValueError('Código do projeto deve ter exatamente 7 caracteres')
        if not v.isalnum():
            raise ValueError('Código do projeto deve conter apenas letras e números')
        return v.upper()

    @field_validator('tipo_empreendimento')
    @classmethod
    def validate_tipo_empreendimento(cls, v):
        """Valida tipo de empreendimento"""
        tipos_validos = ['Residencial', 'Comercial', 'Misto']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de empreendimento deve ser um dos seguintes: {", ".join(tipos_validos)}')
        return v

    @field_validator('natureza')
    @classmethod
    def validate_natureza(cls, v):
        """Valida natureza do empreendimento"""
        naturezas_validas = [
            'Desmembramento', 
            'Loteamento e Condomínio', 
            'Arquitetonico',
            'Urbanistico',
            'Não se aplica'
        ]
        if v not in naturezas_validas:
            raise ValueError(f'Natureza deve ser uma das seguintes: {", ".join(naturezas_validas)}')
        return v

    @field_validator('avenida')
    @classmethod
    def validate_avenida(cls, v):
        """Valida avenida para zonas especiais"""
        if v is None:
            return None
        
        avenidas_validas = [
            "Av. Porto Alegre",
            "Av. dos Emigrantes", 
            "Av. Paulista",
            "Av. Brasil",
            "Av. Joao Natalino Brescansin",
            "Av. Tancredo Neves"
        ]
        
        if v not in avenidas_validas:
            raise ValueError(f'Avenida deve ser uma das seguintes: {", ".join(avenidas_validas)}')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Valida status do projeto"""
        status_validos = ['ativo', 'inativo', 'concluido', 'cancelado']
        if v not in status_validos:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(status_validos)}')
        return v

    @field_validator('nome_projeto', 'descricao', 'observacoes', mode='before')
    @classmethod
    def convert_to_uppercase(cls, v):
        """Converte campos de texto para maiúsculas"""
        if isinstance(v, str):
            return v.upper()
        return v


class ProjetoCreate(ProjetoBase):
    """Modelo para criação de projeto"""
    pass


class ProjetoUpdate(BaseModel):
    """Modelo para atualização de projeto"""
    nome_projeto: Optional[str] = Field(None, min_length=1, max_length=200)
    cliente_id: Optional[str] = None
    terreno_id: Optional[str] = None
    tipo_empreendimento: Optional[str] = None
    natureza: Optional[str] = None
    pavimentos: Optional[int] = Field(None, ge=1, le=50)
    altura_total: Optional[float] = Field(None, gt=0, le=200)
    area_construida: Optional[float] = Field(None, gt=0)
    area_minima_lote: Optional[float] = Field(None, gt=0)
    avenida: Optional[str] = Field(None, max_length=200)
    descricao: Optional[str] = Field(None, max_length=1000)
    observacoes: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None


class ProjetoInDB(ProjetoBase):
    """Modelo interno do projeto no banco"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class Projeto(ProjetoInDB):
    """Modelo público do projeto"""
    pass


class ProjetoResponse(BaseModel):
    """Modelo para resposta de projeto"""
    success: bool
    message: str
    projeto: Optional[ProjetoInDB] = None


class ProjetoListResponse(BaseModel):
    """Modelo para lista de projetos"""
    success: bool
    message: str
    projetos: List[ProjetoInDB] = []
    total: int = 0


class ProjetoComDadosCompletos(BaseModel):
    """Modelo para projeto com dados relacionados"""
    projeto: ProjetoInDB
    cliente: Optional[dict] = None  # Dados do cliente se associado
    terreno: Optional[dict] = None  # Dados do terreno se associado
    parametros_urbanisticos: Optional[dict] = None  # Parâmetros calculados