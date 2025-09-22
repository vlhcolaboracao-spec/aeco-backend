"""
Modelos Pydantic para Parâmetros Urbanísticos de Terrenos.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
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


class ParametroCalculado(BaseModel):
    """Modelo para um parâmetro calculado individual"""
    nome: str = Field(..., description="Nome do parâmetro")
    valor: Any = Field(..., description="Valor calculado do parâmetro")
    unidade: str = Field(..., description="Unidade de medida")
    regra_aplicada: str = Field(..., description="Descrição da regra aplicada")
    dependencias: List[str] = Field(default_factory=list, description="Lista de dependências usadas no cálculo")
    erro: Optional[str] = Field(None, description="Mensagem de erro se houver")


class ParametrosUrbanisticosBase(BaseModel):
    """Modelo base para parâmetros urbanísticos"""
    terreno_id: PyObjectId = Field(..., description="ID do terreno relacionado")
    municipio: str = Field(..., description="Município")
    legislacao: str = Field(default="LC_108_2009_ALTERADA_LC_415_2023", description="Legislação aplicada")
    data_calculo: datetime = Field(default_factory=datetime.now, description="Data do cálculo")
    
    # Parâmetros calculados
    recuo_frontal: Optional[ParametroCalculado] = Field(None, description="Recuo frontal")
    recuo_lateral: Optional[ParametroCalculado] = Field(None, description="Recuo lateral")
    recuo_fundos: Optional[ParametroCalculado] = Field(None, description="Recuo de fundos")
    testada_minima: Optional[ParametroCalculado] = Field(None, description="Testada mínima")
    altura_maxima: Optional[ParametroCalculado] = Field(None, description="Altura máxima permitida")
    outorga_onerosa: Optional[ParametroCalculado] = Field(None, description="Outorga onerosa")
    
    # Metadados
    status: str = Field(default="ativo", description="Status do registro")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")


class ParametrosUrbanisticosCreate(ParametrosUrbanisticosBase):
    """Modelo para criação de parâmetros urbanísticos"""
    pass


class ParametrosUrbanisticosUpdate(BaseModel):
    """Modelo para atualização de parâmetros urbanísticos"""
    recuo_frontal: Optional[ParametroCalculado] = None
    recuo_lateral: Optional[ParametroCalculado] = None
    recuo_fundos: Optional[ParametroCalculado] = None
    testada_minima: Optional[ParametroCalculado] = None
    altura_maxima: Optional[ParametroCalculado] = None
    outorga_onerosa: Optional[ParametroCalculado] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None


class ParametrosUrbanisticosInDB(ParametrosUrbanisticosBase):
    """Modelo interno dos parâmetros no banco"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class ParametrosUrbanisticos(ParametrosUrbanisticosInDB):
    """Modelo público dos parâmetros"""
    pass


class ParametrosUrbanisticosResponse(BaseModel):
    """Modelo para resposta de parâmetros urbanísticos"""
    success: bool
    message: str
    parametros: Optional[ParametrosUrbanisticosInDB] = None


class ParametrosUrbanisticosListResponse(BaseModel):
    """Modelo para lista de parâmetros urbanísticos"""
    success: bool
    message: str
    parametros: List[ParametrosUrbanisticosInDB] = []
    total: int = 0


class DadosCalculoParametros(BaseModel):
    """Modelo para dados necessários para cálculo dos parâmetros"""
    zona: str = Field(..., description="Zona do terreno")
    tipologia: str = Field(..., description="Tipologia (Residencial/Comercial/Misto)")
    municipio: str = Field(default="SORRISO", description="Município")
    
    # Dados opcionais para cálculos dinâmicos
    pavimentos: Optional[int] = Field(None, description="Número de pavimentos")
    altura_total: Optional[float] = Field(None, description="Altura total em metros")
    avenida: Optional[str] = Field(None, description="Avenida para zonas especiais")
    natureza: Optional[str] = Field(None, description="Natureza do empreendimento")
    
    # Dados para herança de zonas de transição
    zona_atravessada: Optional[str] = Field(None, description="Zona atravessada para ZCT")
