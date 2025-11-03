/**
 * ========================================================================
 * SCRIPT PRINCIPAL: Exportação de Tabelas para Excel
 * ========================================================================
 * Coordena a exportação de diferentes tipos de dados para Excel
 * Utiliza módulos modulares para formatação e manipulação
 * 
 * Módulos necessários:
 * - excel/excel_formatacao_core.js
 * - excel/excel_utils.js
 * - excel/excel_tabelas.js
 * - excel/excel_informativos.js
 * ========================================================================
 */

document.addEventListener("DOMContentLoaded", function () {
  // Verifica se estamos numa página de edição de checklist
  const tabela = document.querySelector("#form-container table");
  if (tabela) {
    // Cria e adiciona o botão de exportar Excel para checklists
    adicionarBotaoExportarExcel();
  }
  
  // Verifica se estamos na página de funcionários
  const btnExportarFuncionarios = document.getElementById('funcionarios-btn-exportar');
  if (btnExportarFuncionarios) {
    btnExportarFuncionarios.addEventListener('click', exportarFuncionariosExcel);
  }
});

// ========================================================================
// EXPORTAÇÃO DE CHECKLISTS
// ========================================================================

/**
 * Adiciona o botão "Exportar em Excel" na página de checklist
 */
function adicionarBotaoExportarExcel() {
  // Verifica se já existe um botão de exportar Excel
  const botaoExistente = document.getElementById("btn-exportar-excel");
  if (botaoExistente) {
    // Se já existe, apenas adiciona o evento de clique e sai
    botaoExistente.addEventListener("click", exportarParaExcel);
    return;
  }

  const formContainer = document.getElementById("form-container");
  if (!formContainer) return;

  // Encontra a área dos botões
  const botoesArea = formContainer.querySelector("form");
  if (!botoesArea) return;

  // Cria o botão apenas se não existir
  const botaoExportar = document.createElement("button");
  botaoExportar.type = "button";
  botaoExportar.id = "btn-exportar-excel";
  botaoExportar.innerHTML = '<i class="fas fa-file-excel"></i> Exportar em Excel';

  // Adiciona evento de clique
  botaoExportar.addEventListener("click", exportarParaExcel);

  // Insere o botão antes do botão "Retornar ao Início"
  const botaoRetornar = document.getElementById("btn-voltarInicio");
  if (botaoRetornar) {
    botaoRetornar.parentNode.insertBefore(botaoExportar, botaoRetornar);
  } else {
    // Se não encontrar o botão de retornar, adiciona no final
    botoesArea.appendChild(botaoExportar);
  }
}

/**
 * Função principal que exporta a tabela de checklist para Excel
 */
function exportarParaExcel() {
  try {
    // Verifica biblioteca XLSX
    if (!window.ExcelUtils.verificarBibliotecaXLSX()) {
      return;
    }

    const tabela = document.querySelector("#form-container table");
    const secaoTitle = document.getElementById("secaoTitle");
    const nomeSecao = secaoTitle ? secaoTitle.textContent.trim() : "Checklist";

    // Usa o módulo de tabelas para exportação direta
    window.ExcelTabelas.exportarTabelaHTML(tabela, nomeSecao, nomeSecao);
    
  } catch (error) {
    console.error('Erro ao exportar para Excel:', error);
    alert('Erro ao exportar para Excel. Verifique o console para mais detalhes.');
  }
}

// ========================================================================
// EXPORTAÇÃO DE FUNCIONÁRIOS
// ========================================================================

/**
 * Exporta dados de funcionários para Excel
 */
function exportarFuncionariosExcel() {
  try {
    // Verifica biblioteca XLSX
    if (!window.ExcelUtils.verificarBibliotecaXLSX()) {
      return;
    }
    
    // Coleta dados dos cards de funcionários
    const funcionarios = [];
    document.querySelectorAll('.funcionarios-card').forEach(card => {
      const id = card.getAttribute('data-employee-id') || '';
      const nome = card.querySelector('.funcionarios-input-nome')?.value || '';
      const cpf = card.querySelector('.funcionarios-input-cpf')?.value || '';
      const telefone = card.querySelector('.funcionarios-input-telefone')?.value || '';
      const cargo = window.ExcelUtils.obterValorCampo(card, '.funcionarios-input-cargo');
      const endereco = card.querySelector('.funcionarios-input-endereco')?.value || '';
      const empresa = window.ExcelUtils.obterValorCampo(card, '.funcionarios-input-empresa');
      const escolaridade = window.ExcelUtils.obterValorCampo(card, '.funcionarios-input-escolaridade');
      
      funcionarios.push({
        ID: id,
        'Nome Completo': nome,
        CPF: cpf,
        Telefone: telefone,
        'Cargo/Função': cargo,
        'Endereço': endereco,
        Empresa: empresa,
        Escolaridade: escolaridade
      });
    });
    
    if (funcionarios.length === 0) {
      alert('Não há funcionários para exportar!');
      return;
    }
    
    // Cria o livro de Excel
    const workbook = XLSX.utils.book_new();
    
    // Adiciona aba com formatação de tabela
    window.ExcelTabelas.adicionarAbaTabelaJSON(funcionarios, workbook, "Funcionários");
    
    // Gera o arquivo Excel e faz download
    const nomeArquivo = window.ExcelUtils.gerarNomeArquivo('Funcionarios');
    XLSX.writeFile(workbook, nomeArquivo, { cellStyles: true });
    
    console.log(`Exportado ${funcionarios.length} funcionários para Excel`);
  } catch (error) {
    console.error('Erro ao exportar funcionários para Excel:', error);
    alert('Erro ao exportar para Excel. Verifique o console para mais detalhes.');
  }
}

// ========================================================================
// COMPATIBILIDADE RETROATIVA
// ========================================================================
// Expõe funções no escopo global para compatibilidade com código legado

/**
 * @deprecated Use window.ExcelTabelas.aplicarFormatacaoTabelaAzul
 */
function aplicarFormatacaoTabelaAzul(worksheet, dados) {
  return window.ExcelTabelas.aplicarFormatacaoTabelaAzul(worksheet, dados);
}

/**
 * @deprecated Use window.ExcelInformativos.aplicarFormatacaoInformativa
 */
function aplicarFormatacaoInformativa(worksheet, dados) {
  return window.ExcelInformativos.aplicarFormatacaoInformativa(worksheet, dados);
}

/**
 * @deprecated Use window.ExcelInformativos.aplicarFormatacaoInformativaAvancada
 */
function aplicarFormatacaoInformativaAvancada(worksheet, dados) {
  return window.ExcelInformativos.aplicarFormatacaoInformativaAvancada(worksheet, dados);
}

/**
 * @deprecated Use window.ExcelUtils.prepararDadosTabela
 */
function prepararDadosTabela(tabela) {
  return window.ExcelUtils.prepararDadosTabela(tabela);
}

/**
 * @deprecated Use window.ExcelUtils.calcularLargurasColunas
 */
function calcularLargurasColunas(worksheet, range) {
  return window.ExcelUtils.calcularLargurasColunas(worksheet, range);
}


