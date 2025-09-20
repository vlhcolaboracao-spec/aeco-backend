# Sistema AECO - Backend API

Backend em Python com FastAPI para o sistema AECO, conectado ao MongoDB com endpoints REST e sistema de verificação de conexões.

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **Motor** - Driver assíncrono para MongoDB
- **Pydantic** - Validação de dados e schemas
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Uvicorn** - Servidor ASGI

## 📁 Estrutura do Projeto

```
PROJETO_IAP/
├── backend/
│   └── app/
│       ├── main.py                 # Aplicação FastAPI principal
│       ├── config.py               # Configurações carregadas do .env
│       ├── db/
│       │   └── mongo.py            # Conexão e configuração MongoDB
│       ├── models/
│       │   ├── comum.py            # Schemas comuns (Response, Health, etc.)
│       │   └── projeto.py          # Schemas para Projetos
│       ├── repositories/
│       │   └── projetos_repo.py    # CRUD de projetos no MongoDB
│       ├── routers/
│       │   ├── health.py           # Endpoint /health
│       │   └── projetos.py         # CRUD de projetos
│       └── services/
│           └── connections_check.py # Verificação de conexões
├── tests/
│   └── test_connections.py         # Script de teste das conexões
├── env.example                     # Variáveis de ambiente (template)
├── pyproject.toml                  # Dependências e configurações
└── README.md                       # Este arquivo
```

## ⚡ Setup Rápido (Menos de 5 minutos)

### 1. Pré-requisitos

- Python 3.11 ou superior
- MongoDB instalado e rodando
- Git (opcional)

### 2. Clonar/Preparar o Projeto

```bash
# Se usando Git
git clone <seu-repositorio>
cd PROJETO_IAP

# Ou simplesmente navegue até a pasta do projeto
cd C:\PROJETO_IAP
```

### 3. Criar Ambiente Virtual

```bash
# Criar venv
python -m venv venv

# Ativar venv (Windows)
venv\Scripts\activate

# Ativar venv (Linux/Mac)
source venv/bin/activate
```

### 4. Instalar Dependências

```bash
# Instalar dependências
pip install -e .

# Ou usando pip diretamente
pip install fastapi uvicorn motor pymongo pydantic pydantic-settings python-dotenv aiohttp
```

### 5. Configurar Variáveis de Ambiente

```bash
# Copiar template de configuração
copy env.example .env

# Editar .env com suas configurações
notepad .env
```

**Exemplo de .env para desenvolvimento local:**
```env
APP_ENV=dev
APP_PORT=8000
API_BASE_URL=http://127.0.0.1:8000
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=aeco_db
LOG_LEVEL=INFO
```

### 6. Iniciar a API

```bash
# Comando para iniciar o servidor
uvicorn backend.app.main:app --reload --port 8000

# Ou usando o comando mais curto
uvicorn backend.app.main:app --reload
```

### 7. Testar as Conexões

Em outro terminal (mantendo a API rodando):

```bash
# Executar teste de conexões
python -m tests.test_connections

# Ou diretamente
python tests/test_connections.py
```

## 🔍 Endpoints Disponíveis

### Health Check
- **GET** `/health` - Verifica status da aplicação e MongoDB

### Projetos (CRUD)
- **POST** `/projetos` - Criar novo projeto
- **GET** `/projetos/{id}` - Buscar projeto por ID
- **GET** `/projetos` - Listar todos os projetos (com paginação)
- **PUT** `/projetos/{id}` - Atualizar projeto
- **DELETE** `/projetos/{id}` - Deletar projeto

### Informações
- **GET** `/` - Informações básicas da API
- **GET** `/info` - Informações detalhadas da aplicação

## 📖 Documentação Interativa

Após iniciar a API, acesse:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Teste de Conexões

O script `tests/test_connections.py` verifica:

1. **Conexão com MongoDB** - Ping e tempo de resposta
2. **API Health** - Requisição GET para `/health`

### Execução do Teste

```bash
# Ativar venv primeiro
venv\Scripts\activate

# Executar teste
python tests/test_connections.py
```

### Saída Esperada (Sucesso)

```
============================================================
🔍 TESTE DE CONEXÕES - SISTEMA AECO
============================================================
Ambiente: dev
API Base URL: http://127.0.0.1:8000
MongoDB URI: mongodb://localhost:27017/
MongoDB Database: aeco_db
------------------------------------------------------------

🗄️ MongoDB
   Status: ✅ OK
   Mensagem: Conexão com MongoDB estabelecida
   Tempo de resposta: 15.23ms
   Conectado: Sim

🌐 API Health
   Status: ✅ OK
   Mensagem: API respondendo corretamente
   Tempo de resposta: 45.67ms
   HTTP Status: 200

============================================================
📊 RESUMO DOS TESTES
============================================================
Total de verificações: 2
✅ Aprovadas: 2
❌ Falharam: 0

Status Geral: ✅ OK
============================================================

🎉 Todos os testes passaram! Sistema pronto para uso.
```

## ⚙️ Configurações Detalhadas

### Variáveis de Ambiente (.env)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `APP_ENV` | Ambiente da aplicação | `dev`, `prod` |
| `APP_PORT` | Porta da API | `8000` |
| `API_BASE_URL` | URL base da API | `http://127.0.0.1:8000` |
| `MONGO_URI` | URI de conexão MongoDB | `mongodb://localhost:27017/` |
| `MONGO_DB` | Nome do banco de dados | `aeco_db` |
| `LOG_LEVEL` | Nível de log | `INFO`, `DEBUG`, `ERROR` |

### Configurações MongoDB

#### Desenvolvimento Local (sem autenticação)
```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=aeco_dev
```

#### Com Autenticação
```env
MONGO_URI=mongodb://usuario:senha@localhost:27017/?authSource=admin
MONGO_DB=aeco_dev
```

#### MongoDB Atlas (Cloud)
```env
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=aeco_production
```

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Iniciar com hot-reload
uvicorn backend.app.main:app --reload --port 8000

# Iniciar em modo debug
uvicorn backend.app.main:app --reload --log-level debug

# Testar conexões
python tests/test_connections.py
```

### Produção
```bash
# Iniciar servidor de produção
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Com Gunicorn (alternativa)
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Exemplos de Uso

### Criar um Projeto
```bash
curl -X POST "http://127.0.0.1:8000/projetos" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Projeto Exemplo",
       "descricao": "Descrição do projeto",
       "responsavel": "Douglas Roberto"
     }'
```

### Listar Projetos
```bash
curl -X GET "http://127.0.0.1:8000/projetos"
```

### Health Check
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. MongoDB não conecta
- Verifique se o MongoDB está rodando: `mongosh`
- Confirme a URI no `.env`
- Teste conectividade: `telnet localhost 27017`

#### 2. API não inicia
- Verifique se a porta 8000 está livre
- Confirme se o venv está ativado
- Verifique dependências: `pip list`

#### 3. Teste de conexões falha
- Certifique-se de que a API está rodando
- Verifique o arquivo `.env`
- Execute o teste com mais detalhes

### Logs de Debug

Para mais detalhes nos logs, altere no `.env`:
```env
LOG_LEVEL=DEBUG
```

## ✅ Checklist "Deu Tudo Certo"

- [ ] ✅ API inicia sem erros: `uvicorn backend.app.main:app --reload`
- [ ] ✅ GET `/health` retorna `{"status":"ok","mongo":true}`
- [ ] ✅ Teste de conexões retorna exit code 0
- [ ] ✅ Swagger UI acessível em `/docs`
- [ ] ✅ MongoDB conecta e responde ao ping
- [ ] ✅ CRUD de projetos funciona (criar, listar, buscar, atualizar, deletar)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido por Douglas Roberto** 🚀
