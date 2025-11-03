# admin.py - Rotas administrativas para JardimGIS
import json
import os
from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, url_for, request, flash, make_response
import logging

from ...config import DATA_DIR
from ...utils.managers.GerenciadorBackupJSON import backup_manager, list_backups, restore_backup, create_backup
from .GerenciadorAutorizacoes import requisitar_autorizacao_especial

jardimgis_logger = logging.getLogger('jardimgis')

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/backups', methods=['GET'])
@requisitar_autorizacao_especial
def gerenciar_backups():
    """
    Página para gerenciar backups dos arquivos JSON do sistema.
    """
    # Lista de arquivos principais que podem ter backups
    arquivos_principais = [
        ("Controle de Árvores", os.path.join(DATA_DIR, 'arvores.json')),
    ]
    
    backup_info = {}
    
    for nome, caminho in arquivos_principais:
        if os.path.exists(caminho):
            info = backup_manager.get_backup_info(caminho)
            backups = list_backups(caminho)
            
            # Converte timestamp para formato legível
            for i, (num, path, size, mtime) in enumerate(backups):
                backups[i] = (
                    num,
                    path,
                    size,
                    datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M:%S")
                )
            
            backup_info[nome] = {
                'caminho': caminho,
                'info': info,
                'backups': backups
            }
    
    response = make_response(render_template('nfs/backups.html', backup_info=backup_info))
    # Headers para evitar cache do navegador
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@admin_bp.route('/backups/restore', methods=['POST'])
@requisitar_autorizacao_especial
def restaurar_backup():
    """
    Restaura um backup específico de um arquivo.
    """
    arquivo = request.form.get('arquivo')
    backup_number = request.form.get('backup_number')
    
    if not arquivo or not backup_number:
        flash('Parâmetros inválidos para restauração', 'error')
        return redirect(url_for('admin.gerenciar_backups'))
    
    try:
        backup_number = int(backup_number)
        
        # Verifica se o backup existe antes de tentar restaurar
        backups_disponiveis = list_backups(arquivo)
        numeros_disponiveis = [b[0] for b in backups_disponiveis]
        
        if backup_number not in numeros_disponiveis:
            flash(f'Backup #{backup_number} não encontrado. Backups disponíveis: {numeros_disponiveis}', 'error')
            return redirect(url_for('admin.gerenciar_backups'))
        
        if restore_backup(arquivo, backup_number):
            flash(f'Backup #{backup_number} restaurado com sucesso para {os.path.basename(arquivo)}', 'success')
            # Força o recarregamento da página com timestamp para evitar cache do navegador
            import time
            timestamp = int(time.time())
            return redirect(url_for('admin.gerenciar_backups', _ts=timestamp))
        else:
            flash(f'Erro ao restaurar backup #{backup_number}', 'error')
            
    except ValueError:
        flash('Número de backup inválido', 'error')
    except Exception as e:
        flash(f'Erro durante restauração: {str(e)}', 'error')
    
    return redirect(url_for('admin.gerenciar_backups'))

@admin_bp.route('/backups/cleanup', methods=['POST'])
@requisitar_autorizacao_especial
def limpar_backups():
    """
    Remove backups antigos mantendo apenas os mais recentes.
    """
    arquivo = request.form.get('arquivo')
    keep_count = request.form.get('keep_count', 10)
    
    if not arquivo:
        flash('Arquivo não especificado', 'error')
        return redirect(url_for('admin.gerenciar_backups'))
    
    try:
        keep_count = int(keep_count)
        removed_count = backup_manager.cleanup_old_backups(arquivo, keep_count)
        
        if removed_count > 0:
            flash(f'{removed_count} backups antigos removidos de {os.path.basename(arquivo)}', 'success')
        else:
            flash('Nenhum backup antigo para remover', 'info')
            
    except ValueError:
        flash('Número de backups a manter inválido', 'error')
    except Exception as e:
        flash(f'Erro durante limpeza: {str(e)}', 'error')
    
    return redirect(url_for('admin.gerenciar_backups'))

@admin_bp.route('/backups/verify', methods=['POST'])
@requisitar_autorizacao_especial
def verificar_integridade_backups():
    """
    Verifica e corrige a integridade dos backups de todos os arquivos.
    """
    # Lista de arquivos principais que podem ter backups
    arquivos_principais = [
        ("Controle de Árvores", os.path.join(DATA_DIR, 'arvores.json')),
    ]
    
    total_duplicates = 0
    total_gaps = 0
    arquivos_verificados = 0
    
    try:
        for nome, caminho in arquivos_principais:
            if os.path.exists(caminho):
                result = backup_manager.verify_backup_integrity(caminho)
                total_duplicates += result['duplicates_removed']
                total_gaps += result['gaps_fixed']
                arquivos_verificados += 1
                
                if result['errors']:
                    for error in result['errors']:
                        flash(f'Erro em {nome}: {error}', 'error')
        
        # Mensagem de sucesso
        msg_parts = []
        if total_duplicates > 0:
            msg_parts.append(f'{total_duplicates} duplicatas removidas')
        if total_gaps > 0:
            msg_parts.append(f'{total_gaps} lacunas corrigidas')
        
        if msg_parts:
            flash(f'Verificação concluída: {", ".join(msg_parts)} em {arquivos_verificados} arquivo(s)', 'success')
        else:
            flash(f'Integridade verificada: {arquivos_verificados} arquivo(s) sem problemas', 'success')
            
    except Exception as e:
        flash(f'Erro durante verificação: {str(e)}', 'error')
    
    return redirect(url_for('admin.gerenciar_backups'))

@admin_bp.route('/backups/create', methods=['POST'])
@requisitar_autorizacao_especial
def criar_backup_manual():
    """
    Cria um backup manual de um arquivo específico.
    """
    arquivo = request.form.get('arquivo')
    
    if not arquivo:
        flash('Arquivo não especificado', 'error')
        return redirect(url_for('admin.gerenciar_backups'))
    
    if not os.path.exists(arquivo):
        flash(f'Arquivo não encontrado: {os.path.basename(arquivo)}', 'error')
        return redirect(url_for('admin.gerenciar_backups'))
    
    try:
        backup_path = create_backup(arquivo)
        if backup_path:
            flash(f'Backup criado com sucesso para {os.path.basename(arquivo)}', 'success')
        else:
            flash(f'Erro ao criar backup de {os.path.basename(arquivo)}', 'error')
            
    except Exception as e:
        flash(f'Erro durante criação de backup: {str(e)}', 'error')
    
    return redirect(url_for('admin.gerenciar_backups'))
