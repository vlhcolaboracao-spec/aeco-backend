"""
Modelos Pydantic para Cadastro de Projetos.
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
    """Modelo base para Cadastro de Projetos"""
    
    # Dados do Cliente
    nome_completo: Optional[str] = Field(None, max_length=200, description="Nome completo do cliente")
    contato: Optional[str] = Field(None, max_length=200, description="Telefone/e-mail do cliente")
    estado_civil_composicao: Optional[str] = Field(None, max_length=200, description="Estado civil / composição familiar")
    profissao_rotina: Optional[str] = Field(None, max_length=200, description="Profissão / rotina")
    
    # Programa de Necessidades
    tipologia: Optional[str] = Field(None, max_length=100, description="Tipologia (residencial, comercial, institucional, mista)")
    ambientes_desejados: Optional[str] = Field(None, max_length=500, description="Ambientes desejados (quantos quartos, banheiros, salas, etc.)")
    prioridades: Optional[str] = Field(None, max_length=500, description="Prioridades (ex.: cozinha integrada, área gourmet, garagem ampla)")
    
    # Estilo e Referências
    estilo_arquitetonico: Optional[str] = Field(None, max_length=200, description="Estilo arquitetônico preferido (moderno, clássico, rústico, minimalista)")
    materiais_interesse: Optional[str] = Field(None, max_length=500, description="Materiais de interesse (madeira, vidro, concreto, tijolo aparente)")
    exemplos_referencias: Optional[str] = Field(None, max_length=1000, description="Exemplos de projetos/referências que agradam")
    
    # Rotina e Funcionalidade
    uso_espacos_dia_dia: Optional[str] = Field(None, max_length=500, description="Como a família utiliza os espaços no dia a dia")
    animais_estimacao: Optional[str] = Field(None, max_length=200, description="Há animais de estimação")
    necessidades_especiais: Optional[str] = Field(None, max_length=500, description="Necessidades especiais (acessibilidade, home office, ateliê, etc.)")
    frequencia_visitas: Optional[str] = Field(None, max_length=300, description="Frequência de visitas/recepção de convidados")
    
    # Aspectos Financeiros e Prazos
    orcamento_estimado: Optional[str] = Field(None, max_length=200, description="Orçamento estimado para a obra")
    fonte_recursos: Optional[str] = Field(None, max_length=200, description="Fonte de recursos (financiamento, recursos próprios)")
    prazo_entrega: Optional[str] = Field(None, max_length=200, description="Prazo de entrega esperado")
    
    # Sustentabilidade e Tecnologia
    solucoes_sustentaveis: Optional[str] = Field(None, max_length=500, description="Interesse em soluções sustentáveis (energia solar, captação de água da chuva, ventilação cruzada)")
    nivel_automacao: Optional[str] = Field(None, max_length=300, description="Nível de automação desejado (casa inteligente, segurança, climatização)")
    
    # Observações do Cliente
    desejos_expectativas: Optional[str] = Field(None, max_length=1000, description="Desejos e expectativas específicas")
    restricoes: Optional[str] = Field(None, max_length=500, description="Restrições (o que não pode ter de jeito nenhum)")
    
    # Dados de controle
    data_cadastro: Optional[datetime] = Field(default_factory=datetime.now, description="Data do cadastro")
    observacoes_internas: Optional[str] = Field(None, max_length=1000, description="Observações internas")

    @field_validator('tipologia')
    @classmethod
    def validate_tipologia(cls, v):
        """Valida tipologia do projeto"""
        if v is not None:
            tipologias_validas = ['residencial', 'comercial', 'institucional', 'mista']
            if v.lower() not in tipologias_validas:
                raise ValueError(f'Tipologia deve ser uma das seguintes: {", ".join(tipologias_validas)}')
        return v

    @field_validator('estilo_arquitetonico')
    @classmethod
    def validate_estilo_arquitetonico(cls, v):
        """Valida estilo arquitetônico"""
        if v is not None:
            estilos_validos = ['moderno', 'clássico', 'rústico', 'minimalista', 'contemporâneo', 'tradicional', 'ecletismo']
            if v.lower() not in estilos_validos:
                raise ValueError(f'Estilo arquitetônico deve ser um dos seguintes: {", ".join(estilos_validos)}')
        return v

    @field_validator('nome_completo', mode='before')
    @classmethod
    def convert_to_uppercase(cls, v):
        """Converte campos de texto para maiúsculas"""
        if isinstance(v, str):
            return v.upper()
        return v

    @field_validator('tipologia', 'estilo_arquitetonico', mode='before')
    @classmethod
    def convert_to_lowercase(cls, v):
        """Converte campos específicos para minúsculas"""
        if isinstance(v, str):
            return v.lower()
        return v


class ProjetoCreate(ProjetoBase):
    """Modelo para criação de projeto"""
    pass


class ProjetoUpdate(BaseModel):
    """Modelo para atualização de projeto"""
    nome_completo: Optional[str] = Field(None, max_length=200)
    contato: Optional[str] = Field(None, max_length=200)
    estado_civil_composicao: Optional[str] = Field(None, max_length=200)
    profissao_rotina: Optional[str] = Field(None, max_length=200)
    tipologia: Optional[str] = Field(None, max_length=100)
    ambientes_desejados: Optional[str] = Field(None, max_length=500)
    prioridades: Optional[str] = Field(None, max_length=500)
    estilo_arquitetonico: Optional[str] = Field(None, max_length=200)
    materiais_interesse: Optional[str] = Field(None, max_length=500)
    exemplos_referencias: Optional[str] = Field(None, max_length=1000)
    uso_espacos_dia_dia: Optional[str] = Field(None, max_length=500)
    animais_estimacao: Optional[str] = Field(None, max_length=200)
    necessidades_especiais: Optional[str] = Field(None, max_length=500)
    frequencia_visitas: Optional[str] = Field(None, max_length=300)
    orcamento_estimado: Optional[str] = Field(None, max_length=200)
    fonte_recursos: Optional[str] = Field(None, max_length=200)
    prazo_entrega: Optional[str] = Field(None, max_length=200)
    solucoes_sustentaveis: Optional[str] = Field(None, max_length=500)
    nivel_automacao: Optional[str] = Field(None, max_length=300)
    desejos_expectativas: Optional[str] = Field(None, max_length=1000)
    restricoes: Optional[str] = Field(None, max_length=500)
    observacoes_internas: Optional[str] = Field(None, max_length=1000)


class ProjetoInDB(ProjetoBase):
    """Modelo interno do projeto no banco"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

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


class ProjetosListResponse(BaseModel):
    """Modelo para lista de projetos"""
    success: bool
    message: str
    projetos: List[ProjetoInDB] = []
    total: int = 0