# 📁 Estrutura do Projeto - Sistema ACEDEPOL

## 🗂️ Visão Geral

```
acedepol-sistema/
│
├── 🤖 BOT DISCORD (SquareCloud)
│   ├── bot_ponto_acedepol.py      # Bot principal
│   ├── requirements.txt            # Dependências do bot
│   ├── .env                        # Configurações (não commitar!)
│   └── .env.example               # Exemplo de configuração
│
├── 🌐 DASHBOARD WEB (Vercel)
│   ├── app.py                      # Servidor Flask
│   ├── vercel.json                 # Config Vercel
│   ├── requirements-vercel.txt     # Dependências do site
│   └── templates/
│       └── index.html             # Interface web
│
├── 📚 DOCUMENTAÇÃO
│   ├── README_VERCEL.md           # README principal
│   ├── DEPLOY_VERCEL.md           # Guia completo de deploy
│   ├── GUIA_RAPIDO.md             # Deploy em 5 minutos
│   ├── GUIA_HOSPEDAGEM.md         # Opções de hospedagem
│   ├── RESUMO_COMPLETO.md         # Resumo de tudo
│   ├── COMANDOS_DEPLOY.md         # Comandos prontos
│   └── ESTRUTURA_PROJETO.md       # Este arquivo
│
└── 🔧 CONFIGURAÇÃO
    └── .gitignore                  # Arquivos ignorados
```

## 📦 Arquivos por Função

### 🤖 Bot Discord

```
bot_ponto_acedepol.py (1316 linhas)
├── Configurações
│   ├── BOT_TOKEN
│   ├── ADMIN_IDS
│   └── DATABASE_URL
│
├── Comandos Slash
│   ├── /painel      → Controle de ponto
│   ├── /admin       → Painel administrativo
│   ├── /config      → Configurações
│   └── /reset       → Resetar horários
│
├── Eventos
│   ├── on_ready()              → Inicialização
│   └── on_voice_state_update() → Fechar ponto automático
│
├── Views (Painéis Interativos)
│   ├── PainelPonto      → Abrir/Fechar ponto
│   ├── PainelAdmin      → Relatórios
│   ├── PainelReset      → Reset de dados
│   └── PainelConfig     → Configurações
│
└── Funções Auxiliares
    ├── load_data()              → Carregar dados
    ├── save_data()              → Salvar dados
    ├── is_admin()               → Verificar admin
    ├── has_allowed_role()       → Verificar cargo
    └── enviar_log()             → Enviar logs
```

### 🌐 Dashboard Web

```
app.py (150 linhas)
├── Rotas Web
│   └── /                → Página principal
│
├── APIs REST
│   ├── /api/stats       → Estatísticas gerais
│   ├── /api/usuarios    → Lista de usuários
│   ├── /api/usuario/:id → Detalhes de usuário
│   └── /api/online      → Usuários online
│
└── Funções
    └── load_data()      → Carregar dados do banco

templates/index.html (250 linhas)
├── Header
│   ├── Título
│   └── Subtítulo
│
├── Cards de Estatísticas
│   ├── Total de Policiais
│   ├── Em Serviço
│   ├── Fora de Serviço
│   └── Total de Registros
│
├── Seção: Policiais Online
│   └── Lista em tempo real
│
├── Seção: Ranking de Horas
│   └── Todos os usuários ordenados
│
└── JavaScript
    ├── carregarDados()     → Buscar dados da API
    └── setInterval()       → Atualizar a cada 30s
```

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO COMPLETO                            │
└─────────────────────────────────────────────────────────────┘

1. USUÁRIO BATE PONTO
   Discord → /painel → Abrir Ponto
                ↓
2. BOT PROCESSA
   bot_ponto_acedepol.py
   ├── Verifica permissões
   ├── Valida canal de voz
   └── Salva no banco
                ↓
3. BANCO DE DADOS
   Neon.tech (PostgreSQL)
   ├── Tabela: ponto_data
   └── Formato: JSONB
                ↓
4. DASHBOARD LÊ
   app.py
   ├── load_data()
   └── Retorna JSON via API
                ↓
5. INTERFACE MOSTRA
   index.html
   ├── fetch('/api/stats')
   ├── Atualiza cards
   └── Mostra em tempo real
```

## 🗄️ Estrutura de Dados

### ponto_data.json (ou banco)

```json
{
  "123456789": {
    "name": "João Silva",
    "records": [
      {
        "entrada": "2025-06-10 08:00:00",
        "saida": "2025-06-10 17:00:00",
        "canal": "Patrulha 01",
        "duracao": "9:00:00",
        "manual": false
      }
    ],
    "current_session": {
      "entrada": "2025-06-10 08:00:00",
      "canal": "Patrulha 01"
    }
  }
}
```

### server_config.json

```json
{
  "987654321": {
    "cargos_permitidos": ["Policial", "Delegado"],
    "cargos_admin": ["Delegado", "Supervisor"],
    "canais_permitidos": ["Patrulha 01", "Patrulha 02"],
    "canal_log": "1234567890"
  }
}
```

## 🚀 Deploy por Arquivo

### SquareCloud (Bot)

```
Arquivos necessários:
✅ bot_ponto_acedepol.py
✅ requirements.txt
✅ .env

Configuração:
├── RAM: 512MB (mínimo)
├── CPU: 1 core
└── Disco: 100MB
```

### Vercel (Dashboard)

```
Arquivos necessários:
✅ app.py
✅ vercel.json
✅ requirements-vercel.txt
✅ templates/index.html

Configuração automática:
├── Build: Automático
├── Deploy: Git push
└── HTTPS: Automático
```

### GitHub (Repositório)

```
Arquivos a commitar:
✅ app.py
✅ vercel.json
✅ requirements-vercel.txt
✅ templates/index.html
✅ .gitignore
✅ README_VERCEL.md

Arquivos a NÃO commitar:
❌ .env
❌ ponto_data.json
❌ server_config.json
❌ __pycache__/
```

## 📊 Tamanho dos Arquivos

```
bot_ponto_acedepol.py      ~50 KB
app.py                     ~5 KB
templates/index.html       ~10 KB
requirements.txt           ~1 KB
requirements-vercel.txt    ~1 KB
vercel.json               ~1 KB
.env                      ~1 KB
─────────────────────────────────
TOTAL                     ~69 KB
```

## 🔗 Dependências

### Bot (requirements.txt)

```
discord.py>=2.3.0          # Bot Discord
python-dotenv>=1.0.0       # Variáveis de ambiente
flask>=3.0.0               # Servidor web (opcional)
psycopg2-binary>=2.9.0     # PostgreSQL (se usar)
pymongo>=4.0.0             # MongoDB (se usar)
```

### Dashboard (requirements-vercel.txt)

```
flask>=3.0.0               # Servidor web
psycopg2-binary>=2.9.0     # PostgreSQL (se usar)
pymongo>=4.0.0             # MongoDB (se usar)
```

## 🎯 Checklist de Arquivos

### Antes do Deploy:

```
Bot (SquareCloud):
[ ] bot_ponto_acedepol.py existe
[ ] requirements.txt existe
[ ] .env configurado com BOT_TOKEN
[ ] .env configurado com ADMIN_IDS
[ ] .env configurado com DATABASE_URL (se usar banco)

Dashboard (Vercel):
[ ] app.py existe
[ ] vercel.json existe
[ ] requirements-vercel.txt existe
[ ] templates/index.html existe
[ ] .gitignore configurado

GitHub:
[ ] Repositório criado
[ ] .env NÃO está no repositório
[ ] README_VERCEL.md adicionado
[ ] Arquivos commitados
```

## 🔍 Localização de Recursos

### Onde está cada funcionalidade:

```
Bater Ponto:
├── Comando: bot_ponto_acedepol.py (linha 200)
├── View: PainelPonto (linha 300)
└── Botão: "Abrir Ponto" (linha 320)

Relatórios:
├── Comando: bot_ponto_acedepol.py (linha 600)
├── View: PainelAdmin (linha 700)
└── API: app.py /api/usuarios (linha 50)

Dashboard:
├── HTML: templates/index.html (linha 1)
├── CSS: templates/index.html (linha 10)
└── JS: templates/index.html (linha 200)

Configurações:
├── Cargos: bot_ponto_acedepol.py (linha 900)
├── Canais: bot_ponto_acedepol.py (linha 950)
└── Logs: bot_ponto_acedepol.py (linha 150)
```

## 📝 Notas Importantes

### ⚠️ Segurança:
- **NUNCA** commite `.env`
- **SEMPRE** use `.gitignore`
- **PROTEJA** `BOT_TOKEN` e `DATABASE_URL`

### 🔄 Sincronização:
- Bot e Dashboard devem usar o **mesmo banco**
- Configure `DATABASE_URL` em **ambos**
- Teste a sincronização antes de usar

### 📦 Backups:
- Faça backup de `ponto_data.json` regularmente
- Mantenha cópias de `server_config.json`
- Use controle de versão (Git)

---

**Estrutura organizada para máxima eficiência!** 🚀
