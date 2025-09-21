"""
Modelos Pydantic para Projetos.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
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
    """Modelo base para Projeto"""
    nome: str = Field(..., min_length=1, max_length=200, description="Nome do projeto")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição do projeto")
    status: str = Field(default="ativo", description="Status do projeto")
    responsavel: Optional[str] = Field(None, max_length=100, description="Responsável pelo projeto")


class ProjetoCreate(ProjetoBase):
    """Modelo para criação de projeto"""
    pass


class ProjetoUpdate(BaseModel):
    """Modelo para atualização de projeto"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    descricao: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None)
    responsavel: Optional[str] = Field(None, max_length=100)


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
    projeto: Optional[Projeto] = None


class ProjetosListResponse(BaseModel):
    """Modelo para lista de projetos"""
    success: bool
    message: str
    projetos: List[Projeto] = []
    total: int = 0
