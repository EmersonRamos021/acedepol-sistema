# 🧪 Testar Dashboard Localmente

## 🎯 Problema

O dashboard não mostra dados porque:
1. Não tem acesso ao banco de dados
2. Ou não tem o arquivo `database.py`
3. Ou não tem a variável `DATABASE_URL`

## ✅ Solução: Testar Localmente Primeiro

### 1️⃣ Instalar Dependências

```bash
pip install flask psycopg2-binary python-dotenv
```

### 2️⃣ Verificar Arquivos

Certifique-se que tem:
```
✅ app.py
✅ database.py
✅ templates/index.html
✅ .env (com DATABASE_URL)
```

### 3️⃣ Rodar Dashboard Local

```bash
python app.py
```

**Deve aparecer:**
```
✅ Usando banco de dados PostgreSQL
 * Running on http://127.0.0.1:5000
```

### 4️⃣ Testar no Navegador

Abra: http://localhost:5000

**Deve mostrar:**
- Cards com estatísticas
- Lista de usuários (se houver dados)

## 🔍 Debugar Problemas

### Problema 1: "Module not found: database"

**Solução:** Certifique-se que `database.py` está na mesma pasta que `app.py`

```bash
# Verificar
dir  # Windows
ls   # Linux/Mac
```

### Problema 2: "Can't connect to database"

**Solução:** Verifique se `DATABASE_URL` está no `.env`

```bash
# Ver conteúdo do .env
type .env  # Windows
cat .env   # Linux/Mac
```

Deve ter:
```
DATABASE_URL=postgresql://neondb_owner:...
```

### Problema 3: "Nenhum dado aparece"

**Causas possíveis:**
1. Bot não salvou dados ainda
2. Banco está vazio
3. Erro ao carregar dados

**Solução:** Testar se bot salvou dados:

```python
# Testar conexão
python -c "from database import load_data; print(load_data())"
```

**Deve mostrar:**
```python
{'303184113639358464': {'name': 'Emerson', 'records': [...], ...}}
```

Se mostrar `{}`, o banco está vazio!

## 🎯 Testar Fluxo Completo

### 1. Bater Ponto no Discord

1. Use `/painel` no Discord
2. Clique em "Abrir Ponto"
3. Aguarde confirmação

### 2. Verificar no Banco

```python
python -c "from database import load_data; import json; print(json.dumps(load_data(), indent=2))"
```

**Deve mostrar seus dados:**
```json
{
  "303184113639358464": {
    "name": "Emerson",
    "current_session": {
      "entrada": "2025-06-10 12:00:00",
      "canal": "Geral"
    },
    "records": []
  }
}
```

### 3. Ver no Dashboard

Abra: http://localhost:5000

**Deve mostrar:**
- Total de Policiais: 1
- Em Serviço: 1
- Seu nome na lista

## 🚀 Deploy no Vercel

Depois de testar localmente, faça deploy:

### 1️⃣ Criar Repositório no GitHub

```bash
git init
git add app.py database.py templates/ requirements-vercel.txt vercel.json
git commit -m "Dashboard ACEDEPOL"
git remote add origin https://github.com/SEU_USUARIO/acedepol-dashboard.git
git push -u origin main
```

### 2️⃣ Conectar no Vercel

1. Acesse: https://vercel.com
2. Clique em "Add New" → "Project"
3. Conecte GitHub
4. Selecione o repositório
5. Configure:
   - Framework: Other
   - Build Command: (vazio)
   - Output Directory: (vazio)

### 3️⃣ Adicionar Variável de Ambiente

No Vercel:
1. Settings → Environment Variables
2. Adicione:
   - **Name:** `DATABASE_URL`
   - **Value:** `postgresql://neondb_owner:npg_nNvCf4Yz5DKJ@ep-rapid-sea-ack6ct21-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require`

### 4️⃣ Deploy

Clique em "Deploy"

Aguarde alguns minutos...

**URL gerada:**
```
https://seu-projeto.vercel.app
```

## 🔍 Verificar Deploy

### Logs do Vercel

1. Acesse o projeto no Vercel
2. Clique em "Deployments"
3. Clique no último deployment
4. Veja os logs

**Procure por:**
```
✅ Usando banco de dados PostgreSQL
```

### Testar APIs

```bash
# Estatísticas
curl https://seu-projeto.vercel.app/api/stats

# Usuários
curl https://seu-projeto.vercel.app/api/usuarios

# Online
curl https://seu-projeto.vercel.app/api/online
```

## 📋 Checklist de Debug

```
[ ] database.py existe na pasta
[ ] .env tem DATABASE_URL
[ ] pip install psycopg2-binary
[ ] python app.py funciona localmente
[ ] http://localhost:5000 mostra a página
[ ] Bot salvou dados no banco
[ ] python -c "from database import load_data; print(load_data())" mostra dados
[ ] Dashboard local mostra dados
[ ] Repositório criado no GitHub
[ ] Vercel conectado ao GitHub
[ ] DATABASE_URL configurada no Vercel
[ ] Deploy concluído
[ ] URL do Vercel funciona
```

## 🆘 Ainda Não Funciona?

### Opção 1: Testar com Dados Fake

Adicione dados de teste:

```python
# test_data.py
from database import save_data
from datetime import datetime

dados_teste = {
    "123456789": {
        "name": "Teste Policial",
        "current_session": {
            "entrada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "canal": "Patrulha 01"
        },
        "records": [
            {
                "entrada": "2025-06-10 08:00:00",
                "saida": "2025-06-10 17:00:00",
                "canal": "Patrulha 01",
                "duracao": "9:00:00"
            }
        ]
    }
}

save_data(dados_teste)
print("✅ Dados de teste salvos!")
```

Execute:
```bash
python test_data.py
```

Depois teste o dashboard novamente.

### Opção 2: Ver Logs Detalhados

Adicione prints no `app.py`:

```python
def load_data():
    print("🔍 Tentando carregar dados...")
    if USE_DATABASE:
        try:
            data = load_data_db()
            print(f"✅ Dados carregados: {len(data)} usuários")
            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
    return {}
```

## 💡 Dica Final

Se o dashboard local funciona mas o Vercel não:
- Verifique se `database.py` foi commitado
- Verifique se `DATABASE_URL` está no Vercel
- Veja os logs do Vercel para erros

---

**Teste localmente primeiro, depois faça deploy!** 🚀
