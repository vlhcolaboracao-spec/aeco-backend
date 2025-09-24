"""
Modelos Pydantic para Formulário de Terrenos de Projetos.
"""
from datetime import datetime
from typing import Optional, List, Dict, Union
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


class FormularioTerrenosProjetosBase(BaseModel):
    """Modelo base para Formulário de Terrenos de Projetos"""
    
    # Identificação do Projeto
    cod_projeto: Optional[str] = Field(None, min_length=7, max_length=7, description="Código único do projeto (7 caracteres) - gerado automaticamente")
    projeto_id: Optional[str] = Field(None, description="ID do projeto associado (opcional)")
    
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
    lados_poligono: int = Field(..., ge=3, le=10, description="Número de lados do polígono")
    angulos_internos: List[float] = Field(..., description="Lista de ângulos internos do polígono")
    dimensoes_lados: List[Dict[str, Union[str, float]]] = Field(..., description="Lista de dimensões dos lados do terreno")
    tipo_lote: str = Field(..., description="Tipo de lote: Padrão, Esquina, Único na Quadra")
    area: str = Field(..., min_length=1, max_length=20, description="Área total do terreno")
    norte_verdadeiro: float = Field(..., ge=0, lt=360, description="Norte verdadeiro em graus (máximo 2 casas decimais)")
    zona: str = Field(..., description="Zona conforme legislação de Sorriso/MT")
    
    # Observações
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")

    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v):
        """Valida formato do CEP"""
        # Remove caracteres não numéricos
        cep_clean = ''.join(filter(str.isdigit, v))
        if len(cep_clean) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return cep_clean

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        """Valida formato do estado (UF)"""
        if len(v) != 2 or not v.isupper():
            raise ValueError('Estado deve ser uma UF válida (2 letras maiúsculas)')
        return v

    @field_validator('lados_poligono')
    @classmethod
    def validate_lados_poligono(cls, v):
        """Valida número de lados do polígono"""
        if v < 3 or v > 10:
            raise ValueError('Número de lados deve estar entre 3 e 10')
        return v

    @field_validator('angulos_internos')
    @classmethod
    def validate_angulos_internos(cls, v, info):
        """Valida ângulos internos do polígono"""
        if not isinstance(v, list):
            raise ValueError('Ângulos internos deve ser uma lista')
        
        # Converte para float e verifica se todos os ângulos são números positivos
        angulos_convertidos = []
        for i, angulo in enumerate(v):
            try:
                angulo_float = float(angulo)
                if angulo_float <= 0 or angulo_float >= 180:
                    raise ValueError(f'Ângulo {i+1} deve estar entre 0 e 180 graus (valor: {angulo_float})')
                angulos_convertidos.append(angulo_float)
            except (ValueError, TypeError):
                raise ValueError(f'Ângulo {i+1} deve ser um número válido (valor: {angulo})')
        
        # Verifica se a soma não excede 360 graus
        soma_angulos = sum(angulos_convertidos)
        if soma_angulos > 360:
            raise ValueError(f'A soma dos ângulos internos ({soma_angulos:.2f}°) não pode exceder 360°')
        
        # Verifica se o número de ângulos corresponde ao número de lados
        lados = info.data.get('lados_poligono')
        if lados and len(angulos_convertidos) != lados:
            raise ValueError(f'Deve haver exatamente {lados} ângulos para {lados} lados')
        
        return angulos_convertidos

    @field_validator('dimensoes_lados')
    @classmethod
    def validate_dimensoes_lados(cls, v, info):
        """Valida dimensões dos lados do terreno"""
        if not isinstance(v, list):
            raise ValueError('Dimensões dos lados deve ser uma lista')
        
        lados = info.data.get('lados_poligono')
        if lados and len(v) != lados:
            raise ValueError(f'Deve haver exatamente {lados} dimensões para {lados} lados')
        
        dimensoes_validas = []
        for i, dimensao in enumerate(v):
            if not isinstance(dimensao, dict):
                raise ValueError(f'Dimensão {i+1} deve ser um objeto com tipo e medida')
            
            if 'tipo' not in dimensao or 'medida' not in dimensao:
                raise ValueError(f'Dimensão {i+1} deve ter campos "tipo" e "medida"')
            
            tipo = dimensao['tipo']
            tipos_validos = ['Alinhamento Predial', 'Fundos', 'Divisa Lateral']
            if tipo not in tipos_validos:
                raise ValueError(f'Tipo da dimensão {i+1} deve ser um dos seguintes: {", ".join(tipos_validos)}')
            
            try:
                medida_float = float(dimensao['medida'])
                if medida_float <= 0:
                    raise ValueError(f'Medida da dimensão {i+1} deve ser maior que zero')
                dimensoes_validas.append({
                    'tipo': tipo,
                    'medida': medida_float
                })
            except (ValueError, TypeError):
                raise ValueError(f'Medida da dimensão {i+1} deve ser um número válido')
        
        return dimensoes_validas

    @field_validator('tipo_lote')
    @classmethod
    def validate_tipo_lote(cls, v):
        """Valida tipo de lote"""
        tipos_validos = ['Padrão', 'Esquina', 'Único na Quadra']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de lote deve ser um dos seguintes: {", ".join(tipos_validos)}')
        return v

    @field_validator('projeto_id')
    @classmethod
    def validate_projeto_id(cls, v):
        """Valida ID do projeto"""
        if v is None:
            return None  # Permite None para terrenos sem projeto
        if not ObjectId.is_valid(v):
            raise ValueError('ID do projeto deve ser um ObjectId válido')
        return v

    @field_validator('norte_verdadeiro')
    @classmethod
    def validate_norte_verdadeiro(cls, v):
        """Valida norte verdadeiro com máximo 2 casas decimais"""
        if v < 0 or v >= 360:
            raise ValueError('Norte verdadeiro deve estar entre 0 e 360 graus')
        
        # Verifica se tem no máximo 2 casas decimais
        if round(v, 2) != v:
            raise ValueError('Norte verdadeiro deve ter no máximo 2 casas decimais')
        
        return v

    @field_validator('cod_projeto')
    @classmethod
    def validate_cod_projeto(cls, v):
        """Valida código do projeto"""
        if v is None:
            return None  # Permite None para geração automática
        if len(v) != 7:
            raise ValueError('Código do projeto deve ter exatamente 7 caracteres')
        if not v.isalnum():
            raise ValueError('Código do projeto deve conter apenas letras e números')
        return v.upper()

    @field_validator('zona')
    @classmethod
    def validate_zona(cls, v):
        """Valida zona conforme legislação de Sorriso/MT"""
        zonas_validas = [
            'ZAD1', 'ZAD2', 'ZC1', 'ZC2', 'ZCT1', 'ZCT2', 'ZCT3', 'ZCT4',
            'ZEIS', 'ZH1', 'ZH2', 'ZH3', 'ZHL', 'ZI1', 'ZI2', 'ZIA1', 'ZIA2', 'ZII'
        ]
        if v not in zonas_validas:
            raise ValueError(f'Zona deve ser uma das seguintes: {", ".join(zonas_validas)}')
        return v

    @field_validator('matricula', 'municipio', 'bairro', 'logradouro', 'numero', 'area', mode='before')
    @classmethod
    def convert_to_uppercase(cls, v):
        """Converte campos de texto para maiúsculas"""
        if isinstance(v, str):
            return v.upper()
        return v

    @field_validator('tipo_lote', mode='before')
    @classmethod
    def convert_tipo_lote_to_title(cls, v):
        """Converte tipo de lote para formato título"""
        if isinstance(v, str):
            return v.title()
        return v


class FormularioTerrenosProjetosCreate(FormularioTerrenosProjetosBase):
    """Modelo para criação de terreno"""
    pass


class FormularioTerrenosProjetosUpdate(BaseModel):
    """Modelo para atualização de terreno"""
    cod_projeto: Optional[str] = Field(None, min_length=7, max_length=7)
    projeto_id: Optional[str] = None
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
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

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
    terreno: Optional[FormularioTerrenosProjetosInDB] = None


class FormularioTerrenosProjetosListResponse(BaseModel):
    """Modelo para lista de terrenos"""
    success: bool
    message: str
    terrenos: List[FormularioTerrenosProjetosInDB] = []
    total: int = 0
