/**
 * ========================================================================
 * MÓDULO: Formatação de Tabelas Excel
 * ========================================================================
 * Funções para formatação de tabelas tabulares no estilo Excel
 * Namespace: window.ExcelTabelas
 * Requer: ExcelFormatacao, ExcelUtils
 * ========================================================================
 */

window.ExcelTabelas = (function() {
    'use strict';

    // =====================================================
    // FUNÇÃO PRINCIPAL DE FORMATAÇÃO
    // =====================================================

    /**
     * Aplica formatação estilo "Tabela Excel Azul Médio" com linhas alternadas
     * @param {Object} worksheet - Worksheet do SheetJS-Style
     * @param {Array} dados - Dados da tabela
     */
    function aplicarFormatacaoTabelaAzul(worksheet, dados) {
        if (!worksheet || !dados) return;
        
        // Define o range da tabela
        const range = XLSX.utils.decode_range(worksheet['!ref']);
        
        // Obtém estilos do módulo core
        const estilosCabecalho = window.ExcelFormatacao.ESTILO_CABECALHO_TABELA;
        const estilosLinhaClara = window.ExcelFormatacao.ESTILO_LINHA_CLARA;
        const estilosLinhaEscura = window.ExcelFormatacao.ESTILO_LINHA_ESCURA;
        
        // Aplica formatação célula por célula
        for (let row = range.s.r; row <= range.e.r; row++) {
            for (let col = range.s.c; col <= range.e.c; col++) {
                const cellRef = XLSX.utils.encode_cell({ r: row, c: col });
                
                if (!worksheet[cellRef]) continue;
                
                // Cabeçalho da tabela (primeira linha)
                if (row === 0) {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estilosCabecalho);
                }
                // Linhas de dados alternadas
                else {
                    // Linhas pares (2, 4, 6...) = escuras, ímpares (3, 5, 7...) = claras
                    if (row % 2 === 0) {
                        worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estilosLinhaEscura);
                    } else {
                        worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estilosLinhaClara);
                    }
                    
                    // Formatação especial para status OK/NC e Sim/Não
                    aplicarFormatacaoStatus(worksheet, cellRef);
                }
            }
        }
        
        // Define larguras das colunas automaticamente (apenas se não foram definidas antes)
        if (!worksheet['!cols']) {
            const colWidths = window.ExcelUtils.calcularLargurasColunas(worksheet, range);
            worksheet['!cols'] = colWidths;
        }
        
        // Adiciona filtro automático na linha do cabeçalho
        window.ExcelUtils.adicionarFiltroAutomatico(worksheet, range);
        
        // Define a área como uma Table do Excel
        window.ExcelUtils.definirComoTabelaExcel(worksheet, dados);
    }

    // =====================================================
    // FUNÇÕES AUXILIARES
    // =====================================================

    /**
     * Aplica formatação especial para células de status
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {string} cellRef - Referência da célula
     */
    function aplicarFormatacaoStatus(worksheet, cellRef) {
        const valor = worksheet[cellRef].v;
        
        // Valores positivos (OK, Sim)
        if (valor === "OK" || valor === "Sim") {
            const estiloPositivo = window.ExcelFormatacao.ESTILO_POSITIVO;
            worksheet[cellRef].s = window.ExcelFormatacao.mesclarEstilos(
                worksheet[cellRef].s,
                estiloPositivo
            );
        }
        // Valores negativos (NC, Não)
        else if (valor === "NC" || valor === "NC (Não Conforme)" || valor === "Não") {
            const estiloNegativo = window.ExcelFormatacao.ESTILO_NEGATIVO;
            worksheet[cellRef].s = window.ExcelFormatacao.mesclarEstilos(
                worksheet[cellRef].s,
                estiloNegativo
            );
        }
    }

    /**
     * Exporta uma tabela HTML para Excel com formatação azul
     * @param {HTMLTableElement} tabelaElement - Elemento da tabela HTML
     * @param {string} nomeAba - Nome da aba no Excel
     * @param {string} nomeArquivo - Nome do arquivo (sem extensão)
     * @returns {Object} Workbook criado
     */
    function exportarTabelaHTML(tabelaElement, nomeAba, nomeArquivo) {
        // Verifica biblioteca XLSX
        if (!window.ExcelUtils.verificarBibliotecaXLSX()) {
            return null;
        }
        
        // Prepara os dados da tabela
        const dadosTabela = window.ExcelUtils.prepararDadosTabela(tabelaElement);
        
        // Cria a workbook
        const workbook = XLSX.utils.book_new();
        
        // Cria a worksheet a partir dos dados
        const worksheet = XLSX.utils.aoa_to_sheet(dadosTabela);
        
        // Aplica formatação
        aplicarFormatacaoTabelaAzul(worksheet, dadosTabela);
        
        // Adiciona a worksheet ao workbook
        XLSX.utils.book_append_sheet(workbook, worksheet, nomeAba);
        
        // Gera o arquivo
        const nomeCompleto = window.ExcelUtils.gerarNomeArquivo(nomeArquivo);
        XLSX.writeFile(workbook, nomeCompleto, { cellStyles: true });
        
        return workbook;
    }

    /**
     * Cria uma aba de tabela formatada a partir de dados JSON
     * @param {Array} dados - Array de objetos com os dados
     * @param {Object} workbook - Workbook existente
     * @param {string} nomeAba - Nome da aba
     */
    function adicionarAbaTabelaJSON(dados, workbook, nomeAba) {
        if (!dados || dados.length === 0) {
            console.warn('Nenhum dado para exportar na aba:', nomeAba);
            return;
        }
        
        // Cria planilha a partir do JSON
        const worksheet = XLSX.utils.json_to_sheet(dados);
        
        // Converte para array de arrays para formatação
        const range = XLSX.utils.decode_range(worksheet['!ref']);
        const dadosArray = [];
        
        // Coleta cabeçalhos
        const cabecalhos = Object.keys(dados[0]);
        dadosArray.push(cabecalhos);
        
        // Coleta dados
        dados.forEach(row => {
            dadosArray.push(cabecalhos.map(key => row[key]));
        });
        
        // Aplica formatação
        aplicarFormatacaoTabelaAzul(worksheet, dadosArray);
        
        // Adiciona ao workbook
        XLSX.utils.book_append_sheet(workbook, worksheet, nomeAba);
    }

    // =====================================================
    // API PÚBLICA
    // =====================================================

    return {
        // Função principal
        aplicarFormatacaoTabelaAzul,
        
        // Funções auxiliares
        aplicarFormatacaoStatus,
        
        // Funções de exportação
        exportarTabelaHTML,
        adicionarAbaTabelaJSON
    };

})();
