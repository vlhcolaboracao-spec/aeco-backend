#!/usr/bin/env python3
"""
Script de Teste Automatizado - Sistema AECO
Testa cadastro de clientes, terrenos e projetos com dados realistas
"""

import requests
import json
import random
import time
from datetime import datetime, date
from typing import List, Dict, Any
import uuid

# Configurações
BASE_URL = "http://127.0.0.1:8000"
API_BASE = BASE_URL  # Removendo /api pois as rotas não têm esse prefixo

# Dados de teste para Sorriso-MT
ZONAS_SORRISO = ["ZAD1", "ZAD2", "ZC1", "ZC2", "ZCT1", "ZCT2", "ZCT3", "ZCT4", "ZEIS", "ZH1", "ZH2", "ZH3", "ZHL", "ZI1", "ZI2", "ZIA1", "ZIA2", "ZII"]
AVENIDAS_SORRISO = [
    "Av. Porto Alegre", "Av. dos Emigrantes", "Av. Paulista", 
    "Av. Brasil", "Av. Joao Natalino Brescansin", "Av. Tancredo Neves"
]
BAIRROS_SORRISO = [
    "Centro", "Jardim das Palmeiras", "Jardim Europa", "Jardim América",
    "Vila Nova", "Residencial Sorriso", "Jardim Botânico", "Jardim das Flores"
]
TIPOS_EMPREENDIMENTO = ["Residencial", "Comercial", "Misto"]
NATUREZAS_PROJETO = ["Desmembramento", "Loteamento e Condomínio", "Arquitetonico", "Urbanistico", "Não se aplica"]

class TesteAutomatizado:
    def __init__(self):
        self.clientes_cadastrados = []
        self.terrenos_cadastrados = []
        self.projetos_cadastrados = []
        self.erros = []
        self.sucessos = 0
        
    def log(self, mensagem: str, tipo: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {tipo}: {mensagem}")
        
    def gerar_dados_cliente(self, index: int) -> Dict[str, Any]:
        """Gera dados realistas para um cliente"""
        nomes = [
            "João Silva Santos", "Maria Oliveira Costa", "Pedro Almeida Lima",
            "Ana Paula Rodrigues", "Carlos Eduardo Ferreira", "Lucia Mendes Silva",
            "Roberto Carlos Souza", "Fernanda Alves Pereira", "Marcos Antonio Dias",
            "Patricia Santos Oliveira", "Ricardo Lima Costa", "Sandra Maria Silva",
            "Antonio Carlos Mendes", "Juliana Ferreira Santos", "Eduardo Silva Costa"
        ]
        
        tipos = ["Pessoa Física", "Pessoa Jurídica"]
        tipo = random.choice(tipos)
        
        if tipo == "Pessoa Física":
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            nome = random.choice(nomes)
        else:
            cpf = f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/{random.randint(1000, 9999)}-{random.randint(10, 99)}"
            nome = f"Empresa {random.choice(['Construtora', 'Imobiliária', 'Engenharia'])} {random.choice(['Ltda', 'S.A.', 'EIRELI'])}"
        
        return {
            "nome_completo_razao_social": nome,
            "cpf_cnpj": cpf,
            "rg_inscricao_estadual": f"{random.randint(1000000, 9999999)}",
            "data_nascimento_fundacao": f"{random.randint(1950, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "telefone_principal": f"(65) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "telefone_secundario": f"(65) {random.randint(3000, 3999)}-{random.randint(1000, 9999)}",
            "email": f"cliente{index}@email.com",
            "redes_sociais": f"@cliente{index}",
            "logradouro": f"Rua {random.choice(['das Flores', 'dos Lírios', 'das Palmeiras', 'dos Ipês'])}",
            "numero": str(random.randint(1, 9999)),
            "complemento": random.choice(["", "Apto 101", "Casa 2", "Sala 3"]),
            "bairro": random.choice(BAIRROS_SORRISO),
            "cidade": "Sorriso",
            "estado": "MT",
            "cep": f"78890-{random.randint(100, 999)}",
            "pais": "Brasil"
        }
    
    def gerar_dados_terreno(self, index: int) -> Dict[str, Any]:
        """Gera dados realistas para um terreno em Sorriso-MT"""
        zona = random.choice(ZONAS_SORRISO)
        area = random.randint(200, 2000)
        
        # Gerar dados para um terreno retangular (4 lados)
        lados_poligono = 4
        angulos_internos = [90.0, 90.0, 90.0, 90.0]  # Retângulo
        dimensoes_lados = [
            {"tipo": "Alinhamento Predial", "medida": random.randint(10, 50)},
            {"tipo": "Fundos", "medida": random.randint(10, 50)},
            {"tipo": "Divisa Lateral", "medida": random.randint(10, 50)},
            {"tipo": "Divisa Lateral", "medida": random.randint(10, 50)}
        ]
        
        return {
            "matricula": f"MT-{random.randint(100000, 999999)}",
            "data": datetime.now().isoformat(),
            "municipio": "Sorriso",
            "estado": "MT",
            "pais": "BRASIL",
            "bairro": random.choice(BAIRROS_SORRISO),
            "logradouro": f"Rua {random.choice(['das Flores', 'dos Lírios', 'das Palmeiras', 'dos Ipês', 'das Acácias'])}",
            "numero": str(random.randint(1, 9999)),
            "cep": f"78890{random.randint(100, 999)}",
            "lados_poligono": lados_poligono,
            "angulos_internos": angulos_internos,
            "dimensoes_lados": dimensoes_lados,
            "tipo_lote": random.choice(["Padrão", "Esquina", "Único na Quadra"]),
            "area": str(area),
            "norte_verdadeiro": round(random.uniform(0, 360), 2),
            "zona": zona,
            "observacoes": f"Terreno teste {index} - {zona}"
        }
    
    def gerar_dados_projeto(self, index: int, terreno_id: str) -> Dict[str, Any]:
        """Gera dados realistas para um projeto"""
        natureza = random.choice(NATUREZAS_PROJETO)
        tipo_empreendimento = random.choice(TIPOS_EMPREENDIMENTO)
        
        dados = {
            "nome_projeto": f"Projeto Teste {index} - {tipo_empreendimento}",
            "tipo_empreendimento": tipo_empreendimento,
            "natureza": natureza,
            "descricao": f"Descrição do projeto teste {index}",
            "terreno_id": terreno_id,
            "cliente_id": random.choice(self.clientes_cadastrados)["id"] if self.clientes_cadastrados else str(uuid.uuid4()),
            "observacoes": f"Projeto teste {index}"
        }
        
        # Dados condicionais baseados na natureza
        if natureza in ["Desmembramento", "Loteamento e Condomínio"]:
            dados["area_minima_lote"] = random.randint(200, 1000)
        
        if natureza == "Arquitetonico":
            dados["pavimentos"] = random.randint(1, 10)
            dados["altura_total"] = round(random.uniform(3.0, 30.0), 2)
            dados["area_construida"] = round(random.uniform(50.0, 500.0), 2)
        elif natureza == "Urbanistico":
            dados["area_construida"] = round(random.uniform(100.0, 1000.0), 2)
        
        # Avenida para zonas ZCT2/ZCT4
        if random.choice([True, False]):  # 50% chance de ter avenida
            dados["avenida"] = random.choice(AVENIDAS_SORRISO)
        
        return dados
    
    def testar_cadastro_clientes(self, quantidade: int = 15):
        """Testa cadastro de clientes"""
        self.log(f"Iniciando teste de cadastro de {quantidade} clientes...")
        
        for i in range(1, quantidade + 1):
            try:
                dados = self.gerar_dados_cliente(i)
                response = requests.post(f"{API_BASE}/clientes", json=dados)
                
                if response.status_code in [200, 201]:
                    resultado = response.json()
                    # Extrair ID do cliente da resposta
                    if "cliente" in resultado:
                        cliente_data = resultado["cliente"]
                        cliente_data["id"] = cliente_data.get("_id", str(uuid.uuid4()))
                        self.clientes_cadastrados.append(cliente_data)
                    else:
                        resultado["id"] = resultado.get("_id", str(uuid.uuid4()))
                        self.clientes_cadastrados.append(resultado)
                    self.sucessos += 1
                    self.log(f"Cliente {i} cadastrado com sucesso: {dados['nome_completo_razao_social']}")
                else:
                    erro = f"Erro ao cadastrar cliente {i}: {response.status_code} - {response.text[:200]}"
                    self.erros.append(erro)
                    self.log(erro, "ERRO")
                    
            except Exception as e:
                erro = f"Exceção ao cadastrar cliente {i}: {str(e)}"
                self.erros.append(erro)
                self.log(erro, "ERRO")
            
            time.sleep(0.1)  # Pequena pausa entre requisições
    
    def testar_cadastro_terrenos(self, quantidade: int = 50):
        """Testa cadastro de terrenos"""
        self.log(f"Iniciando teste de cadastro de {quantidade} terrenos...")
        
        for i in range(1, quantidade + 1):
            try:
                dados = self.gerar_dados_terreno(i)
                response = requests.post(f"{API_BASE}/formulario-terrenos-projetos/", json=dados)
                
                if response.status_code in [200, 201]:
                    resultado = response.json()
                    # Extrair ID do terreno da resposta
                    if "terreno" in resultado:
                        terreno_data = resultado["terreno"]
                        terreno_data["id"] = terreno_data.get("_id", str(uuid.uuid4()))
                        self.terrenos_cadastrados.append(terreno_data)
                    else:
                        resultado["id"] = resultado.get("_id", str(uuid.uuid4()))
                        self.terrenos_cadastrados.append(resultado)
                    self.sucessos += 1
                    self.log(f"Terreno {i} cadastrado com sucesso: {dados['matricula']}")
                else:
                    erro = f"Erro ao cadastrar terreno {i}: {response.status_code} - {response.text[:200]}"
                    self.erros.append(erro)
                    self.log(erro, "ERRO")
                    
            except Exception as e:
                erro = f"Exceção ao cadastrar terreno {i}: {str(e)}"
                self.erros.append(erro)
                self.log(erro, "ERRO")
            
            time.sleep(0.1)
    
    def testar_cadastro_projetos(self, quantidade: int = 50):
        """Testa cadastro de projetos"""
        self.log(f"Iniciando teste de cadastro de {quantidade} projetos...")
        
        for i in range(1, quantidade + 1):
            try:
                # Seleciona um terreno aleatório se disponível
                if self.terrenos_cadastrados:
                    terreno = random.choice(self.terrenos_cadastrados)
                    terreno_id = terreno.get("id", terreno.get("_id", str(uuid.uuid4())))
                else:
                    terreno_id = str(uuid.uuid4())
                
                dados = self.gerar_dados_projeto(i, terreno_id)
                
                response = requests.post(f"{API_BASE}/projetos", json=dados)
                
                if response.status_code in [200, 201]:
                    resultado = response.json()
                    self.projetos_cadastrados.append(resultado)
                    self.sucessos += 1
                    self.log(f"Projeto {i} cadastrado com sucesso: {dados['nome_projeto']}")
                else:
                    erro = f"Erro ao cadastrar projeto {i}: {response.status_code} - {response.text[:200]}"
                    self.erros.append(erro)
                    self.log(erro, "ERRO")
                    
            except Exception as e:
                erro = f"Exceção ao cadastrar projeto {i}: {str(e)}"
                self.erros.append(erro)
                self.log(erro, "ERRO")
            
            time.sleep(0.1)
    
    def testar_consultas(self):
        """Testa funcionalidades de consulta"""
        self.log("Testando funcionalidades de consulta...")
        
        # Teste consulta de clientes
        try:
            response = requests.get(f"{API_BASE}/projetos/consulta/clientes")
            if response.status_code == 200:
                self.log("✅ Consulta de clientes funcionando")
            else:
                self.erros.append(f"Erro na consulta de clientes: {response.status_code}")
        except Exception as e:
            self.erros.append(f"Exceção na consulta de clientes: {str(e)}")
        
        # Teste consulta de terrenos
        try:
            response = requests.get(f"{API_BASE}/projetos/consulta/terrenos")
            if response.status_code == 200:
                self.log("✅ Consulta de terrenos funcionando")
            else:
                self.erros.append(f"Erro na consulta de terrenos: {response.status_code}")
        except Exception as e:
            self.erros.append(f"Exceção na consulta de terrenos: {str(e)}")
        
        # Teste consulta de parâmetros urbanísticos
        if self.terrenos_cadastrados:
            terreno = random.choice(self.terrenos_cadastrados)
            try:
                # Usar cod_projeto do terreno (não do projeto)
                cod_projeto = terreno.get('cod_projeto')
                if not cod_projeto:
                    # Se não tem cod_projeto, buscar na estrutura de resposta da API
                    if 'terreno' in terreno:
                        cod_projeto = terreno['terreno'].get('cod_projeto')
                    elif 'terrenos' in terreno and terreno['terrenos']:
                        cod_projeto = terreno['terrenos'][0].get('cod_projeto')
                
                if cod_projeto:
                    response = requests.get(f"{API_BASE}/parametros-urbanisticos/api/parametros/projeto/{cod_projeto}")
                    if response.status_code == 200:
                        self.log("✅ Consulta de parâmetros urbanísticos funcionando")
                    else:
                        self.erros.append(f"Erro na consulta de parâmetros: {response.status_code}")
                else:
                    self.erros.append("Terreno não possui cod_projeto para consulta de parâmetros")
            except Exception as e:
                self.erros.append(f"Exceção na consulta de parâmetros: {str(e)}")
    
    def gerar_relatorio(self):
        """Gera relatório final do teste"""
        self.log("=" * 60)
        self.log("RELATÓRIO FINAL DO TESTE AUTOMATIZADO")
        self.log("=" * 60)
        self.log(f"✅ Sucessos: {self.sucessos}")
        self.log(f"❌ Erros: {len(self.erros)}")
        self.log(f"👥 Clientes cadastrados: {len(self.clientes_cadastrados)}")
        self.log(f"🏠 Terrenos cadastrados: {len(self.terrenos_cadastrados)}")
        self.log(f"📋 Projetos cadastrados: {len(self.projetos_cadastrados)}")
        
        if self.erros:
            self.log("\nERROS ENCONTRADOS:")
            for erro in self.erros:
                self.log(f"  - {erro}", "ERRO")
        else:
            self.log("\n🎉 NENHUM ERRO ENCONTRADO! Todos os testes passaram com sucesso!")
        
        self.log("=" * 60)

def main():
    """Função principal do teste"""
    print("🚀 INICIANDO TESTE AUTOMATIZADO DO SISTEMA AECO")
    print("=" * 60)
    
    teste = TesteAutomatizado()
    
    try:
        # Teste 1: Cadastro de clientes
        teste.testar_cadastro_clientes(15)
        
        # Teste 2: Cadastro de terrenos
        teste.testar_cadastro_terrenos(50)
        
        # Teste 3: Cadastro de projetos
        teste.testar_cadastro_projetos(50)
        
        # Teste 4: Funcionalidades de consulta
        teste.testar_consultas()
        
        # Relatório final
        teste.gerar_relatorio()
        
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro crítico no teste: {str(e)}")
    finally:
        print("\n🏁 Teste finalizado!")

if __name__ == "__main__":
    main()
