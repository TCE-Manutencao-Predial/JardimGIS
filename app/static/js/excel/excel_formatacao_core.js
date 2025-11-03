/**
 * ========================================================================
 * MÓDULO: Formatação Core para Excel
 * ========================================================================
 * Define estilos base e configurações de formatação Excel reutilizáveis
 * Namespace: window.ExcelFormatacao
 * ========================================================================
 */

window.ExcelFormatacao = (function() {
    'use strict';

    // =====================================================
    // CONFIGURAÇÕES DE CORES
    // =====================================================
    
    const CORES = {
        // Cores primárias (baseado no padrão Excel "Table Style Medium 2")
        AZUL_MEDIO: "4472C4",
        AZUL_CLARO: "D9E2F3",
        BRANCO: "FFFFFF",
        
        // Cores de status
        VERDE_SUCESSO: "006100",
        VERDE_CLARO: "C6EFCE",
        VERMELHO_ERRO: "9C0006",
        VERMELHO_CLARO: "FFC7CE",
        
        // Cores de texto
        TEXTO_BRANCO: "FFFFFF",
        TEXTO_ESCURO: "333333",
        TEXTO_CINZA: "2F4F4F",
        
        // Cores de fundo informativos
        CINZA_CLARO: "F2F2F2",
        CINZA_MEDIO: "E7E6E6",
        CINZA_ESCURO: "F0F0F0",
        FUNDO_CLARO: "F8F9FA",
        
        // Cores de destaque
        VERDE_DESTAQUE: "2E8B57",
        VERDE_FUNDO: "F1F8E9",
        AZUL_DESTAQUE: "4169E1",
        AZUL_FUNDO: "E3F2FD",
        ROXO_DESTAQUE: "7B1FA2",
        ROXO_FUNDO: "F3E5F5",
        VERMELHO_ALERTA: "B85450",
        VERMELHO_FUNDO: "FFF2F2",
        
        // Cores de bordas
        BORDA_CLARA: "D1D1D1",
        BORDA_MEDIA: "E1E5E9"
    };

    // =====================================================
    // ESTILOS BASE
    // =====================================================
    
    /**
     * Estilo para cabeçalho de tabela (Table Style Medium 2)
     */
    const ESTILO_CABECALHO_TABELA = {
        font: { 
            bold: true, 
            color: { rgb: CORES.TEXTO_BRANCO }, 
            size: 11,
            name: "Calibri"
        },
        alignment: { 
            horizontal: "center", 
            vertical: "center",
            wrapText: true
        },
        fill: { fgColor: { rgb: CORES.AZUL_MEDIO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.TEXTO_BRANCO } },
            bottom: { style: "thin", color: { rgb: CORES.TEXTO_BRANCO } },
            left: { style: "thin", color: { rgb: CORES.TEXTO_BRANCO } },
            right: { style: "thin", color: { rgb: CORES.TEXTO_BRANCO } }
        }
    };

    /**
     * Estilo para linhas claras de tabela
     */
    const ESTILO_LINHA_CLARA = {
        font: { 
            size: 11,
            name: "Calibri"
        },
        alignment: { 
            horizontal: "center", 
            vertical: "center",
            wrapText: true
        },
        fill: { fgColor: { rgb: CORES.BRANCO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            bottom: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            left: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            right: { style: "thin", color: { rgb: CORES.BORDA_CLARA } }
        }
    };

    /**
     * Estilo para linhas escuras de tabela (alternadas)
     */
    const ESTILO_LINHA_ESCURA = {
        font: { 
            size: 11,
            name: "Calibri"
        },
        alignment: { 
            horizontal: "center", 
            vertical: "center",
            wrapText: true
        },
        fill: { fgColor: { rgb: CORES.AZUL_CLARO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            bottom: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            left: { style: "thin", color: { rgb: CORES.BORDA_CLARA } },
            right: { style: "thin", color: { rgb: CORES.BORDA_CLARA } }
        }
    };

    /**
     * Estilo para título principal (dados informativos)
     */
    const ESTILO_TITULO_PRINCIPAL = {
        font: { 
            bold: true, 
            size: 16,
            name: "Calibri",
            color: { rgb: CORES.TEXTO_BRANCO }
        },
        alignment: { 
            horizontal: "center", 
            vertical: "center"
        },
        fill: { fgColor: { rgb: CORES.AZUL_MEDIO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.AZUL_MEDIO } },
            bottom: { style: "thin", color: { rgb: CORES.AZUL_MEDIO } },
            left: { style: "thin", color: { rgb: CORES.AZUL_MEDIO } },
            right: { style: "thin", color: { rgb: CORES.AZUL_MEDIO } }
        }
    };

    /**
     * Estilo para título de seção (dados informativos)
     */
    const ESTILO_TITULO_SECAO = {
        font: { 
            bold: true, 
            size: 14,
            name: "Calibri",
            color: { rgb: CORES.AZUL_MEDIO }
        },
        alignment: { 
            horizontal: "left", 
            vertical: "center"
        },
        fill: { fgColor: { rgb: CORES.CINZA_CLARO } }
    };

    /**
     * Estilo para rótulos (primeira coluna de dados informativos)
     */
    const ESTILO_ROTULO = {
        font: { 
            bold: true, 
            size: 12,
            name: "Calibri",
            color: { rgb: CORES.TEXTO_CINZA }
        },
        alignment: { 
            horizontal: "right", 
            vertical: "center"
        },
        fill: { fgColor: { rgb: CORES.FUNDO_CLARO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            bottom: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            left: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            right: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } }
        }
    };

    /**
     * Estilo para rótulos simples (versão mais simples)
     */
    const ESTILO_ROTULO_SIMPLES = {
        font: { 
            bold: true, 
            size: 11,
            name: "Calibri"
        },
        alignment: { 
            horizontal: "left", 
            vertical: "center"
        },
        fill: { fgColor: { rgb: CORES.CINZA_MEDIO } }
    };

    /**
     * Estilo para valores (segunda coluna de dados informativos)
     */
    const ESTILO_VALOR = {
        font: { 
            size: 12,
            name: "Calibri",
            color: { rgb: CORES.TEXTO_ESCURO }
        },
        alignment: { 
            horizontal: "left", 
            vertical: "center"
        },
        fill: { fgColor: { rgb: CORES.BRANCO } },
        border: {
            top: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            bottom: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            left: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } },
            right: { style: "thin", color: { rgb: CORES.BORDA_MEDIA } }
        }
    };

    /**
     * Estilo para valores simples (versão mais simples)
     */
    const ESTILO_VALOR_SIMPLES = {
        font: { 
            size: 11,
            name: "Calibri"
        },
        alignment: { 
            horizontal: "left", 
            vertical: "center"
        }
    };

    /**
     * Estilo para separadores/linhas vazias
     */
    const ESTILO_SEPARADOR = {
        font: { size: 8 },
        fill: { fgColor: { rgb: CORES.CINZA_ESCURO } }
    };

    // =====================================================
    // ESTILOS DE STATUS
    // =====================================================
    
    /**
     * Estilo para valores positivos (OK, Sim)
     */
    const ESTILO_POSITIVO = {
        font: { 
            bold: true, 
            color: { rgb: CORES.VERDE_SUCESSO }
        },
        fill: { fgColor: { rgb: CORES.VERDE_CLARO } }
    };

    /**
     * Estilo para valores negativos (NC, Não)
     */
    const ESTILO_NEGATIVO = {
        font: { 
            bold: true, 
            color: { rgb: CORES.VERMELHO_ERRO }
        },
        fill: { fgColor: { rgb: CORES.VERMELHO_CLARO } }
    };

    // =====================================================
    // ESTILOS DE DESTAQUE (para dados informativos)
    // =====================================================
    
    const ESTILOS_DESTAQUE = {
        numero_positivo: {
            font: { 
                bold: true,
                color: { rgb: CORES.VERDE_DESTAQUE }
            },
            fill: { fgColor: { rgb: CORES.VERDE_FUNDO } }
        },
        media: {
            font: { 
                bold: true,
                color: { rgb: CORES.AZUL_DESTAQUE }
            },
            fill: { fgColor: { rgb: CORES.AZUL_FUNDO } }
        },
        data_hora: {
            font: { 
                color: { rgb: CORES.ROXO_DESTAQUE }
            },
            fill: { fgColor: { rgb: CORES.ROXO_FUNDO } }
        },
        valor_falta: {
            font: { 
                italic: true,
                color: { rgb: CORES.VERMELHO_ALERTA }
            },
            fill: { fgColor: { rgb: CORES.VERMELHO_FUNDO } }
        }
    };

    // =====================================================
    // FUNÇÕES AUXILIARES
    // =====================================================

    /**
     * Clona profundamente um estilo para evitar mutações
     * @param {Object} estilo - Estilo a ser clonado
     * @returns {Object} Cópia do estilo
     */
    function clonarEstilo(estilo) {
        return JSON.parse(JSON.stringify(estilo));
    }

    /**
     * Mescla dois estilos (sobrescreve propriedades do base com override)
     * @param {Object} base - Estilo base
     * @param {Object} override - Estilo que sobrescreve
     * @returns {Object} Estilo mesclado
     */
    function mesclarEstilos(base, override) {
        const resultado = clonarEstilo(base);
        
        Object.keys(override).forEach(prop => {
            if (typeof override[prop] === 'object' && !Array.isArray(override[prop])) {
                resultado[prop] = { ...resultado[prop], ...override[prop] };
            } else {
                resultado[prop] = override[prop];
            }
        });
        
        return resultado;
    }

    // =====================================================
    // API PÚBLICA
    // =====================================================

    return {
        // Cores
        CORES,
        
        // Estilos de tabelas
        ESTILO_CABECALHO_TABELA,
        ESTILO_LINHA_CLARA,
        ESTILO_LINHA_ESCURA,
        
        // Estilos informativos
        ESTILO_TITULO_PRINCIPAL,
        ESTILO_TITULO_SECAO,
        ESTILO_ROTULO,
        ESTILO_ROTULO_SIMPLES,
        ESTILO_VALOR,
        ESTILO_VALOR_SIMPLES,
        ESTILO_SEPARADOR,
        
        // Estilos de status
        ESTILO_POSITIVO,
        ESTILO_NEGATIVO,
        
        // Estilos de destaque
        ESTILOS_DESTAQUE,
        
        // Funções auxiliares
        clonarEstilo,
        mesclarEstilos
    };

})();
