# ⚡ Guia Rápido - Deploy em 5 Minutos

## 🎯 O Que Você Vai Ter

```
┌─────────────────────────────────────────┐
│  Bot Discord (SquareCloud)              │
│  • Comandos /painel, /admin             │
│  • Controle de ponto automático         │
│  • Salva dados em ponto_data.json       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Dashboard Web (Vercel)                 │
│  • https://seu-site.vercel.app          │
│  • Mostra estatísticas em tempo real    │
│  • Ranking de horas trabalhadas         │
└─────────────────────────────────────────┘
```

## 📦 Arquivos Necessários

### Para SquareCloud (Bot):
- ✅ `bot_ponto_acedepol.py`
- ✅ `requirements.txt`
- ✅ `.env` (com BOT_TOKEN)

### Para Vercel (Dashboard):
- ✅ `app.py`
- ✅ `templates/index.html`
- ✅ `vercel.json`
- ✅ `requirements-vercel.txt`

## 🚀 Passo 1: Bot no SquareCloud

```bash
# 1. Crie conta em squarecloud.app
# 2. Faça upload dos arquivos:
bot_ponto_acedepol.py
requirements.txt
.env

# 3. Configure .env:
BOT_TOKEN=seu_token_aqui
ADMIN_IDS=seu_id_discord

# 4. Inicie o bot
```

## 🌐 Passo 2: Dashboard no Vercel

### Opção A: Via GitHub (Recomendado)

```bash
# 1. Criar repositório
git init
git add app.py vercel.json requirements-vercel.txt templates/
git commit -m "Dashboard ACEDEPOL"

# 2. Subir para GitHub
git remote add origin https://github.com/SEU_USUARIO/acedepol.git
git push -u origin main

# 3. No Vercel:
# - Conecte o GitHub
# - Selecione o repositório
# - Deploy automático!
```

### Opção B: Via Vercel CLI

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Seguir instruções
```

## ⚠️ PROBLEMA: Dados Não Aparecem

O bot salva em `ponto_data.json` no SquareCloud, mas o Vercel não tem acesso a esse arquivo!

### 🔧 Solução: Use Banco de Dados

#### Opção 1: Neon.tech (PostgreSQL Grátis)

```bash
# 1. Criar conta em neon.tech
# 2. Criar banco de dados
# 3. Copiar DATABASE_URL

# 4. Adicionar no bot E no dashboard:
pip install psycopg2-binary

# 5. Código (ambos):
import psycopg2
import os
import json

DATABASE_URL = os.getenv("DATABASE_URL")

def save_data(data):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ponto_data (
            id SERIAL PRIMARY KEY,
            data JSONB
        )
    """)
    cur.execute("DELETE FROM ponto_data")
    cur.execute("INSERT INTO ponto_data (data) VALUES (%s)", (json.dumps(data),))
    conn.commit()
    conn.close()

def load_data():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT data FROM ponto_data ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    conn.close()
    return json.loads(result[0]) if result else {}
```

#### Opção 2: MongoDB Atlas (Grátis)

```bash
# 1. Criar conta em mongodb.com/cloud/atlas
# 2. Criar cluster grátis
# 3. Copiar connection string

# 4. Instalar:
pip install pymongo

# 5. Código:
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.acedepol

def save_data(data):
    db.ponto.replace_one({}, data, upsert=True)

def load_data():
    result = db.ponto.find_one()
    return result if result else {}
```

## 🎨 Personalizar Dashboard

Edite `templates/index.html`:

```html
<!-- Linha 18: Mudar cores -->
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

<!-- Linha 67: Mudar título -->
<h1>🚔 Seu Título Aqui</h1>
```

## ✅ Checklist Final

- [ ] Bot rodando no SquareCloud
- [ ] Dashboard no Vercel
- [ ] Banco de dados configurado (Neon ou MongoDB)
- [ ] Variável `DATABASE_URL` no SquareCloud
- [ ] Variável `DATABASE_URL` no Vercel
- [ ] Testar: bater ponto no Discord
- [ ] Verificar: dados aparecem no dashboard

## 🔗 URLs Importantes

- **SquareCloud:** https://squarecloud.app
- **Vercel:** https://vercel.com
- **Neon (PostgreSQL):** https://neon.tech
- **MongoDB Atlas:** https://mongodb.com/cloud/atlas

## 💡 Dica de Ouro

**Use Neon.tech!** É o mais fácil:
1. Criar conta (30 segundos)
2. Criar banco (1 clique)
3. Copiar URL
4. Colar no `.env`
5. Pronto! ✅

## 🆘 Ajuda Rápida

### Bot não inicia
- Verifique `BOT_TOKEN` no `.env`
- Veja logs no SquareCloud

### Dashboard em branco
- Verifique se `DATABASE_URL` está configurado
- Veja logs no Vercel

### Dados não aparecem
- Certifique-se que bot E dashboard usam o mesmo banco
- Teste bater ponto no Discord

---

**Pronto em 5 minutos!** 🚀
