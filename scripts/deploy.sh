#!/bin/bash

# Versão: 2.0.0 (12-factor app)

# Atenção:
# Este Script deve ser executado na raiz do projeto
# Ou pela makefile através do "make deploy"


# Parâmetros de Deploy
# ----------------------------

source ./scripts/config.sh


# Validação .env.deploy
# -------------------------------------

validar_env_deploy() {
    echo "[Deploy] Validando configuração .env.deploy..."
    
    if [ ! -f "$PROJECT_ROOT/.env.deploy" ]; then
        echo "[Deploy] ERRO: Arquivo .env.deploy não encontrado!"
        echo "[Deploy] Execute: cp .env.deploy.template .env.deploy"
        return 1
    fi
    
    # Valida com Python validator
    if ! python3 "$PROJECT_ROOT/tools/validate-env.py" 2>/dev/null; then
        echo "[Deploy] ERRO: Validação falhou. Corrija .env.deploy e tente novamente."
        return 1
    fi
    
    echo "[Deploy] ✅ Configuração validada com sucesso."
}


# Atualizar projeto do git
# ----------------------------

atualizar_projeto_local() {
    echo "[Deploy] Iniciando verificação de atualizações do projeto..."
    git pull
    echo "[Deploy] Atualização do repositório local concluída."
}


# Deploy Frontend
# ----------------------------

deploy_frontend() {
    echo "[Deploy] Iniciando instalação do Frontend..."
    
    if [ ! -e $ROOT_FRONTEND ]; then
        echo "[Deploy] Diretório do Frontend não encontrado. Criando..."
        sudo mkdir -p $ROOT_FRONTEND
        echo "[Deploy] Diretório do Frontend criado: $ROOT_FRONTEND"
    fi

    echo "[Deploy] Copiando arquivos HTML e estáticos para o diretório do Frontend..."
    atualizar_caso_diferente "app/templates/index.html" $ROOT_FRONTEND"/index.html"
    if ! sudo cp -r "app/static" $ROOT_FRONTEND 2>/dev/null; then
        echo "[Deploy] Erro ao copiar arquivos estáticos para $ROOT_FRONTEND"
        return 1
    fi
    echo "[Deploy] Arquivos do Frontend instalados."

    if [ -e $HTACCESS_FILE ]; then
        echo "[Deploy] Encontrado arquivo .htaccess. Instalando no Frontend..."
        atualizar_caso_diferente $HTACCESS_FILE $ROOT_FRONTEND"/.htaccess"
        echo "[Deploy] Arquivo .htaccess copiado."
    else
        echo "[Deploy] Arquivo .htaccess não encontrado. Pulando esta etapa."
    fi
}


# Deploy Backend
# ---------------------

deploy_backend() {
    echo "[Deploy] Iniciando instalação do Backend..."
    
    if [ -e $ROOT_BACKEND ]; then
        echo "[Deploy] Projeto antigo do Backend encontrado. Atualizando arquivos por meio do GIT..."
        dir_atual=$(pwd)
        cd $ROOT_BACKEND
        git restore .
        git pull
        cd $dir_atual
        echo "[Deploy] Atualização do Backend concluída."
    else
        echo "[Deploy] Diretório do Backend não encontrado. Criando novo repositório..."
        if ! sudo mkdir -p $ROOT_SOFTWARES 2>/dev/null; then
            echo "[Deploy] Erro ao criar diretório $ROOT_SOFTWARES"
            return 1
        fi
        git clone $GIT_REPO_LINK
        if ! sudo mv $GIT_REPO_NAME $ROOT_BACKEND 2>/dev/null; then
            echo "[Deploy] Erro ao mover repositório para $ROOT_BACKEND"
            return 1
        fi
        echo "[Deploy] Repositório do Backend clonado para: $ROOT_BACKEND"
    fi

    echo "[Deploy] Ajustando permissões do diretório do Backend..."
    if ! sudo chown -R $(whoami) $ROOT_BACKEND 2>/dev/null; then
        echo "[Deploy] Erro ao ajustar permissões do Backend"
        return 1
    fi
    echo "[Deploy] Permissões do Backend ajustadas."

    echo "[Deploy] Criando diretório centralizado de logs..."
    sudo mkdir -p /var/softwaresTCE/logs/$PROJECT_NAME
    sudo chown -R $(whoami) /var/softwaresTCE/logs/$PROJECT_NAME
    echo "[Deploy] Diretório de logs criado: /var/softwaresTCE/logs/$PROJECT_NAME"

    echo "[Deploy] Configurando projeto do Backend..."
    dir_atual=$(pwd)
    cd $ROOT_BACKEND
    make setup
    cd $dir_atual
    echo "[Deploy] Configuração do Backend concluída."

    # Ajustar permissões de logs (se existirem arquivos)
    if [ -d "$LOGS_PATH" ]; then
        echo "[Deploy] Ajustando permissões dos arquivos de log..."
        
        # Conta arquivos .log existentes
        log_count=$(find "$LOGS_PATH" -maxdepth 1 -name "*.log" 2>/dev/null | wc -l)
        
        if [ "$log_count" -gt 0 ]; then
            if sudo chown tcego:tcego "$LOGS_PATH"/*.log 2>/dev/null; then
                echo "[Deploy] ✅ Permissões de $log_count arquivo(s) de log alteradas com sucesso."
            else
                echo "[Deploy] ⚠️  Aviso: Não foi possível alterar permissões de logs (normal no primeiro deploy)."
            fi
        else
            echo "[Deploy] ℹ️  Nenhum arquivo de log encontrado ainda (será criado na primeira execução)."
        fi
    else
        echo "[Deploy] ⚠️  Diretório de logs $LOGS_PATH não existe ainda."
    fi

    echo "[Deploy] Verificando permissões de execução para scripts do Backend..."
    [ ! -x "$ROOT_BACKEND/scripts/deploy.sh" ] && sudo chmod +x "$ROOT_BACKEND/scripts/deploy.sh" 2>/dev/null
    [ ! -x "$ROOT_BACKEND/scripts/run.sh" ] && sudo chmod +x "$ROOT_BACKEND/scripts/run.sh" 2>/dev/null

    CURRENT_CONTEXT=$(ls -Z "$ROOT_BACKEND/scripts/run.sh" | awk -F: '{print $3}')
    if [[ "$CURRENT_CONTEXT" != "bin_t" ]]; then
        echo "[Deploy] Ajustando contexto SELinux para o script run.sh..."
        sudo chcon -t bin_t "$ROOT_BACKEND/scripts/run.sh"
        echo "[Deploy] Contexto SELinux ajustado."
    else
        echo "[Deploy] Contexto SELinux já configurado corretamente."
    fi

    echo "[Deploy] Instalação do Backend concluída."
}


# Deploy Servico
# ------------------------------------

deploy_servico() {
    echo "[Deploy] Iniciando instalação do serviço..."

    if [ -e "/usr/lib/systemd/system/$SERVICE_NAME" ]; then
        echo "[Deploy] Serviço existente encontrado. Removendo configuração antiga..."
        if ! sudo rm "/usr/lib/systemd/system/$SERVICE_NAME" 2>/dev/null; then
            echo "[Deploy] Erro ao remover serviço antigo"
            return 1
        fi
    fi

    echo "[Deploy] Copiando novo arquivo de serviço..."
    if ! sudo cp scripts/$SERVICE_NAME /usr/lib/systemd/system/$SERVICE_NAME 2>/dev/null; then
        echo "[Deploy] Erro ao copiar arquivo de serviço"
        return 1
    fi

    if ! systemctl is-enabled "$SERVICE_NAME" && [ $AUTO_HABILITAR_SERVICO ]; then
        echo "[Deploy] Serviço desabilitado. Habilitando..."
        sudo systemctl enable "$SERVICE_NAME"
        echo "[Deploy] Serviço habilitado."
    else
        echo "[Deploy] Serviço já habilitado."
    fi

    echo "[Deploy] Reiniciando o serviço..."
    make service-reload
    make service-restart
    echo "[Deploy] Serviço reiniciado com sucesso."
}


# Específicos deste app
# -------------------------------------

exportar_key_openai() {
    echo "[Deploy] Exportando chave da OPENAI..."
    export OPENAI_API_KEY=$(cat /var/softwaresTCE/openai_api_key/.openai_api_key)
    echo "[Deploy] Chave exportada: $OPENAI_API_KEY"

    sudo -u $(whoami) -s << EOF
echo "[Deploy] Exportando chave da OPENAI com sudo..."
export OPENAI_API_KEY=$(cat /var/softwaresTCE/openai_api_key/.openai_api_key)
echo "[Deploy] Chave exportada com sucesso."
EOF
}


# Main
# -------------------------------------

main() {
    echo "[Deploy] Iniciando processo de Deploy JardimGIS v2.0.0..."
    
    # NOVO: Validação obrigatória .env.deploy
    validar_env_deploy || exit 1
    
    atualizar_projeto_local
    # deploy_frontend  # Não usado - JardimGIS é SPA servido pelo Flask
    deploy_backend
    deploy_servico
    exportar_key_openai
    echo "[Deploy] Processo de Deploy concluído com sucesso!"
    echo "[Deploy] "
    echo "[Deploy] ✅ JardimGIS v2.0.0 implantado com sucesso!"
    echo "[Deploy] 🌐 Acesse: http://automacao.tce.go.gov.br/jardimgis"
    echo "[Deploy] 📝 Logs: sudo journalctl -u jardim_gis -f"
    echo "[Deploy] 🔧 Status: sudo systemctl status jardim_gis"
    echo "[Deploy] ℹ️  Configuração Apache gerenciada pelo scada-web"
}

main
