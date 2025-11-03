// editar_controle_nfs.js - Script para edição de NFs

// Função para remover um card de NF
function removeNFCard(button) {
    if (confirm('Tem certeza que deseja remover esta nota fiscal?')) {
        const card = button.closest('.nfs-card');
        card.style.opacity = '0';
        card.style.transform = 'scale(0.8)';
        setTimeout(() => {
            card.remove();
            updateNFIndexes();
        }, 300);
    }
}

// Função para atualizar os índices após remoção
function updateNFIndexes() {
    const cards = document.querySelectorAll('.nfs-card');
    cards.forEach((card, index) => {
        card.setAttribute('data-nf-index', index);
        
        // Atualiza todos os inputs dentro do card
        const inputs = card.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            const name = input.getAttribute('name');
            if (name) {
                const newName = name.replace(/row-\d+-/, `row-${index}-`);
                input.setAttribute('name', newName);
            }
        });
    });
}

// Função para adicionar nova NF
document.addEventListener('DOMContentLoaded', function() {
    const btnAddRow = document.getElementById('btn-add-row');
    
    if (btnAddRow) {
        btnAddRow.addEventListener('click', function() {
            const container = document.getElementById('nfs-container');
            const currentCards = container.querySelectorAll('.nfs-card');
            const newIndex = currentCards.length;
            
            const newCard = createNFCard(newIndex);
            container.insertAdjacentHTML('beforeend', newCard);
            
            // Animação de entrada
            const addedCard = container.lastElementChild;
            addedCard.style.opacity = '0';
            addedCard.style.transform = 'scale(0.8)';
            setTimeout(() => {
                addedCard.style.transition = 'all 0.3s';
                addedCard.style.opacity = '1';
                addedCard.style.transform = 'scale(1)';
            }, 10);
            
            // Scroll suave até o novo card
            addedCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
    
    // Formatação de valores monetários
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('nfs-input-valor')) {
            formatarValor(e.target);
        }
    });
    
    // Atualização do display de valor
    document.addEventListener('blur', function(e) {
        if (e.target.classList.contains('nfs-input-valor')) {
            const card = e.target.closest('.nfs-card');
            const display = card.querySelector('.nfs-valor-display');
            if (display) {
                display.textContent = e.target.value || 'R$ 0,00';
            }
        }
    }, true);
});

// Função para criar HTML de um novo card de NF
function createNFCard(index) {
    return `
        <div class="nfs-card" data-nf-index="${index}">
            <div class="nfs-card-header">
                <div class="nfs-card-empresa">Nova Nota Fiscal</div>
                <button type="button" class="nfs-btn-remove" onclick="removeNFCard(this)">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
            
            <div class="nfs-card-body">
                <div class="nfs-valor-display">R$ 0,00</div>
                
                <div class="nfs-form-row">
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-building"></i> Empresa
                        </label>
                        <input type="text" 
                               name="row-${index}-Empresa" 
                               value=""
                               class="nfs-input"
                               placeholder="Nome da empresa">
                    </div>
                    
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-file-contract"></i> Processo
                        </label>
                        <input type="text" 
                               name="row-${index}-Processo do Contrato" 
                               value=""
                               class="nfs-input"
                               placeholder="Número do processo">
                    </div>
                </div>

                <div class="nfs-form-group">
                    <label class="nfs-label">
                        <i class="fas fa-clipboard-list"></i> Objeto do Contrato
                    </label>
                    <input type="text" 
                           name="row-${index}-Objeto do Contrato" 
                           value=""
                           class="nfs-input"
                           placeholder="Descrição do objeto">
                </div>

                <div class="nfs-form-row">
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-calendar-times"></i> Término
                        </label>
                        <input type="text" 
                               name="row-${index}-Data término do contrato" 
                               value=""
                               class="nfs-input nfs-input-data"
                               placeholder="mm/aaaa">
                    </div>
                    
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-file-alt"></i> Memorando
                        </label>
                        <input type="text" 
                               name="row-${index}-N° Memorando" 
                               value=""
                               class="nfs-input nfs-input-memorando"
                               placeholder="000/aaaa">
                    </div>
                </div>

                <div class="nfs-form-row">
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-calendar-alt"></i> Data Memo
                        </label>
                        <input type="text" 
                               name="row-${index}-Data Memorando" 
                               value=""
                               class="nfs-input nfs-input-data"
                               placeholder="DD/MM/AAAA">
                    </div>
                    
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-dollar-sign"></i> Valor
                        </label>
                        <input type="text" 
                               name="row-${index}-Valor da NF" 
                               value=""
                               class="nfs-input nfs-input-valor"
                               placeholder="R$ 0,00">
                    </div>
                </div>

                <div class="nfs-form-row">
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-user-tie"></i> Responsável
                        </label>
                        <input type="text" 
                               name="row-${index}-Responsável" 
                               value="Não definido"
                               class="nfs-input nfs-input-readonly"
                               placeholder="Responsável pela edição"
                               readonly>
                    </div>
                    
                    <div class="nfs-form-group">
                        <label class="nfs-label">
                            <i class="fas fa-clock"></i> Última Atualização
                        </label>
                        <input type="text" 
                               name="row-${index}-Data da Última Atualização" 
                               value="Nunca editado"
                               class="nfs-input nfs-input-readonly"
                               placeholder="Data da última modificação"
                               readonly>
                    </div>
                </div>

                <div class="nfs-form-group">
                    <label class="nfs-label">
                        <i class="fas fa-sticky-note"></i> Observações
                    </label>
                    <textarea name="row-${index}-Observações" 
                              class="nfs-textarea"
                              placeholder="Observações adicionais"
                              rows="2"></textarea>
                </div>

                <input type="hidden" name="row-${index}-original" value="{}" />
            </div>
        </div>
    `;
}

// Função para formatar valor monetário
function formatarValor(input) {
    let valor = input.value.replace(/\D/g, '');
    
    if (valor.length === 0) {
        input.value = '';
        return;
    }
    
    valor = (parseInt(valor) / 100).toFixed(2);
    valor = valor.replace('.', ',');
    valor = valor.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');
    input.value = 'R$ ' + valor;
}

// Confirmação antes de sair da página com alterações não salvas
let formModified = false;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('nfs-form');
    
    if (form) {
        form.addEventListener('input', function() {
            formModified = true;
        });
        
        form.addEventListener('submit', function() {
            formModified = false;
        });
    }
});

window.addEventListener('beforeunload', function(e) {
    if (formModified) {
        e.preventDefault();
        e.returnValue = '';
    }
});
