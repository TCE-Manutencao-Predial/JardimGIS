# Changelog - JardimGIS

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2.0.0] - 2025-01-XX

### 🔒 Segurança

- **CRÍTICO:** Substituído `SECRET_KEY='123'` hardcoded por variável de ambiente segura
  - Localização: `app/__init__.py` linha 21
  - Impacto: Previne session hijacking e bypass de autenticação
- Adicionado `.env` e `.env.deploy` ao `.gitignore` para proteção de secrets
- Geração obrigatória de SECRET_KEY antes de primeiro deploy (64 caracteres hexadecimais)

### ✨ Refatoração Arquitetural

- **Migração para padrão 12-factor app**
  - `.env.deploy` como fonte única de verdade para configurações
  - 10 variáveis de ambiente centralizadas
- **Criado `app/settings.py`** - Centralizador de todas as configurações
  - Carrega automaticamente .env.deploy em produção ou .env em desenvolvimento
  - Validação de variáveis obrigatórias com mensagens de erro claras
  - Auto-detecção de modo systemd vs desenvolvimento
- **Removida lógica platform-dependent**
  - Eliminado `if platform.system() == "Linux"` em `app/config.py`
  - Paths agora configuráveis via variáveis de ambiente
  - Melhor portabilidade entre ambientes
- **Depreciado `app/config.py`**
  - Mantido apenas para compatibilidade com imports legados
  - Todas as novas features devem usar `app/settings.py`

### 📝 Deployment

- **Validação obrigatória de `.env.deploy` antes de deploy**
  - Criado `tools/validate-env.py` - valida 10 variáveis com tipos e ranges
  - `deploy.sh` executa validação automaticamente
  - Deploy é interrompido se configuração inválida
- **Aprimorado `scripts/config.sh`**
  - Função `load_env_file()` com fix para expansão de variáveis (sed + aspas duplas)
  - Carrega variáveis do .env.deploy automaticamente
  - Mensagens de log estruturadas
- **Suporte a dev/prod modes em `jardim_gis.py`**
  - Modo desenvolvimento: Flask debug server
  - Modo produção: Waitress com ProxyFix
  - Auto-seleção de .env vs .env.deploy

### 🐛 Correções

- **Adicionado `waitress==3.0.0` ao `requirements.txt`**
  - Biblioteca estava sendo usada mas não listada como dependência
  - Previne falhas em deployments limpos
- **PORT 4141 agora configurável via `.env`**
  - Anteriormente hardcoded em `makefile`
  - Permite testes paralelos e flexibilidade de deployment
- **Substituídos `print()` por logging estruturado**
  - Todas as mensagens de debug agora usam módulo `logging`
  - Logs mais limpos e filtráveis em produção
  - Facilita troubleshooting via journalctl

### 🎨 Melhorias

- **Cache busting para assets estáticos**
  - Variável `STATIC_VERSION` injetada em templates
  - Previne problemas de cache após atualizações
- **MAX_UPLOAD_SIZE_MB configurável**
  - Anteriormente hardcoded (100MB)
  - Agora ajustável via variável de ambiente
- **Configurações de backup agendado flexíveis**
  - `BACKUP_ENABLED`: Liga/desliga scheduler
  - `BACKUP_TIME`: Configurável (padrão 20:00)
  - Não requer edição de código

### 📚 Documentação

- Criado `PLANO_REFATORACAO_v2.0.0.md` - Plano completo de migração
- Criado este `CHANGELOG.md`
- Backups de código original em `docs/legacy/`:
  - `app__init__.py.backup`
  - `app_config.py.backup`
- Comentários expandidos em arquivos de configuração

### 🔧 Configuração

**Variáveis de ambiente adicionadas (10 total):**

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `SECRET_KEY` | string | *(obrigatório)* | Chave secreta Flask (mínimo 32 chars) |
| `FLASK_CONFIG` | string | `production` | Modo: development/production |
| `PORT` | int | `4141` | Porta Waitress |
| `DATA_DIR` | path | `/var/softwaresTCE/dados/jardimgis` | Diretório de dados (arvores.json, backups) |
| `LOGS_DIR` | path | `/var/softwaresTCE/logs/jardim_gis` | Diretório de logs |
| `BACKUP_ENABLED` | bool | `true` | Habilita scheduler de backups automáticos |
| `BACKUP_TIME` | string | `20:00` | Horário backup diário (HH:MM) |
| `MAX_UPLOAD_SIZE_MB` | int | `100` | Tamanho máximo upload (MB) |
| `IS_REVERSE_PROXY` | bool | `true` | Ativa ProxyFix (Apache integration) |
| `STATIC_VERSION` | string | `2.0.0` | Versão para cache busting |

### ⚙️ Arquivos Modificados

- `.env.deploy.template` *(NOVO)* - Template com valores produção
- `.gitignore` - Proteção .env files
- `CHANGELOG.md` *(NOVO)* - Este arquivo
- `app/__init__.py` - SECRET_KEY, logging estruturado, STATIC_VERSION
- `app/settings.py` *(NOVO)* - Centralizador configurações
- `app/config.py` - Marcado como deprecated
- `jardim_gis.py` - Reescrito com .env loader e dev/prod modes
- `requirements.txt` - Adicionado waitress==3.0.0
- `makefile` - Adicionado target `validate`
- `scripts/config.sh` - Função `load_env_file()`
- `scripts/deploy.sh` - Validação obrigatória .env.deploy
- `tools/validate-env.py` *(NOVO)* - Validador 10 variáveis
- `docs/legacy/` *(NOVO)* - Backups código original

### 🚀 Instruções de Deploy

1. Copiar template: `cp .env.deploy.template .env.deploy`
2. **CRÍTICO:** Gerar SECRET_KEY seguro:
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
   Substituir em `.env.deploy` linha 6
3. Validar configuração: `make validate`
4. Testar em dev: `FLASK_CONFIG=development python3 jardim_gis.py`
5. Deploy: `make deploy`

### ⚠️ Breaking Changes

- **Variáveis de ambiente obrigatórias:** `.env.deploy` deve existir antes de deploy
- **SECRET_KEY deve ser gerado:** Valor default `GERAR_ANTES_DEPLOY_64_CHARS_HEX` falha na validação
- **Novo fluxo de deploy:** Validação automática pode interromper deploy se configuração inválida

### 📊 Estatísticas da Refatoração

- **Vulnerabilidades corrigidas:** 6 (1 crítica, 1 alta, 2 médias, 2 baixas)
- **Arquivos novos:** 5
- **Arquivos modificados:** 9
- **Linhas adicionadas:** ~600
- **Linhas removidas:** ~50
- **Padrão aplicado:** SCADA-Web v2.0.0 (commits 9650a07, a59de11, 909df21)

---

## [0.x] - Pré-refatoração

### Histórico Legado
- Sistema desenvolvido originalmente com configurações hardcoded
- Lógica platform-dependent para suporte Linux/Windows
- Deployment manual sem validações automáticas
- SECRET_KEY weak ('123') conhecida

**Nota:** Versões anteriores não seguiam versionamento semântico.