# 📁 Estrutura de Utils - ChecklistsPredial

Este documento descreve a organização dos utilitários e gerenciadores da aplicação.

## 🗂️ Organização

### **utils/managers/** - Gerenciadores de Domínio (9 arquivos)
Classes responsáveis por gerenciar dados e lógica de negócio:

- **GerenciadorBackupDB.py** - Backup de bancos de dados SQLite
- **GerenciadorBackupJSON.py** - Backup de arquivos JSON
- **GerenciadorControleAcesso.py** - Controle de acesso (terminais Hikvision)
- **GerenciadorEmpresasFuncionarios.py** - Gestão de empresas e funcionários
- **GerenciadorGestaoDocumental.py** - Gestão de documentos
- **GerenciadorHistoricoChecklists.py** - Histórico de alterações em checklists
- **GerenciadorJornadasTrabalho.py** - Jornadas de trabalho
- **GerenciadorResponsaveis.py** - Responsáveis por checklists
- **GerenciadorRevisaoArquivos.py** - Revisão de arquivos documentais

### **utils/schedulers/** - Agendadores (2 arquivos)
Tarefas agendadas e schedulers:

- **AgendadorChecklist.py** - Verificação diária de itens vencidos de checklists
- **agendador_relatorios.py** - Agendamento de relatórios por email

### **utils/communication/** - Comunicação (3 arquivos)
Ferramentas de comunicação e geração de relatórios:

- **email_sender.py** - Envio de emails
- **gerador_relatorios_email.py** - Geração de relatórios para envio por email
- **gerador_afd.py** - Geração de arquivos AFD (Hikvision)

### **utils/data/** - Manipulação de Dados (1 arquivo)
Utilitários para manipulação de arquivos de dados:

- **GerenciadorJSON.py** - Load, save e transformações de arquivos JSON

### **utils/templates/** - Filtros de Templates (1 arquivo)
Filtros customizados para Jinja2:

- **template_filters.py** - Filtros enumerate e obter_icone_secao

### **utils/** - Módulos Raiz (1 arquivo)
Módulos utilitários gerais:

- **statistics_processor.py** - Processamento de estatísticas e análise de dados históricos dos checklists

## 📊 Estatísticas
- **Total de arquivos:** 17
- **Categorias:** 6 (managers, schedulers, communication, data, templates, root)
- **Gerenciadores:** 9 classes de gestão de domínio
- **Agendadores:** 2 schedulers automatizados
- **Comunicação:** 3 módulos de comunicação
- **Processadores:** 1 módulo de análise estatística

## 🔗 Imports

### Estrutura de Imports

#### Para arquivos em `routes/api/` ou `routes/web/`:
```python
from ...utils.managers.GerenciadorEmpresasFuncionarios import GerenciadorEmpresasFuncionarios
from ...utils.data.GerenciadorJSON import load_json_file
from ...utils.schedulers.AgendadorChecklist import start_scheduler
from ...utils.communication.email_sender import EmailSender
from ...utils.templates.template_filters import enumerate_filter
```

#### Para arquivos em `routes/features/dominio/`:
```python
from ....utils.managers.GerenciadorHistoricoChecklists import get_history_manager
from ....utils.data.GerenciadorJSON import save_json_file
from ....utils.schedulers.agendador_relatorios import AgendadorRelatorios
```

#### Para arquivos em `app/` (__init__.py, etc):
```python
from .utils.managers.GerenciadorControleAcesso import GerenciadorControleAcesso
from .utils.schedulers.AgendadorChecklist import start_scheduler, stop_scheduler
from .utils.communication.gerador_relatorios_email import GeradorRelatoriosEmail
from .utils.templates.template_filters import enumerate_filter, obter_icone_secao
```

#### Imports entre arquivos utils:
```python
# De managers/ para managers/
from .GerenciadorBackupDB import GerenciadorBackupDB

# De managers/ para data/
from ..data.GerenciadorJSON import load_json_file

# De schedulers/ para managers/
from ..managers.GerenciadorResponsaveis import GerenciadorResponsaveis

# De communication/ para communication/
from ..communication.email_sender import EmailSender

# Imports de config (todos os utils)
from ...config import DATA_DIR, CHECKLISTS_JSON_PATH
```

## 🎯 Principais Gerenciadores

### Gerenciadores de Banco de Dados (SQLite)
- **GerenciadorEmpresasFuncionarios** - Empresas e funcionários
- **GerenciadorJornadasTrabalho** - Jornadas de trabalho
- **GerenciadorGestaoDocumental** - Documentos
- **GerenciadorRevisaoArquivos** - Revisões de arquivos
- **GerenciadorControleAcesso** - Controle de acesso

### Gerenciadores de JSON
- **GerenciadorJSON** - Checklists, periodicidade
- **GerenciadorBackupJSON** - Backups de JSON
- **GerenciadorResponsaveis** - Responsáveis
- **GerenciadorHistoricoChecklists** - Histórico (SQLite + JSON)

## 📝 Manutenção

### Adicionar Novo Gerenciador

1. **Identificar categoria:** managers, schedulers, communication, data ou templates?
2. **Criar arquivo na pasta apropriada**
3. **Configurar imports relativos:**
   - Para módulos na mesma pasta: `from .outro_modulo import ...`
   - Para módulos em outra pasta utils: `from ..outra_pasta.modulo import ...`
   - Para config: `from ...config import ...`
   - Para app root: `from ...ContatosAPI import ...`
4. **Atualizar imports nos arquivos que usarão o gerenciador**
5. **Se necessário, registrar em `__init__.py` da aplicação**

### Mover Arquivo Existente

1. Mover arquivo fisicamente
2. Atualizar imports relativos no arquivo movido:
   - Ajustar níveis de `.` conforme a profundidade
3. Atualizar imports em todos os arquivos que usam este módulo:
   - `app/__init__.py`
   - `routes/**/*.py`
   - `utils/**/*.py` (outros utilitários)
4. Testar aplicação: `python -c "from app import create_app; app = create_app()"`

## 🚀 Benefícios da Estrutura
- ✅ Organização clara por responsabilidade
- ✅ Fácil localização de utilitários
- ✅ Separação de gerenciadores, agendadores e comunicação
- ✅ Escalabilidade para novos módulos
- ✅ Manutenibilidade melhorada
- ✅ Redução de conflitos entre módulos

## ⚠️ Notas Importantes

1. **Imports Relativos:** A profundidade dos `..` varia conforme o nível do arquivo
2. **Gerenciadores Singleton:** Muitos gerenciadores usam pattern Singleton (`.get_instance()`)
3. **Imports Circulares:** Alguns gerenciadores importam outros dentro de funções para evitar ciclos
4. **Config:** Todos os utils importam config de `...config` (3 níveis acima)
5. **Agendadores:** Inicializados em `__init__.py` e gerenciados via atexit

---
**Última atualização:** 2025-10-02  
**Versão:** 1.0  
**Autor:** Sistema ChecklistsPredial
