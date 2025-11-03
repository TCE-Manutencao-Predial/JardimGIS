# 🔌 API de Empresas - ChecklistPredial

**Base URL:** `https://automacao.tce.go.gov.br/checklistpredial/api`  
**Versão:** 2.0  
**Data:** 27/10/2025

---

## 📋 Visão Geral

API REST simplificada para acesso externo aos dados de **empresas cadastradas** no sistema ChecklistPredial. Criada para permitir integração com sistemas externos como o **Controle de NFs**.

### Fontes de Dados Unificadas

A API retorna empresas de **AMBOS** os bancos de dados:
- ✅ **Gestão Documental** (`gestao_documental.db` → tabela `gestao_empresas`)
- ✅ **Banco de Funcionários** (`empresas_funcionarios.db` → tabela `empresas`)

Cada empresa retornada inclui um campo `origem` que identifica de qual banco ela veio.

---

## 🔐 Autenticação

**Headers obrigatórios:**
```http
Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce
Content-Type: application/json
```

Utiliza Bearer Token para autenticação de sistemas externos.

---

## 📡 Endpoints Disponíveis

### 1. Listar Todas as Empresas

**GET** `/api/empresas`

Lista **todas** as empresas de ambos os bancos de dados (sempre unificado).

#### Response 200
```json
{
  "sucesso": true,
  "total": 35,
  "empresas": [
    {
      "id": 1,
      "nome": "Empresa XYZ Ltda",
      "cnpj": "00.000.000/0001-00",
      "email": "contato@xyz.com",
      "origem": "gestao_documental",
      "whatsapp": "62999999999",
      "endereco": "Rua ABC, 123",
      "representante": "João Silva"
    },
    {
      "id": 2,
      "nome": "Empresa ABC Serviços",
      "cnpj": "11.111.111/0001-11",
      "email": "abc@servicos.com",
      "origem": "funcionarios",
      "endereco": "Av. Principal, 456",
      "representante_legal": "Maria Santos",
      "contrato": "Contrato 001/2025"
    }
  ],
  "info": {
    "total_gestao_documental": 15,
    "total_funcionarios": 20
  }
}
```

#### Exemplo cURL
```bash
curl https://automacao.tce.go.gov.br/checklistpredial/api/empresas \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json"
```

---

### 2. Obter Empresa Específica

**GET** `/api/empresas/{origem}/{id}`

Retorna detalhes de uma empresa específica.

#### Path Parameters

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `origem` | string | `gestao_documental` ou `funcionarios` |
| `id` | integer | ID da empresa no banco de origem |

#### Response 200
```json
{
  "sucesso": true,
  "empresa": {
    "id": 1,
    "nome": "Empresa XYZ Ltda",
    "cnpj": "00.000.000/0001-00",
    "email": "contato@xyz.com",
    "origem": "gestao_documental",
    "whatsapp": "62999999999",
    "endereco": "Rua ABC, 123",
    "representante": "João Silva"
  }
}
```

#### Response 404
```json
{
  "sucesso": false,
  "erro": "Empresa ID 999 não encontrada na origem 'gestao_documental'"
}
```

#### Exemplo cURL
```bash
curl https://automacao.tce.go.gov.br/checklistpredial/api/empresas/gestao_documental/1 \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json"
```

---

### 3. Buscar Empresas (Autocomplete)

**GET** `/api/empresas/buscar`

Busca empresas por nome ou CNPJ. **Ideal para autocomplete/typeahead**.

#### Query Parameters

| Parâmetro | Tipo | Descrição | Default |
|-----------|------|-----------|---------|
| `q` | string | Termo de busca (mínimo 2 caracteres) | *obrigatório* |
| `limite` | integer | Máximo de resultados | 20 |

#### Response 200
```json
{
  "sucesso": true,
  "total": 3,
  "termo_busca": "xyz",
  "empresas": [
    {
      "id": 1,
      "nome": "Empresa XYZ Ltda",
      "cnpj": "00.000.000/0001-00",
      "origem": "gestao_documental",
      "email": "contato@xyz.com"
    }
  ]
}
```

#### Response 400
```json
{
  "sucesso": false,
  "erro": "Termo de busca deve ter no mínimo 2 caracteres"
}
```

#### Exemplos cURL
```bash
# Buscar por nome
curl "https://automacao.tce.go.gov.br/checklistpredial/api/empresas/buscar?q=xyz" \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json"

# Buscar por CNPJ
curl "https://automacao.tce.go.gov.br/checklistpredial/api/empresas/buscar?q=00.000" \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json"

# Limitar a 10 resultados
curl "https://automacao.tce.go.gov.br/checklistpredial/api/empresas/buscar?q=empresa&limite=10" \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json"
```

---

## 🐍 Cliente Python

```python
import requests
from typing import Dict, List, Optional

class EmpresasAPI:
    """Cliente Python para API de Empresas do ChecklistPredial"""
    
    def __init__(self, base_url: str, bearer_token: str = "whatsapp_api_token_2025_helpdeskmonitor_tce"):
        """
        Args:
            base_url: URL base (ex: https://automacao.tce.go.gov.br/checklistpredial)
            bearer_token: Token de autenticação Bearer
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }
    
    def listar_empresas(self) -> Dict:
        """
        Lista todas as empresas de ambos os bancos
        
        Returns:
            {
                "sucesso": True,
                "total": 35,
                "empresas": [...],
                "info": {...}
            }
        """
        response = requests.get(
            f"{self.base_url}/api/empresas",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def obter_empresa(self, origem: str, empresa_id: int) -> Optional[Dict]:
        """
        Obtém empresa específica
        
        Args:
            origem: 'gestao_documental' ou 'funcionarios'
            empresa_id: ID da empresa
            
        Returns:
            Dados da empresa ou None se não encontrada
        """
        response = requests.get(
            f"{self.base_url}/api/empresas/{origem}/{empresa_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('empresa')
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
    
    def buscar_empresas(self, termo: str, limite: int = 20) -> Dict:
        """
        Busca empresas por nome ou CNPJ
        
        Args:
            termo: Texto para buscar (mínimo 2 caracteres)
            limite: Máximo de resultados (default: 20)
            
        Returns:
            {
                "sucesso": True,
                "total": 3,
                "termo_busca": "xyz",
                "empresas": [...]
            }
        """
        response = requests.get(
            f"{self.base_url}/api/empresas/buscar",
            params={'q': termo, 'limite': limite},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    # Inicializar cliente
    api = EmpresasAPI(
        base_url='https://automacao.tce.go.gov.br/checklistpredial',
        bearer_token='whatsapp_api_token_2025_helpdeskmonitor_tce'
    )
    
    # 1. Listar todas as empresas
    empresas = api.listar_empresas()
    print(f"Total de empresas: {empresas['total']}")
    print(f"- Gestão Documental: {empresas['info']['total_gestao_documental']}")
    print(f"- Funcionários: {empresas['info']['total_funcionarios']}")
    
    # 2. Buscar empresas
    resultados = api.buscar_empresas('xyz')
    print(f"\nBusca por 'xyz': {resultados['total']} empresas encontradas")
    for empresa in resultados['empresas']:
        print(f"- {empresa['nome']} ({empresa['origem']})")
    
    # 3. Obter empresa específica
    empresa = api.obter_empresa('gestao_documental', 1)
    if empresa:
        print(f"\nEmpresa ID 1: {empresa['nome']}")
    else:
        print("\nEmpresa não encontrada")
```

---

## 💡 Casos de Uso - Controle de NFs

### 1. Autocomplete de Empresas

**JavaScript/Frontend:**

```javascript
// Autocomplete com debounce para evitar muitas requisições
let timeoutId;

async function autocompletarEmpresas(termo) {
    clearTimeout(timeoutId);
    
    // Aguarda 300ms antes de fazer a requisição
    timeoutId = setTimeout(async () => {
        if (termo.length < 2) return;
        
        try {
            const response = await fetch(
                `https://automacao.tce.go.gov.br/checklistpredial/api/empresas/buscar?q=${termo}&limite=10`,
                {
                    headers: {
                        'Authorization': 'Bearer whatsapp_api_token_2025_helpdeskmonitor_tce',
                        'Content-Type': 'application/json'
                    }
                }
            );
            
            const data = await response.json();
            
            if (data.sucesso) {
                // Popular lista de sugestões
                const sugestoes = data.empresas.map(e => ({
                    value: e.nome,
                    label: `${e.nome} - ${e.cnpj} [${e.origem === 'gestao_documental' ? 'GD' : 'Func'}]`,
                    data: e
                }));
                
                // Mostrar sugestões no DOM
                exibirSugestoes(sugestoes);
            }
        } catch (error) {
            console.error('Erro ao buscar empresas:', error);
        }
    }, 300);
}

// Usar no input
document.getElementById('empresa-input').addEventListener('input', (e) => {
    autocompletarEmpresas(e.target.value);
});
```

### 2. Popular Select de Empresas

**Python/Backend:**

```python
def obter_empresas_para_select():
    """
    Obtém lista de empresas formatada para popular um <select>
    
    Returns:
        Lista de tuplas (nome, label_formatado)
    """
    api = EmpresasAPI(
        'https://automacao.tce.go.gov.br/checklistpredial',
        'whatsapp_api_token_2025_helpdeskmonitor_tce'
    )
    
    try:
        empresas = api.listar_empresas()
        
        options = []
        for empresa in empresas['empresas']:
            # Label com origem visual
            origem_label = '🏢 GD' if empresa['origem'] == 'gestao_documental' else '👥 Func'
            label = f"{empresa['nome']} [{origem_label}]"
            
            options.append((empresa['nome'], label))
        
        # Ordenar alfabeticamente
        options.sort(key=lambda x: x[0])
        
        return options
        
    except Exception as e:
        print(f"Erro ao obter empresas: {e}")
        return []


# Usar em template Flask/Jinja2
@app.route('/nfs/novo')
def nova_nf():
    empresas_opcoes = obter_empresas_para_select()
    return render_template('nova_nf.html', empresas=empresas_opcoes)
```

### 3. Validar Empresa Antes de Salvar

**Python:**

```python
def validar_empresa_existe(nome_empresa: str) -> tuple[bool, Optional[Dict]]:
    """
    Verifica se empresa existe no sistema principal antes de salvar NF
    
    Args:
        nome_empresa: Nome da empresa a validar
        
    Returns:
        (existe, dados_empresa)
    """
    api = EmpresasAPI(
        'https://automacao.tce.go.gov.br/checklistpredial',
        'whatsapp_api_token_2025_helpdeskmonitor_tce'
    )
    
    try:
        # Busca exata por nome
        resultado = api.buscar_empresas(nome_empresa, limite=1)
        
        if resultado['total'] > 0:
            empresa = resultado['empresas'][0]
            
            # Verifica se o nome é exato (não apenas contém)
            if empresa['nome'].lower() == nome_empresa.lower():
                return True, empresa
        
        return False, None
        
    except Exception as e:
        print(f"Erro ao validar empresa: {e}")
        return False, None


# Usar ao salvar NF
def salvar_nota_fiscal(dados_nf):
    empresa = dados_nf['empresa']
    
    # Validar se empresa existe
    existe, empresa_dados = validar_empresa_existe(empresa)
    
    if not existe:
        raise ValueError(f"Empresa '{empresa}' não encontrada no sistema principal")
    
    # Adicionar dados extras da empresa na NF (opcional)
    dados_nf['empresa_cnpj'] = empresa_dados.get('cnpj', '')
    dados_nf['empresa_origem'] = empresa_dados.get('origem', '')
    
    # Salvar NF...
    save_json_file(CONTROLE_NFS_JSON_PATH, dados_nf)
```

### 4. Cache Local para Performance

**Python:**

```python
from datetime import datetime, timedelta
import json

class EmpresasAPIComCache:
    """Cliente com cache local para reduzir requisições"""
    
    def __init__(self, base_url: str, bearer_token: str, cache_duration_minutes: int = 30):
        self.api = EmpresasAPI(base_url, bearer_token)
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
    
    def listar_empresas(self) -> Dict:
        """Lista empresas com cache"""
        cache_key = 'listar_empresas'
        
        # Verificar cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                print("🔄 Retornando do cache")
                return cached_data
        
        # Cache expirado ou inexistente - buscar da API
        print("🌐 Buscando da API")
        data = self.api.listar_empresas()
        
        # Atualizar cache
        self.cache[cache_key] = (data, datetime.now())
        
        return data
    
    def limpar_cache(self):
        """Limpa o cache manualmente"""
        self.cache = {}
        print("🗑️ Cache limpo")


# Uso
api_cached = EmpresasAPIComCache(
    'https://automacao.tce.go.gov.br/checklistpredial',
    'whatsapp_api_token_2025_helpdeskmonitor_tce',
    cache_duration_minutes=30
)

# Primeira chamada busca da API
empresas = api_cached.listar_empresas()

# Chamadas seguintes usam cache (por 30 minutos)
empresas = api_cached.listar_empresas()
```

---

## ⚠️ Códigos de Erro

| Código | Descrição | Solução |
|--------|-----------|---------|
| 200 | ✅ Sucesso | - |
| 400 | ❌ Requisição inválida | Verificar parâmetros obrigatórios |
| 401 | ❌ Não autenticado | Adicionar header `Authorization: Bearer <token>` |
| 403 | ❌ Token inválido | Verificar se o Bearer token está correto |
| 404 | ❌ Empresa não encontrada | Verificar ID e origem |
| 500 | ❌ Erro interno do servidor | Verificar logs do servidor |

### Formato de Erro Padrão

```json
{
  "sucesso": false,
  "erro": "Descrição detalhada do erro"
}
```

---

## 📝 Campos Retornados por Origem

### Gestão Documental

Campos principais da tabela `gestao_empresas`:

```json
{
  "id": 1,
  "nome": "Empresa XYZ Ltda",
  "cnpj": "00.000.000/0001-00",
  "email": "contato@xyz.com",
  "whatsapp": "62999999999",
  "endereco": "Rua ABC, 123",
  "representante": "João Silva",
  "origem": "gestao_documental"
}
```

### Banco de Funcionários

Campos principais da tabela `empresas`:

```json
{
  "id": 2,
  "nome": "Empresa ABC Serviços",
  "cnpj": "11.111.111/0001-11",
  "email": "abc@servicos.com",
  "endereco": "Av. Principal, 456",
  "representante_legal": "Maria Santos",
  "proprietario": "Carlos Silva",
  "telefone_proprietario": "62988888888",
  "contrato": "Contrato 001/2025",
  "origem": "funcionarios"
}
```

**Nota:** O campo `origem` sempre identifica a fonte dos dados.

---

## 🧪 Testando a API

### Teste Rápido - cURL

```bash
# 1. Listar todas as empresas
curl https://automacao.tce.go.gov.br/checklistpredial/api/empresas \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json" | jq

# 2. Buscar empresas
curl "https://automacao.tce.go.gov.br/checklistpredial/api/empresas/buscar?q=empresa" \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json" | jq

# 3. Obter empresa específica
curl https://automacao.tce.go.gov.br/checklistpredial/api/empresas/gestao_documental/1 \
  -H "Authorization: Bearer whatsapp_api_token_2025_helpdeskmonitor_tce" \
  -H "Content-Type: application/json" | jq
```

**Dica:** Use `| jq` para formatar o JSON de forma legível.

### Script de Teste - Python

```python
# teste_api_empresas.py
import requests
import json

BASE_URL = 'https://automacao.tce.go.gov.br/checklistpredial/api'
HEADERS = {
    'Authorization': 'Bearer whatsapp_api_token_2025_helpdeskmonitor_tce',
    'Content-Type': 'application/json'
}

def testar_api():
    print("=" * 60)
    print("TESTANDO API DE EMPRESAS")
    print("=" * 60)
    
    # Teste 1: Listar todas
    print("\n1️⃣ TESTE: Listar todas as empresas")
    response = requests.get(f'{BASE_URL}/empresas', headers=HEADERS)
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"✅ Total: {data['total']} empresas")
        print(f"   - Gestão Documental: {data['info']['total_gestao_documental']}")
        print(f"   - Funcionários: {data['info']['total_funcionarios']}")
    
    # Teste 2: Buscar
    print("\n2️⃣ TESTE: Buscar empresas")
    response = requests.get(
        f'{BASE_URL}/empresas/buscar',
        params={'q': 'empresa', 'limite': 5},
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"✅ Encontradas: {data['total']} empresas")
        for empresa in data['empresas'][:3]:
            print(f"   - {empresa['nome']} ({empresa['origem']})")
    
    # Teste 3: Empresa específica
    print("\n3️⃣ TESTE: Obter empresa específica")
    response = requests.get(
        f'{BASE_URL}/empresas/gestao_documental/1',
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        empresa = data['empresa']
        print(f"✅ Empresa: {empresa['nome']}")
        print(f"   CNPJ: {empresa.get('cnpj', 'N/A')}")
        print(f"   Origem: {empresa['origem']}")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 60)

if __name__ == "__main__":
    testar_api()
```

---

## 📊 Informações de Migração de Dados

### Base de Dados NFs - Localização

Para migração do Controle de NFs separado:

**Arquivo:** `controle_nfs.json`

**Produção (Linux):**
```
/var/softwaresTCE/dados/checklistspredial/dados/controle_nfs.json
```

**Desenvolvimento (Windows):**
```
c:\Users\Pedro\Repositórios\checklistpredial\checklistpredial\app\dados\controle_nfs.json
```

**Formato:**
```json
{
  "Controle de NFs": [
    {
      "id": "uuid-único",
      "empresa": "Nome da Empresa",
      "numero_nf": "12345",
      "valor": "R$ 1.500,00",
      "data_emissao": "2025-10-15",
      "status": "Pendente",
      "responsavel": "pedro",
      ...
    }
  ]
}
```

---

## 📞 Suporte

- **Logs do servidor:** `/var/softwaresTCE/logs/checklistpredial/checklist.log`
- **Arquivo da API:** `app/routes/api/api_empresas.py`
- **Contato:** Pedro Henrique

---

## ✅ Checklist de Integração - Controle de NFs

Ao separar o Controle de NFs, integrar com esta API:

- [x] API de empresas criada
- [ ] Implementar autocomplete de empresas no frontend
- [ ] Validar empresa antes de salvar NF
- [ ] Popular select de empresas ao carregar página
- [ ] Adicionar loading/spinner durante busca
- [ ] Tratar erros de conexão com mensagens amigáveis
- [ ] Implementar cache local (opcional)
- [ ] Testar em ambiente de desenvolvimento
- [ ] Testar em produção

---

## 🔄 Futuras Melhorias

Planejadas para próximas versões:

- [ ] Unificar bancos de empresas em um único banco
- [ ] Adicionar endpoint para criar/editar empresas via API
- [ ] Implementar paginação na listagem
- [ ] Adicionar filtros avançados (por CNPJ, cidade, etc.)
- [ ] Adicionar rate limiting
- [ ] Adicionar API keys em vez de htpasswd

---

**Versão:** 2.0  
**Última atualização:** 27/10/2025  
**Criado por:** Pedro Henrique
