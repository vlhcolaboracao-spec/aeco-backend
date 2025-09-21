# 🎨 Guia de Personalização - Formulário de Terrenos de Projetos

## 📋 Visão Geral

Este guia explica como personalizar completamente o formulário de terrenos, desde a aparência visual até a funcionalidade, mantendo a flexibilidade de edição que você solicitou.

## 🌐 Modos de Funcionamento

### **Modo Static (Padrão)**
- **Arquivo**: `frontend/public/formulario_terrenos.html`
- **Vantagem**: Edição direta, sem necessidade de reiniciar servidor
- **Ideal para**: Mudanças visuais rápidas, testes de layout

### **Modo Jinja2**
- **Arquivo**: `backend/app/web/templates/formulario_terrenos.html`
- **Vantagem**: Variáveis dinâmicas, lógica server-side
- **Ideal para**: Funcionalidades avançadas, dados dinâmicos

## 🎯 Como Escolher o Modo

No arquivo `.env`:
```env
# Para modo static (padrão)
FRONTEND_MODE=static

# Para modo Jinja2
FRONTEND_MODE=jinja
```

## 📁 Estrutura dos Arquivos

```
PROJETO_IAP/
├── frontend/public/
│   └── formulario_terrenos.html      # Versão static editável
├── backend/app/web/templates/
│   ├── base.html                     # Template base (Jinja2)
│   └── formulario_terrenos.html      # Versão Jinja2
└── backend/app/routers/
    └── web.py                        # Lógica do backend
```

## 🎨 Personalização Visual

### **1. Cores e Tema**

#### **Cores Principais**
```html
<!-- Cores atuais -->
bg-green-600    # Botão "Cadastrar Terreno"
bg-blue-600     # Botões secundários
bg-gray-600     # Botão "Voltar"
bg-white        # Fundo dos cards
bg-gray-50      # Fundo da página

<!-- Para mudar as cores, substitua as classes: -->
bg-green-600 → bg-purple-600    # Botão principal roxo
bg-blue-600 → bg-red-600        # Botões secundários vermelhos
```

#### **Exemplo de Mudança de Tema**
```html
<!-- Substitua no arquivo HTML: -->
<button class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700">
    Cadastrar Terreno
</button>

<!-- Por: -->
<button class="bg-purple-600 text-white px-6 py-2 rounded-md hover:bg-purple-700">
    Cadastrar Terreno
</button>
```

### **2. Layout e Estrutura**

#### **Modificar Colunas**
```html
<!-- Layout atual: 2 colunas em desktop -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

<!-- Para 3 colunas: -->
<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

<!-- Para 1 coluna (mobile-first): -->
<div class="grid grid-cols-1 gap-6">
```

#### **Alterar Espaçamento**
```html
<!-- Espaçamento atual: gap-6 -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

<!-- Para mais espaço: -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

<!-- Para menos espaço: -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
```

### **3. Campos do Formulário**

#### **Adicionar Novo Campo**
```html
<!-- Exemplo: Adicionar campo "Valor do Terreno" -->
<div>
    <label for="valor_terreno" class="block text-sm font-medium text-gray-700 mb-1">
        Valor do Terreno (R$)
    </label>
    <input type="number" 
           id="valor_terreno" 
           name="valor_terreno" 
           step="0.01" 
           min="0"
           placeholder="Ex: 150000.00"
           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>
```

#### **Remover Campo**
```html
<!-- Para remover um campo, simplesmente delete todo o <div> que contém o campo -->
<!-- Exemplo: Remover campo "Observações" -->
<!-- DELETE ESTE BLOCO COMPLETO: -->
<div>
    <label for="observacoes" class="block text-sm font-medium text-gray-700 mb-1">
        Observações
    </label>
    <textarea id="observacoes" 
              name="observacoes" 
              rows="4"
              placeholder="Observações adicionais sobre o terreno"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>
```

#### **Modificar Opções de Select**
```html
<!-- Exemplo: Adicionar mais tipos de lote -->
<select id="tipo_lote" name="tipo_lote" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
    <option value="">Selecione</option>
    <option value="Esquina">Esquina</option>
    <option value="Fundo">Fundo</option>
    <option value="Meio">Meio</option>
    <option value="Canto">Canto</option>
    <option value="Outro">Outro</option>
    
    <!-- ADICIONAR NOVAS OPÇÕES: -->
    <option value="Frente">Frente</option>
    <option value="Quadra">Quadra</option>
    <option value="Gleba">Gleba</option>
</select>
```

### **4. Validações**

#### **Adicionar Validação HTML5**
```html
<!-- Exemplo: Validar CEP com padrão -->
<input type="text" 
       id="cep" 
       name="cep" 
       pattern="[0-9]{5}-?[0-9]{3}"
       placeholder="Ex: 78890-000"
       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
       required>
```

#### **Validação JavaScript Personalizada**
```html
<!-- Adicionar no final da página, antes do </body> -->
<script>
function validarFormulario() {
    const cep = document.getElementById('cep').value;
    const area = document.getElementById('area').value;
    
    // Validação de CEP
    if (!/^[0-9]{5}-?[0-9]{3}$/.test(cep)) {
        alert('CEP deve ter formato 12345-678');
        return false;
    }
    
    // Validação de área
    if (parseFloat(area) < 10) {
        alert('Área deve ser maior que 10 m²');
        return false;
    }
    
    return true;
}

// Aplicar validação ao formulário
document.getElementById('terreno-form').addEventListener('submit', function(e) {
    if (!validarFormulario()) {
        e.preventDefault();
    }
});
</script>
```

## 🔧 Personalização de Funcionalidades

### **1. Modificar Comportamento HTMX**

#### **Alterar Target de Resposta**
```html
<!-- Atual: Resposta aparece abaixo do formulário -->
<form hx-post="/formulario-terrenos-projetos" 
      hx-target="#form-response" 
      hx-swap="innerHTML">

<!-- Para aparecer no topo da página: -->
<form hx-post="/formulario-terrenos-projetos" 
      hx-target="#form-response" 
      hx-swap="innerHTML"
      hx-target-request="#form-response">

<!-- Para aparecer em modal: -->
<form hx-post="/formulario-terrenos-projetos" 
      hx-target="#modal-response" 
      hx-swap="innerHTML">
```

#### **Adicionar Loading State**
```html
<!-- Adicionar indicador de carregamento -->
<button type="submit" 
        class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
        hx-indicator="#loading">
    <span id="loading" class="htmx-indicator">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Salvando...
    </span>
    <span class="htmx-indicator:hidden">Cadastrar Terreno</span>
</button>
```

### **2. Personalizar Lista de Terrenos**

#### **Modificar Colunas da Tabela**
```html
<!-- No arquivo web.py, função terrenos_list_widget, modificar as colunas: -->
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
    Matrícula
</th>
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
    Município
</th>
<!-- ADICIONAR NOVA COLUNA: -->
<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
    Valor (R$)
</th>

<!-- E no corpo da tabela: -->
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
    R$ {terreno.valor_terreno:,.2f}
</td>
```

### **3. Adicionar Novos Campos ao Backend**

#### **1. Atualizar Modelo Pydantic**
```python
# Em backend/app/models/formulario_terrenos_projetos.py
class FormularioTerrenosProjetosBase(BaseModel):
    # ... campos existentes ...
    
    # ADICIONAR NOVO CAMPO:
    valor_terreno: Optional[float] = Field(None, gt=0, description="Valor do terreno em reais")
    proprietario: Optional[str] = Field(None, max_length=200, description="Nome do proprietário")
```

#### **2. Atualizar Formulário HTML**
```html
<!-- Adicionar campo no HTML -->
<div>
    <label for="valor_terreno" class="block text-sm font-medium text-gray-700 mb-1">
        Valor do Terreno (R$)
    </label>
    <input type="number" 
           id="valor_terreno" 
           name="valor_terreno" 
           step="0.01" 
           min="0"
           placeholder="Ex: 150000.00"
           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>
```

#### **3. Atualizar Router Web**
```python
# Em backend/app/routers/web.py, função criar_terreno_web
async def criar_terreno_web(
    # ... parâmetros existentes ...
    valor_terreno: Optional[float] = Form(None),  # ADICIONAR
    proprietario: Optional[str] = Form(None),     # ADICIONAR
):
    # ... código existente ...
    
    terreno_data = FormularioTerrenosProjetosCreate(
        # ... campos existentes ...
        valor_terreno=valor_terreno,      # ADICIONAR
        proprietario=proprietario,        # ADICIONAR
    )
```

## 🎨 Exemplos de Personalizações Prontas

### **1. Tema Escuro**
```html
<!-- Substituir classes de cor -->
<body class="bg-gray-900 min-h-screen">
<header class="bg-gray-800 shadow-sm border-b border-gray-700">
<div class="bg-gray-800 shadow rounded-lg p-6">
<input class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-white">
```

### **2. Layout Compacto**
```html
<!-- Reduzir espaçamentos -->
<div class="space-y-2">  <!-- era space-y-4 -->
<div class="gap-3">       <!-- era gap-6 -->
<div class="p-4">         <!-- era p-6 -->
```

### **3. Formulário em Steps**
```html
<!-- Dividir em etapas -->
<div id="step1" class="step">
    <h3>Identificação do Imóvel</h3>
    <!-- campos de identificação -->
</div>

<div id="step2" class="step hidden">
    <h3>Localização</h3>
    <!-- campos de localização -->
</div>

<div id="step3" class="step hidden">
    <h3>Características do Terreno</h3>
    <!-- campos de características -->
</div>
```

## 🚀 Como Aplicar as Mudanças

### **Modo Static:**
1. Edite `frontend/public/formulario_terrenos.html`
2. Salve o arquivo
3. Recarregue a página no navegador

### **Modo Jinja2:**
1. Edite `backend/app/web/templates/formulario_terrenos.html`
2. Reinicie o servidor: `python -m uvicorn backend.app.main:app --reload`
3. Recarregue a página

## 📝 Dicas Importantes

### **1. Backup**
- Sempre faça backup antes de grandes mudanças
- Use Git para versionar suas modificações

### **2. Testes**
- Teste em diferentes tamanhos de tela
- Verifique se todos os campos funcionam
- Teste validações

### **3. Performance**
- Evite JavaScript muito complexo
- Use classes Tailwind otimizadas
- Mantenha o HTML limpo

### **4. Acessibilidade**
- Mantenha labels nos campos
- Use cores com contraste adequado
- Teste com leitores de tela

## 🔗 Recursos Úteis

- **Tailwind CSS**: https://tailwindcss.com/docs
- **HTMX**: https://htmx.org/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Pydantic**: https://pydantic-docs.helpmanual.io

## 🆘 Solução de Problemas

### **Formulário não salva:**
- Verifique se o backend está rodando
- Confirme se o MongoDB está conectado
- Verifique o console do navegador para erros

### **Estilos não aparecem:**
- Verifique se o Tailwind CSS está carregando
- Confirme se as classes estão corretas
- Teste em modo incógnito

### **HTMX não funciona:**
- Verifique se o script HTMX está carregado
- Confirme se os atributos hx-* estão corretos
- Verifique o console do navegador

---

**Este guia permite personalização completa do formulário mantendo a flexibilidade e facilidade de edição que você solicitou!** 🎨✨
