# 📁 Estrutura de CSS - ChecklistsPredial

Este documento descreve a organização dos arquivos CSS da aplicação.

## 🗂️ Organização

### **css/core/** - Estilos Base (5 arquivos)
Estilos compartilhados entre todas as páginas:

- **base.css** (10KB) - Estilos base globais
- **styles.css** (18KB) - Estilos principais da aplicação
- **mobile.css** (11KB) - Responsividade mobile
- **erros.css** (15KB) - Páginas de erro
- **index.css** (22KB) - Página inicial

### **css/pages/** - Estilos Específicos (15 arquivos)
Estilos organizados por domínio funcional:

#### **pages/checklists/** (1 arquivo)
- **checklists.css** (33KB) - Sistema de checklists

#### **pages/funcionarios/** (5 arquivos)
- **empresas_funcionarios.css** (15KB) - Relação empresas/funcionários
- **funcionarios.css** (26KB) - Gerenciamento de funcionários
- **detalhes_funcionario.css** (11KB) - Detalhes individuais
- **dashboard_faltas.css** (5KB) - Dashboard de faltas
- **empresas.css** (19KB) - Cadastro de empresas

#### **pages/frequencia/** (4 arquivos)
- **controle_frequencia.css** (23KB) - Controle de frequência
- **controle_frequencia_gerenciar_terminal.css** (12KB) - Gestão de terminal
- **debug_terminal.css** (11KB) - Debug de terminal
- **gerenciar_terminal_errors.css** (6KB) - Erros de terminal

#### **pages/gestao_documental/** (2 arquivos)
- **gestao_documental.css** (65KB) ⭐ - Gestão de documentos
- **revisao_arquivos.css** (4KB) - Revisão de arquivos

#### **pages/outros/** (3 arquivos)
- **controle_nfs.css** (19KB) - Controle de notas fiscais
- **editar_jornada.css** (12KB) - Edição de jornadas
- **gerenciar_jornadas.css** (9KB) - Gerenciamento de jornadas

## 📊 Estatísticas
- **Total de arquivos:** 20
- **Tamanho total:** ~360KB
- **Maior arquivo:** gestao_documental.css (65KB)
- **Referências nos templates:** 88

## 🔗 Como Usar

### Templates HTML
Use `url_for` para referenciar CSS:

```html
<!-- CSS Core -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/core/base.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/core/mobile.css') }}">

<!-- CSS Pages -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/checklists/checklists.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/funcionarios/funcionarios.css') }}">
```

## 📝 Manutenção

### Adicionar Novo CSS
1. Identifique se é **core** (compartilhado) ou **pages** (específico)
2. Se for pages, escolha a categoria apropriada ou crie nova
3. Crie o arquivo na pasta correta
4. Referencie usando `url_for` nos templates

### Mover Arquivo Existente
1. Mova o arquivo fisicamente
2. Atualize TODAS as referências nos templates
3. Teste em desenvolvimento antes de deploy

## 🚀 Benefícios da Estrutura
- ✅ Organização clara por domínio funcional
- ✅ Fácil localização de estilos
- ✅ Separação core vs. pages
- ✅ Redução de conflitos entre estilos
- ✅ Manutenibilidade melhorada

---
**Última atualização:** 2025-01-XX  
**Versão:** 1.0  
**Autor:** Sistema ChecklistsPredial
