"""
Modelos Pydantic para Formulário de Terrenos de Projetos.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from bson import ObjectId


class PyObjectId(ObjectId):
    """Classe para serializar ObjectId do MongoDB"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class FormularioTerrenosProjetosBase(BaseModel):
    """Modelo base para Formulário de Terrenos de Projetos"""
    
    # Identificação do Imóvel
    matricula: str = Field(..., min_length=1, max_length=50, description="Matrícula do imóvel")
    data: datetime = Field(..., description="Data do cadastro")
    
    # Localização
    municipio: str = Field(..., min_length=1, max_length=100, description="Município")
    estado: str = Field(..., min_length=2, max_length=2, description="Estado/UF")
    pais: str = Field(default="BRASIL", max_length=50, description="País")
    bairro: str = Field(..., min_length=1, max_length=100, description="Bairro")
    logradouro: str = Field(..., min_length=1, max_length=200, description="Logradouro/Rua")
    numero: str = Field(..., min_length=1, max_length=20, description="Número")
    cep: str = Field(..., min_length=8, max_length=10, description="CEP")
    
    # Características do Terreno
    lados_poligono: int = Field(..., ge=3, le=20, description="Número de lados do polígono")
    tipo_lote: str = Field(..., description="Tipo de lote (Esquina, Fundo, Meio, etc.)")
    area: float = Field(..., gt=0, description="Área em metros quadrados")
    norte_verdadeiro: float = Field(..., ge=0, lt=360, description="Norte verdadeiro em graus")
    zona: str = Field(..., description="Zona (Residencial, Comercial, etc.)")
    
    # Observações
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")

    @validator('cep')
    def validate_cep(cls, v):
        """Valida formato do CEP"""
        # Remove caracteres não numéricos
        cep_clean = ''.join(filter(str.isdigit, v))
        if len(cep_clean) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return cep_clean

    @validator('estado')
    def validate_estado(cls, v):
        """Valida formato do estado (UF)"""
        if len(v) != 2 or not v.isupper():
            raise ValueError('Estado deve ser uma UF válida (2 letras maiúsculas)')
        return v


class FormularioTerrenosProjetosCreate(FormularioTerrenosProjetosBase):
    """Modelo para criação de terreno"""
    pass


class FormularioTerrenosProjetosUpdate(BaseModel):
    """Modelo para atualização de terreno"""
    matricula: Optional[str] = Field(None, min_length=1, max_length=50)
    data: Optional[datetime] = None
    municipio: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    pais: Optional[str] = Field(None, max_length=50)
    bairro: Optional[str] = Field(None, min_length=1, max_length=100)
    logradouro: Optional[str] = Field(None, min_length=1, max_length=200)
    numero: Optional[str] = Field(None, min_length=1, max_length=20)
    cep: Optional[str] = Field(None, min_length=8, max_length=10)
    lados_poligono: Optional[int] = Field(None, ge=3, le=20)
    tipo_lote: Optional[str] = None
    area: Optional[float] = Field(None, gt=0)
    norte_verdadeiro: Optional[float] = Field(None, ge=0, lt=360)
    zona: Optional[str] = None
    observacoes: Optional[str] = Field(None, max_length=1000)


class FormularioTerrenosProjetosInDB(FormularioTerrenosProjetosBase):
    """Modelo interno do terreno no banco"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class FormularioTerrenosProjetos(FormularioTerrenosProjetosInDB):
    """Modelo público do terreno"""
    pass


class FormularioTerrenosProjetosResponse(BaseModel):
    """Modelo para resposta de terreno"""
    success: bool
    message: str
    terreno: Optional[FormularioTerrenosProjetos] = None


class FormularioTerrenosProjetosListResponse(BaseModel):
    """Modelo para lista de terrenos"""
    success: bool
    message: str
    terrenos: List[FormularioTerrenosProjetos] = []
    total: int = 0
