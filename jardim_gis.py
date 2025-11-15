#!/usr/bin/env python3
"""
JardimGIS - Sistema de Controle Geográfico de Árvores - TCE-GO
Entry point com suporte a dev/prod modes (v2.0.0)

Este script:
1. Carrega .env.deploy (produção) ou .env (desenvolvimento)
2. Cria app Flask com configurações centralizadas
3. Inicia Waitress (produção) ou Flask dev server (desenvolvimento)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def load_environment():
    """
    Carrega variáveis de ambiente do .env ou .env.deploy.
    
    Lógica:
    - Desenvolvimento: Procura .env na raiz do projeto, fallback para .env.deploy
    - Produção (systemd): Sempre usa .env.deploy
    
    Returns:
        bool: True se arquivo carregado com sucesso, False caso contrário
    """
    base_dir = Path(__file__).resolve().parent
    
    # Desenvolvimento: Usa .env se existir, senão .env.deploy
    env_file = base_dir / '.env'
    if not env_file.exists():
        env_file = base_dir / '.env.deploy'
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[JardimGIS] ✅ Variáveis carregadas de: {env_file}")
        return True
    else:
        print(f"[JardimGIS] ❌ ERRO: Nenhum .env ou .env.deploy encontrado!", file=sys.stderr)
        print(f"[JardimGIS] Copie .env.deploy.template para .env.deploy e configure", file=sys.stderr)
        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    # 1. Carrega ambiente ANTES de importar app (settings depende de .env)
    if not load_environment():
        print("[JardimGIS] Deploy abortado: configuração não encontrada", file=sys.stderr)
        sys.exit(1)
    
    # 2. Importa app (após carregar .env)
    try:
        from app import create_app
        from app import settings
    except Exception as e:
        print(f"[JardimGIS] ❌ ERRO ao importar app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 3. Cria app Flask
    try:
        app = create_app()
    except Exception as e:
        print(f"[JardimGIS] ❌ ERRO ao criar app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 4. Modo desenvolvimento vs produção
    print("\n" + "="*60)
    print("JARDIMGIS - SISTEMA DE CONTROLE GEOGRÁFICO DE ÁRVORES")
    print("="*60)
    print(f"Versão:       2.0.0")
    print(f"Modo:         {settings.FLASK_CONFIG}")
    print(f"Porta:        {settings.PORT}")
    print(f"Debug:        {settings.DEBUG}")
    print(f"Data Dir:     {settings.DATA_DIR}")
    print(f"Logs Dir:     {settings.LOGS_DIR}")
    print("="*60 + "\n")
    
    if settings.FLASK_CONFIG == 'development':
        # Desenvolvimento: Flask debug server
        print(f"[JardimGIS] 🔧 Iniciando em MODO DESENVOLVIMENTO")
        print(f"[JardimGIS] 🌐 Acesse: http://127.0.0.1:{settings.PORT}{settings.ROUTES_PREFIX}")
        print(f"[JardimGIS] 🔄 Auto-reload: ATIVADO")
        print(f"[JardimGIS] 🐛 Debug mode: ATIVADO\n")
        
        try:
            app.run(
                host='127.0.0.1',
                port=settings.PORT,
                debug=True,
                use_reloader=True
            )
        except KeyboardInterrupt:
            print("\n[JardimGIS] Servidor interrompido pelo usuário")
            sys.exit(0)
    
    else:
        # Produção: Waitress WSGI server
        print(f"[JardimGIS] 🚀 Iniciando em MODO PRODUÇÃO")
        
        try:
            from waitress import serve
            from werkzeug.middleware.proxy_fix import ProxyFix
        except ImportError as e:
            print(f"[JardimGIS] ❌ ERRO: {e}", file=sys.stderr)
            print("[JardimGIS] Instale dependências: pip install -r requirements.txt", file=sys.stderr)
            sys.exit(1)
        
        # Configura ProxyFix se reverse proxy ativado
        if settings.IS_REVERSE_PROXY:
            app.wsgi_app = ProxyFix(
                app.wsgi_app,
                x_for=1,
                x_host=1,
                x_proto=1
            )
            print(f"[JardimGIS] 🔒 ProxyFix habilitado (Apache integration)")
        else:
            print(f"[JardimGIS] ⚠️  ProxyFix desabilitado")
        
        print(f"[JardimGIS] 🌐 Waitress rodando em 127.0.0.1:{settings.PORT}")
        print(f"[JardimGIS] 📁 Dados: {settings.DATA_DIR}")
        print(f"[JardimGIS] 📝 Logs: {settings.LOGS_DIR}")
        
        if settings.BACKUP_ENABLED:
            print(f"[JardimGIS] 💾 Backups automáticos: ATIVADO ({settings.BACKUP_TIME})")
        else:
            print(f"[JardimGIS] 💾 Backups automáticos: DESATIVADO")
        
        print(f"\n[JardimGIS] ✅ Servidor iniciado com sucesso!")
        print(f"[JardimGIS] Pressione CTRL+C para parar\n")
        
        try:
            serve(
                app,
                host='127.0.0.1',
                port=settings.PORT,
                threads=4,
                url_scheme='http'
            )
        except KeyboardInterrupt:
            print("\n[JardimGIS] Servidor finalizado pelo usuário")
            sys.exit(0)
        except Exception as e:
            print(f"\n[JardimGIS] ❌ ERRO no servidor: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

