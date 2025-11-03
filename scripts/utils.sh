
# Funções utilitárias
# ------------------------


atualizar_caso_diferente() {
    # Compara se dois arquivos são diferentes. Caso sim, então copia
    # o primeiro arquivo para o segundo, atualizando-o.
    #
    # Param:
    #     1. Arquivo Fonte
    #     2. Arquivo Destino
    #
    # Obs.:
    #     Utilizar apenas para arquivos. Não funciona com diretórios.

    ARQUIVO_FONTE="$1"
    ARQUIVO_DESTINO="$2"

    if [ -d "$ARQUIVO_FONTE" ] || [ -d "$ARQUIVO_DESTINO" ]; then
        echo "[Deploy.atualizar_caso_diferente] Entrada inválida $ARQUIVO_FONTE $ARQUIVO_DESTINO"
        return
    fi

    if diff "$ARQUIVO_FONTE" "$ARQUIVO_DESTINO" > /dev/null 2>&1; then
        echo "[Deploy] Arquivos atualizados"
    else
        echo "[Deploy] Arquivos diferentes. Atualizando..."
        if ! cp "$ARQUIVO_FONTE" "$ARQUIVO_DESTINO" 2>/dev/null; then
            echo "[Deploy] Erro ao copiar $ARQUIVO_FONTE para $ARQUIVO_DESTINO"
            return 1
        fi
    fi
}
