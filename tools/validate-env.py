#!/usr/bin/env python3
"""
Validador de .env.deploy para JardimGIS v2.0.0
Verifica 10 variáveis obrigatórias com tipos, ranges e valores

Uso:
    python3 tools/validate-env.py

Exit codes:
    0 - Validação completa (todas as 10 variáveis OK)
    1 - Validação falhou (erros encontrados)
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Cores ANSI para terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# ============================================================
# CONFIGURAÇÃO DE VARIÁVEIS OBRIGATÓRIAS
# ============================================================

REQUIRED_VARS = {
    'SECRET_KEY': {
        'tipo': 'string',
        'minlen': 32,
        'descricao': 'Chave secreta Flask (mínimo 32 caracteres)'
    },
    'FLASK_CONFIG': {
        'tipo': 'choice',
        'choices': ['development', 'production'],
        'descricao': 'Modo Flask (development/production)'
    },
    'PORT': {
        'tipo': 'int',
        'min': 1024,
        'max': 65535,
        'descricao': 'Porta Waitress (1024-65535)'
    },
    'DATA_DIR': {
        'tipo': 'path',
        'must_exist': False,
        'descricao': 'Diretório de dados (será criado se não existir)'
    },
    'LOGS_DIR': {
        'tipo': 'path',
        'must_exist': False,
        'descricao': 'Diretório de logs (será criado se não existir)'
    },
    'BACKUP_ENABLED': {
        'tipo': 'bool',
        'descricao': 'Habilita backups automáticos (true/false)'
    },
    'BACKUP_TIME': {
        'tipo': 'time',
        'descricao': 'Horário backup diário (formato HH:MM)'
    },
    'MAX_UPLOAD_SIZE_MB': {
        'tipo': 'int',
        'min': 1,
        'max': 1000,
        'descricao': 'Tamanho máximo upload em MB (1-1000)'
    },
    'IS_REVERSE_PROXY': {
        'tipo': 'bool',
        'descricao': 'Ativa ProxyFix para Apache (true/false)'
    },
    'STATIC_VERSION': {
        'tipo': 'string',
        'minlen': 1,
        'descricao': 'Versão assets estáticos (ex: 2.0.0)'
    }
}


# ============================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================

def validate_variable(var_name, config):
    """
    Valida uma variável de ambiente.
    
    Args:
        var_name: Nome da variável
        config: Dicionário de configuração com tipo e validações
    
    Returns:
        bool: True se válida, False caso contrário
    """
    value = os.getenv(var_name)
    
    # Verifica se existe
    if not value:
        print(f"{RED}❌ {var_name}: NÃO CONFIGURADA{RESET}")
        print(f"   {config['descricao']}")
        return False
    
    # Validações por tipo
    tipo = config['tipo']
    
    try:
        if tipo == 'int':
            val = int(value)
            if 'min' in config and val < config['min']:
                raise ValueError(f"Valor {val} menor que mínimo {config['min']}")
            if 'max' in config and val > config['max']:
                raise ValueError(f"Valor {val} maior que máximo {config['max']}")
        
        elif tipo == 'bool':
            if value.lower() not in ['true', 'false', '1', '0']:
                raise ValueError(f"Valor '{value}' não é booleano (use true/false)")
        
        elif tipo == 'choice':
            if value not in config['choices']:
                raise ValueError(f"Valor '{value}' não está em {config['choices']}")
        
        elif tipo == 'string':
            if 'minlen' in config and len(value) < config['minlen']:
                raise ValueError(f"String muito curta (mínimo {config['minlen']} caracteres)")
        
        elif tipo == 'path':
            path = Path(value)
            if config.get('must_exist', False) and not path.exists():
                raise ValueError(f"Path '{value}' não existe")
        
        elif tipo == 'time':
            # Valida formato HH:MM
            parts = value.split(':')
            if len(parts) != 2:
                raise ValueError(f"Formato inválido. Use HH:MM (ex: 20:00)")
            h, m = int(parts[0]), int(parts[1])
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError(f"Horário inválido: {value}")
    
    except ValueError as e:
        print(f"{RED}❌ {var_name}: {e}{RESET}")
        print(f"   Valor atual: '{value}'")
        return False
    
    # Warnings especiais
    if var_name == 'SECRET_KEY':
        if value == 'GERAR_ANTES_DEPLOY_64_CHARS_HEX':
            print(f"{YELLOW}⚠️  {var_name}: AINDA NÃO GERADO!{RESET}")
            print(f"   Execute: python3 -c \"import secrets; print(secrets.token_hex(32))\"")
            print(f"   E substitua em .env.deploy linha 6")
            return False
        
        # Verifica se é hexadecimal
        try:
            int(value, 16)
        except ValueError:
            print(f"{YELLOW}⚠️  {var_name}: Não parece ser hexadecimal{RESET}")
            print(f"   Recomendado: Gere com secrets.token_hex(32)")
    
    print(f"{GREEN}✅ {var_name}: OK{RESET}")
    return True


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """Executa validação completa do .env.deploy"""
    
    # Carrega .env.deploy
    env_file = Path(__file__).resolve().parent.parent / '.env.deploy'
    
    if not env_file.exists():
        print(f"\n{RED}{'='*60}{RESET}")
        print(f"{RED}ERRO: Arquivo .env.deploy não encontrado{RESET}")
        print(f"{RED}{'='*60}{RESET}")
        print(f"\nLocalização esperada: {env_file}")
        print(f"\nPara criar:")
        print(f"  1. Copie o template: cp .env.deploy.template .env.deploy")
        print(f"  2. Gere SECRET_KEY: python3 -c \"import secrets; print(secrets.token_hex(32))\"")
        print(f"  3. Edite .env.deploy e substitua SECRET_KEY")
        print(f"  4. Execute novamente: python3 tools/validate-env.py\n")
        return 1
    
    load_dotenv(env_file)
    
    # Banner
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}VALIDAÇÃO .env.deploy - JardimGIS v2.0.0{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Arquivo: {env_file}")
    print(f"Variáveis a validar: {len(REQUIRED_VARS)}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Valida todas as variáveis
    erros = 0
    for var_name, config in REQUIRED_VARS.items():
        if not validate_variable(var_name, config):
            erros += 1
        print()
    
    # Resultado final
    print(f"{BLUE}{'='*60}{RESET}")
    if erros == 0:
        print(f"{GREEN}✅ VALIDAÇÃO COMPLETA: Todas as {len(REQUIRED_VARS)} variáveis OK!{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        print(f"{GREEN}Configuração pronta para deploy.{RESET}")
        print(f"Execute: make deploy\n")
        return 0
    else:
        print(f"{RED}❌ VALIDAÇÃO FALHOU: {erros} erro(s) encontrado(s){RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        print(f"{YELLOW}Corrija os erros acima e execute novamente.{RESET}\n")
        return 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    sys.exit(main())
