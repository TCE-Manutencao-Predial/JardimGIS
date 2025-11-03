# utils/GerenciadorAutorizacoes.py
from functools import wraps
from flask import request, render_template
import logging
import socket

logger = logging.getLogger('jardimgis')

# Lista de usuários autorizados para rotas administrativas
USUARIOS_AUTORIZADOS = {'pedro', 'lucas', 'kleandro', 'gcosta', 'farruda', 'jbsouza', 'spimentel'}

# Hostnames autorizados para debugging (bypass de autenticação)
HOSTNAMES_DEBUG = {'TCE-WORK19', 'LAPTOPI7DELL'}

def verificar_usuario_autorizado(usuario_autenticado=None):
    """
    Verifica se um usuário é autorizado para funcionalidades administrativas.
    Retorna True se autorizado, False caso contrário.
    """
    # Obtém o hostname da máquina atual
    hostname_atual = socket.gethostname().upper()
    
    # Se estiver executando em hostname de debugging, autoriza qualquer usuário
    if hostname_atual in HOSTNAMES_DEBUG:
        return True
    
    # Obtém o usuário do parâmetro ou do header
    if not usuario_autenticado:
        usuario_autenticado = request.headers.get("X-Remote-User")
    
    # Se não há usuário autenticado, usa "admin" como fallback (para desenvolvimento)
    if not usuario_autenticado:
        usuario_autenticado = "admin"
    
    # Converte para minúsculo para comparação case-insensitive
    usuario_lower = usuario_autenticado.lower()
    
    # Verifica se o usuário está na lista de autorizados
    return usuario_lower in USUARIOS_AUTORIZADOS

def requisitar_autorizacao_especial(f):
    """
    Decorador que verifica se o usuário autenticado tem permissão para acessar rotas administrativas.
    
    Verifica o header X-Remote-User (usuário autenticado pelo htpasswd) e compara
    com a lista de usuários autorizados. Se não autorizado, redireciona para página de acesso negado.
    
    Para debugging: autoriza qualquer usuário em hostnames específicos (TCE-WORK19, LAPTOPI7DELL).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtém o hostname da máquina atual
        hostname_atual = socket.gethostname().upper()
        
        # Se estiver executando em hostname de debugging, autoriza qualquer usuário
        if hostname_atual in HOSTNAMES_DEBUG:
            usuario_autenticado = request.headers.get("X-Remote-User", "debug-user")
            logger.info(f"Modo DEBUG ativo - Hostname '{hostname_atual}' detectado. Acesso autorizado para usuário '{usuario_autenticado}' na rota '{request.endpoint}'")
            return f(*args, **kwargs)
        
        # Obtém o usuário autenticado do header
        usuario_autenticado = request.headers.get("X-Remote-User")
        
        # Se não há usuário autenticado, usa "admin" como fallback (para desenvolvimento)
        if not usuario_autenticado:
            usuario_autenticado = "admin"
        
        # Converte para minúsculo para comparação case-insensitive
        usuario_lower = usuario_autenticado.lower()
        
        # Verifica se o usuário está na lista de autorizados
        if usuario_lower not in USUARIOS_AUTORIZADOS:
            logger.warning(f"Acesso negado para usuário '{usuario_autenticado}' na rota '{request.endpoint}' - Hostname: '{hostname_atual}'")
            return render_template('base/erro_acesso_negado.html', 
                                 usuario_atual=usuario_autenticado,
                                 pagina_solicitada=request.endpoint), 200
        
        # Log de acesso autorizado
        logger.info(f"Acesso autorizado para usuário '{usuario_autenticado}' na rota '{request.endpoint}' - Hostname: '{hostname_atual}'")
        
        # Se autorizado, executa a função original
        return f(*args, **kwargs)
    
    return decorated_function
