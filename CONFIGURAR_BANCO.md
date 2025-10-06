# 🗄️ Configurar Banco de Dados - Neon.tech

## ✅ Você Já Criou o Banco!

Pela imagem que você mostrou, você já tem:
- ✅ Banco criado no Neon.tech
- ✅ Nome: `neondb`
- ✅ Região: São Paulo (sa-east-1)
- ✅ Connection string disponível

## 📋 Próximos Passos

### 1️⃣ Copiar a Connection String

Na tela do Neon.tech, você viu a connection string:

```
postgresql://neondb_owner:***************@ep-rapid-sea-ack6ct21-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require
```

**Clique em "Copiar trecho"** para copiar a URL completa (com a senha).

### 2️⃣ Adicionar no Bot (.env)

Abra o arquivo `.env` e adicione a linha:

```bash
DATABASE_URL=postgresql://neondb_owner:SUA_SENHA_AQUI@ep-rapid-sea-ack6ct21-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require
```

**Substitua `SUA_SENHA_AQUI` pela senha real que você copiou!**

### 3️⃣ Testar Localmente

```bash
# Instalar dependência
pip install psycopg2-binary

# Testar conexão
python -c "from database import init_database; init_database()"
```

Se aparecer `✅ Banco de dados inicializado com sucesso!`, está funcionando!

### 4️⃣ Configurar no SquareCloud

1. Acesse o painel do SquareCloud
2. Vá em **Configurações** → **Variáveis de Ambiente**
3. Adicione:
   - **Nome:** `DATABASE_URL`
   - **Valor:** Cole a connection string completa

### 5️⃣ Configurar no Vercel

```bash
# Via CLI
vercel env add DATABASE_URL

# Ou via interface web:
# Settings → Environment Variables → Add
# Nome: DATABASE_URL
# Valor: Cole a connection string
```

## 🔧 Arquivos Criados

Criei 3 arquivos novos para você:

### 1. `database.py`
```
Funções para conectar com PostgreSQL:
- init_database()      → Cria tabelas
- save_data()          → Salva dados
- load_data()          → Carrega dados
- save_server_config() → Salva config
- load_server_config() → Carrega config
```

### 2. `bot_ponto_acedepol.py` (atualizado)
```
Agora usa banco de dados automaticamente:
- Se DATABASE_URL existe → Usa PostgreSQL
- Se não existe → Usa JSON (fallback)
```

### 3. `app.py` (atualizado)
```
Dashboard também usa banco:
- Lê dados do PostgreSQL
- Sincroniza com o bot
```

## ✅ Como Funciona

```
┌─────────────────────────────────────────────────────────┐
│                    FLUXO DE DADOS                        │
└─────────────────────────────────────────────────────────┘

1. Policial bate ponto no Discord
         ↓
2. Bot salva no PostgreSQL (Neon.tech)
         ↓
3. Dashboard lê do PostgreSQL
         ↓
4. Dados aparecem em tempo real!
```

## 🧪 Testar Tudo

### Teste 1: Conexão Local

```bash
python -c "from database import init_database; init_database()"
```

**Esperado:** `✅ Banco de dados inicializado com sucesso!`

### Teste 2: Salvar Dados

```python
from database import save_data, load_data

# Salvar
save_data({"teste": "funcionou"})

# Carregar
dados = load_data()
print(dados)  # {'teste': 'funcionou'}
```

### Teste 3: Bot Completo

```bash
python bot_ponto_acedepol.py
```

**Esperado:**
```
✅ Módulo de banco de dados carregado
🔄 Inicializando banco de dados...
✅ Banco de dados pronto!
Bot está online!
```

## 🔍 Verificar no Neon.tech

1. Acesse: https://console.neon.tech
2. Selecione seu projeto
3. Vá em **SQL Editor**
4. Execute:

```sql
-- Ver tabelas criadas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Ver dados
SELECT * FROM ponto_data;
SELECT * FROM server_config;
```

## ⚠️ Problemas Comuns

### Erro: "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### Erro: "connection refused"

- Verifique se a `DATABASE_URL` está correta
- Confirme que copiou a senha completa
- Teste a conexão no SQL Editor do Neon

### Erro: "SSL required"

Adicione `?sslmode=require` no final da URL:

```
postgresql://...neon.tech/neondb?sslmode=require
```

## 📊 Estrutura do Banco

### Tabela: ponto_data

```sql
CREATE TABLE ponto_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Armazena:** Todos os registros de ponto dos usuários

### Tabela: server_config

```sql
CREATE TABLE server_config (
    id SERIAL PRIMARY KEY,
    config JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Armazena:** Configurações dos servidores (cargos, canais, etc)

## 🎯 Checklist Final

```
[ ] Copiei a connection string do Neon.tech
[ ] Adicionei DATABASE_URL no .env
[ ] Instalei psycopg2-binary
[ ] Testei a conexão localmente
[ ] Configurei no SquareCloud
[ ] Configurei no Vercel
[ ] Testei o bot
[ ] Testei o dashboard
```

## 🚀 Pronto!

Agora seu sistema está usando banco de dados PostgreSQL!

**Vantagens:**
- ✅ Bot e Dashboard sincronizados
- ✅ Dados persistentes
- ✅ Backup automático
- ✅ Escalável
- ✅ Grátis (Neon.tech)

---

**Dúvidas?** Consulte [GUIA_RAPIDO.md](GUIA_RAPIDO.md) ou [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md)
