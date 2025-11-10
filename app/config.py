# config.py - Sistema JardimGIS - Controle Geográfico de Árvores
import os
import sys
import platform
import logging

# Configuração do diretório base e de dados
if platform.system() == "Linux":
    DATA_DIR = '/var/softwaresTCE/dados/jardimgis'
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'dados')

# Garante que o diretório de dados existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

# Definição dos caminhos dos arquivos
ARVORES_JSON_PATH = os.path.join(DATA_DIR, 'arvores.json')


# Diretório para backups centralizados
BACKUP_DIR = os.path.join(DATA_DIR, 'bak')
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR, exist_ok=True)

ROUTES_PREFIX = ''  # Vazio - Apache adiciona o prefixo

# Configurações do SQLite
SQLITE_CONFIG = {
    'timeout': 30.0,
    'check_same_thread': False,
}

# Configurações de histórico
HISTORY_CONFIG = {
    'default_limit': 25,
    'max_records': 1000,
}



# Configuração dos diretórios de logs
if platform.system() == "Linux":
    LOG_DIR = '/var/softwaresTCE/logs/jardim_gis'
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

LOG_FILE = os.path.join(LOG_DIR, 'app.log')

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