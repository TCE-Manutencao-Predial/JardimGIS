# Módulos de Exportação Excel

Esta pasta contém módulos JavaScript modulares para exportação e formatação de arquivos Excel usando a biblioteca SheetJS (xlsx-js-style).

## 📁 Estrutura dos Módulos

```
js/excel/
├── excel_formatacao_core.js   # Estilos base e configurações
├── excel_utils.js              # Funções utilitárias
├── excel_tabelas.js            # Formatação de tabelas tabulares
└── excel_informativos.js       # Formatação de dados informativos
```

## 🔧 Módulos

### 1. **excel_formatacao_core.js**
**Namespace:** `window.ExcelFormatacao`

Define todos os estilos base e cores utilizados na formatação Excel.

**Principais recursos:**
- Definição de cores padronizadas (CORES)
- Estilos para cabeçalhos de tabela
- Estilos para linhas alternadas (clara/escura)
- Estilos para dados informativos (títulos, rótulos, valores)
- Estilos de status (positivo/negativo)
- Estilos de destaque (números, datas, médias)
- Funções auxiliares (clonarEstilo, mesclarEstilos)

**Exemplo de uso:**
```javascript
const estiloCabecalho = window.ExcelFormatacao.ESTILO_CABECALHO_TABELA;
const corAzul = window.ExcelFormatacao.CORES.AZUL_MEDIO;
```

---

### 2. **excel_utils.js**
**Namespace:** `window.ExcelUtils`

Funções utilitárias para manipulação de dados e worksheets.

**Principais recursos:**
- `prepararDadosTabela(tabela)` - Extrai dados de tabela HTML
- `obterValorCampo(container, selector)` - Obtém valor de input/select
- `calcularLargurasColunas(worksheet, range)` - Calcula larguras ideais
- `calcularAlturasLinhas(worksheet, range)` - Calcula alturas de linha
- `definirComoTabelaExcel(worksheet, dados)` - Define como tabela Excel
- `adicionarFiltroAutomatico(worksheet)` - Adiciona filtro automático
- `mesclarCelulas(worksheet, ...)` - Mescla células
- `verificarBibliotecaXLSX()` - Verifica se XLSX está disponível
- `gerarNomeArquivo(prefixo)` - Gera nome com data

**Exemplo de uso:**
```javascript
const dados = window.ExcelUtils.prepararDadosTabela(minhaTabela);
const larguras = window.ExcelUtils.calcularLargurasColunas(worksheet, range);
```

---

### 3. **excel_tabelas.js**
**Namespace:** `window.ExcelTabelas`  
**Requer:** `ExcelFormatacao`, `ExcelUtils`

Formatação de tabelas tabulares no estilo Excel (Table Style Medium 2 - Azul).

**Principais recursos:**
- `aplicarFormatacaoTabelaAzul(worksheet, dados)` - Formata tabela completa
- `aplicarFormatacaoStatus(worksheet, cellRef)` - Formata células de status
- `exportarTabelaHTML(elemento, nomeAba, nomeArquivo)` - Exportação direta
- `adicionarAbaTabelaJSON(dados, workbook, nomeAba)` - Adiciona aba de JSON

**Exemplo de uso:**
```javascript
// Formatação manual
window.ExcelTabelas.aplicarFormatacaoTabelaAzul(worksheet, dados);

// Exportação direta de tabela HTML
window.ExcelTabelas.exportarTabelaHTML(
    document.querySelector('#minhaTabela'),
    'Dados',
    'relatorio'
);
```

---

### 4. **excel_informativos.js**
**Namespace:** `window.ExcelInformativos`  
**Requer:** `ExcelFormatacao`, `ExcelUtils`

Formatação de dados não-tabulares (informações de funcionários, estatísticas, etc).

**Principais recursos:**
- `aplicarFormatacaoInformativa(worksheet, dados)` - Formatação simples
- `aplicarFormatacaoInformativaAvancada(worksheet, dados)` - Formatação profissional
- `aplicarFormatacaoCondicional(worksheet, dados, range)` - Destaque de valores
- `aplicarFormatacaoTipoValor(worksheet, cellRef, valor)` - Formatação por tipo
- `adicionarAbaInformativa(dados, workbook, nomeAba, avancado)` - Adiciona aba

**Exemplo de uso:**
```javascript
// Dados informativos simples
const dadosInfo = [
    ['TÍTULO PRINCIPAL'],
    [''],
    ['Nome:', 'João Silva'],
    ['CPF:', '123.456.789-00']
];

// Formatação avançada
window.ExcelInformativos.aplicarFormatacaoInformativaAvancada(worksheet, dadosInfo);
```

---

## 📝 Como Usar

### Ordem de Importação nos Templates HTML

```html
<!-- Biblioteca SheetJS -->
<script src="{{ url_for('static', filename='js/xlsx.bundle.js') }}"></script>

<!-- Módulos de Exportação Excel (ordem importante!) -->
<script src="{{ url_for('static', filename='js/excel/excel_formatacao_core.js') }}"></script>
<script src="{{ url_for('static', filename='js/excel/excel_utils.js') }}"></script>
<script src="{{ url_for('static', filename='js/excel/excel_tabelas.js') }}"></script>
<script src="{{ url_for('static', filename='js/excel/excel_informativos.js') }}"></script>

<!-- Script principal (para compatibilidade) -->
<script src="{{ url_for('static', filename='js/exportar_tabela_excel.js') }}"></script>
```

### Exemplo Completo: Exportando Tabela

```javascript
// Verifica biblioteca
if (!window.ExcelUtils.verificarBibliotecaXLSX()) {
    return;
}

// Cria workbook
const workbook = XLSX.utils.book_new();

// Método 1: Exportação direta de tabela HTML
window.ExcelTabelas.exportarTabelaHTML(
    document.querySelector('#minhaTabela'),
    'Dados',
    'relatorio'
);

// Método 2: Controle manual
const dados = window.ExcelUtils.prepararDadosTabela(minhaTabela);
const worksheet = XLSX.utils.aoa_to_sheet(dados);
window.ExcelTabelas.aplicarFormatacaoTabelaAzul(worksheet, dados);
XLSX.utils.book_append_sheet(workbook, worksheet, 'Dados');

// Salvar arquivo
const nomeArquivo = window.ExcelUtils.gerarNomeArquivo('MeuRelatorio');
XLSX.writeFile(workbook, nomeArquivo, { cellStyles: true });
```

### Exemplo: Múltiplas Abas

```javascript
const workbook = XLSX.utils.book_new();

// Aba 1: Dados tabulares
const dadosTabela = [...];
window.ExcelTabelas.adicionarAbaTabelaJSON(dadosTabela, workbook, 'Funcionários');

// Aba 2: Informações
const dadosInfo = [
    ['RELATÓRIO MENSAL'],
    [''],
    ['Data:', '02/10/2025'],
    ['Total de Funcionários:', '50']
];
window.ExcelInformativos.adicionarAbaInformativa(
    dadosInfo, 
    workbook, 
    'Informações',
    true // formatação avançada
);

// Salvar
XLSX.writeFile(workbook, 'relatorio.xlsx', { cellStyles: true });
```

---

## 🔄 Compatibilidade Retroativa

O arquivo `exportar_tabela_excel.js` mantém funções globais para compatibilidade com código legado:

```javascript
// ✅ Funções antigas ainda funcionam (deprecated)
aplicarFormatacaoTabelaAzul(worksheet, dados);
aplicarFormatacaoInformativa(worksheet, dados);
prepararDadosTabela(tabela);

// ✨ Novas funções modulares (recomendado)
window.ExcelTabelas.aplicarFormatacaoTabelaAzul(worksheet, dados);
window.ExcelInformativos.aplicarFormatacaoInformativa(worksheet, dados);
window.ExcelUtils.prepararDadosTabela(tabela);
```

---

## 🎨 Paleta de Cores

| Nome | Código RGB | Uso |
|------|-----------|-----|
| AZUL_MEDIO | 4472C4 | Cabeçalhos, títulos principais |
| AZUL_CLARO | D9E2F3 | Linhas alternadas |
| VERDE_SUCESSO | 006100 | Status positivo (OK, Sim) |
| VERMELHO_ERRO | 9C0006 | Status negativo (NC, Não) |
| ROXO_DESTAQUE | 7B1FA2 | Datas e horários |
| VERDE_DESTAQUE | 2E8B57 | Números positivos |

---

## 🧪 Testes

Páginas que utilizam estes módulos:
- ✅ `checklists_editar.html` - Exportação de checklists
- ✅ `editar_funcionarios.html` - Exportação de funcionários
- ✅ `editar_controle_nfs.html` - Exportação de notas fiscais
- ✅ `controle_frequencia.html` - Relatórios de frequência
- ✅ `detalhes_funcionario.html` - Detalhes individuais

---

## 📚 Dependências

- **SheetJS (xlsx-js-style)**: Biblioteca para criação e formatação de Excel
- Todos os módulos devem ser carregados APÓS `xlsx.bundle.js`
- `excel_formatacao_core.js` deve ser carregado primeiro (base para outros)

---

## 🚀 Benefícios da Modularização

1. **Manutenção**: Código organizado em responsabilidades claras
2. **Reutilização**: Módulos independentes podem ser usados em qualquer página
3. **Consistência**: Estilos centralizados garantem visual uniforme
4. **Testabilidade**: Módulos isolados são mais fáceis de testar
5. **Performance**: Carregamento sob demanda possível no futuro
6. **Documentação**: Cada módulo tem responsabilidade bem definida

---

**Desenvolvido por:** Eng. Pedro Henrique  
**Data:** Outubro 2025  
**Versão:** 1.0.0
