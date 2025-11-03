/**
 * ========================================================================
 * MÓDULO: Formatação de Dados Informativos Excel
 * ========================================================================
 * Funções para formatação de dados não-tabulares (informações de funcionários, etc)
 * Namespace: window.ExcelInformativos
 * Requer: ExcelFormatacao, ExcelUtils
 * ========================================================================
 */

window.ExcelInformativos = (function() {
    'use strict';

    // =====================================================
    // FORMATAÇÃO SIMPLES
    // =====================================================

    /**
     * Aplica formatação simples para dados informativos (não tabulares)
     * @param {Object} worksheet - Worksheet do SheetJS-Style
     * @param {Array} dados - Dados informativos (array de arrays [rotulo, valor])
     */
    function aplicarFormatacaoInformativa(worksheet, dados) {
        if (!worksheet || !dados) return;
        
        const range = XLSX.utils.decode_range(worksheet['!ref']);
        
        // Obtém estilos do módulo core
        const estiloTitulo = window.ExcelFormatacao.ESTILO_TITULO_SECAO;
        const estiloRotulo = window.ExcelFormatacao.ESTILO_ROTULO_SIMPLES;
        const estiloValor = window.ExcelFormatacao.ESTILO_VALOR_SIMPLES;
        
        // Aplica formatação célula por célula
        for (let row = range.s.r; row <= range.e.r; row++) {
            for (let col = range.s.c; col <= range.e.c; col++) {
                const cellRef = XLSX.utils.encode_cell({ r: row, c: col });
                
                if (!worksheet[cellRef]) continue;
                
                const valor = worksheet[cellRef].v ? worksheet[cellRef].v.toString() : '';
                
                // Identifica títulos das seções (células que contêm apenas texto em maiúscula e não têm valor na coluna B)
                if (col === 0 && valor.match(/^[A-ZÁÊÔÇÃO\s]+$/) && (!worksheet[XLSX.utils.encode_cell({ r: row, c: 1 })] || !worksheet[XLSX.utils.encode_cell({ r: row, c: 1 })].v)) {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloTitulo);
                }
                // Primeira coluna com dados (rótulos)
                else if (col === 0 && valor && valor !== '') {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloRotulo);
                }
                // Segunda coluna (valores)
                else if (col === 1) {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloValor);
                }
            }
        }
    }

    // =====================================================
    // FORMATAÇÃO AVANÇADA
    // =====================================================

    /**
     * Aplica formatação profissional avançada para dados informativos de funcionários
     * @param {Object} worksheet - Worksheet do SheetJS-Style
     * @param {Array} dados - Dados informativos (array de arrays [rotulo, valor])
     */
    function aplicarFormatacaoInformativaAvancada(worksheet, dados) {
        if (!worksheet || !dados) return;
        
        const range = XLSX.utils.decode_range(worksheet['!ref']);
        
        // Obtém estilos do módulo core
        const estiloTituloPrincipal = window.ExcelFormatacao.ESTILO_TITULO_PRINCIPAL;
        const estiloRotulo = window.ExcelFormatacao.ESTILO_ROTULO;
        const estiloValor = window.ExcelFormatacao.ESTILO_VALOR;
        const estiloSeparador = window.ExcelFormatacao.ESTILO_SEPARADOR;
        
        // Aplica formatação célula por célula
        for (let row = range.s.r; row <= range.e.r; row++) {
            for (let col = range.s.c; col <= range.e.c; col++) {
                const cellRef = XLSX.utils.encode_cell({ r: row, c: col });
                
                if (!worksheet[cellRef]) continue;
                
                const valor = worksheet[cellRef].v ? worksheet[cellRef].v.toString() : '';
                
                // Títulos principais das seções (INFORMAÇÕES DO FUNCIONÁRIO, ESTATÍSTICAS)
                if (col === 0 && valor.match(/^[A-ZÁÊÔÇÃO\s]+$/) && (!worksheet[XLSX.utils.encode_cell({ r: row, c: 1 })] || !worksheet[XLSX.utils.encode_cell({ r: row, c: 1 })].v)) {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloTituloPrincipal);
                    
                    // Mesclar células para o título ocupar toda a largura
                    window.ExcelUtils.mesclarCelulas(worksheet, row, 0, row, 1);
                }
                // Linhas vazias (separadores)
                else if (valor === '' || valor === ' ') {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloSeparador);
                }
                // Rótulos (primeira coluna com dados)
                else if (col === 0 && valor && valor !== '') {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloRotulo);
                }
                // Valores (segunda coluna)
                else if (col === 1 && valor && valor !== '') {
                    worksheet[cellRef].s = window.ExcelFormatacao.clonarEstilo(estiloValor);
                    
                    // Formatação especial para valores numéricos importantes
                    aplicarFormatacaoTipoValor(worksheet, cellRef, valor);
                }
            }
        }
        
        // Definir altura das linhas para melhor espaçamento
        const alturas = window.ExcelUtils.calcularAlturasLinhas(worksheet, range);
        worksheet['!rows'] = alturas;
        
        // Aplicar formatação condicional especial
        aplicarFormatacaoCondicional(worksheet, dados, range);
    }

    // =====================================================
    // FUNÇÕES AUXILIARES
    // =====================================================

    /**
     * Aplica formatação baseada no tipo de valor
     * @param {Object} worksheet - Worksheet do SheetJS
     * @param {string} cellRef - Referência da célula
     * @param {string} valor - Valor da célula
     */
    function aplicarFormatacaoTipoValor(worksheet, cellRef, valor) {
        // Formatação especial para valores numéricos importantes
        if (typeof valor === 'number' || valor.toString().match(/^\d+$/)) {
            const estiloNumero = window.ExcelFormatacao.ESTILOS_DESTAQUE.numero_positivo;
            worksheet[cellRef].s = window.ExcelFormatacao.mesclarEstilos(
                worksheet[cellRef].s,
                estiloNumero
            );
        }
        // Formatação especial para datas
        else if (valor.toString().match(/^\d{2}\/\d{2}\/\d{4}/)) {
            const estiloData = window.ExcelFormatacao.ESTILOS_DESTAQUE.data_hora;
            worksheet[cellRef].s = window.ExcelFormatacao.mesclarEstilos(
                worksheet[cellRef].s,
                estiloData
            );
        }
    }

    /**
     * Aplica formatação condicional baseada no conteúdo das células informativas
     * @param {Object} worksheet - Worksheet do SheetJS-Style
     * @param {Array} dados - Dados informativos
     * @param {Object} range - Range da planilha
     */
    function aplicarFormatacaoCondicional(worksheet, dados, range) {
        const estilos = window.ExcelFormatacao.ESTILOS_DESTAQUE;
        
        for (let row = range.s.r; row <= range.e.r; row++) {
            const cellRefCol1 = XLSX.utils.encode_cell({ r: row, c: 1 });
            
            if (!worksheet[cellRefCol1] || !worksheet[cellRefCol1].v) continue;
            
            const valor = worksheet[cellRefCol1].v.toString();
            
            // Destacar valores importantes com cores especiais
            if (valor === 'Nunca' || valor === 'Não informado' || valor === 'Não identificado' || valor === '0' || valor === '0.0') {
                // Valores em falta ou zero - cor vermelha suave
                worksheet[cellRefCol1].s = window.ExcelFormatacao.mesclarEstilos(
                    worksheet[cellRefCol1].s,
                    estilos.valor_falta
                );
            }
            // Valores numéricos positivos - destaque verde
            else if (valor.match(/^[1-9]\d*$/) && parseInt(valor) > 0) {
                worksheet[cellRefCol1].s = window.ExcelFormatacao.mesclarEstilos(
                    worksheet[cellRefCol1].s,
                    estilos.numero_positivo
                );
            }
            // Valores de média - destaque azul
            else if (valor.match(/^\d+\.\d+$/) && parseFloat(valor) > 0) {
                worksheet[cellRefCol1].s = window.ExcelFormatacao.mesclarEstilos(
                    worksheet[cellRefCol1].s,
                    estilos.media
                );
            }
            // Datas e horários - destaque roxo suave
            else if (valor.match(/\d{2}\/\d{2}\/\d{4}/) || valor.match(/\d{2}:\d{2}/)) {
                worksheet[cellRefCol1].s = window.ExcelFormatacao.mesclarEstilos(
                    worksheet[cellRefCol1].s,
                    estilos.data_hora
                );
            }
        }
    }

    /**
     * Cria uma aba de informações formatada
     * @param {Array} dadosInformativos - Array de arrays [rótulo, valor]
     * @param {Object} workbook - Workbook existente
     * @param {string} nomeAba - Nome da aba
     * @param {boolean} avancado - Se true, usa formatação avançada
     */
    function adicionarAbaInformativa(dadosInformativos, workbook, nomeAba, avancado = false) {
        if (!dadosInformativos || dadosInformativos.length === 0) {
            console.warn('Nenhum dado informativo para exportar na aba:', nomeAba);
            return;
        }
        
        // Cria worksheet a partir dos dados
        const worksheet = XLSX.utils.aoa_to_sheet(dadosInformativos);
        
        // Define larguras das colunas otimizadas
        worksheet['!cols'] = [
            { wch: 32 }, // rótulos (um pouco maior para acomodar textos mais longos)
            { wch: 45 }  // valores (maior para acomodar informações completas)
        ];
        
        // Aplica formatação apropriada
        if (avancado) {
            aplicarFormatacaoInformativaAvancada(worksheet, dadosInformativos);
        } else {
            aplicarFormatacaoInformativa(worksheet, dadosInformativos);
        }
        
        // Adiciona ao workbook
        XLSX.utils.book_append_sheet(workbook, worksheet, nomeAba);
    }

    // =====================================================
    // API PÚBLICA
    // =====================================================

    return {
        // Formatação simples
        aplicarFormatacaoInformativa,
        
        // Formatação avançada
        aplicarFormatacaoInformativaAvancada,
        aplicarFormatacaoCondicional,
        
        // Funções auxiliares
        aplicarFormatacaoTipoValor,
        
        // Funções de exportação
        adicionarAbaInformativa
    };

})();
