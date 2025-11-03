/**
 * ========================================================================
 * MÓDULO: Utilitários para Excel
 * ========================================================================
 * Funções auxiliares para manipulação de dados e worksheet
 * Namespace: window.ExcelUtils
 * ========================================================================
 */

window.ExcelUtils = (function() {
    'use strict';

    // =====================================================
    // FUNÇÕES DE PREPARAÇÃO DE DADOS
    // =====================================================

    /**
     * Prepara os dados da tabela HTML para exportação
     * @param {HTMLTableElement} tabela - Elemento de tabela HTML
     * @returns {Array} Array bidimensional com os dados da tabela
     */
    function prepararDadosTabela(tabela) {
        const dados = [];
        
        // Processa o cabeçalho
        const cabecalho = tabela.querySelector("thead tr");
        if (cabecalho) {
            const linhaCabecalho = [];
            cabecalho.querySelectorAll("th").forEach(th => {
                linhaCabecalho.push(th.textContent.trim());
            });
            dados.push(linhaCabecalho);
        }
        
        // Processa as linhas de dados
        const linhasCorpo = tabela.querySelectorAll("tbody tr");
        linhasCorpo.forEach((linha, indice) => {
            const linhaData = [];
            
            // Primeira célula é sempre o número do item
            linhaData.push(indice);
            
            // Processa as outras células (incluindo a última que é Observações)
            const celulas = linha.querySelectorAll("td");
            for (let i = 1; i < celulas.length; i++) { // Pula apenas a primeira célula (item)
                const celula = celulas[i];
                let valor = "";
                
                // Pula inputs hidden (não visíveis)
                const input = celula.querySelector("input[type='hidden']");
                if (input && input.type === "hidden") {
                    continue; // Pula esta célula e vai para a próxima
                }
                
                // Verifica diferentes tipos de input/select
                const inputVisivel = celula.querySelector("input:not([type='hidden']), select, textarea");
                if (inputVisivel) {
                    if (inputVisivel.type === "date") {
                        // Converte data do formato YYYY-MM-DD para DD/MM/YYYY
                        if (inputVisivel.value) {
                            const partesData = inputVisivel.value.split("-");
                            valor = `${partesData[2]}/${partesData[1]}/${partesData[0]}`;
                        }
                    } else if (inputVisivel.tagName === "SELECT") {
                        // Para selects, pega o texto da opção selecionada
                        const opcaoSelecionada = inputVisivel.options[inputVisivel.selectedIndex];
                        valor = opcaoSelecionada ? opcaoSelecionada.text : inputVisivel.value;
                    } else {
                        valor = inputVisivel.value || "";
                    }
                } else {
                    valor = celula.textContent.trim();
                }
                
                linhaData.push(valor);
            }
            
            dados.push(linhaData);
        });
        
        return dados;
    }

    /**
     * Função auxiliar para obter valor de campo que pode ser input ou select
     * @param {HTMLElement} container - Container do campo
     * @param {string} selector - O seletor CSS para o campo
     * @returns {string} O valor do campo
     */
    function obterValorCampo(container, selector) {
        const field = container.querySelector(selector);
        if (!field) return '';
        
        if (field.tagName === 'SELECT') {
            return field.options[field.selectedIndex]?.text || '';
        } else {
            return field.value || '';
        }
    }

    // =====================================================
    // FUNÇÕES DE CÁLCULO DE DIMENSÕES
    // =====================================================

    /**
     * Calcula as larguras ideais das colunas baseado no conteúdo
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {Object} range - Range da worksheet
     * @returns {Array} Array com as configurações de largura
     */
    function calcularLargurasColunas(worksheet, range) {
        const colWidths = [];
        
        // Primeiro, identificar os cabeçalhos das colunas para aplicar larguras específicas
        const headers = [];
        for (let col = range.s.c; col <= range.e.c; col++) {
            const headerCellRef = XLSX.utils.encode_cell({ r: 0, c: col });
            if (worksheet[headerCellRef] && worksheet[headerCellRef].v) {
                headers[col] = worksheet[headerCellRef].v.toString().trim();
            }
        }
        
        for (let col = range.s.c; col <= range.e.c; col++) {
            const headerText = headers[col] || '';
            let isCargoFuncao = headerText.toLowerCase().includes('cargo') || headerText.toLowerCase().includes('função');
            let isObservacoes = headerText.toLowerCase().includes('observações') || headerText.toLowerCase().includes('observacoes');
            let isEndereco = headerText.toLowerCase().includes('endereço') || headerText.toLowerCase().includes('endereco');
            
            // Aplicar larguras fixas específicas para colunas especiais
            if (isObservacoes) {
                // Para coluna Observações, definir largura fixa de 85 caracteres
                colWidths.push({ wch: 85 });
                continue;
            } else if (isCargoFuncao || isEndereco) {
                // Para colunas Cargo/Função e Endereço, definir largura fixa de 40 caracteres
                colWidths.push({ wch: 40 });
                continue;
            }
            
            // Para outras colunas, calcular baseado no conteúdo
            let maxWidth = 10; // Largura mínima
            
            for (let row = range.s.r; row <= range.e.r; row++) {
                const cellRef = XLSX.utils.encode_cell({ r: row, c: col });
                if (worksheet[cellRef] && worksheet[cellRef].v) {
                    const content = worksheet[cellRef].v.toString();
                    let contentWidth = content.length;
                    
                    // Ajustes especiais para diferentes tipos de conteúdo
                    if (row === 0) {
                        // Cabeçalhos precisam de mais espaço
                        contentWidth = Math.max(contentWidth, 12);
                    }
                    
                    // Para datas, define uma largura adequada
                    if (content.match(/^\d{2}\/\d{2}\/\d{4}$/)) {
                        contentWidth = 14;
                    }
                    
                    // Para valores monetários
                    if (content.includes('R$')) {
                        contentWidth = Math.max(contentWidth, 15);
                    }
                    
                    maxWidth = Math.max(maxWidth, contentWidth + 3);
                }
            }
            
            // Limita a largura máxima para outras colunas
            maxWidth = Math.min(maxWidth, 60);
            
            colWidths.push({ wch: maxWidth });
        }
        
        return colWidths;
    }

    /**
     * Define alturas de linha baseado no conteúdo
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {Object} range - Range da worksheet
     * @param {Object} opcoes - Opções de configuração
     * @returns {Array} Array com configurações de altura
     */
    function calcularAlturasLinhas(worksheet, range, opcoes = {}) {
        const alturas = [];
        const padroes = {
            titulo: 24,
            normal: 18,
            separador: 12,
            cabecalho: 20
        };
        
        for (let row = range.s.r; row <= range.e.r; row++) {
            const cellRef = XLSX.utils.encode_cell({ r: row, c: 0 });
            const cellValue = worksheet[cellRef]?.v || '';
            const cellText = cellValue.toString();
            
            let altura;
            
            // Linhas de título principais ficam mais altas
            if (cellText.match(/^[A-ZÁÊÔÇÃO\s]+$/)) {
                altura = padroes.titulo;
            }
            // Linhas vazias ficam menores
            else if (!cellText || cellText === '') {
                altura = padroes.separador;
            }
            // Primeira linha (cabeçalho)
            else if (row === 0 && opcoes.primoiraLinhaCabecalho) {
                altura = padroes.cabecalho;
            }
            // Linhas normais
            else {
                altura = padroes.normal;
            }
            
            alturas.push({ hpt: altura });
        }
        
        return alturas;
    }

    // =====================================================
    // FUNÇÕES DE CONFIGURAÇÃO DE WORKSHEET
    // =====================================================

    /**
     * Define a área como uma Table do Excel com estilo
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {Array} dados - Dados da tabela
     * @param {string} estilo - Nome do estilo da tabela (padrão: TableStyleMedium2)
     */
    function definirComoTabelaExcel(worksheet, dados, estilo = "TableStyleMedium2") {
        if (!dados || dados.length === 0) return;
        
        // Define o range da tabela
        const tableRange = {
            s: { r: 0, c: 0 },
            e: { r: dados.length - 1, c: dados[0].length - 1 }
        };
        
        // Define metadados da tabela Excel
        if (!worksheet['!tables']) {
            worksheet['!tables'] = [];
        }
        
        worksheet['!tables'].push({
            ref: XLSX.utils.encode_range(tableRange),
            name: "Table1",
            displayName: "Table1",
            headerRowCount: 1,
            totalsRowCount: 0,
            totalsRowShown: false,
            tableBorderDxfId: 0,
            tableStyle: estilo,
            tableStyleInfo: {
                name: estilo,
                showFirstColumn: false,
                showLastColumn: false,
                showRowStripes: true,
                showColumnStripes: false
            }
        });
    }

    /**
     * Adiciona filtro automático na linha do cabeçalho
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {Object} range - Range da worksheet (opcional, calculado se não fornecido)
     */
    function adicionarFiltroAutomatico(worksheet, range = null) {
        if (!range) {
            range = XLSX.utils.decode_range(worksheet['!ref']);
        }
        
        worksheet['!autofilter'] = { 
            ref: `A1:${XLSX.utils.encode_cell({ r: 0, c: range.e.c })}` 
        };
    }

    /**
     * Mescla células
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {number} startRow - Linha inicial (0-based)
     * @param {number} startCol - Coluna inicial (0-based)
     * @param {number} endRow - Linha final (0-based)
     * @param {number} endCol - Coluna final (0-based)
     */
    function mesclarCelulas(worksheet, startRow, startCol, endRow, endCol) {
        if (!worksheet['!merges']) {
            worksheet['!merges'] = [];
        }
        
        worksheet['!merges'].push({
            s: { r: startRow, c: startCol },
            e: { r: endRow, c: endCol }
        });
    }

    // =====================================================
    // FUNÇÕES DE VALIDAÇÃO
    // =====================================================

    /**
     * Verifica se a biblioteca XLSX está disponível
     * @returns {boolean} True se disponível, false caso contrário
     */
    function verificarBibliotecaXLSX() {
        if (typeof XLSX === 'undefined') {
            console.error('Biblioteca XLSX não encontrada!');
            alert('Biblioteca de exportação Excel não encontrada. Contacte o administrador.');
            return false;
        }
        return true;
    }

    /**
     * Gera nome de arquivo com data atual
     * @param {string} prefixo - Prefixo do nome do arquivo
     * @param {string} extensao - Extensão do arquivo (padrão: xlsx)
     * @returns {string} Nome do arquivo formatado
     */
    function gerarNomeArquivo(prefixo, extensao = 'xlsx') {
        const dataAtual = new Date();
        const dataFormatada = `${dataAtual.getDate().toString().padStart(2, '0')}-${(dataAtual.getMonth() + 1).toString().padStart(2, '0')}-${dataAtual.getFullYear()}`;
        return `${prefixo}_${dataFormatada}.${extensao}`;
    }

    // =====================================================
    // API PÚBLICA
    // =====================================================

    return {
        // Preparação de dados
        prepararDadosTabela,
        obterValorCampo,
        
        // Cálculo de dimensões
        calcularLargurasColunas,
        calcularAlturasLinhas,
        
        // Configuração de worksheet
        definirComoTabelaExcel,
        adicionarFiltroAutomatico,
        mesclarCelulas,
        
        // Validação e utilidades
        verificarBibliotecaXLSX,
        gerarNomeArquivo
    };

})();
