"""
Modelos Pydantic para Cadastro de Clientes.
"""
from datetime import datetime, date
from typing import Optional
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


class ClienteBase(BaseModel):
    """Modelo base para Cliente"""
    
    # Identificação básica
    nome_completo_razao_social: Optional[str] = Field(None, max_length=200, description="Nome completo ou razão social")
    cpf_cnpj: Optional[str] = Field(None, max_length=18, description="CPF ou CNPJ")
    rg_inscricao_estadual: Optional[str] = Field(None, max_length=50, description="RG ou Inscrição Estadual")
    data_nascimento_fundacao: Optional[date] = Field(None, description="Data de nascimento ou de fundação")
    
    # Contato
    telefone_principal: Optional[str] = Field(None, max_length=20, description="Telefone principal (celular/WhatsApp)")
    telefone_secundario: Optional[str] = Field(None, max_length=20, description="Telefone secundário")
    email: Optional[str] = Field(None, max_length=100, description="E-mail")
    redes_sociais: Optional[str] = Field(None, max_length=500, description="Redes sociais")
    
    # Endereço
    logradouro: Optional[str] = Field(None, max_length=200, description="Logradouro")
    numero: Optional[str] = Field(None, max_length=20, description="Número")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento")
    bairro: Optional[str] = Field(None, max_length=100, description="Bairro")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")
    estado: Optional[str] = Field(None, max_length=2, description="Estado/UF")
    cep: Optional[str] = Field(None, max_length=10, description="CEP")
    pais: Optional[str] = Field(default="BRASIL", max_length=50, description="País")

    @field_validator('cpf_cnpj')
    @classmethod
    def validate_cpf_cnpj(cls, v):
        """Valida formato do CPF/CNPJ"""
        if v:
            # Remove caracteres não numéricos
            cpf_cnpj_clean = ''.join(filter(str.isdigit, v))
            if len(cpf_cnpj_clean) not in [11, 14]:
                raise ValueError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos')
            return cpf_cnpj_clean
        return v

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        """Valida formato do estado (UF)"""
        if v and (len(v) != 2 or not v.isupper()):
            raise ValueError('Estado deve ser uma UF válida (2 letras maiúsculas)')
        return v

    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v):
        """Valida formato do CEP"""
        if v:
            # Remove caracteres não numéricos
            cep_clean = ''.join(filter(str.isdigit, v))
            if len(cep_clean) != 8:
                raise ValueError('CEP deve ter 8 dígitos')
            return cep_clean
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Valida formato do e-mail"""
        if v and '@' not in v:
            raise ValueError('E-mail deve ter formato válido')
        return v

    @field_validator('nome_completo_razao_social', 'logradouro', 'bairro', 'cidade', 'complemento', mode='before')
    @classmethod
    def convert_to_uppercase(cls, v):
        """Converte campos de texto para maiúsculas"""
        if isinstance(v, str):
            return v.upper()
        return v


class ClienteCreate(ClienteBase):
    """Modelo para criação de cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Modelo para atualização de cliente"""
    nome_completo_razao_social: Optional[str] = Field(None, min_length=1, max_length=200)
    cpf_cnpj: Optional[str] = Field(None, min_length=11, max_length=18)
    rg_inscricao_estadual: Optional[str] = Field(None, max_length=50)
    data_nascimento_fundacao: Optional[date] = None
    telefone_principal: Optional[str] = Field(None, max_length=20)
    telefone_secundario: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    redes_sociais: Optional[str] = Field(None, max_length=500)
    logradouro: Optional[str] = Field(None, max_length=200)
    numero: Optional[str] = Field(None, max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=2)
    cep: Optional[str] = Field(None, max_length=10)
    pais: Optional[str] = Field(None, max_length=50)


class ClienteInDB(ClienteBase):
    """Modelo interno do cliente no banco"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class Cliente(ClienteInDB):
    """Modelo público do cliente"""
    pass


class ClienteResponse(BaseModel):
    """Modelo para resposta de cliente"""
    success: bool
    message: str
    cliente: Optional[ClienteInDB] = None


class ClienteListResponse(BaseModel):
    """Modelo para lista de clientes"""
    success: bool
    message: str
    clientes: list[ClienteInDB] = []
    total: int = 0
