# 🚀 Guia de Inicialização - Sistema AECO

## 📋 Visão Geral

Este guia explica como inicializar e usar o Sistema AECO com backend FastAPI, MongoDB e frontend editável.

## ⚡ Inicialização Rápida (2 minutos)

### **1. Verificar Pré-requisitos**
- ✅ Python 3.11+ instalado
- ✅ MongoDB rodando (localhost:27017)
- ✅ Usuário MongoDB: `leandro` / Senha: `Leandro123.`

### **2. Navegar para o Diretório**
```bash
cd C:\PROJETO_IAP
```

### **3. Iniciar a Aplicação**
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

### **4. Acessar o Sistema**
- **Dashboard**: http://127.0.0.1:8000/
- **Formulário de Terrenos**: http://127.0.0.1:8000/formulario-terrenos-projetos
- **API Docs**: http://127.0.0.1:8000/docs

## 🔧 Inicialização Detalhada

### **Passo 1: Verificar Ambiente**

#### **Verificar Python**
```bash
python --version
# Deve retornar: Python 3.11.x ou superior
```

#### **Verificar MongoDB**
```bash
# Testar conexão MongoDB
python tests/test_connections.py
# Deve retornar: Status Geral: ✅ OK
```

### **Passo 2: Configurar Variáveis de Ambiente**

#### **Arquivo .env (já configurado)**
```env
# Configurações da Aplicação
APP_ENV=dev
APP_PORT=8000
API_BASE_URL=http://127.0.0.1:8000

# Configurações do MongoDB
MONGODB_USERNAME=leandro
MONGODB_PASSWORD=Leandro123.
MONGODB_HOST=localhost
MONGODB_PORT=27017
DATABASE_NAME=dev

# Configurações de Logging
LOG_LEVEL=INFO

# Configurações do Frontend
FRONTEND_MODE=static
```

### **Passo 3: Instalar Dependências**

#### **Se necessário (dependências já instaladas)**
```bash
pip install fastapi uvicorn motor pymongo pydantic pydantic-settings python-dotenv aiohttp jinja2
```

### **Passo 4: Iniciar o Servidor**

#### **Comando Principal**
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

#### **Comandos Alternativos**
```bash
# Usando uvicorn diretamente (se no PATH)
uvicorn backend.app.main:app --reload --port 8000

# Com configurações específicas
python -m uvicorn backend.app.main:app --reload --port 8000 --host 0.0.0.0 --log-level debug
```

## 🌐 Acessando o Sistema

### **URLs Principais**

| URL | Descrição |
|-----|-----------|
| http://127.0.0.1:8000/ | Dashboard principal |
| http://127.0.0.1:8000/formulario-terrenos-projetos | Formulário de terrenos |
| http://127.0.0.1:8000/dashboard | Dashboard Jinja2 |
| http://127.0.0.1:8000/docs | Documentação Swagger |
| http://127.0.0.1:8000/redoc | Documentação ReDoc |
| http://127.0.0.1:8000/health | Health check |

### **Navegação no Sistema**

1. **Dashboard**: Página inicial com status do sistema e ações rápidas
2. **Formulário de Terrenos**: Cadastro completo de terrenos
3. **API Docs**: Documentação interativa da API
4. **Health Check**: Verificação de status do sistema

## 🎯 Funcionalidades Disponíveis

### **1. Dashboard**
- ✅ Status do sistema (API + MongoDB)
- ✅ Estatísticas de projetos e terrenos
- ✅ Ações rápidas (navegação)
- ✅ Lista de terrenos recentes

### **2. Formulário de Terrenos**
- ✅ Cadastro completo com validação
- ✅ Lista de terrenos cadastrados
- ✅ Busca e filtros
- ✅ Estatísticas

### **3. API REST**
- ✅ CRUD de projetos
- ✅ CRUD de terrenos
- ✅ Health check
- ✅ Documentação automática

## 🔄 Modos de Frontend

### **Modo Static (Padrão)**
```env
FRONTEND_MODE=static
```
- **Arquivo**: `frontend/public/index.html`
- **Vantagem**: Edição direta, sem restart
- **Uso**: Mudanças visuais rápidas

### **Modo Jinja2**
```env
FRONTEND_MODE=jinja
```
- **Arquivo**: `backend/app/web/templates/dashboard.html`
- **Vantagem**: Variáveis dinâmicas
- **Uso**: Funcionalidades avançadas

## 🧪 Testando o Sistema

### **1. Teste de Conexões**
```bash
python tests/test_connections.py
```

**Resultado esperado:**
```
============================================================
🔍 TESTE DE CONEXÕES - SISTEMA AECO
============================================================

🗄️ MongoDB
   Status: ✅ OK
   Mensagem: Conexão com MongoDB estabelecida

🌐 API Health
   Status: ✅ OK
   Mensagem: API respondendo corretamente

Status Geral: ✅ OK
🎉 Todos os testes passaram! Sistema pronto para uso.
```

### **2. Teste via Navegador**
1. Acesse http://127.0.0.1:8000/
2. Clique em "Verificar Status" - deve mostrar ✅
3. Clique em "Cadastrar Terreno" - deve abrir o formulário
4. Preencha o formulário e teste o cadastro

### **3. Teste via API**
```bash
# Health check
curl http://127.0.0.1:8000/health

# Listar projetos
curl http://127.0.0.1:8000/projetos

# Listar terrenos
curl http://127.0.0.1:8000/formulario-terrenos-projetos
```

## 🐛 Solução de Problemas

### **Erro: "uvicorn não é reconhecido"**
```bash
# Solução: Use Python diretamente
python -m uvicorn backend.app.main:app --reload --port 8000
```

### **Erro: "MongoDB não conecta"**
```bash
# Verificar se MongoDB está rodando
python tests/test_connections.py

# Verificar credenciais no .env
# Usuário: leandro
# Senha: Leandro123.
```

### **Erro: "Porta 8000 em uso"**
```bash
# Usar porta diferente
python -m uvicorn backend.app.main:app --reload --port 8001

# Ou matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

### **Erro: "Módulo não encontrado"**
```bash
# Reinstalar dependências
pip install -r requirements.txt
# ou
pip install fastapi uvicorn motor pymongo pydantic pydantic-settings python-dotenv aiohttp jinja2
```

### **Frontend não carrega**
- Verifique se o servidor está rodando
- Confirme a URL: http://127.0.0.1:8000/
- Verifique o console do navegador para erros
- Teste em modo incógnito

## 📊 Monitoramento

### **Logs do Servidor**
O servidor mostra logs em tempo real:
```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### **Logs da Aplicação**
```
2024-01-15 10:30:00 - backend.app.main - INFO - Iniciando aplicação AECO...
2024-01-15 10:30:00 - backend.app.db.mongo - INFO - Conectado ao MongoDB: dev
2024-01-15 10:30:00 - backend.app.main - INFO - Aplicação iniciada com sucesso!
```

## 🔧 Configurações Avançadas

### **Desenvolvimento**
```bash
# Com hot-reload e debug
python -m uvicorn backend.app.main:app --reload --port 8000 --log-level debug

# Com host externo
python -m uvicorn backend.app.main:app --reload --port 8000 --host 0.0.0.0
```

### **Produção**
```bash
# Sem reload, com workers
python -m uvicorn backend.app.main:app --port 8000 --workers 4

# Com Gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Comandos Úteis

### **Desenvolvimento**
```bash
# Iniciar servidor
python -m uvicorn backend.app.main:app --reload --port 8000

# Testar conexões
python tests/test_connections.py

# Ver logs em tempo real
tail -f logs/app.log  # se configurado
```

### **Manutenção**
```bash
# Verificar status
curl http://127.0.0.1:8000/health

# Backup do banco
mongodump --db dev --out backup/

# Limpar cache
# Reiniciar servidor
```

## ✅ Checklist de Inicialização

- [ ] ✅ Python 3.11+ instalado
- [ ] ✅ MongoDB rodando
- [ ] ✅ Credenciais MongoDB corretas
- [ ] ✅ Dependências instaladas
- [ ] ✅ Arquivo .env configurado
- [ ] ✅ Servidor iniciado sem erros
- [ ] ✅ Dashboard acessível
- [ ] ✅ Formulário de terrenos funcionando
- [ ] ✅ Health check retorna OK
- [ ] ✅ Teste de conexões passa

## 🎉 Sistema Pronto!

Após seguir este guia, você terá:
- ✅ Backend FastAPI funcionando
- ✅ Frontend editável acessível
- ✅ MongoDB conectado
- ✅ Formulário de terrenos operacional
- ✅ API REST documentada
- ✅ Sistema de monitoramento ativo

**Acesse http://127.0.0.1:8000/ e comece a usar o Sistema AECO!** 🚀
