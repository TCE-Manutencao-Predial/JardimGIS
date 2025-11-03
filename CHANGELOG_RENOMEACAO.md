# Changelog - Renomeação do Sistema para JardimGIS

**Data:** 02/11/2025  
**Objetivo:** Transformar o sistema de controle de notas fiscais em sistema de controle geográfico de árvores (JardimGIS)

## Arquivos Renomeados

### Arquivo Principal
- `controle_nfs.py` → `jardimgis.py`

### Arquivos de Dados
- `app/dados/controle_nfs.json` → `app/dados/arvores.json`

### Módulos e Rotas
- `app/routes/features/nfs/` → `app/routes/features/arvores/`
- `app/routes/features/arvores/rotas_nfs.py` → `app/routes/features/arvores/rotas_arvores.py`

### Arquivos CSS
- `app/static/css/pages/nfs/` → `app/static/css/pages/arvores/`
- `app/static/css/pages/arvores/controle_nfs.css` → `app/static/css/pages/arvores/controle_arvores.css`

### Arquivos JavaScript
- `app/static/js/pages/nfs/` → `app/static/js/pages/arvores/`
- `app/static/js/pages/arvores/editar_controle_nfs.js` → `app/static/js/pages/arvores/editar_controle_arvores.js`

### Scripts de Sistema
- `scripts/controle_nfs.service` → `scripts/jardimgis.service`

## Alterações em Código

### Variáveis e Constantes
- `CONTROLE_NFS_JSON_PATH` → `ARVORES_JSON_PATH`
- `nfs_data` → `arvores_data`
- `controle_nfs_logger` → `jardimgis_logger`
- `nfs_bp` → `arvores_bp`

### Rotas
- `/controle_nfs` → `/jardimgis`
- `ROUTES_PREFIX = '/controle_nfs'` → `ROUTES_PREFIX = '/jardimgis'`

### Logs e Configurações
- Logger: `'controle_nfs'` → `'jardimgis'`
- Diretório de logs Linux: `/var/softwaresTCE/logs/controle_nfs` → `/var/softwaresTCE/logs/jardimgis`
- Diretório de dados Linux: `/var/softwaresTCE/dados/controle_nfs` → `/var/softwaresTCE/dados/jardimgis`
- Arquivo de log: `controle_nfs.log` → `jardimgis.log`

### Blueprints
- `nfs_bp = Blueprint('nfs', __name__)` → `arvores_bp = Blueprint('arvores', __name__)`

## Arquivos Modificados

1. **app/config.py**
   - Atualizado comentário principal
   - Renomeado `CONTROLE_NFS_JSON_PATH` para `ARVORES_JSON_PATH`
   - Atualizado diretórios de dados e logs
   - Atualizado logger

2. **app/__init__.py**
   - Atualizado comentário principal
   - Atualizado import do blueprint de árvores
   - Alterado `ROUTES_PREFIX` para `/jardimgis`
   - Atualizado rotas de fallback

3. **app/routes/web/web.py**
   - Atualizado comentário principal
   - Alterado variável `nfs_data` para `arvores_data`
   - Atualizado mensagens para mencionar árvores
   - Alterado rotas de `/controle_nfs` para `/jardimgis`
   - Atualizado logger

4. **app/routes/web/admin.py**
   - Atualizado comentário principal
   - Alterado referências de arquivos JSON
   - Atualizado logger

5. **app/routes/features/arvores/rotas_arvores.py**
   - Atualizado comentário principal
   - Renomeado blueprint
   - Atualizado logger

6. **app/utils/data/GerenciadorJSON.py**
   - Atualizado comentário principal
   - Atualizado logger

7. **app/utils/managers/GerenciadorBackupJSON.py**
   - Atualizado logger

8. **app/utils/schedulers/agendador_backups_automatico.py**
   - Atualizado import `CONTROLE_NFS_JSON_PATH` para `ARVORES_JSON_PATH`
   - Alterado descrição da lista de arquivos
   - Atualizado logger

9. **app/routes/web/GerenciadorAutorizacoes.py**
   - Atualizado logger

10. **jardimgis.py** (anteriormente controle_nfs.py)
    - Atualizado comentário principal

## Próximos Passos Recomendados

### Templates HTML
Os arquivos HTML ainda precisam ser atualizados com:
- Referências aos novos caminhos CSS/JS
- Variáveis de template (`nfs_data` → `arvores_data`)
- URLs e rotas atualizadas
- Textos descritivos sobre árvores ao invés de notas fiscais

### Arquivos de Configuração
- `pyproject.toml`: Atualizar `name = "controle_nfs"` para `name = "jardimgis"`
- `makefile`: Atualizar variáveis `APP_NAME` e `SERVICE_NAME`
- `scripts/config.sh`: Atualizar todas as variáveis de configuração

### Scripts de Deploy
- `scripts/deploy.sh`
- `scripts/undeploy.sh`
- `scripts/run.sh`
- Atualizar referências aos caminhos e nomes de serviço

### Documentação
Os arquivos em `app/docs/` ainda referenciam o sistema antigo:
- `DOC_API_EXTERNA_CHECKLIST.md`
- `DOC_API_EXTERNA_NOME_RESPONSAVEIS.md`

## Status

✅ Renomeação de arquivos concluída  
✅ Atualização de imports Python concluída  
✅ Atualização de loggers concluída  
✅ Sem erros de compilação  
⚠️ Templates HTML precisam ser atualizados  
⚠️ Arquivos de configuração precisam ser atualizados  
⚠️ Scripts de deploy precisam ser atualizados  

## Observações

O sistema foi cuidadosamente renomeado mantendo a compatibilidade e estrutura do código. Todos os imports foram atualizados e não há erros de compilação Python. As próximas fases envolvem atualização dos templates HTML e arquivos de configuração para completar a transformação.
