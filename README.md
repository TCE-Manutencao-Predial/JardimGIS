# 🌳 JardimGIS

**Sistema de Controle Geográfico de Árvores e Jardins**  
*Tribunal de Contas do Estado de Goiás*

---

## 📋 Sobre o Projeto

O **JardimGIS** é um sistema web desenvolvido para gestão e mapeamento de árvores, mudas, jardins e placas de identificação. O sistema permite o controle detalhado de espécies vegetais incluindo dados botânicos, localização geográfica (GPS), estado de conservação e histórico de plantio.

### 🎯 Principais Funcionalidades

- 🌲 **Cadastro completo de árvores** com dados botânicos
- 📍 **Geolocalização por GPS** (coordenadas latitude/longitude)
- 🏷️ **Controle de placas de identificação** e seu estado de conservação
- 📊 **Estado de conservação** das árvores (Excelente, Bom, Regular, Ruim, Crítico)
- 📅 **Histórico de plantio** com data e responsável
- 🌸 **Informações fenológicas** (época de floração e frutificação)
- 💾 **Sistema de backup automático** circular com 15 níveis
- 📤 **Exportação para Excel** dos dados cadastrados

---

## 🗂️ Estrutura de Dados

Cada árvore cadastrada possui os seguintes campos:

| Campo | Descrição |
|-------|-----------|
| **ID** | Código único de identificação |
| **Nome Popular** | Nome comum da espécie |
| **Nome Científico** | Nome botânico (nomenclatura binomial) |
| **Localização Textual** | Descrição do local onde está plantada |
| **Coordenadas GPS** | Latitude e longitude (formato: -16.6869, -49.2648) |
| **Data de Plantio** | Quando foi plantada (opcional) |
| **Plantado Por** | Nome do responsável pelo plantio (opcional) |
| **Nomes Populares Adicionais** | Outros nomes conhecidos da espécie |
| **Época de Floração** | Período do ano em que floresce |
| **Época de Frutificação** | Período do ano em que frutifica |
| **Características** | Descrição detalhada da espécie |
| **Estado de Conservação da Árvore** | Excelente / Bom / Regular / Ruim / Crítico |
| **Estado de Conservação da Placa** | Excelente / Bom / Regular / Ruim / Sem Placa |
| **Observações** | Anotações gerais |
| **Responsável** | Usuário que fez a última edição (automático) |
| **Data da Última Atualização** | Timestamp da última modificação (automático) |

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask 3.0.3** - Framework web
- **Waitress 3.0.0** - Servidor WSGI para produção
- **Schedule** - Agendamento de backups automáticos
- **FileHash** - Controle de concorrência em arquivos

### Frontend
- **HTML5 / CSS3**
- **JavaScript (ES6+)**
- **Font Awesome** - Ícones
- **SheetJS (xlsx)** - Exportação Excel

### Armazenamento
- **JSON** - Banco de dados de arquivos
- Sistema de backup circular automático

---

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Make (opcional, para usar comandos do Makefile)

### 1. Clone o repositório
```bash
git clone https://github.com/TCE-Manutencao-Predial/JardimGIS.git
cd JardimGIS
```

### 2. Configure o ambiente
```bash
make setup
```

### 3. Execute localmente
```bash
make run
```

O sistema estará disponível em: `http://127.0.0.1:4141`

---

## 🐧 Deploy em Produção v2.0.0 (TCE-GO)

### Pré-requisitos
- Python 3.8+ com pip
- Apache HTTP Server com mod_proxy habilitado
- Acesso sudo no servidor
- **Repositório scada-web atualizado** (gerencia configurações Apache)

### Deploy Completo (Recomendado)

#### 1. Clone e Configure o Repositório
```bash
# Navegar para o diretório de softwares
cd /var/softwaresTCE

# Clonar repositório
git clone <URL_DO_REPO> jardim_gis
cd jardim_gis
```

#### 2. Configure as Variáveis de Ambiente
```bash
# Copiar template
cp .env.deploy.template .env.deploy

# Gerar SECRET_KEY segura
python3 -c "import secrets; print(secrets.token_hex(32))"

# Editar .env.deploy e substituir SECRET_KEY
nano .env.deploy
```

**Variáveis obrigatórias em `.env.deploy`:**
- `SECRET_KEY`: Chave secreta gerada (nunca use '123'!)
- `FLASK_CONFIG`: production
- `PORT`: 4141
- `DATA_DIR`: /var/softwaresTCE/dados/jardim_gis
- `LOGS_DIR`: /var/softwaresTCE/logs/jardim_gis

#### 3. Valide a Configuração
```bash
make validate
```

#### 4. Execute o Deploy Automático
```bash
make deploy
```

**O que o deploy automático faz:**
1. ✅ Valida todas as variáveis de ambiente
2. ✅ Cria diretórios de dados e logs
3. ✅ Configura permissões corretas
4. ✅ Instala/atualiza o serviço systemd (`jardim_gis.service`)
5. ✅ Exporta chaves de autenticação
6. ✅ Inicia o serviço

**⚠️ Configuração Apache:**
- Gerenciada pelo repositório **scada-web**
- Arquivo: `scada-web/scripts/httpd_67_jardimgis.conf`
- O deploy do scada-web copia automaticamente para `/etc/httpd/conf.d/`

### Acesso ao Sistema
- **URL**: http://automacao.tce.go.gov.br/jardimgis
- **Autenticação**: htpasswd via Apache (`/etc/httpd/.htpasswd`)
- **Porta backend**: 4141 (proxy reverso via Apache)

### Gerenciamento do Serviço
```bash
# Status do serviço
sudo systemctl status jardim_gis

# Reiniciar serviço
sudo systemctl restart jardim_gis

# Ver logs em tempo real
sudo journalctl -u jardim_gis -f

# Últimas 100 linhas de log
sudo journalctl -u jardim_gis -n 100

# Recarregar Apache (se necessário)
sudo systemctl reload httpd
```

### Deploy Manual (Avançado)
```bash
# 1. Validar ambiente
make validate

# 2. Configurar backend (venv, dependências)
cd /var/softwaresTCE/jardim_gis
bash scripts/config.sh

# 3. Deploy do serviço systemd
sudo cp scripts/jardim_gis.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jardim_gis.service
sudo systemctl start jardim_gis.service

# 4. Verificar funcionamento
curl http://127.0.0.1:4141/jardimgis/

# 5. Configuração Apache (via scada-web)
# Execute o deploy do scada-web para instalar httpd_67_jardimgis.conf
cd /var/softwaresTCE/scada-web
make deploy
```

### Troubleshooting

#### Serviço não inicia
```bash
# Verificar logs
sudo journalctl -u jardim_gis -xe

# Verificar variáveis de ambiente
cat /var/softwaresTCE/jardim_gis/.env.deploy

# Revalidar configuração
cd /var/softwaresTCE/jardim_gis
make validate
```

#### Erro 502 (Bad Gateway)
```bash
# Verificar se backend está rodando
sudo systemctl status jardim_gis
curl http://127.0.0.1:4141/jardimgis/

# Verificar logs do Apache
sudo tail -f /var/log/httpd/error_log

# Verificar configuração Apache (gerenciada pelo scada-web)
cat /etc/httpd/conf.d/httpd_67_jardimgis.conf
```

#### Dependências não encontradas
```bash
# Reconfigurar ambiente virtual
cd /var/softwaresTCE/jardim_gis
bash scripts/config.sh
```

---

## 📁 Estrutura do Projeto v2.0.0

```
jardim_gis/                          # Nome do diretório em produção
├── app/
│   ├── __init__.py                  # Factory pattern (create_app)
│   ├── settings.py                  # Configurações (carrega .env.deploy)
│   ├── dados/                       # [DEPRECATED] Dados locais
│   ├── routes/
│   │   ├── web/                     # Rotas principais
│   │   └── features/
│   │       └── arvores/             # CRUD de árvores
│   ├── static/
│   │   ├── css/                     # Estilos
│   │   └── js/                      # Scripts JavaScript
│   ├── templates/                   # Templates Jinja2
│   └── utils/
│       ├── data/                    # Gerenciamento de JSON
│       ├── managers/                # BackupManager
│       └── schedulers/              # APScheduler (backups)
├── scripts/
│   ├── jardim_gis.service           # Serviço systemd (nome correto)
│   ├── deploy.sh                    # Deploy automático completo
│   ├── undeploy.sh                  # Remoção limpa
│   ├── run.sh                       # Startup com venv detection
│   ├── config.sh                    # Setup de ambiente
│   └── utils.sh                     # Funções auxiliares
├── tools/
│   └── validate-env.py              # Validador de .env.deploy
├── docs/
│   ├── legacy/                      # Backups de configs antigas
│   ├── CHANGELOG.md                 # Histórico de mudanças
│   └── PLANO_REFATORACAO_v2.0.0.md  # Plano de migração
├── .env.deploy.template             # Template de configuração
├── .env.deploy                      # Configuração real (não versionado)
├── jardim_gis.py                    # Ponto de entrada
├── makefile                         # Comandos make (validate, deploy)
├── requirements.txt                 # Dependências Python
└── pyproject.toml                   # Metadados do projeto
```

### 🆕 Novidades v2.0.0
- ✅ **`.env.deploy`**: Configuração centralizada (substitui hardcoded configs)
- ✅ **`scripts/deploy.sh`**: Deploy completo (backend + systemd + Apache)
- ✅ **`tools/validate-env.py`**: Validação de 10 variáveis obrigatórias
- ✅ **`jardim_gis.service`**: Serviço systemd com nome correto
- ✅ **Factory pattern**: `create_app()` em `app/__init__.py`
- ✅ **Apache auto-deploy**: Copia config de scada-web automaticamente

---

## 🔧 Configuração v2.0.0

### Arquivo Principal: `.env.deploy`

**Variáveis Obrigatórias (validadas por `make validate`):**

```bash
# Segurança
SECRET_KEY=<gerar_com_secrets.token_hex(32)>

# Ambiente
FLASK_CONFIG=production

# Rede
PORT=4141

# Diretórios
DATA_DIR=/var/softwaresTCE/dados/jardim_gis
LOGS_DIR=/var/softwaresTCE/logs/jardim_gis

# Backup automático
BACKUP_ENABLED=true
BACKUP_TIME=20:00

# Upload
MAX_UPLOAD_SIZE_MB=100

# Proxy reverso (Apache)
IS_REVERSE_PROXY=true

# Versionamento de assets
STATIC_VERSION=2.0.0
```

### Configurações por Ambiente

**app/settings.py** carrega automaticamente de `.env.deploy`:

```python
class ProductionConfig(Config):
    """Configuração de Produção"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # ← Vem de .env.deploy
    
    # Diretórios (sobrescreve defaults)
    DATA_DIR = os.getenv('DATA_DIR', '/var/softwaresTCE/dados/jardim_gis')
    LOGS_DIR = os.getenv('LOGS_DIR', '/var/softwaresTCE/logs/jardim_gis')
    
    # Prefixo para Apache
    ROUTES_PREFIX = '/jardimgis'  # ← Lowercase (importante!)
```

### Backups Automáticos
- **Frequência**: Configurável em `BACKUP_TIME` (padrão 20:00)
- **Níveis**: 15 backups circulares
- **Localização**: `$DATA_DIR/bak/`
- **Formato**: `arvores.json.bak1` até `.bak15`
- **Trigger**: Mudanças via APScheduler

### Localização de Arquivos em Produção

```bash
# Aplicação
/var/softwaresTCE/jardim_gis/        # Código fonte
/var/softwaresTCE/jardim_gis/.venv/  # Virtual environment

# Dados
/var/softwaresTCE/dados/jardim_gis/arvores.json
/var/softwaresTCE/dados/jardim_gis/bak/          # Backups

# Logs
/var/softwaresTCE/logs/jardim_gis/jardim_gis.log

# Configurações
/var/softwaresTCE/jardim_gis/.env.deploy         # Variáveis
/etc/httpd/conf.d/httpd_67_jardimgis.conf        # Apache
/usr/lib/systemd/system/jardim_gis.service       # Systemd
```

---

## 🌐 Rotas da Aplicação

| Rota | Descrição |
|------|-----------|
| `/jardimgis` | Página principal - Gestão de árvores |
| `/jardimgis/admin/backups` | Gerenciamento de backups |

---

## 👥 Controle de Acesso

O sistema utiliza autenticação Apache com `X-Remote-User` header.  
Em desenvolvimento, o usuário padrão é `admin`.

---

## 📊 Exportação de Dados

O sistema permite exportar todos os dados para Excel (.xlsx) com formatação profissional incluindo:
- Cabeçalhos formatados
- Colunas com largura ajustada
- Filtros automáticos
- Informações de auditoria

---

## 🔒 Segurança

### ✅ Implementações v2.0.0
- ✅ Validação de tipos de arquivo no upload
- ✅ Limite de tamanho de arquivo (100MB configurável)
- ✅ Autenticação via Apache com htpasswd
- ✅ Backup automático antes de cada alteração
- ✅ SECRET_KEY via variável de ambiente (.env.deploy)
- ✅ Configurações sensíveis isoladas do código
- ✅ Permissões restritas em diretórios de dados

### ⚠️ CRÍTICO - Antes do Deploy em Produção
1. **Gere SECRET_KEY única e segura:**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
2. **Nunca use SECRET_KEY='123' em produção!**
3. **Mantenha `.env.deploy` fora do controle de versão**
4. **Configure backup automático em `.env.deploy`:**
   ```bash
   BACKUP_ENABLED=true
   BACKUP_TIME=20:00
   ```

### 🔐 Vulnerabilidades Corrigidas na v2.0.0
- 🔴 **SECRET_KEY hardcoded** → ✅ Variável de ambiente
- 🔴 **Credenciais em arquivos .py** → ✅ .env.deploy exclusivo
- 🔴 **Sem validação de ambiente** → ✅ make validate obrigatório

---

## 🐛 Logs

### Localização dos Logs
- **Produção**: `/var/softwaresTCE/logs/jardimgis/jardimgis.log`
- **Desenvolvimento**: `app/logs/jardimgis.log`

### Ver Logs do Serviço
```bash
# Logs em tempo real
sudo journalctl -u jardimgis -f

# Últimas 100 linhas
sudo journalctl -u jardimgis -n 100
```

---

## 🤝 Contribuição

Este é um projeto interno do TCE-GO desenvolvido pela equipe de Infraestrutura Predial.

---

## 👨‍💻 Autor

**Eng. Pedro Henrique**  
Serviço de Infraestrutura Predial  
Tribunal de Contas do Estado de Goiás

---

## 📄 Licença

© 2025 - Tribunal de Contas do Estado de Goiás  
Todos os direitos reservados.

---

## 📞 Suporte

Para suporte ou dúvidas sobre o sistema, entre em contato com a equipe de Infraestrutura Predial do TCE-GO.
