# __init__.py - Sistema JardimGIS - Controle Geográfico de Árvores
from flask import Flask, redirect, render_template
import atexit
import logging

from .config import setup_logging

# Configurar logging
setup_logging()

# Importar blueprints
from .routes.web.admin import admin_bp
from .routes.web.web import web_bp
from .routes.features.arvores.rotas_arvores import arvores_bp

ROUTES_PREFIX = '/jardimgis'

def create_app():
    app = Flask(__name__, static_url_path=ROUTES_PREFIX)
    # TODO: Em produção, use uma SECRET_KEY segura de variável de ambiente
    app.config['SECRET_KEY'] = '123'  # Alterar em produção!
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
    
    # Inicializa o agendador de backups automáticos
    try:
        from .utils.schedulers.agendador_backups_automatico import iniciar_agendador_backups
        agendador_backups = iniciar_agendador_backups()
        app.config['AGENDADOR_BACKUPS'] = agendador_backups
        print("✅ Agendador de backups automáticos iniciado (execução diária às 20h)")
    except Exception as e:
        print(f"❌ Erro ao iniciar agendador de backups: {e}")
        app.config['AGENDADOR_BACKUPS'] = None

    @atexit.register
    def shutdown_scheduler():
        try:
            # Parar agendador de backups
            if app.config.get('AGENDADOR_BACKUPS'):
                from .utils.schedulers.agendador_backups_automatico import parar_agendador_backups
                parar_agendador_backups()
                print("Agendador de backups finalizado")
        except Exception as e:
            print(f"Erro ao finalizar scheduler: {e}")

    # Middleware para validação de arquivos
    @app.before_request
    def validate_file_upload():
        """Valida uploads de arquivos."""
        from flask import request, flash, redirect, url_for
        
        ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'txt', 'zip', 'rar'}
        
        if request.method == 'POST' and request.files:
            for file_key, file in request.files.items():
                if file and file.filename:
                    # Verifica extensão
                    if '.' in file.filename:
                        ext = file.filename.rsplit('.', 1)[1].lower()
                        if ext not in ALLOWED_EXTENSIONS:
                            flash(f"Tipo de arquivo não permitido: .{ext}", "error")
                            return redirect(request.referrer or url_for('web.index'))

    # Handlers de erro
    @app.errorhandler(404)
    def not_found_error(error):
        try:
            return render_template('base/erro_pagina_nao_encontrada.html')
        except:
            return "Página não encontrada", 404
    
    @app.errorhandler(401)
    def unauthorized(e):
        try:
            return render_template('base/erro_acesso_negado.html'), 401
        except:
            return "Acesso negado", 401

    @app.errorhandler(403)
    def forbidden(e):
        try:
            return render_template('base/erro_acesso_negado.html'), 403
        except:
            return "Acesso proibido", 403

    @app.errorhandler(500)
    def internal_error(error):
        print(f"Erro interno: {error}")
        try:
            return render_template('base/erro_interno.html'), 500
        except:
            return "Erro interno do servidor", 500
    
    @app.errorhandler(413)
    def too_large(error):
        from flask import flash, redirect, url_for
        flash("Arquivo muito grande! Tamanho máximo: 100MB", "error")
        return redirect(url_for('web.index'))

    # Rotas
    app.static_url_path = ROUTES_PREFIX if ROUTES_PREFIX else '/static'
    
    print("Registrando blueprints...")
    
    try:
        app.register_blueprint(admin_bp, url_prefix=f'{ROUTES_PREFIX}/admin' if ROUTES_PREFIX else '/admin')
        print("✅ Blueprint admin_bp registrado")
    except Exception as e:
        print(f"❌ Erro ao registrar admin_bp: {e}")
    
    try:
        app.register_blueprint(web_bp, url_prefix=ROUTES_PREFIX if ROUTES_PREFIX else '/')
        print("✅ Blueprint web_bp registrado")
    except Exception as e:
        print(f"❌ Erro ao registrar web_bp: {e}")
    
    # Registra blueprint de árvores
    try:
        app.register_blueprint(arvores_bp)
        print("✅ Blueprint arvores_bp registrado")
    except Exception as e:
        print(f"❌ Erro ao registrar arvores_bp: {e}")

    # Rota raiz redireciona para /jardimgis
    @app.route('/')
    def root_redirect():
        """Redireciona raiz para /jardimgis"""
        return redirect(ROUTES_PREFIX if ROUTES_PREFIX else '/jardimgis', code=302)

    return app
