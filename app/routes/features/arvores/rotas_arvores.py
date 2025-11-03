# rotas_arvores.py - Rotas para controle de árvores
import logging
from flask import Blueprint

arvores_bp = Blueprint('arvores', __name__)
jardimgis_logger = logging.getLogger('jardimgis')

# Blueprint criado para futuras expansões do módulo de árvores
# Atualmente, as rotas principais estão no web_bp para evitar conflitos
