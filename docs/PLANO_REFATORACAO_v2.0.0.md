# Plano de Refatoração JardimGIS v2.0.0

**Data:** 2025-01-XX  
**Objetivo:** Migração para padrão 12-factor com .env.deploy como fonte única de verdade  
**Padrão de referência:** SCADA-Web v2.0.0 (commits 9650a07, a59de11, 909df21)

---

## 1. Estado Atual (v0.x)

### 1.1 Vulnerabilidades Identificadas

| Severidade | Localização | Problema | Impacto |
|------------|-------------|----------|---------|
| **CRÍTICO** | `app/__init__.py:21` | `SECRET_KEY = '123'` hardcoded | Session hijacking, bypass autenticação |
| **ALTO** | Todo o projeto | Sem integração .env.deploy | Deriva de configuração, erros deploy |
| **MÉDIO** | `app/config.py:8-11,42-45` | Paths com lógica platform-dependent | Duplicação código, difícil manter |
| **BAIXO** | `makefile:1` | `PORT=4141` hardcoded | Inflexibilidade deployment |
| **BAIXO** | `requirements.txt` | Waitress ausente (usado mas não listado) | Falhas em deployment |
| **BAIXO** | `app/__init__.py:101-130` | Debug prints (`print()`) no production code | Log poluído, não estruturado |

### 1.2 Arquitetura Atual

**Entry Point:** `jardim_gis.py`
```python
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
serve(app, host='127.0.0.1', port=4141)
```

**Configuração:** Hardcoded em múltiplos arquivos
- `app/config.py`: Paths com `if platform.system() == "Linux"`
- `app/__init__.py`: SECRET_KEY, MAX_CONTENT_LENGTH
- `makefile`: PORT=4141
- `scripts/config.sh`: LOGS_PATH, SERVICE_NAME

**Deployment:** `scripts/deploy.sh` sem validação .env

**Features:**
- Gestão de árvores (JSON: `arvores.json`)
- Backups automáticos (20h diário via scheduler)
- Admin panel + Web interface
- Upload arquivos (PDF, DOC, XLS, images - 100MB limit)
- Apache reverse proxy integration (htpasswd via X-Remote-User)

---

## 2. Arquitetura Alvo (v2.0.0)

### 2.1 Variáveis de Ambiente (.env.deploy)

**Total estimado:** 10 variáveis

| Variável | Tipo | Exemplo/Valor Produção | Descrição |
|----------|------|------------------------|-----------|
| `SECRET_KEY` | string | `(gerado: 64 chars hex)` | Flask secret key - CRÍTICO |
| `FLASK_CONFIG` | string | `production` | Modo: development/production |
| `PORT` | int | `4141` | Porta Waitress (preservar atual) |
| `DATA_DIR` | path | `/var/softwaresTCE/dados/jardimgis` | Diretório dados (arvores.json, backups) |
| `LOGS_DIR` | path | `/var/softwaresTCE/logs/jardim_gis` | Diretório logs centralizado |
| `BACKUP_ENABLED` | bool | `true` | Habilita scheduler backups automáticos |
| `BACKUP_TIME` | string | `20:00` | Horário backup diário (formato HH:MM) |
| `MAX_UPLOAD_SIZE_MB` | int | `100` | Tamanho máximo upload (MB) |
| `IS_REVERSE_PROXY` | bool | `true` | Ativa ProxyFix (Apache integration) |
| `STATIC_VERSION` | string | `2.0.0` | Cache busting para assets estáticos |

**Justificativas:**
- `SECRET_KEY`: Substitui hardcoded '123' - segurança crítica
- `FLASK_CONFIG`: Dev/prod switching (como scada-web)
- `PORT`: Atualmente hardcoded em makefile
- `DATA_DIR` e `LOGS_DIR`: Substituem lógica platform.system()
- `BACKUP_*`: Configuráveis sem editar código
- `MAX_UPLOAD_SIZE_MB`: Atualmente hardcoded no código
- `IS_REVERSE_PROXY`: Controla ProxyFix (pode desabilitar em dev)
- `STATIC_VERSION`: Cache busting (lição do scada-web)

### 2.2 Estrutura de Arquivos (Novo)

```
jardim-gis/
├── .env.deploy.template      # NOVO: Template com valores produção hardcoded
├── .gitignore                 # ATUALIZADO: Proteger .env, .env.deploy
├── CHANGELOG.md               # NOVO: Histórico versões
├── jardim_gis.py              # REFATORADO: Loader .env + dev/prod modes
├── requirements.txt           # ATUALIZADO: Adicionar waitress==3.0.0
├── makefile                   # ATUALIZADO: Adicionar comando validate
├── app/
│   ├── __init__.py            # REFATORADO: Import settings, remover hardcoded
│   ├── config.py              # REFATORADO/DEPRECADO: Usar settings.py
│   ├── settings.py            # NOVO: Centralizador configurações (.env loader)
│   └── ...
├── scripts/
│   ├── config.sh              # REFATORADO: load_env_file() com sed fix
│   └── deploy.sh              # REFATORADO: Validação .env obrigatória
├── tools/
│   └── validate-env.py        # NOVO: Validador 10 variáveis
└── docs/
    ├── PLANO_REFATORACAO_v2.0.0.md  # Este documento
    └── legacy/
        ├── app__init__.py.backup     # NOVO: Backup original
        └── app_config.py.backup      # NOVO: Backup original
```

---

## 3. Plano de Execução

### Fase 1: Documentação e Segurança (Tasks 1-3)

#### Task 1: Criar CHANGELOG.md
- **Arquivo:** `CHANGELOG.md`
- **Conteúdo:**
  ```markdown
  # Changelog - JardimGIS
  
  ## [2.0.0] - 2025-01-XX
  
  ### 🔒 Segurança
  - **CRÍTICO:** Substituído SECRET_KEY='123' por variável de ambiente segura
  - Adicionado .env.deploy ao .gitignore para proteção de secrets
  
  ### ✨ Refatoração Arquitetural
  - Migração para padrão 12-factor app
  - .env.deploy como fonte única de verdade (10 variáveis)
  - Criado app/settings.py centralizador de configurações
  - Removida lógica platform-dependent (if Linux/Windows)
  
  ### 📝 Deployment
  - Validação obrigatória .env.deploy antes de deploy
  - Criado tools/validate-env.py (valida 10 variáveis)
  - deploy.sh com verificação automática de configuração
  - Suporte dev/prod modes em jardim_gis.py
  
  ### 🐛 Correções
  - Adicionado waitress==3.0.0 ao requirements.txt
  - PORT 4141 agora configurável via .env
  - Substituídos print() por logging estruturado
  
  ### 📚 Documentação
  - Criado PLANO_REFATORACAO_v2.0.0.md
  - Backups de código original em docs/legacy/
  ```

#### Task 2: Criar .env.deploy.template
- **Arquivo:** `.env.deploy.template`
- **Conteúdo:** (10 variáveis - valores produção hardcoded OK)
  ```bash
  # JardimGIS Configuration v2.0.0
  # ATENÇÃO: Este arquivo contém valores de produção hardcoded
  # Para desenvolvimento local, copie para .env e ajuste
  
  # Segurança (CRÍTICO - gerar antes de deploy)
  SECRET_KEY=GERAR_ANTES_DEPLOY_64_CHARS_HEX
  
  # Flask
  FLASK_CONFIG=production
  PORT=4141
  
  # Diretórios (Produção - Linux)
  DATA_DIR=/var/softwaresTCE/dados/jardimgis
  LOGS_DIR=/var/softwaresTCE/logs/jardim_gis
  
  # Backups Automáticos
  BACKUP_ENABLED=true
  BACKUP_TIME=20:00
  
  # Upload
  MAX_UPLOAD_SIZE_MB=100
  
  # Reverse Proxy (Apache)
  IS_REVERSE_PROXY=true
  
  # Cache Busting
  STATIC_VERSION=2.0.0
  ```

#### Task 3: Atualizar .gitignore
- **Arquivo:** `.gitignore`
- **Operação:** Adicionar ao final
  ```gitignore
  # Environment files (12-factor app)
  .env
  .env.deploy
  .env.*.local
  ```

---

### Fase 2: Infraestrutura Core (Tasks 4-7)

#### Task 4: Criar app/settings.py
- **Arquivo:** `app/settings.py`
- **Padrão:** Idêntico a scada-web/app/settings.py
- **Conteúdo:**
  ```python
  """
  Configurações centralizadas do JardimGIS.
  Carrega variáveis de ambiente do .env.deploy.
  """
  import os
  import sys
  from pathlib import Path
  from dotenv import load_dotenv
  
  # Detecta se está rodando via systemd ou desenvolvimento
  IS_SYSTEMD = os.getenv('INVOCATION_ID') is not None
  
  # Define qual .env carregar
  if IS_SYSTEMD:
      env_file = Path('/var/softwaresTCE/jardim_gis/.env.deploy')
  else:
      env_file = Path(__file__).resolve().parent.parent / '.env'
      if not env_file.exists():
          env_file = Path(__file__).resolve().parent.parent / '.env.deploy'
  
  # Carrega .env
  if env_file.exists():
      load_dotenv(env_file)
      print(f"[Settings] Variáveis carregadas de: {env_file}")
  else:
      print(f"[Settings] AVISO: Arquivo {env_file} não encontrado", file=sys.stderr)
  
  # Validação de variáveis obrigatórias
  def get_required_env(var_name: str) -> str:
      value = os.getenv(var_name)
      if not value:
          raise ValueError(f"Variável obrigatória não configurada: {var_name}")
      return value
  
  # Configurações carregadas
  SECRET_KEY = get_required_env('SECRET_KEY')
  FLASK_CONFIG = os.getenv('FLASK_CONFIG', 'production')
  PORT = int(os.getenv('PORT', '4141'))
  DATA_DIR = get_required_env('DATA_DIR')
  LOGS_DIR = get_required_env('LOGS_DIR')
  BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
  BACKUP_TIME = os.getenv('BACKUP_TIME', '20:00')
  MAX_UPLOAD_SIZE_MB = int(os.getenv('MAX_UPLOAD_SIZE_MB', '100'))
  IS_REVERSE_PROXY = os.getenv('IS_REVERSE_PROXY', 'true').lower() == 'true'
  STATIC_VERSION = os.getenv('STATIC_VERSION', '2.0.0')
  
  # Paths derivados (compatibilidade com config.py atual)
  ARVORES_JSON_PATH = os.path.join(DATA_DIR, 'arvores.json')
  BACKUP_DIR = os.path.join(DATA_DIR, 'bak')
  LOG_FILE = os.path.join(LOGS_DIR, 'jardimgis.log')
  
  # Routes prefix (manter compatibilidade)
  ROUTES_PREFIX = '/jardimgis'
  
  # Allowed extensions (manter do config.py original)
  ALLOWED_EXTENSIONS = {
      'pdf', 'doc', 'docx', 'xls', 'xlsx',
      'jpg', 'jpeg', 'png', 'gif',
      'zip', 'rar', '7z'
  }
  
  # Development mode
  DEBUG = FLASK_CONFIG == 'development'
  
  # Criar diretórios se não existirem
  os.makedirs(DATA_DIR, exist_ok=True)
  os.makedirs(LOGS_DIR, exist_ok=True)
  os.makedirs(BACKUP_DIR, exist_ok=True)
  ```

#### Task 5: Backup app/__init__.py
- **Operação:** `cp app/__init__.py docs/legacy/app__init__.py.backup`
- **Criar diretório:** `docs/legacy/` se não existir

#### Task 6: Refatorar app/__init__.py
- **Arquivo:** `app/__init__.py`
- **Mudanças:**
  1. Adicionar import: `from . import settings`
  2. **Linha 21:** Substituir `app.config['SECRET_KEY'] = '123'` por:
     ```python
     app.config['SECRET_KEY'] = settings.SECRET_KEY
     ```
  3. **Linha 20:** Remover TODO comment
  4. Adicionar após imports:
     ```python
     # Configurações de upload
     app.config['MAX_CONTENT_LENGTH'] = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
     ```
  5. **Linhas 101-130:** Substituir `print()` por logging estruturado:
     ```python
     logger = logging.getLogger('jardimgis')
     logger.info("Registrando blueprints...")
     # ... usar logger.info(), logger.error() etc
     ```
  6. Adicionar após criar app:
     ```python
     # Injetar STATIC_VERSION em templates
     @app.context_processor
     def inject_static_version():
         return {'STATIC_VERSION': settings.STATIC_VERSION}
     ```

#### Task 7: Backup e deprecar app/config.py
- **Backup:** `cp app/config.py docs/legacy/app_config.py.backup`
- **Opção 1 (Deprecação suave):** Adicionar no topo:
  ```python
  """
  DEPRECATED: Este módulo será removido em versão futura.
  Use app/settings.py para todas as configurações.
  
  Mantido temporariamente para compatibilidade com imports legados.
  """
  import warnings
  from . import settings
  
  warnings.warn(
      "app.config está deprecated. Use app.settings",
      DeprecationWarning,
      stacklevel=2
  )
  
  # Re-exportar de settings para compatibilidade
  DATA_DIR = settings.DATA_DIR
  LOGS_DIR = settings.LOGS_DIR
  # ... etc
  ```
- **Opção 2 (Substituição total):** Apagar conteúdo e deixar apenas:
  ```python
  """Deprecated: Use app.settings"""
  from . import settings
  ```

---

### Fase 3: Entry Point e Deployment (Tasks 8-11)

#### Task 8: Refatorar jardim_gis.py
- **Arquivo:** `jardim_gis.py`
- **Substituir tudo por:**
  ```python
  #!/usr/bin/env python3
  """
  JardimGIS - Sistema de Controle Geográfico de Árvores
  Entry point com suporte a dev/prod modes
  """
  import os
  import sys
  from pathlib import Path
  from dotenv import load_dotenv
  
  # Carrega .env.deploy ANTES de importar app
  # (permite override via .env em desenvolvimento)
  def load_environment():
      """Carrega variáveis de ambiente do .env ou .env.deploy"""
      base_dir = Path(__file__).resolve().parent
      
      # Desenvolvimento: Usa .env se existir, senão .env.deploy
      env_file = base_dir / '.env'
      if not env_file.exists():
          env_file = base_dir / '.env.deploy'
      
      if env_file.exists():
          load_dotenv(env_file)
          print(f"[JardimGIS] Carregado: {env_file}")
          return True
      else:
          print(f"[JardimGIS] ERRO: Nenhum .env ou .env.deploy encontrado!", file=sys.stderr)
          return False
  
  # Carrega ambiente
  if not load_environment():
      sys.exit(1)
  
  # Agora pode importar app (que depende de settings)
  from app import create_app
  from app import settings
  
  # Cria app
  app = create_app()
  
  # Modo desenvolvimento vs produção
  if settings.FLASK_CONFIG == 'development':
      print(f"[JardimGIS] Modo DESENVOLVIMENTO na porta {settings.PORT}")
      print(f"[JardimGIS] DEBUG={settings.DEBUG}")
      app.run(
          host='127.0.0.1',
          port=settings.PORT,
          debug=True
      )
  else:
      # Produção: Waitress com ProxyFix
      from waitress import serve
      from werkzeug.middleware.proxy_fix import ProxyFix
      
      if settings.IS_REVERSE_PROXY:
          app.wsgi_app = ProxyFix(
              app.wsgi_app,
              x_for=1,
              x_host=1,
              x_proto=1
          )
          print(f"[JardimGIS] ProxyFix habilitado")
      
      print(f"[JardimGIS] Iniciando Waitress na porta {settings.PORT}")
      serve(app, host='127.0.0.1', port=settings.PORT)
  ```

#### Task 9: Atualizar scripts/config.sh
- **Arquivo:** `scripts/config.sh`
- **Adicionar função load_env_file (ANTES de qualquer uso de variáveis):**
  ```bash
  # Função para carregar .env.deploy
  load_env_file() {
      local env_file="$1"
      
      if [ ! -f "$env_file" ]; then
          echo "[Config] ERRO: Arquivo $env_file não encontrado!"
          return 1
      fi
      
      echo "[Config] Carregando variáveis de: $env_file"
      
      # Usa sed para remover comentários e linhas vazias
      # Fix: Aspas duplas permitem expansão de variáveis
      while IFS='=' read -r key value; do
          # Remove espaços e aspas do value
          value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")
          export "$key=$value"
          echo "[Config]   $key = $value"
      done < <(sed -e '/^#/d' -e '/^$/d' -e 's/#.*//' "$env_file")
      
      echo "[Config] Variáveis carregadas com sucesso."
  }
  
  # Carregar .env.deploy
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
  ENV_FILE="$PROJECT_ROOT/.env.deploy"
  
  load_env_file "$ENV_FILE" || exit 1
  
  # Agora pode usar variáveis do .env
  SERVICE_NAME="jardim_gis.service"
  PROJECT_NAME="jardim_gis"
  GIT_REPO="TCE-Manutencao-Predial/JardimGIS"
  
  # Variáveis do .env.deploy (agora carregadas)
  ROOT_BACKEND="/var/softwaresTCE/$PROJECT_NAME"
  LOGS_PATH="$LOGS_DIR"  # Do .env
  # PORT já está carregado
  ```

#### Task 10: Atualizar scripts/deploy.sh
- **Arquivo:** `scripts/deploy.sh`
- **Adicionar ANTES de `main()`:**
  ```bash
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
  ```
- **Em `main()`:** Adicionar como primeira linha:
  ```bash
  main() {
      echo "[Deploy] Iniciando processo de Deploy..."
      validar_env_deploy || exit 1  # NOVO: Validação obrigatória
      atualizar_projeto_local
      # ...resto do código
  ```

#### Task 11: Criar tools/validate-env.py
- **Arquivo:** `tools/validate-env.py`
- **Conteúdo:**
  ```python
  #!/usr/bin/env python3
  """
  Validador de .env.deploy para JardimGIS
  Verifica 10 variáveis obrigatórias
  """
  import sys
  import os
  from pathlib import Path
  from dotenv import load_dotenv
  
  # Cores ANSI
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RESET = '\033[0m'
  
  # Variáveis obrigatórias
  REQUIRED_VARS = {
      'SECRET_KEY': {
          'tipo': 'string',
          'minlen': 32,
          'descricao': 'Chave secreta Flask (mínimo 32 caracteres)'
      },
      'FLASK_CONFIG': {
          'tipo': 'choice',
          'choices': ['development', 'production'],
          'descricao': 'Modo Flask'
      },
      'PORT': {
          'tipo': 'int',
          'min': 1024,
          'max': 65535,
          'descricao': 'Porta Waitress'
      },
      'DATA_DIR': {
          'tipo': 'path',
          'must_exist': False,
          'descricao': 'Diretório de dados'
      },
      'LOGS_DIR': {
          'tipo': 'path',
          'must_exist': False,
          'descricao': 'Diretório de logs'
      },
      'BACKUP_ENABLED': {
          'tipo': 'bool',
          'descricao': 'Habilita backups automáticos'
      },
      'BACKUP_TIME': {
          'tipo': 'time',
          'descricao': 'Horário backup (HH:MM)'
      },
      'MAX_UPLOAD_SIZE_MB': {
          'tipo': 'int',
          'min': 1,
          'max': 1000,
          'descricao': 'Tamanho máximo upload (MB)'
      },
      'IS_REVERSE_PROXY': {
          'tipo': 'bool',
          'descricao': 'Ativa ProxyFix'
      },
      'STATIC_VERSION': {
          'tipo': 'string',
          'minlen': 1,
          'descricao': 'Versão assets estáticos'
      }
  }
  
  def validate_variable(var_name, config):
      """Valida uma variável de ambiente"""
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
                  raise ValueError(f"Valor '{value}' não é booleano (true/false)")
          
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
                  raise ValueError(f"Formato inválido. Use HH:MM")
              h, m = int(parts[0]), int(parts[1])
              if not (0 <= h <= 23 and 0 <= m <= 59):
                  raise ValueError(f"Horário inválido: {value}")
      
      except ValueError as e:
          print(f"{RED}❌ {var_name}: {e}{RESET}")
          print(f"   Valor atual: '{value}'")
          return False
      
      # Warnings
      if var_name == 'SECRET_KEY' and value == 'GERAR_ANTES_DEPLOY_64_CHARS_HEX':
          print(f"{YELLOW}⚠️  {var_name}: AINDA NÃO GERADO!{RESET}")
          print(f"   Execute: python3 -c \"import secrets; print(secrets.token_hex(32))\"")
          return False
      
      print(f"{GREEN}✅ {var_name}: OK{RESET}")
      return True
  
  def main():
      """Executa validação completa"""
      # Carrega .env.deploy
      env_file = Path(__file__).resolve().parent.parent / '.env.deploy'
      
      if not env_file.exists():
          print(f"{RED}ERRO: Arquivo .env.deploy não encontrado em {env_file}{RESET}")
          return 1
      
      load_dotenv(env_file)
      
      print(f"\n{'='*60}")
      print(f"Validando .env.deploy - JardimGIS v2.0.0")
      print(f"Arquivo: {env_file}")
      print(f"{'='*60}\n")
      
      # Valida todas as variáveis
      erros = 0
      for var_name, config in REQUIRED_VARS.items():
          if not validate_variable(var_name, config):
              erros += 1
          print()
      
      # Resultado final
      print(f"{'='*60}")
      if erros == 0:
          print(f"{GREEN}✅ VALIDAÇÃO COMPLETA: Todas as 10 variáveis OK!{RESET}")
          print(f"{'='*60}\n")
          return 0
      else:
          print(f"{RED}❌ VALIDAÇÃO FALHOU: {erros} erro(s) encontrado(s){RESET}")
          print(f"{'='*60}\n")
          return 1
  
  if __name__ == '__main__':
      sys.exit(main())
  ```

---

### Fase 4: Finalização (Tasks 12-14)

#### Task 12: Atualizar requirements.txt
- **Arquivo:** `requirements.txt`
- **Adicionar:** `waitress==3.0.0` (após Flask ou no final)

#### Task 13: Atualizar makefile
- **Arquivo:** `makefile`
- **Adicionar target validate (antes de setup):**
  ```makefile
  .PHONY: validate
  validate:
  	@echo "Validando .env.deploy..."
  	@python3 tools/validate-env.py
  ```
- **Atualizar target setup:** Adicionar validação
  ```makefile
  .PHONY: setup
  setup: validate
  	@echo "Instalando dependências..."
  	# ... resto do código setup
  ```

#### Task 14: Git Commit
- **Comandos:**
  ```bash
  git add -A
  git commit -m "refactor(jardim-gis): Migração v2.0.0 - 12-factor app com .env.deploy
  
  🔒 SEGURANÇA:
  - Substituído SECRET_KEY='123' por variável ambiente segura
  - Adicionado .env.deploy ao .gitignore
  
  ✨ REFATORAÇÃO:
  - Criado app/settings.py centralizador (10 variáveis)
  - Removida lógica platform-dependent (if Linux/Windows)
  - jardim_gis.py com suporte dev/prod modes
  - Substituídos print() por logging estruturado
  
  📝 DEPLOYMENT:
  - Validação obrigatória .env.deploy (tools/validate-env.py)
  - deploy.sh com verificação automática
  - config.sh com load_env_file() + sed fix
  
  🐛 CORREÇÕES:
  - Adicionado waitress==3.0.0 ao requirements.txt
  - PORT 4141 agora configurável via .env
  
  📚 DOCUMENTAÇÃO:
  - PLANO_REFATORACAO_v2.0.0.md
  - CHANGELOG.md
  - Backups código original em docs/legacy/
  
  Arquivos modificados:
  - .env.deploy.template (NOVO - 10 variáveis)
  - .gitignore (proteção .env)
  - CHANGELOG.md (NOVO)
  - app/__init__.py (SECRET_KEY, logging, STATIC_VERSION)
  - app/settings.py (NOVO - centralizador)
  - app/config.py (deprecated)
  - jardim_gis.py (reescrito - .env loader)
  - requirements.txt (+waitress)
  - makefile (+validate)
  - scripts/config.sh (load_env_file)
  - scripts/deploy.sh (validação .env)
  - tools/validate-env.py (NOVO)
  - docs/legacy/* (backups)
  
  Padrão: SCADA-Web v2.0.0 (commits 9650a07, a59de11, 909df21)"
  ```

---

## 4. Pós-Refatoração

### 4.1 Checklist de Deploy

Antes do primeiro deploy em produção:

1. ✅ Copiar template: `cp .env.deploy.template .env.deploy`
2. 🔑 **CRÍTICO:** Gerar SECRET_KEY seguro:
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
   Substituir em `.env.deploy`
3. ✅ Validar configuração: `make validate`
4. ✅ Testar em dev: `FLASK_CONFIG=development python3 jardim_gis.py`
5. ✅ Deploy: `make deploy`

### 4.2 Migrações Futuras

Microserviços pendentes do padrão 12-factor:
- `analise-processos` (SSL_CONFIGURATION.md indica complexidade)
- `checklist-predial`
- `controle-nfs`
- `eventos-feriados`
- `helpdesk-monitor`
- `memorando-api`
- Todos em `automacao/`, `ia/`, `monitoramento/`

**Lições aprendidas (scada-web + jardim-gis):**
1. Sempre usar paths reais de produção no .env.deploy.template
2. Função `load_env_file()` com sed fix (aspas duplas)
3. Validação obrigatória antes de deploy
4. Backups de código original em docs/legacy/
5. Substituir print() por logging estruturado
6. STATIC_VERSION para cache busting
7. Dev/prod modes no entry point

---

## 5. Estatísticas Estimadas

- **Arquivos novos:** 5 (settings.py, .env.deploy.template, CHANGELOG.md, validate-env.py, PLANO_REFATORACAO_v2.0.0.md)
- **Arquivos modificados:** 9 (.gitignore, __init__.py, config.py, jardim_gis.py, requirements.txt, makefile, config.sh, deploy.sh, + backups)
- **Linhas adicionadas:** ~600
- **Linhas removidas:** ~50
- **Variáveis ambiente:** 10
- **Vulnerabilidades corrigidas:** 6 (1 crítica, 1 alta, 2 médias, 2 baixas)
- **Tempo estimado:** 2-3 horas (seguindo plano)

---

**Próximo passo:** Executar Tasks 1-14 sequencialmente.
