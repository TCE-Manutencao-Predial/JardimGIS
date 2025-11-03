# web.py - Versão refatorada com rotas principais - JardimGIS
import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash
import json
from datetime import datetime

from ...config import ARVORES_JSON_PATH
from ...utils.data.GerenciadorJSON import load_json_file, save_json_file
from ...utils.managers.GerenciadorBackupJSON import create_backup
from .GerenciadorAutorizacoes import requisitar_autorizacao_especial

web_bp = Blueprint('web', __name__)
jardimgis_logger = logging.getLogger('jardimgis')

@web_bp.route('/', methods=['GET', 'POST'])
@requisitar_autorizacao_especial
def index():
    """Página principal - exibe diretamente o controle de árvores"""
    usuario_autenticado = request.headers.get("X-Remote-User")
    if not usuario_autenticado:
        usuario_autenticado = "admin"
    
    # Carrega dados do controle de árvores
    arvores_data = load_json_file(ARVORES_JSON_PATH)

    # Se os dados estão no formato antigo com chave "Controle de NFs"
    if isinstance(arvores_data, dict) and "Controle de NFs" in arvores_data:
        arvores_data = arvores_data["Controle de NFs"]

    # Se o arquivo não existir ou estiver vazio, inicializa com lista vazia
    if not isinstance(arvores_data, list):
        arvores_data = []
    
    if request.method == 'POST':
        try:
            # Backup do arquivo antes das alterações
            create_backup(ARVORES_JSON_PATH)
            
            # Processa os dados do formulário
            import re
            row_pattern = re.compile(r"row-(\d+)-original")
            row_indexes = sorted({int(m.group(1)) for key in request.form.keys() if (m := row_pattern.match(key))})
            
            # Extrai colunas do formulário
            columns = []
            for key in request.form.keys():
                match_col = re.match(r"row-\d+-(.+)", key)
                if match_col:
                    col_name = match_col.group(1)
                    if col_name not in ["original"] and col_name not in columns:
                        columns.append(col_name)
            
            # Usa o login do usuário como responsável
            nome_responsavel = usuario_autenticado
            
            # Data atual formatada
            data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            
            # Constrói nova lista de árvores
            new_arvores_data = []
            for row_index in row_indexes:
                new_arvore = {}
                
                # Processa todos os campos
                for col in columns:
                    field_name = f"row-{row_index}-{col}"
                    value = request.form.get(field_name, "").strip()
                    new_arvore[col] = value
                
                # Atualiza campos automáticos
                new_arvore["Responsável"] = nome_responsavel
                new_arvore["Data da Última Atualização"] = data_atual
                
                new_arvores_data.append(new_arvore)
            
            # Salva os dados
            save_json_file(ARVORES_JSON_PATH, new_arvores_data)
            
            flash("Controle de árvores atualizado com sucesso!", "success")
            
        except Exception as e:
            jardimgis_logger.error(f"Erro ao processar controle de árvores: {e}")
            flash(f"Erro ao processar dados do controle de árvores: {str(e)}", "error")
            
        return redirect(url_for('web.index'))
    
    return render_template('index.html', arvores_data=arvores_data)

@web_bp.route('/jardimgis')
@requisitar_autorizacao_especial
def jardimgis_sem_barra():
    """
    Rota para compatibilidade com Apache - /jardimgis (sem barra final)
    """
    return redirect('/')

@web_bp.route('/jardimgis/')
@requisitar_autorizacao_especial
def jardimgis_com_barra():
    """
    Rota para compatibilidade com Apache - /jardimgis/ (com barra final)
    """
    return redirect('/')

@web_bp.route('/erro_acesso_negado_401')
@web_bp.route('/erro_acesso_negado_403')
def acesso_negado():
    return render_template('base/erro_acesso_negado.html')

@web_bp.route('/erro_interno_servidor_500')
def erro_interno():
    return render_template('base/erro_interno.html')

@web_bp.route('/erro_pagina_nao_encontrada_404')
def erro_pagina_nao_encontrada():
    return render_template('base/erro_pagina_nao_encontrada.html')