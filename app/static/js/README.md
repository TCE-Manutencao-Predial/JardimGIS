# Estrutura de Scripts JavaScript - Controle de NFs

Esta pasta contém todos os scripts JavaScript do sistema, organizados por responsabilidade e funcionalidade.

## 📁 Estrutura de Diretórios

```
js/
├── core/                          # Scripts compartilhados entre múltiplas páginas
│   ├── analise_horarios_comum.js  # Análise de horários de funcionários (namespace: AnaliseHorarios)
│   └── exportar_tabela_excel.js   # Coordenador de exportação Excel
│
├── excel/                         # Módulos especializados em exportação Excel
│   ├── excel_formatacao_core.js   # Estilos base e cores (namespace: ExcelFormatacao)
│   ├── excel_utils.js             # Utilitários gerais (namespace: ExcelUtils)
│   ├── excel_tabelas.js           # Formatação de tabelas (namespace: ExcelTabelas)
│   ├── excel_informativos.js      # Formatação de dados informativos (namespace: ExcelInformativos)
│   └── README.md                  # Documentação detalhada dos módulos Excel
│
├── libs/                          # Bibliotecas de terceiros
│   └── xlsx.bundle.js             # SheetJS-Style para manipulação de Excel
│
└── pages/                         # Scripts específicos de páginas
    ├── checklist/
    │   ├── editar_checklist.js
    │   └── editar_checklist_mobile.js
    │
    ├── funcionarios/
    │   ├── editar_funcionarios.js
    │   └── dashboard_faltas.js
    │
    ├── frequencia/
    │   ├── controle_frequencia.js
    │   ├── controle_frequencia_gerenciar_terminal.js
    │   └── debug_terminal.js
    │
    ├── gestao_documental/
    │   ├── editar_gestao_documental.js
    │   ├── editar_gestao_documental_empresas.js
    │   └── gestao_anexos_modal.js
    │
    └── outros/
        ├── editar_empresas.js
        ├── editar_controle_nfs.js
        ├── editar_jornada.js
        ├── gerenciar_jornadas.js
        └── historico.js
```

---

## 🎯 Princípios de Organização

### **1. core/** - Código Compartilhado
Scripts que são utilizados por múltiplas páginas e fornecem funcionalidades base do sistema.

**Características:**
- Código reutilizável
- Namespaces globais (window.NomeModulo)
- Sem dependência de páginas específicas
- Alto grau de testabilidade

**Arquivos:**
- `analise_horarios_comum.js`: Funções para análise de horários, padrões de trabalho, cálculos de tempo
- `exportar_tabela_excel.js`: Coordenador de exportações Excel, orquestra os módulos especializados

### **2. excel/** - Módulos de Exportação Excel
Módulos especializados em criar e formatar arquivos Excel com estilos profissionais.

**Arquitetura Modular:**
- Cada módulo tem responsabilidade única e bem definida
- Uso de namespaces (window.ExcelFormatacao, window.ExcelUtils, etc.)
- Backward compatibility mantida em `core/exportar_tabela_excel.js`

**Ordem de Carregamento nos Templates:**
```html
<script src="js/libs/xlsx.bundle.js"></script>
<script src="js/excel/excel_formatacao_core.js"></script>
<script src="js/excel/excel_utils.js"></script>
<script src="js/excel/excel_tabelas.js"></script>
<script src="js/excel/excel_informativos.js"></script>
<script src="js/core/exportar_tabela_excel.js"></script>
```

### **3. libs/** - Bibliotecas Externas
Bibliotecas de terceiros que não são modificadas pelo projeto.

**Regras:**
- Não modificar estes arquivos
- Apenas adicionar bibliotecas já compiladas/minimizadas
- Documentar versão no README se relevante

### **4. pages/** - Scripts Específicos de Páginas
Scripts que implementam funcionalidades de páginas específicas.

**Organização por Domínio:**
- `checklist/`: Funcionalidades relacionadas a checklists
- `funcionarios/`: Gestão de funcionários
- `frequencia/`: Controle de frequência e terminais
- `gestao_documental/`: Gestão de documentos
- `outros/`: Scripts diversos que não se encaixam nas categorias acima

**Características:**
- Cada arquivo corresponde a uma página específica
- Pode importar módulos do `core/` e `excel/`
- Não deve ser importado por outras páginas

---

## 📝 Guia de Uso

### Como Adicionar um Novo Script de Página

1. **Identifique o domínio:**
   - É relacionado a checklists? → `pages/checklist/`
   - É sobre funcionários? → `pages/funcionarios/`
   - É sobre frequência? → `pages/frequencia/`
   - É gestão documental? → `pages/gestao_documental/`
   - Não se encaixa? → `pages/outros/`

2. **Crie o arquivo:**
   ```bash
   touch pages/[dominio]/novo_script.js
   ```

3. **No template HTML correspondente:**
   ```html
   <script src="{{ url_for('static', filename='js/pages/[dominio]/novo_script.js') }}"></script>
   ```

### Como Adicionar um Módulo Compartilhado

1. **Avalie se é realmente compartilhado:**
   - Será usado por 2+ páginas diferentes?
   - Fornece funcionalidade base/utilitária?
   
2. **Se sim, adicione em `core/`:**
   ```javascript
   // Estrutura IIFE com namespace
   window.MeuModulo = (function() {
       'use strict';
       
       // Funções privadas
       function funcaoPrivada() { }
       
       // API pública
       return {
           funcaoPublica: function() { }
       };
   })();
   ```

3. **Importe nos templates que precisam:**
   ```html
   <script src="{{ url_for('static', filename='js/core/meu_modulo.js') }}"></script>
   ```

---

## 🔗 Dependências entre Módulos

### Dependências do Sistema

```
xlsx.bundle.js (libs/)
    ↓
excel_formatacao_core.js (excel/)
    ↓
excel_utils.js (excel/)
    ↓
excel_tabelas.js + excel_informativos.js (excel/)
    ↓
exportar_tabela_excel.js (core/)
```

### Scripts que Dependem do Core

**analise_horarios_comum.js é usado por:**
- `pages/frequencia/controle_frequencia.js`
- `pages/frequencia/debug_terminal.js`
- `pages/funcionarios/editar_funcionarios.js`
- Template: `detalhes_funcionario.html`

**exportar_tabela_excel.js é usado por:**
- `pages/checklist/editar_checklist.js`
- `pages/funcionarios/editar_funcionarios.js`
- `pages/frequencia/controle_frequencia.js`
- `pages/outros/editar_controle_nfs.js`
- Template: `detalhes_funcionario.html`

---

## 🧪 Testes e Validação

### Verificar Estrutura
```bash
# Listar estrutura
tree js/

# Verificar se não há arquivos soltos na raiz
ls js/*.js  # Deve retornar vazio (apenas pastas)
```

### Validar Imports nos Templates
```bash
# Buscar imports antigos (não devem existir)
grep -r "filename='js/[^/]*\.js'" templates/

# Buscar imports corretos (devem ter subpasta)
grep -r "filename='js/[a-z_]*/.*\.js'" templates/
```

---

## 📊 Estatísticas da Estrutura

| Categoria | Quantidade de Arquivos |
|-----------|------------------------|
| core/ | 2 arquivos |
| excel/ | 4 módulos + README |
| libs/ | 1 biblioteca |
| pages/checklist/ | 2 arquivos |
| pages/funcionarios/ | 2 arquivos |
| pages/frequencia/ | 3 arquivos |
| pages/gestao_documental/ | 3 arquivos |
| pages/outros/ | 5 arquivos |
| **TOTAL** | **22 arquivos JS** |

---

## 🚀 Benefícios desta Estrutura

1. **Organização Clara**: Fácil encontrar arquivos por funcionalidade
2. **Escalabilidade**: Simples adicionar novos módulos ou páginas
3. **Manutenibilidade**: Separação de responsabilidades bem definida
4. **Reutilização**: Código compartilhado em `core/` evita duplicação
5. **Modularidade**: Módulos `excel/` podem ser usados independentemente
6. **Navegação Rápida**: Estrutura de pastas intuitiva por domínio

---

## 📚 Documentação Adicional

- Para detalhes sobre os módulos Excel, veja: `excel/README.md`
- Para padrões de código JavaScript, veja documentação do projeto
- Para arquitetura de namespaces, veja exemplos em `core/` e `excel/`

---

**Última atualização:** Outubro 2025  
**Desenvolvido por:** Eng. Pedro Henrique
