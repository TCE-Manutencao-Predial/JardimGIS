# GerenciadorJSON.py - Gerenciador de arquivos JSON para JardimGIS
import json
import os
import logging
from filelock import FileLock
from ..managers.GerenciadorBackupJSON import create_backup

jardimgis_logger = logging.getLogger('jardimgis')


def load_json_file(file_path: str, default_value=None):
    """
    Carrega um arquivo JSON de forma segura.
    
    Args:
        file_path: Caminho do arquivo JSON
        default_value: Valor padrão caso o arquivo não exista ou esteja vazio
        
    Returns:
        Conteúdo do JSON ou default_value
    """
    if default_value is None:
        default_value = []
        
    try:
        if not os.path.exists(file_path):
            jardimgis_logger.warning(f"Arquivo não encontrado: {file_path}")
            return default_value
            
        lock_path = file_path + ".lock"
        with FileLock(lock_path, timeout=10):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    jardimgis_logger.warning(f"Arquivo vazio: {file_path}")
                    return default_value
                return json.loads(content)
                
    except json.JSONDecodeError as e:
        jardimgis_logger.error(f"Erro ao decodificar JSON {file_path}: {e}")
        return default_value
    except Exception as e:
        jardimgis_logger.error(f"Erro ao carregar {file_path}: {e}")
        return default_value


def save_json_file(file_path: str, data, create_backup_first=True):
    """
    Salva dados em um arquivo JSON de forma segura.
    
    Args:
        file_path: Caminho do arquivo JSON
        data: Dados a serem salvos
        create_backup_first: Se True, cria backup antes de salvar
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        # Cria backup antes de salvar (se solicitado)
        if create_backup_first and os.path.exists(file_path):
            create_backup(file_path)
        
        # Garante que o diretório existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        lock_path = file_path + ".lock"
        with FileLock(lock_path, timeout=10):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        
        jardimgis_logger.info(f"Arquivo salvo: {file_path}")
        return True
        
    except Exception as e:
        jardimgis_logger.error(f"Erro ao salvar {file_path}: {e}")
        return False


def transform_dates_in_json(data):
    """
    Transforma datas no formato YYYY-MM-DD para DD/MM/YYYY recursivamente.
    
    Args:
        data: Dados JSON (dict, list ou valor)
        
    Returns:
        Dados com datas transformadas
    """
    if isinstance(data, dict):
        return {key: transform_dates_in_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [transform_dates_in_json(item) for item in data]
    elif isinstance(data, str):
        # Detecta formato YYYY-MM-DD
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(date_pattern, data):
            try:
                parts = data.split('-')
                return f"{parts[2]}/{parts[1]}/{parts[0]}"  # DD/MM/YYYY
            except:
                return data
    return data


def remove_empty_entries(data):
    """
    Remove entradas vazias de listas recursivamente.
    
    Args:
        data: Dados JSON (dict, list ou valor)
        
    Returns:
        Dados sem entradas vazias
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            cleaned = remove_empty_entries(value)
            # Mantém a chave mesmo se o valor for lista vazia
            result[key] = cleaned
        return result
    elif isinstance(data, list):
        # Remove apenas entradas que são dicionários completamente vazios
        return [
            remove_empty_entries(item) 
            for item in data 
            if not (isinstance(item, dict) and all(v == "" or v is None for v in item.values()))
        ]
    return data
