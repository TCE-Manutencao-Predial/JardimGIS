"""
template_filters.py - Filtros para templates Jinja2
"""

def enumerate_filter(iterable):
    """Filtro para enumerar iteráveis nos templates."""
    return enumerate(iterable)

def obter_icone_secao(nome_secao):
    """
    Retorna o ícone FontAwesome apropriado baseado no nome da seção de checklist.
    """
    # Normaliza a string: remove acentos, converte para minúsculas
    nome_normalizado = nome_secao.lower()
    
    # Mapeamento direto para as seções específicas de checklist
    icones_especificos = {
        "alarme incendio": "fas fa-bell",
        "baterias": "fas fa-car-battery",
        "bombas d'agua": "fas fa-tint",
        "bombas d'água": "fas fa-tint",
        "c.a.g.": "fas fa-temperature-low",
        "catracas": "fas fa-door-open",
        "extintores": "fas fa-fire-extinguisher",
        "fancoil": "fas fa-wind",
        "fancoletes": "fas fa-wind",
        "glp": "fas fa-fire",
        "gmgs": "fas fa-plug",
        "hidrantes": "fas fa-water",
        "iluminacao emergencia": "fas fa-lightbulb",
        "iluminação emergência": "fas fa-lightbulb",
        "leitores biometricos": "fas fa-fingerprint",
        "leitores biométricos": "fas fa-fingerprint",
        "purificadores": "fas fa-glass-water",
        "quadros eletricos": "fas fa-bolt",
        "quadros elétricos": "fas fa-bolt",
        "rfid": "fas fa-id-card",
        "sanitarios": "fas fa-toilet",
        "sanitários": "fas fa-toilet",
        "splits": "fas fa-snowflake",
        "ventilacao": "fas fa-fan",
        "ventilação": "fas fa-fan",
        "vistoria area externa": "fas fa-tree",
        "vistoria área externa": "fas fa-tree",
        "gestao documental": "fas fa-folder-open",
        "gestão documental": "fas fa-folder-open"
    }
    
    # Tenta encontrar a seção diretamente
    for secao_nome, icone in icones_especificos.items():
        if secao_nome in nome_normalizado:
            return icone
    
    # Se não encontrou na lista específica, usa mapeamento genérico por palavras-chave
    mapeamento_geral = {
        "alarme": "fas fa-bell",
        "extintor": "fas fa-fire-extinguisher",
        "iluminação": "fas fa-lightbulb",
        "luz": "fas fa-lightbulb",
        "hidrante": "fas fa-tint",
        "agua": "fas fa-tint",
        "água": "fas fa-tint",
        "esgoto": "fas fa-water",
        "quadro": "fas fa-bolt",
        "elétric": "fas fa-bolt",
        "eletric": "fas fa-bolt",
        "gerador": "fas fa-plug",
        "ar condicionado": "fas fa-snowflake",
        "elevador": "fas fa-arrow-up",
        "escada": "fas fa-stairs",
        "porta": "fas fa-door-open",
        "saída": "fas fa-door-open",
        "saida": "fas fa-door-open",
        "emergência": "fas fa-exclamation-triangle",
        "emergencia": "fas fa-exclamation-triangle",
        "camera": "fas fa-video",
        "câmera": "fas fa-video",
        "segurança": "fas fa-shield-alt",
        "seguranca": "fas fa-shield-alt",
        "bomba": "fas fa-faucet",
        "motor": "fas fa-cogs",
        "filtro": "fas fa-filter",
        "ventilador": "fas fa-fan",
        "sanitario": "fas fa-toilet",
        "sanitário": "fas fa-toilet",
        "banheiro": "fas fa-toilet",
        "jardim": "fas fa-leaf",
        "estacionamento": "fas fa-parking",
        "garagem": "fas fa-car",
        "limpeza": "fas fa-broom",
        "vistoria": "fas fa-search",
        "controle": "fas fa-clipboard-check",
        "documental": "fas fa-folder-open",
        "documento": "fas fa-file-alt",
    }
    
    # Procura por palavras-chave no nome da seção
    for termo, icone in mapeamento_geral.items():
        if termo in nome_normalizado:
            return icone
    
    # Ícone padrão se nenhuma correspondência for encontrada
    return "fas fa-clipboard-list"