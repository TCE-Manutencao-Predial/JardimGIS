# 📁 Estrutura de Routes - ChecklistsPredial

Este documento descreve a organização dos arquivos de rotas (blueprints) da aplicação.

## 🗂️ Organização

### **routes/api/** - APIs REST (6 arquivos)
Endpoints de API para consumo via AJAX/fetch:

- **api_checklists.py** - API para gerenciamento de checklists
- **api_controle_acesso.py** - API para controle de acesso (terminais Hikvision)
- **api_detalhes_funcionario.py** - API para detalhes de funcionários
- **api_gerenciar_terminal.py** - API para gerenciamento de terminais
- **api_jornadas_trabalho.py** - API para jornadas de trabalho
- **api_relatorios_email.py** - API para relatórios por email

### **routes/web/** - Páginas Web e Admin (3 arquivos)
Rotas para renderização de páginas HTML:

- **web.py** - Rotas principais da aplicação (índice, páginas base)
- **admin.py** - Painel administrativo (backups, histórico, configurações)
- **GerenciadorAutorizacoes.py** - Decorador de autorização especial

### **routes/features/** - Funcionalidades por Domínio (6 arquivos em 5 subpastas)

#### **features/checklists/** (1 arquivo)
- **rotas_checklists.py** - Sistema de checklists prediais

#### **features/funcionarios/** (1 arquivo)
- **rotas_controle_func_empresas.py** - Gestão de funcionários e empresas

#### **features/gestao_documental/** (2 arquivos)
- **rotas_gestao_documental.py** - Gestão de documentos
- **rotas_revisao_arquivos.py** - Revisão de arquivos documentais

#### **features/jornadas/** (1 arquivo)
- **rotas_jornadas_trabalho.py** - Gerenciamento de jornadas de trabalho

#### **features/nfs/** (1 arquivo)
- **rotas_nfs.py** - Controle de notas fiscais

### **Arquivos de Teste** - ✅ Reorganizados  
Scripts de teste para integração Hikvision foram movidos para `testes/controle_acesso_hikvision/` para melhor organização.

## 📊 Estatísticas
- **Total de arquivos routes:** 15 (reorganizados)
- **Total de blueprints:** 14
- **Categorias:** 3 (api, web, features)
- **Subpastas features:** 5

## 🔗 Imports

### Estrutura de Imports

#### Para arquivos em `routes/api/`:
```python
from ...config import ...              # 3 níveis até app/
from ...utils.Gerenciador import ...   # 3 níveis até app/utils/
from ..web.GerenciadorAutorizacoes import ...  # 2 níveis até routes/web/
```

#### Para arquivos em `routes/web/`:
```python
from ...config import ...              # 3 níveis até app/
from ...utils.Gerenciador import ...   # 3 níveis até app/utils/
from .GerenciadorAutorizacoes import ...  # Mesmo diretório
```

#### Para arquivos em `routes/features/dominio/`:
```python
from ....config import ...             # 4 níveis até app/
from ....utils.Gerenciador import ...  # 4 níveis até app/utils/
from ...web.GerenciadorAutorizacoes import ...  # 3 níveis até routes/web/
```

### Registro de Blueprints em `__init__.py`

```python
# APIs
from .routes.api.api_checklists import api_bp
from .routes.api.api_controle_acesso import controle_acesso_api_bp
# ...

# Web
from .routes.web.admin import admin_bp
from .routes.web.web import web_bp

# Features
from .routes.features.checklists.rotas_checklists import checklists_bp
from .routes.features.funcionarios.rotas_controle_func_empresas import funcionarios_empresas_bp
# ...
```

## 🎯 Blueprints Registrados

| Blueprint | Caminho | URL Prefix |
|-----------|---------|------------|
| `api` | api/api_checklists.py | /controle_nfs/api |
| `admin` | web/admin.py | /controle_nfs/admin |
| `web` | web/web.py | /controle_nfs/ |
| `revisao_arquivos` | features/gestao_documental/ | /controle_nfs/gestao |
| `gerenciar_terminal_api` | api/ | /controle_nfs/api/gerenciar-terminal |
| `checklists` | features/checklists/ | /controle_nfs/ |
| `funcionarios_empresas` | features/funcionarios/ | /controle_nfs/ |
| `nfs` | features/nfs/ | /controle_nfs/ |
| `gestao_documental` | features/gestao_documental/ | /controle_nfs/ |
| `controle_acesso_api` | api/ | /controle_nfs/api/controle-acesso |
| `detalhes_funcionario_api` | api/ | /controle_nfs/api/detalhes-funcionario |
| `relatorios_email_api` | api/ | /controle_nfs/api/relatorios-email |
| `api_jornadas` | api/ | /controle_nfs/ |
| `jornadas` | features/jornadas/ | /controle_nfs/ |

## 📝 Manutenção

### Adicionar Nova Rota

1. **Identificar categoria:** API, Web ou Feature?
2. **Se Feature, identificar domínio:** checklists, funcionários, gestão documental, jornadas, nfs ou criar novo
3. **Criar arquivo no diretório apropriado**
4. **Configurar imports relativos corretamente** (ver exemplos acima)
5. **Registrar blueprint em `app/__init__.py`**

### Mover Arquivo Existente

1. Mover arquivo fisicamente
2. Atualizar imports relativos no arquivo movido
3. Atualizar import do blueprint em `__init__.py`
4. Verificar se outros arquivos importam algo deste arquivo
5. Testar aplicação: `python -c "from app import create_app; app = create_app()"`

## 🚀 Benefícios da Estrutura
- ✅ Organização clara por tipo e domínio
- ✅ Fácil localização de rotas
- ✅ Separação APIs vs. Web vs. Features
- ✅ Escalabilidade para novos módulos
- ✅ Manutenibilidade melhorada
- ✅ Redução de conflitos entre rotas

## ⚠️ Notas Importantes

1. **Imports Relativos:** A profundidade dos `..` varia conforme o nível do arquivo
2. **GerenciadorAutorizacoes:** Está em `routes/web/` e é usado por vários módulos
3. **Scripts de Teste:** Movidos para `testes/controle_acesso_hikvision/` (outubro/2025)
4. **__init__.py:** Cada subpasta tem um `__init__.py` para ser um pacote Python válido

---
**Última atualização:** 2025-10-05  
**Versão:** 1.1 - Scripts de teste reorganizados  
**Autor:** Sistema ChecklistsPredial
