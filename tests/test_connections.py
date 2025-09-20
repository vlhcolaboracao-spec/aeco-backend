#!/usr/bin/env python3
"""
Script de teste para verificar conexões do sistema AECO.
Executa verificações de MongoDB e API, exibindo relatório detalhado.
"""
import asyncio
import sys
import os
from pathlib import Path

# Adiciona o diretório backend ao path para importar módulos
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.connections_check import run_full_connections_check
from app.config import settings


def print_header():
    """Imprime cabeçalho do teste"""
    print("=" * 60)
    print("🔍 TESTE DE CONEXÕES - SISTEMA AECO")
    print("=" * 60)
    print(f"Ambiente: {settings.app_env}")
    print(f"API Base URL: {settings.api_base_url}")
    print(f"MongoDB URI: {settings.mongo_uri.replace(settings.mongo_uri.split('@')[0].split('://')[1], '***') if '@' in settings.mongo_uri else settings.mongo_uri}")
    print(f"MongoDB Database: {settings.mongo_db}")
    print("-" * 60)


def print_result(title: str, result: dict, emoji: str = "🔧"):
    """Imprime resultado formatado de um teste"""
    status_emoji = "✅" if result.get("status") == "OK" else "❌"
    print(f"\n{emoji} {title}")
    print(f"   Status: {status_emoji} {result.get('status', 'UNKNOWN')}")
    print(f"   Mensagem: {result.get('message', 'N/A')}")
    
    # Detalhes específicos
    if "response_time_ms" in result and result["response_time_ms"]:
        print(f"   Tempo de resposta: {result['response_time_ms']}ms")
    
    if "http_status" in result and result["http_status"]:
        print(f"   HTTP Status: {result['http_status']}")
    
    if "connected" in result:
        print(f"   Conectado: {'Sim' if result['connected'] else 'Não'}")


def print_summary(results: dict):
    """Imprime resumo final dos testes"""
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    summary = results.get("summary", {})
    total = summary.get("total_checks", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    
    print(f"Total de verificações: {total}")
    print(f"✅ Aprovadas: {passed}")
    print(f"❌ Falharam: {failed}")
    
    overall_status = results.get("overall_status", "UNKNOWN")
    status_emoji = "✅" if overall_status == "OK" else "❌"
    
    print(f"\nStatus Geral: {status_emoji} {overall_status}")
    print("=" * 60)


async def main():
    """Função principal do teste"""
    try:
        print_header()
        
        # Executa verificação completa
        results = await run_full_connections_check()
        
        # Exibe resultados detalhados
        print_result("MongoDB", results.get("mongo", {}), "🗄️")
        print_result("API Health", results.get("api", {}), "🌐")
        
        # Exibe resumo
        print_summary(results)
        
        # Determina código de saída
        overall_status = results.get("overall_status", "FAIL")
        exit_code = 0 if overall_status == "OK" else 1
        
        if exit_code == 0:
            print("\n🎉 Todos os testes passaram! Sistema pronto para uso.")
        else:
            print("\n⚠️  Alguns testes falharam. Verifique as configurações.")
            print("\n💡 Dicas para resolução:")
            print("   - Verifique se o MongoDB está rodando")
            print("   - Confirme as credenciais no arquivo .env")
            print("   - Certifique-se de que a API está iniciada")
            print("   - Verifique a conectividade de rede")
        
        return exit_code
        
    except Exception as e:
        print(f"\n💥 Erro crítico durante os testes: {e}")
        print("\n💡 Verifique se:")
        print("   - O arquivo .env está configurado corretamente")
        print("   - As dependências estão instaladas")
        print("   - O MongoDB está acessível")
        return 1


if __name__ == "__main__":
    """
    Execução do script de teste.
    
    Uso:
        python -m tests.test_connections
        python tests/test_connections.py
    """
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
