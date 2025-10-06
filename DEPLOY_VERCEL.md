# 🚀 Deploy no Vercel - Dashboard ACEDEPOL

## 📋 Arquitetura do Sistema

```
┌─────────────────┐         ┌─────────────────┐
│   SquareCloud   │         │     Vercel      │
│                 │         │                 │
│  🤖 Discord Bot │◄────────┤  🌐 Dashboard   │
│  (24/7 Online)  │  Lê     │  (Website)      │
│                 │  Dados  │                 │
│  ponto_data.json│─────────►│  app.py         │
└─────────────────┘         └─────────────────┘
```

## ✅ Arquivos Criados

### Para o Vercel (Dashboard):
- ✅ `app.py` - Servidor Flask serverless
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements-vercel.txt` - Dependências do site
- ✅ `templates/index.html` - Interface do dashboard

### Para o SquareCloud (Bot):
- ✅ `bot_ponto_acedepol.py` - Bot Discord
- ✅ `requirements.txt` - Dependências do bot
- ✅ `.env` - Variáveis de ambiente

## 🎯 Passo a Passo - Deploy no Vercel

### 1️⃣ Preparar o Repositório GitHub

```bash
# Criar repositório no GitHub
git init
git add .
git commit -m "Dashboard ACEDEPOL"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/acedepol-dashboard.git
git push -u origin main
```

### 2️⃣ Deploy no Vercel

1. Acesse: https://vercel.com
2. Clique em **"Add New Project"**
3. Conecte seu GitHub
4. Selecione o repositório `acedepol-dashboard`
5. Configure:
   - **Framework Preset:** Other
   - **Build Command:** (deixe vazio)
   - **Output Directory:** (deixe vazio)
   - **Install Command:** `pip install -r requirements-vercel.txt`

6. Clique em **"Deploy"**

### 3️⃣ Resultado

Você receberá uma URL automática:
```
https://acedepol-dashboard.vercel.app
```

## 🔄 Como Funciona a Sincronização

### Bot (SquareCloud):
```python
# Salva dados quando alguém bate ponto
save_data(data)  # Salva em ponto_data.json
```

### Dashboard (Vercel):
```python
# Lê os mesmos dados
data = load_data()  # Lê ponto_data.json
```

## ⚠️ IMPORTANTE: Compartilhar Dados

Para o dashboard mostrar os dados do bot, você precisa:

### Opção 1: Usar Banco de Dados (Recomendado)

**Instalar no Bot e no Dashboard:**
```bash
pip install psycopg2-binary
```

**Código para ambos:**
```python
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def save_data(data):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Salvar no banco
    conn.commit()
    conn.close()
```

**Banco de Dados Grátis:**
- Neon.tech (PostgreSQL grátis)
- Supabase (PostgreSQL grátis)
- MongoDB Atlas (MongoDB grátis)

### Opção 2: API do Bot

**No Bot (SquareCloud):**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/dados')
def get_dados():
    data = load_data()
    return jsonify(data)

# Rodar Flask junto com o bot
```

**No Dashboard (Vercel):**
```python
import requests

def load_data():
    response = requests.get('https://seu-bot.squarecloud.app/api/dados')
    return response.json()
```

## 🎨 Personalizar o Dashboard

Edite `templates/index.html`:

```html
<!-- Mudar cores -->
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>

<!-- Mudar título -->
<h1>🚔 Seu Título Aqui</h1>
```

## 📊 APIs Disponíveis

O dashboard expõe estas APIs:

```
GET /api/stats
Retorna: estatísticas gerais

GET /api/usuarios
Retorna: lista de todos os usuários

GET /api/usuario/<id>
Retorna: detalhes de um usuário

GET /api/online
Retorna: usuários online agora
```

## 🔧 Comandos Úteis

```bash
# Testar localmente
python app.py

# Atualizar no Vercel
git add .
git commit -m "Atualização"
git push

# Ver logs no Vercel
vercel logs
```

## 💡 Dicas

1. **Domínio Personalizado:**
   - No Vercel: Settings → Domains
   - Adicione: `acedepol.com.br`

2. **Atualização Automática:**
   - Cada push no GitHub atualiza o site automaticamente

3. **HTTPS Grátis:**
   - Vercel fornece HTTPS automático

4. **Variáveis de Ambiente:**
   - No Vercel: Settings → Environment Variables
   - Adicione `DATABASE_URL` se usar banco

## 🆘 Problemas Comuns

### Erro: "ponto_data.json não encontrado"
**Solução:** Use banco de dados compartilhado

### Erro: "Module not found"
**Solução:** Adicione no `requirements-vercel.txt`

### Dashboard não atualiza
**Solução:** Verifique se o bot está salvando os dados

## 📞 Suporte

- Vercel Docs: https://vercel.com/docs
- Discord.py Docs: https://discordpy.readthedocs.io

---

**Pronto!** Agora você tem:
- ✅ Bot no SquareCloud
- ✅ Dashboard no Vercel
- ✅ URLs automáticas
- ✅ HTTPS grátis
- ✅ Deploy automático
