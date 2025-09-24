#!/usr/bin/env python3
"""
Script para limpar o banco MongoDB, exceto a collection 'compliance criteria'
"""

import asyncio
import sys
import os

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.db.mongo import get_database, connect_to_mongo
from backend.app.config import settings

async def limpar_banco():
    """Limpa todas as collections exceto 'compliance criteria'"""
    try:
        print("🔌 Conectando ao MongoDB...")
        await connect_to_mongo()
        db = await get_database()
        
        print("📋 Listando collections existentes...")
        collections = await db.list_collection_names()
        print(f"Collections encontradas: {collections}")
        
        # Collections a serem removidas (exceto compliance criteria)
        collections_para_remover = []
        for collection in collections:
            if collection.lower() != 'compliance criteria':
                collections_para_remover.append(collection)
        
        print(f"\n🗑️ Collections que serão removidas: {collections_para_remover}")
        
        # Remove cada collection
        for collection_name in collections_para_remover:
            try:
                print(f"  🗑️ Removendo collection: {collection_name}")
                await db.drop_collection(collection_name)
                print(f"  ✅ Collection {collection_name} removida com sucesso")
            except Exception as e:
                print(f"  ❌ Erro ao remover {collection_name}: {e}")
        
        print(f"\n✅ Limpeza concluída! {len(collections_para_remover)} collections removidas")
        print("📋 Collections restantes:")
        collections_restantes = await db.list_collection_names()
        for collection in collections_restantes:
            print(f"  - {collection}")
            
    except Exception as e:
        print(f"❌ Erro durante a limpeza: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧹 INICIANDO LIMPEZA DO BANCO MONGODB")
    print("=" * 50)
    
    # Executa a limpeza
    resultado = asyncio.run(limpar_banco())
    
    if resultado:
        print("\n🎉 Limpeza concluída com sucesso!")
    else:
        print("\n❌ Erro durante a limpeza!")
        sys.exit(1)
