"""
Configurações centralizadas do JardimGIS.
Carrega variáveis de ambiente do .env.deploy (produção) ou .env (desenvolvimento).

Este módulo é a FONTE ÚNICA DE VERDADE para todas as configurações.
Substitui a lógica hardcoded e platform-dependent do app/config.py (deprecated).

Variáveis obrigatórias (.env.deploy):
- SECRET_KEY: Chave secreta Flask (mínimo 32 caracteres)
- FLASK_CONFIG: Modo (development/production)
- PORT: Porta Waitress
- DATA_DIR: Diretório de dados
- LOGS_DIR: Diretório de logs
- BACKUP_ENABLED: Habilita scheduler backups
- BACKUP_TIME: Horário backup diário (HH:MM)
- MAX_UPLOAD_SIZE_MB: Tamanho máximo upload (MB)
- IS_REVERSE_PROXY: Ativa ProxyFix (Apache)
- STATIC_VERSION: Versão assets (cache busting)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# DETECÇÃO DE AMBIENTE
# ============================================================

# Detecta se está rodando via systemd (produção) ou desenvolvimento
IS_SYSTEMD = os.getenv('INVOCATION_ID') is not None

# Define qual .env carregar
if IS_SYSTEMD:
    # Produção: Carrega .env.deploy da pasta de instalação
    env_file = Path('/var/softwaresTCE/jardim_gis/.env.deploy')
else:
    # Desenvolvimento: Usa .env se existir, senão fallback para .env.deploy
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / '.env'
    if not env_file.exists():
        env_file = base_dir / '.env.deploy'

# Carrega .env
if env_file.exists():
    load_dotenv(env_file)
    print(f"[Settings] Variáveis carregadas de: {env_file}")
else:
    print(f"[Settings] ERRO: Arquivo {env_file} não encontrado!", file=sys.stderr)
    print(f"[Settings] Copie .env.deploy.template para .env.deploy e configure", file=sys.stderr)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def get_required_env(var_name: str, default=None) -> str:
    """
    Obtém variável de ambiente obrigatória.
    Levanta ValueError se não configurada (exceto se default fornecido).
    """
    value = os.getenv(var_name)
    if not value:
        if default is not None:
            return default
        raise ValueError(
            f"[Settings] Variável obrigatória não configurada: {var_name}\n"
            f"[Settings] Configure em {env_file}"
        )
    return value


def get_bool_env(var_name: str, default: bool = False) -> bool:
    """Converte variável de ambiente para booleano."""
    value = os.getenv(var_name, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')


def get_int_env(var_name: str, default: int) -> int:
    """Converte variável de ambiente para inteiro."""
    value = os.getenv(var_name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"[Settings] AVISO: {var_name}='{value}' não é inteiro. Usando default={default}", file=sys.stderr)
        return default


# ============================================================
# CONFIGURAÇÕES CORE
# ============================================================

# Segurança (CRÍTICO)
SECRET_KEY = get_required_env('SECRET_KEY')

# Validação SECRET_KEY
if SECRET_KEY == 'GERAR_ANTES_DEPLOY_64_CHARS_HEX':
    raise ValueError(
        "[Settings] SECRET_KEY não foi gerado!\n"
        "[Settings] Execute: python3 -c \"import secrets; print(secrets.token_hex(32))\"\n"
        "[Settings] E substitua em .env.deploy"
    )
if len(SECRET_KEY) < 32:
    print(f"[Settings] AVISO: SECRET_KEY muito curta ({len(SECRET_KEY)} chars). Recomendado: >=32", file=sys.stderr)

# Flask
FLASK_CONFIG = get_required_env('FLASK_CONFIG', 'production')
PORT = get_int_env('PORT', 4141)

# Diretórios
DATA_DIR = get_required_env('DATA_DIR')
LOGS_DIR = get_required_env('LOGS_DIR')

# Backups automáticos
BACKUP_ENABLED = get_bool_env('BACKUP_ENABLED', True)
BACKUP_TIME = get_required_env('BACKUP_TIME', '20:00')

# Upload
MAX_UPLOAD_SIZE_MB = get_int_env('MAX_UPLOAD_SIZE_MB', 100)

# Reverse Proxy (Apache)
IS_REVERSE_PROXY = get_bool_env('IS_REVERSE_PROXY', True)

# Cache Busting
STATIC_VERSION = get_required_env('STATIC_VERSION', '2.0.0')


# ============================================================
# PATHS DERIVADOS (Compatibilidade com config.py)
# ============================================================

# Arquivos de dados
ARVORES_JSON_PATH = os.path.join(DATA_DIR, 'arvores.json')
BACKUP_DIR = os.path.join(DATA_DIR, 'bak')

# Logs
LOG_FILE = os.path.join(LOGS_DIR, 'jardimgis.log')

# Routes
ROUTES_PREFIX = '/jardimgis'


# ============================================================
# CONFIGURAÇÕES FLASK
# ============================================================

# Debug mode
DEBUG = FLASK_CONFIG == 'development'

# Allowed file extensions (compatibilidade)
ALLOWED_EXTENSIONS = {
    # Documentos
    'pdf', 'doc', 'docx', 'xls', 'xlsx',
    # Imagens
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',
    # Arquivos compactados
    'zip', 'rar', '7z', 'tar', 'gz'
}


# ============================================================
# INICIALIZAÇÃO DE DIRETÓRIOS
# ============================================================

# Cria diretórios se não existirem
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"[Settings] Diretórios verificados/criados:")
    print(f"[Settings]   DATA_DIR: {DATA_DIR}")
    print(f"[Settings]   LOGS_DIR: {LOGS_DIR}")
    print(f"[Settings]   BACKUP_DIR: {BACKUP_DIR}")
except PermissionError as e:
    print(f"[Settings] ERRO: Sem permissão para criar diretórios: {e}", file=sys.stderr)
except Exception as e:
    print(f"[Settings] ERRO ao criar diretórios: {e}", file=sys.stderr)


# ============================================================
# LOG DE CONFIGURAÇÃO (DEBUG)
# ============================================================

if DEBUG:
    print("\n" + "="*60)
    print("CONFIGURAÇÃO JARDIMGIS v2.0.0")
    print("="*60)
    print(f"Modo:                {FLASK_CONFIG}")
    print(f"Porta:               {PORT}")
    print(f"Debug:               {DEBUG}")
    print(f"Reverse Proxy:       {IS_REVERSE_PROXY}")
    print(f"Backups Automáticos: {BACKUP_ENABLED}")
    if BACKUP_ENABLED:
        print(f"Horário Backup:      {BACKUP_TIME}")
    print(f"Max Upload:          {MAX_UPLOAD_SIZE_MB} MB")
    print(f"Static Version:      {STATIC_VERSION}")
    print(f"DATA_DIR:            {DATA_DIR}")
    print(f"LOGS_DIR:            {LOGS_DIR}")
    print(f"Secret Key:          {'*' * len(SECRET_KEY)} ({len(SECRET_KEY)} chars)")
    print("="*60 + "\n")


# ============================================================
# EXPORTS (Para compatibilidade com imports existentes)
# ============================================================

__all__ = [
    # Core
    'SECRET_KEY',
    'FLASK_CONFIG',
    'PORT',
    'DEBUG',
    
    # Diretórios
    'DATA_DIR',
    'LOGS_DIR',
    'BACKUP_DIR',
    
    # Paths
    'ARVORES_JSON_PATH',
    'LOG_FILE',
    'ROUTES_PREFIX',
    
    # Features
    'BACKUP_ENABLED',
    'BACKUP_TIME',
    'MAX_UPLOAD_SIZE_MB',
    'IS_REVERSE_PROXY',
    'STATIC_VERSION',
    
    # Constantes
    'ALLOWED_EXTENSIONS',
]
