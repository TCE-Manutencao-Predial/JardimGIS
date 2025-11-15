# config.py - Sistema JardimGIS - Controle Geográfico de Árvores
"""
DEPRECATED: Este módulo está obsoleto desde v2.0.0.

Use `app.settings` para todas as configurações.
Este arquivo é mantido apenas para compatibilidade com imports legados
e será removido em versão futura.

Migração:
- ANTES: from .config import DATA_DIR, LOGS_DIR
- DEPOIS: from . import settings (usar settings.DATA_DIR, settings.LOGS_DIR)

Backup do código original: docs/legacy/app_config.py.backup
"""

import os
import sys
import logging
import warnings

warnings.warn(
    "app.config está deprecated desde v2.0.0. Use app.settings.",
    DeprecationWarning,
    stacklevel=2
)

# Re-exporta de settings para compatibilidade
from . import settings

# Exports para compatibilidade com código legado
DATA_DIR = settings.DATA_DIR
LOGS_DIR = settings.LOGS_DIR
LOG_DIR = settings.LOGS_DIR  # Alias
LOG_FILE = settings.LOG_FILE
ARVORES_JSON_PATH = settings.ARVORES_JSON_PATH
BACKUP_DIR = settings.BACKUP_DIR
ROUTES_PREFIX = settings.ROUTES_PREFIX
ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS

# SQLite config (mantido do original)
SQLITE_CONFIG = {
    'timeout': 30.0,
    'check_same_thread': False,
}

# History config (mantido do original)
HISTORY_CONFIG = {
    'default_limit': 25,
    'max_records': 1000,
}

# Mantém função setup_logging para compatibilidade

def setup_logging():
    """Configura o sistema de logging da aplicação."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('jardimgis')
    logger.info("Sistema de logging inicializado")
    
    return logger