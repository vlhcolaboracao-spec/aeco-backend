# 📋 Guia de Versionamento - Sistema AECO

## 🎯 Status Atual
- ✅ **Repositório Git inicializado**
- ✅ **Primeiro commit realizado** (e4a6996)
- ✅ **Tag v1.0.0 criada** - Versão inicial funcional
- ✅ **Arquivo .gitignore configurado**

## 🚀 Próximos Passos para Conectar ao GitHub/GitLab

### 1. Criar Repositório Remoto

#### GitHub:
1. Acesse https://github.com
2. Clique em "New repository"
3. Nome: `aeco-backend` ou `sistema-aeco`
4. Descrição: "Backend API para Sistema AECO com FastAPI e MongoDB"
5. **NÃO** inicialize com README (já temos um)
6. Clique "Create repository"

#### GitLab:
1. Acesse https://gitlab.com
2. Clique em "New project"
3. Nome: `aeco-backend`
4. Descrição: "Backend API para Sistema AECO com FastAPI e MongoDB"
5. **NÃO** inicialize com README
6. Clique "Create project"

### 2. Conectar Repositório Local ao Remoto

```bash
# Para GitHub
git remote add origin https://github.com/SEU_USUARIO/aeco-backend.git

# Para GitLab
git remote add origin https://gitlab.com/SEU_USUARIO/aeco-backend.git

# Enviar código para o repositório remoto
git push -u origin master

# Enviar tags
git push origin --tags
```

### 3. Verificar Conexão

```bash
# Ver repositórios remotos
git remote -v

# Ver status
git status
```

## 📝 Convenções de Commit

### Tipos de Commit:
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação, sem mudança de código
- `refactor:` - Refatoração de código
- `test:` - Adição de testes
- `chore:` - Tarefas de manutenção

### Exemplos:
```bash
git commit -m "feat: adicionar autenticação JWT"
git commit -m "fix: corrigir validação de email"
git commit -m "docs: atualizar README com novas APIs"
git commit -m "refactor: melhorar estrutura de repositories"
```

## 🏷️ Versionamento Semântico

### Formato: MAJOR.MINOR.PATCH

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Nova funcionalidade compatível
- **PATCH**: Correções de bugs compatíveis

### Exemplos:
- `v1.0.0` - Versão inicial (atual)
- `v1.1.0` - Nova funcionalidade (ex: autenticação)
- `v1.1.1` - Correção de bug
- `v2.0.0` - Mudança breaking (ex: nova estrutura de API)

### Criar Tags:
```bash
# Versão patch (correção)
git tag -a v1.0.1 -m "Fix: corrigir timeout de conexão MongoDB"

# Versão minor (nova funcionalidade)
git tag -a v1.1.0 -m "Feat: adicionar autenticação JWT"

# Versão major (breaking changes)
git tag -a v2.0.0 -m "Feat: reestruturar API endpoints"
```

## 🌿 Branches

### Estratégia Recomendada:
- `master` - Código em produção
- `develop` - Desenvolvimento ativo
- `feature/nome-da-feature` - Novas funcionalidades
- `hotfix/nome-do-fix` - Correções urgentes

### Comandos:
```bash
# Criar branch de desenvolvimento
git checkout -b develop
git push -u origin develop

# Criar branch para feature
git checkout -b feature/autenticacao-jwt
git push -u origin feature/autenticacao-jwt

# Fazer merge
git checkout develop
git merge feature/autenticacao-jwt
git push origin develop
```

## 📊 Comandos Úteis

### Informações:
```bash
# Histórico de commits
git log --oneline --graph

# Status atual
git status

# Diferenças
git diff

# Ver tags
git tag -l

# Ver branches
git branch -a
```

### Manutenção:
```bash
# Atualizar repositório remoto
git fetch origin
git pull origin master

# Limpar branches locais deletadas
git remote prune origin

# Ver informações do repositório
git remote show origin
```

## 🔐 Configurações de Segurança

### Arquivos NUNCA versionados:
- `.env` (contém senhas)
- `*.log` (logs)
- `__pycache__/` (cache Python)
- `venv/` (ambiente virtual)

### Já configurado no .gitignore ✅

## 🎯 Próximas Funcionalidades para Versionar

1. **v1.1.0** - Sistema de autenticação JWT
2. **v1.2.0** - CRUD de usuários
3. **v1.3.0** - Sistema de permissões
4. **v1.4.0** - Upload de arquivos
5. **v1.5.0** - Relatórios e dashboards
6. **v2.0.0** - Refatoração completa da API

---

**Repositório pronto para desenvolvimento colaborativo!** 🚀
