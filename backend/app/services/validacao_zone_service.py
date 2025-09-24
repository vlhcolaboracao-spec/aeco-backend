"""
Serviço para validações dinâmicas por zona urbana.
"""
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ValidacaoZoneService:
    """Serviço para validações dinâmicas baseadas na zona urbana"""
    
    def __init__(self):
        # Zonas que requerem avenida
        self.zonas_com_avenida = {"ZCT2", "ZCT4"}
        
        # Zonas que requerem cálculos dinâmicos
        self.zonas_com_recuos_dinamicos = {
            "ZC1", "ZC2", "ZAD1", "ZAD2", "ZH1", "ZH2", "ZH3", 
            "ZCT1", "ZCT2", "ZCT3", "ZCT4", "ZEIS"
        }
        
        # Zonas que requerem testada mínima
        self.zonas_com_testada = {
            "ZAD1", "ZAD2", "ZH2", "ZH3", "ZCT2", "ZCT3", "ZCT4"
        }
        
        # Naturezas que requerem testada e área mínima
        self.naturezas_com_testada = {
            "Desmembramento", "Loteamento e Condomínio"
        }
        
        # Naturezas que requerem dados técnicos específicos
        self.naturezas_arquitetonico = {
            "Arquitetonico"
        }
        
        self.naturezas_urbanistico = {
            "Urbanistico"
        }
    
    def get_dependencias_por_zona(self, zona: str) -> Dict[str, Any]:
        """
        Retorna as dependências de campos baseadas na zona
        
        Args:
            zona: Zona urbana selecionada
            
        Returns:
            Dict com informações sobre campos obrigatórios e opcionais
        """
        try:
            zona = zona.strip().upper()
            
            dependencias = {
                "zona": zona,
                "campos_obrigatorios": [],
                "campos_opcionais": [],
                "campos_condicionais": {},
                "mensagens": [],
                "preview_parametros": []
            }
            
            # Campos sempre obrigatórios para qualquer zona
            dependencias["campos_obrigatorios"].extend([
                "tipo_empreendimento",
                "natureza"
            ])
            
            # Campos obrigatórios para recuos dinâmicos
            if zona in self.zonas_com_recuos_dinamicos:
                dependencias["campos_obrigatorios"].extend([
                    "pavimentos",
                    "altura_total"
                ])
                dependencias["mensagens"].append(
                    "⚠️ Pavimentos e altura são obrigatórios para cálculo de recuos laterais e de fundos"
                )
            
            # Campo avenida para zonas específicas
            if zona in self.zonas_com_avenida:
                dependencias["campos_obrigatorios"].append("avenida")
                dependencias["campos_condicionais"]["avenida"] = {
                    "obrigatorio": True,
                    "motivo": "Necessário para cálculo de altura máxima e outorga onerosa",
                    "opcoes": [
                        "Av. Porto Alegre",
                        "Av. dos Emigrantes",
                        "Av. Paulista",
                        "Av. Brasil",
                        "Av. Joao Natalino Brescansin",
                        "Av. Tancredo Neves"
                    ]
                }
                dependencias["mensagens"].append(
                    "ℹ️ Campo avenida é obrigatório para zonas ZCT2 e ZCT4"
                )
            
            # Testada mínima para zonas específicas
            if zona in self.zonas_com_testada:
                dependencias["campos_condicionais"]["testada_minima"] = {
                    "obrigatorio_por_natureza": True,
                    "naturezas_validas": list(self.naturezas_com_testada),
                    "motivo": "Aplicável apenas para loteamentos e desmembramentos"
                }
                dependencias["mensagens"].append(
                    "ℹ️ Testada mínima aplicável para loteamentos e desmembramentos"
                )
            
            # Área mínima do lote (condicional por natureza)
            dependencias["campos_condicionais"]["area_minima_lote"] = {
                "obrigatorio_por_natureza": True,
                "naturezas_validas": list(self.naturezas_com_testada),
                "motivo": "Área mínima do lote para projetos de loteamento"
            }
            
            # Preview dos parâmetros que serão calculados
            dependencias["preview_parametros"] = self._get_preview_parametros(zona)
            
            return dependencias
            
        except Exception as e:
            logger.error(f"Erro ao obter dependências da zona {zona}: {e}")
            return {
                "zona": zona,
                "erro": f"Erro interno: {str(e)}",
                "campos_obrigatorios": ["tipo_empreendimento", "natureza"],
                "campos_opcionais": [],
                "campos_condicionais": {},
                "mensagens": [],
                "preview_parametros": []
            }
    
    def _get_preview_parametros(self, zona: str) -> List[Dict[str, Any]]:
        """
        Retorna preview dos parâmetros que serão calculados para a zona
        
        Args:
            zona: Zona urbana
            
        Returns:
            Lista com preview dos parâmetros
        """
        parametros = [
            {
                "nome": "recuo_frontal",
                "descricao": "Recuo frontal",
                "dependencias": ["zona", "tipo_empreendimento"],
                "calculavel": True
            }
        ]
        
        if zona in self.zonas_com_recuos_dinamicos:
            parametros.extend([
                {
                    "nome": "recuo_lateral",
                    "descricao": "Recuo lateral",
                    "dependencias": ["zona", "pavimentos", "altura_total"],
                    "calculavel": True
                },
                {
                    "nome": "recuo_fundos",
                    "descricao": "Recuo de fundos",
                    "dependencias": ["zona", "pavimentos", "altura_total"],
                    "calculavel": True
                }
            ])
        
        if zona in self.zonas_com_testada:
            parametros.append({
                "nome": "testada_minima",
                "descricao": "Testada mínima",
                "dependencias": ["zona", "natureza"],
                "calculavel": True,
                "condicional": "Apenas para loteamentos e desmembramentos"
            })
        
        if zona in self.zonas_com_avenida:
            parametros.extend([
                {
                    "nome": "altura_maxima",
                    "descricao": "Altura máxima",
                    "dependencias": ["zona", "avenida"],
                    "calculavel": True
                },
                {
                    "nome": "outorga_onerosa",
                    "descricao": "Outorga onerosa",
                    "dependencias": ["zona", "avenida"],
                    "calculavel": True
                }
            ])
        else:
            parametros.extend([
                {
                    "nome": "altura_maxima",
                    "descricao": "Altura máxima",
                    "dependencias": ["zona"],
                    "calculavel": True
                },
                {
                    "nome": "outorga_onerosa",
                    "descricao": "Outorga onerosa",
                    "dependencias": ["zona"],
                    "calculavel": True
                }
            ])
        
        return parametros
    
    def validate_campos_por_natureza(self, natureza: str, campos_preenchidos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida campos baseados na natureza do empreendimento
        
        Args:
            natureza: Natureza do empreendimento
            campos_preenchidos: Campos já preenchidos
            
        Returns:
            Dict com validações específicas por natureza
        """
        try:
            validacao = {
                "natureza": natureza,
                "campos_obrigatorios": [],
                "campos_opcionais": [],
                "campos_ignorados": [],
                "mensagens": []
            }
            
            if natureza == "Não se aplica":
                # Para "Não se aplica", ignora testada e área mínima
                validacao["campos_ignorados"].extend([
                    "testada_minima",
                    "area_minima_lote"
                ])
                validacao["mensagens"].append(
                    "ℹ️ Testada mínima e área mínima do lote não se aplicam para este tipo de projeto"
                )
                
            elif natureza in self.naturezas_com_testada:
                # Para loteamentos e desmembramentos, testada e área são obrigatórias
                validacao["campos_obrigatorios"].extend([
                    "testada_minima",
                    "area_minima_lote"
                ])
                validacao["mensagens"].append(
                    "⚠️ Testada mínima e área mínima do lote são obrigatórias para loteamentos e desmembramentos"
                )
                
            elif natureza in self.naturezas_arquitetonico:
                # Para projetos arquitetônicos, dados técnicos são obrigatórios
                validacao["campos_obrigatorios"].extend([
                    "pavimentos",
                    "altura_total",
                    "area_construida"
                ])
                validacao["mensagens"].append(
                    "⚠️ Pavimentos, altura total e área construída são obrigatórios para projetos arquitetônicos"
                )
                
            elif natureza in self.naturezas_urbanistico:
                # Para projetos urbanísticos, área total é obrigatória
                validacao["campos_obrigatorios"].extend([
                    "area_construida"
                ])
                validacao["mensagens"].append(
                    "⚠️ Área construída é obrigatória para projetos urbanísticos"
                )
            
            return validacao
            
        except Exception as e:
            logger.error(f"Erro ao validar campos por natureza {natureza}: {e}")
            return {
                "natureza": natureza,
                "erro": f"Erro interno: {str(e)}",
                "campos_obrigatorios": [],
                "campos_opcionais": [],
                "campos_ignorados": [],
                "mensagens": []
            }
    
    def get_campos_condicionais_por_zona_e_natureza(self, zona: str, natureza: str) -> Dict[str, Any]:
        """
        Retorna campos condicionais baseados na combinação zona + natureza
        
        Args:
            zona: Zona urbana
            natureza: Natureza do empreendimento
            
        Returns:
            Dict com campos condicionais
        """
        try:
            zona = zona.strip().upper()
            natureza = natureza.strip()
            
            condicionais = {
                "zona": zona,
                "natureza": natureza,
                "campos_visiveis": [],
                "campos_ocultos": [],
                "campos_obrigatorios": [],
                "campos_opcionais": []
            }
            
            # Lógica para testada mínima
            if zona in self.zonas_com_testada:
                if natureza in self.naturezas_com_testada:
                    condicionais["campos_visiveis"].append("testada_minima")
                    condicionais["campos_obrigatorios"].append("testada_minima")
                elif natureza == "Não se aplica":
                    condicionais["campos_ocultos"].append("testada_minima")
            
            # Lógica para área mínima do lote
            if natureza in self.naturezas_com_testada:
                condicionais["campos_visiveis"].append("area_minima_lote")
                condicionais["campos_obrigatorios"].append("area_minima_lote")
            elif natureza in ["Não se aplica", "Arquitetonico", "Urbanistico"]:
                condicionais["campos_ocultos"].append("area_minima_lote")
            
            # Lógica para campos técnicos específicos
            if natureza in self.naturezas_arquitetonico:
                condicionais["campos_obrigatorios"].extend([
                    "pavimentos", "altura_total", "area_construida"
                ])
            elif natureza in self.naturezas_urbanistico:
                condicionais["campos_obrigatorios"].append("area_construida")
            
            # Lógica para avenida
            if zona in self.zonas_com_avenida:
                condicionais["campos_visiveis"].append("avenida")
                condicionais["campos_obrigatorios"].append("avenida")
            else:
                condicionais["campos_ocultos"].append("avenida")
            
            return condicionais
            
        except Exception as e:
            logger.error(f"Erro ao obter campos condicionais {zona}+{natureza}: {e}")
            return {
                "zona": zona,
                "natureza": natureza,
                "erro": f"Erro interno: {str(e)}",
                "campos_visiveis": [],
                "campos_ocultos": [],
                "campos_obrigatorios": [],
                "campos_opcionais": []
            }


# Instância global do serviço
validacao_zone_service = ValidacaoZoneService()
