#!/bin/bash

# Config do JardimGIS v2.0.0
# Carrega variáveis do .env.deploy (12-factor app)

# ============================================================
# FUNÇÃO PARA CARREGAR .env.deploy
# ============================================================

load_env_file() {
    local env_file="$1"
    
    if [ ! -f "$env_file" ]; then
        echo "[Config] ERRO: Arquivo $env_file não encontrado!"
        return 1
    fi
    
    echo "[Config] Carregando variáveis de: $env_file"
    
    # Usa sed para remover comentários e linhas vazias
    # FIX: Aspas duplas permitem expansão de variáveis
    while IFS='=' read -r key value; do
        # Remove espaços e aspas do value
        value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")
        export "$key=$value"
        echo "[Config]   $key = $value"
    done < <(sed -e '/^#/d' -e '/^$/d' -e 's/#.*//' "$env_file")
    
    echo "[Config] Variáveis carregadas com sucesso."
}

# ============================================================
# DETECTA DIRETÓRIOS E CARREGA .env.deploy
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env.deploy"

# Carrega .env.deploy (interrompe se falhar)
load_env_file "$ENV_FILE" || exit 1

# ============================================================
# PARÂMETROS DE DEPLOY
# ============================================================

PROJECT_NAME="jardim_gis"
SERVICE_NAME="jardim_gis.service"

ROOT_FRONTEND=/var/www/automacao.tce.go.gov.br/$PROJECT_NAME

ROOT_SOFTWARES=/var/softwaresTCE
ROOT_BACKEND=$ROOT_SOFTWARES"/"$PROJECT_NAME

GIT_REPO_NAME="JardimGIS"
GIT_REPO_OWNER="TCE-Manutencao-Predial"
GIT_REPO_LINK="https://github.com/$GIT_REPO_OWNER/$GIT_REPO_NAME.git"

HTACCESS_FILE="scripts/htaccess"

# Configurações
AUTO_HABILITAR_SERVICO=true

# LOGS_PATH agora vem do .env.deploy (variável LOGS_DIR)
LOGS_PATH="$LOGS_DIR"
