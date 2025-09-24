"""
Service para cálculo de parâmetros urbanísticos conforme LC 108/2009 - ALTERADA PELA LC 415-2023.
"""
from typing import Dict, Any, Optional, List
import logging
from ..models.parametros_urbanisticos import ParametroCalculado, DadosCalculoParametros

logger = logging.getLogger(__name__)


class ParametrosUrbanisticosService:
    """Service para cálculo de parâmetros urbanísticos"""
    
    def __init__(self):
        self.legislacao = "LC_108_2009_ALTERADA_LC_415_2023"
    
    async def calcular_todos_parametros(self, dados: DadosCalculoParametros) -> Dict[str, ParametroCalculado]:
        """
        Calcula todos os parâmetros urbanísticos para um terreno
        """
        parametros = {}
        
        try:
            # Recuo Frontal
            parametros["recuo_frontal"] = self._calcular_recuo_frontal(dados.zona, dados.tipo_empreendimento)
            
            # Recuo Lateral
            parametros["recuo_lateral"] = self._calcular_recuo_lateral(
                dados.zona, 
                dados.pavimentos, 
                dados.altura_total,
                dados.zona_atravessada
            )
            
            # Recuo de Fundos
            parametros["recuo_fundos"] = self._calcular_recuo_fundos(
                dados.zona,
                dados.pavimentos,
                dados.altura_total,
                dados.zona_atravessada
            )
            
            # Testada Mínima
            parametros["testada_minima"] = self._calcular_testada_minima(
                dados.zona,
                dados.natureza
            )
            
            # Altura Máxima
            parametros["altura_maxima"] = self._calcular_altura_maxima(
                dados.zona,
                dados.avenida
            )
            
            # Outorga Onerosa
            parametros["outorga_onerosa"] = self._calcular_outorga_onerosa(
                dados.zona,
                dados.avenida
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular parâmetros: {e}")
            raise
        
        return parametros
    
    def _calcular_recuo_frontal(self, zona: str, tipologia: str) -> ParametroCalculado:
        """
        Calcula recuo frontal conforme LC 108/2009
        """
        # Normaliza entradas
        zona = zona.strip().upper()
        tipologia = tipologia.strip().capitalize()
        
        zonas_padrao = {"ZC1", "ZC2", "ZAD1", "ZAD2", "ZH2", "ZH3", "ZCT1", "ZCT2", "ZCT3"}
        
        try:
            if zona in zonas_padrao:
                if tipologia == "Residencial":
                    valor = 4.0
                    regra = f"Zona {zona} - Uso Residencial"
                elif tipologia == "Comercial":
                    valor = 1.5
                    regra = f"Zona {zona} - Uso Comercial"
                else:
                    return ParametroCalculado(
                        nome="recuo_frontal",
                        valor=None,
                        unidade="metros",
                        regra_aplicada=f"Zona {zona} - Uso {tipologia}",
                        dependencias=["zona", "tipologia"],
                        erro=f"⚠️ Uso {tipologia} não reconhecido para zona {zona}"
                    )
                    
            elif zona == "ZEIS":
                if tipologia == "Residencial":
                    valor = 2.0
                    regra = f"Zona {zona} - Uso Residencial"
                elif tipologia == "Comercial":
                    valor = 1.5
                    regra = f"Zona {zona} - Uso Comercial"
                else:
                    return ParametroCalculado(
                        nome="recuo_frontal",
                        valor=None,
                        unidade="metros",
                        regra_aplicada=f"Zona {zona} - Uso {tipologia}",
                        dependencias=["zona", "tipologia"],
                        erro=f"⚠️ Uso {tipologia} não reconhecido para zona {zona}"
                    )
            else:
                return ParametroCalculado(
                    nome="recuo_frontal",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona"],
                    erro=f"⚠️ Zona {zona} não encontrada"
                )
            
            return ParametroCalculado(
                nome="recuo_frontal",
                valor=valor,
                unidade="metros",
                regra_aplicada=regra,
                dependencias=["zona", "tipologia"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular recuo frontal: {e}")
            return ParametroCalculado(
                nome="recuo_frontal",
                valor=None,
                unidade="metros",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "tipologia"],
                erro=f"Erro interno: {str(e)}"
            )
    
    def _calcular_recuo_lateral(self, zona: str, pavimentos: Optional[int] = None, 
                               altura_total: Optional[float] = None, 
                               zona_atravessada: Optional[str] = None) -> ParametroCalculado:
        """
        Calcula recuo lateral conforme LC 108/2009
        """
        try:
            zona = zona.strip().upper()
            zona_ref = zona
            
            # Se for zona de transição (ZCT), usar zona atravessada
            if zona.startswith("ZCT") and zona_atravessada:
                zona_ref = zona_atravessada.strip().upper()
                # TODO: Implementar busca de recuo fixo no MongoDB quando disponível
                # Por enquanto, usa a regra dinâmica
            
            # Validações para cálculos dinâmicos
            if pavimentos is None or altura_total is None:
                return ParametroCalculado(
                    nome="recuo_lateral",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona", "pavimentos", "altura_total"],
                    erro="⚠️ Dados insuficientes para cálculo (pavimentos e altura total necessários)"
                )
            
            # Definição de grupos de zonas
            grupo_min_15 = {"ZC1", "ZC2", "ZAD1", "ZAD2", "ZH1", "ZH2", "ZH3", "ZHL", "ZEIS"}
            grupo_min_20 = {"ZI1", "ZI2"}
            
            if zona_ref in grupo_min_15:
                min_recuo = 1.5
            elif zona_ref in grupo_min_20:
                min_recuo = 2.0
            else:
                return ParametroCalculado(
                    nome="recuo_lateral",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona"],
                    erro=f"⚠️ Zona {zona} não cadastrada em nenhuma regra"
                )
            
            # Aplicação da regra
            if pavimentos <= 2:
                valor = f"0 m (exceto se houver aberturas → mínimo {min_recuo:.1f} m)"
                regra = f"Zona {zona} - Até 2 pavimentos"
            else:
                recuo_calc = altura_total / 10
                recuo_final = max(recuo_calc, min_recuo)
                valor = f"{recuo_final:.2f} m"
                regra = f"Zona {zona} - {pavimentos} pavimentos, altura {altura_total:.1f}m"
            
            return ParametroCalculado(
                nome="recuo_lateral",
                valor=valor,
                unidade="metros",
                regra_aplicada=regra,
                dependencias=["zona", "pavimentos", "altura_total"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular recuo lateral: {e}")
            return ParametroCalculado(
                nome="recuo_lateral",
                valor=None,
                unidade="metros",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "pavimentos", "altura_total"],
                erro=f"Erro interno: {str(e)}"
            )
    
    def _calcular_recuo_fundos(self, zona: str, pavimentos: Optional[int] = None,
                              altura_total: Optional[float] = None,
                              zona_atravessada: Optional[str] = None) -> ParametroCalculado:
        """
        Calcula recuo de fundos conforme LC 108/2009
        (Mesma lógica do recuo lateral)
        """
        try:
            zona = zona.strip().upper()
            zona_ref = zona
            
            # Se for zona de transição (ZCT), usar zona atravessada
            if zona.startswith("ZCT") and zona_atravessada:
                zona_ref = zona_atravessada.strip().upper()
            
            # Validações para cálculos dinâmicos
            if pavimentos is None or altura_total is None:
                return ParametroCalculado(
                    nome="recuo_fundos",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona", "pavimentos", "altura_total"],
                    erro="⚠️ Dados insuficientes para cálculo (pavimentos e altura total necessários)"
                )
            
            # Definição de grupos de zonas
            grupo_min_15 = {"ZC1", "ZC2", "ZAD1", "ZAD2", "ZH1", "ZH2", "ZH3", "ZHL", "ZEIS"}
            grupo_min_20 = {"ZI1", "ZI2"}
            
            if zona_ref in grupo_min_15:
                min_recuo = 1.5
            elif zona_ref in grupo_min_20:
                min_recuo = 2.0
            else:
                return ParametroCalculado(
                    nome="recuo_fundos",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona"],
                    erro=f"⚠️ Zona {zona} não cadastrada em nenhuma regra"
                )
            
            # Aplicação da regra
            if pavimentos <= 2:
                valor = f"0 m (exceto se houver aberturas → mínimo {min_recuo:.1f} m)"
                regra = f"Zona {zona} - Até 2 pavimentos"
            else:
                recuo_calc = altura_total / 10
                recuo_final = max(recuo_calc, min_recuo)
                valor = f"{recuo_final:.2f} m"
                regra = f"Zona {zona} - {pavimentos} pavimentos, altura {altura_total:.1f}m"
            
            return ParametroCalculado(
                nome="recuo_fundos",
                valor=valor,
                unidade="metros",
                regra_aplicada=regra,
                dependencias=["zona", "pavimentos", "altura_total"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular recuo de fundos: {e}")
            return ParametroCalculado(
                nome="recuo_fundos",
                valor=None,
                unidade="metros",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "pavimentos", "altura_total"],
                erro=f"Erro interno: {str(e)}"
            )
    
    def _calcular_testada_minima(self, zona: str, natureza: Optional[str] = None) -> ParametroCalculado:
        """
        Calcula testada mínima conforme LC 108/2009
        """
        try:
            zona = zona.strip().upper()
            natureza = natureza.strip().lower() if natureza else None
            
            # Dicionário de regras: (zona, natureza) -> valor do parâmetro
            regras = {
                ("ZAD1", "desmembramento"): 10.0,
                ("ZAD1", "loteamento e condominio"): 15.0,
                ("ZAD2", "desmembramento"): 10.0,
                ("ZAD2", "loteamento e condominio"): 15.0,
                ("ZH2", "desmembramento"): 10.0,
                ("ZH2", "loteamento e condominio"): 15.0,
                ("ZH3", "desmembramento"): 10.0,
                ("ZH3", "loteamento e condominio"): 12.0,
                ("ZCT2", "desmembramento"): 10.0,
                ("ZCT2", "loteamento e condominio"): 15.0,
                ("ZCT3", "desmembramento"): 10.0,
                ("ZCT3", "loteamento e condominio"): 15.0,
                ("ZCT4", "desmembramento"): 10.0,
                ("ZCT4", "loteamento e condominio"): 15.0,
            }
            
            # Se natureza é "Não se aplica", retorna valor None (não aplicável)
            if natureza == "não se aplica":
                return ParametroCalculado(
                    nome="testada_minima",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona} - Não se aplica",
                    dependencias=["zona", "natureza"],
                    erro=None  # Não é erro, apenas não se aplica
                )
            
            if not natureza:
                return ParametroCalculado(
                    nome="testada_minima",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona", "natureza"],
                    erro="⚠️ Natureza do empreendimento necessária para cálculo"
                )
            
            parametro = regras.get((zona, natureza))
            
            if parametro is None:
                return ParametroCalculado(
                    nome="testada_minima",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona} - Natureza {natureza}",
                    dependencias=["zona", "natureza"],
                    erro=f"⚠️ Combinação zona {zona} + natureza {natureza} não encontrada"
                )
            
            return ParametroCalculado(
                nome="testada_minima",
                valor=parametro,
                unidade="metros",
                regra_aplicada=f"Zona {zona} - Natureza {natureza}",
                dependencias=["zona", "natureza"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular testada mínima: {e}")
            return ParametroCalculado(
                nome="testada_minima",
                valor=None,
                unidade="metros",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "natureza"],
                erro=f"Erro interno: {str(e)}"
            )
    
    def _calcular_altura_maxima(self, zona: str, avenida: Optional[str] = None) -> ParametroCalculado:
        """
        Calcula altura máxima permitida conforme LC 108/2009
        """
        try:
            zona = zona.strip().upper()
            
            # Casos simples
            if zona == "ZC1":
                valor = 12
                regra = f"Zona {zona} - Altura máxima fixa"
            elif zona == "ZC2":
                valor = 8
                regra = f"Zona {zona} - Altura máxima fixa"
            elif zona == "ZII":
                valor = 2
                regra = f"Zona {zona} - Altura máxima fixa (consultar CONDESS para mais pavimentos)"
            elif zona in ["ZAD2", "ZCT1"]:
                valor = "livre"
                regra = f"Zona {zona} - Altura livre"
            
            # Zonas que dependem da avenida
            elif zona in ["ZCT2", "ZCT4"]:
                if not avenida:
                    return ParametroCalculado(
                        nome="altura_maxima",
                        valor=None,
                        unidade="metros",
                        regra_aplicada=f"Zona {zona}",
                        dependencias=["zona", "avenida"],
                        erro="⚠️ Avenida necessária para cálculo"
                    )
                
                avenidas_livres = {
                    "Av. Porto Alegre",
                    "Av. dos Emigrantes", 
                    "Av. Paulista",
                    "Av. Brasil",
                    "Av. Joao Natalino Brescansin",
                    "Av. Tancredo Neves"
                }
                
                if avenida in avenidas_livres:
                    valor = "livre"
                    regra = f"Zona {zona} - Avenida {avenida} (altura livre)"
                else:
                    valor = 12
                    regra = f"Zona {zona} - Avenida {avenida} (altura padrão)"
            
            # Zona não reconhecida
            else:
                return ParametroCalculado(
                    nome="altura_maxima",
                    valor=None,
                    unidade="metros",
                    regra_aplicada=f"Zona {zona}",
                    dependencias=["zona"],
                    erro=f"⚠️ Zona {zona} não encontrada"
                )
            
            return ParametroCalculado(
                nome="altura_maxima",
                valor=valor,
                unidade="metros" if isinstance(valor, (int, float)) else "livre",
                regra_aplicada=regra,
                dependencias=["zona", "avenida"] if avenida else ["zona"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular altura máxima: {e}")
            return ParametroCalculado(
                nome="altura_maxima",
                valor=None,
                unidade="metros",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "avenida"],
                erro=f"Erro interno: {str(e)}"
            )
    
    def _calcular_outorga_onerosa(self, zona: str, avenida: Optional[str] = None) -> ParametroCalculado:
        """
        Calcula se há cobrança de outorga onerosa conforme LC 108/2009
        """
        try:
            zona = zona.strip().upper()
            
            if zona in {"ZCT2", "ZCT4"} and avenida:
                avenidas_livres = {
                    "Av. Porto Alegre",
                    "Av. dos Emigrantes",
                    "Av. Paulista", 
                    "Av. Brasil",
                    "Av. Joao Natalino Brescansin",
                    "Av. Tancredo Neves"
                }
                
                if avenida in avenidas_livres:
                    valor = "livre"
                    regra = f"Zona {zona} - Avenida {avenida} (sem cobrança)"
                else:
                    valor = "cobrança"
                    regra = f"Zona {zona} - Avenida {avenida} (com cobrança)"
            else:
                valor = "cobrança"
                regra = f"Zona {zona} - Cobrança padrão"
            
            return ParametroCalculado(
                nome="outorga_onerosa",
                valor=valor,
                unidade="status",
                regra_aplicada=regra,
                dependencias=["zona", "avenida"] if avenida else ["zona"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular outorga onerosa: {e}")
            return ParametroCalculado(
                nome="outorga_onerosa",
                valor=None,
                unidade="status",
                regra_aplicada="Erro no cálculo",
                dependencias=["zona", "avenida"],
                erro=f"Erro interno: {str(e)}"
            )


# Instância global do service
parametros_service = ParametrosUrbanisticosService()
