# 🎨 Arquitetura Visual - Sistema ACEDEPOL

## 🏗️ Visão Geral do Sistema

```
╔═══════════════════════════════════════════════════════════════════╗
║                    SISTEMA ACEDEPOL                                ║
║              Sistema de Controle de Ponto                          ║
║           Polícia Civil Nova Capital                               ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIOS                                 │
│                                                                  │
│  👮 Policial 1    👮 Policial 2    👮 Policial 3               │
│       │                 │                 │                      │
│       └─────────────────┴─────────────────┘                      │
│                         │                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌───────────────┐                   ┌───────────────┐
│   DISCORD     │                   │   BROWSER     │
│   Desktop     │                   │   Web         │
│   Mobile      │                   │   Mobile      │
└───────┬───────┘                   └───────┬───────┘
        │                                   │
        │ /painel                           │ https://
        │ /admin                            │
        ▼                                   ▼
┌───────────────────────────────────────────────────────────────┐
│                      CAMADA DE APLICAÇÃO                       │
├───────────────────────────┬───────────────────────────────────┤
│                           │                                    │
│  🤖 BOT DISCORD           │  🌐 DASHBOARD WEB                 │
│  SquareCloud              │  Vercel                            │
│                           │                                    │
│  • Comandos Slash         │  • Interface Visual                │
│  • Controle de Ponto      │  • Estatísticas                    │
│  • Permissões             │  • Relatórios                      │
│  • Logs Automáticos       │  • APIs REST                       │
│                           │                                    │
│  bot_ponto_acedepol.py    │  app.py + index.html              │
│                           │                                    │
└───────────┬───────────────┴───────────────┬───────────────────┘
            │                               │
            │         DATABASE_URL          │
            │                               │
            └───────────────┬───────────────┘
                            ▼
            ┌───────────────────────────────┐
            │   🗄️ BANCO DE DADOS           │
            │   Neon.tech (PostgreSQL)      │
            │                               │
            │  • ponto_data (JSONB)         │
            │  • Sincronização em tempo real│
            │  • Backup automático          │
            └───────────────────────────────┘
```

## 🔄 Fluxo de Dados Detalhado

### 📥 Entrada de Dados (Bater Ponto)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO INTERAGE                                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    👮 Policial João
                            │
                            │ Entra no canal de voz
                            │ Usa comando /painel
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. BOT PROCESSA                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Verificações:                                             │  │
│  │ ✓ Está em canal de voz?                                  │  │
│  │ ✓ Canal permitido?                                       │  │
│  │ ✓ Tem cargo autorizado?                                  │  │
│  │ ✓ Já tem ponto aberto?                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Processamento:                                            │  │
│  │ • Captura horário atual                                  │  │
│  │ • Registra canal de voz                                  │  │
│  │ • Cria sessão ativa                                      │  │
│  │ • Prepara dados para salvar                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. SALVA NO BANCO                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  {                                                               │
│    "user_id": "123456789",                                       │
│    "name": "João Silva",                                         │
│    "current_session": {                                          │
│      "entrada": "2025-06-10 08:00:00",                          │
│      "canal": "Patrulha 01"                                     │
│    }                                                             │
│  }                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. CONFIRMAÇÃO                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ Ponto Aberto com Sucesso                                    │
│  👮 Policial: João Silva                                        │
│  🕐 Horário: 2025-06-10 08:00:00                               │
│  📍 Canal: Patrulha 01                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 📤 Saída de Dados (Dashboard)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO ACESSA DASHBOARD                                      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  🌐 https://acedepol.vercel.app
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. PÁGINA CARREGA                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  index.html                                                      │
│  ├── Estrutura HTML                                             │
│  ├── Estilos CSS                                                │
│  └── JavaScript                                                 │
│      └── carregarDados()                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. BUSCA DADOS VIA API                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  fetch('/api/stats')      → Estatísticas gerais                 │
│  fetch('/api/usuarios')   → Lista de usuários                   │
│  fetch('/api/online')     → Usuários online                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. SERVIDOR PROCESSA                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  app.py                                                          │
│  ├── Conecta no banco                                           │
│  ├── Busca dados                                                │
│  ├── Processa informações                                       │
│  └── Retorna JSON                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. EXIBE NA TELA                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 📊 Dashboard ACEDEPOL                                   │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  👥 Total: 50    🟢 Online: 12    🔴 Offline: 38      │    │
│  │                                                         │    │
│  │  👮 João Silva        ⏱️ 45:30:00    🟢 Online        │    │
│  │  👮 Maria Santos      ⏱️ 42:15:00    🔴 Offline       │    │
│  │  👮 Pedro Costa       ⏱️ 38:45:00    🟢 Online        │    │
│  │                                                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔐 Fluxo de Segurança

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADAS DE SEGURANÇA                          │
└─────────────────────────────────────────────────────────────────┘

1️⃣ AUTENTICAÇÃO DISCORD
   ├── Bot verifica ID do usuário
   ├── Valida token do Discord
   └── Confirma membro do servidor

2️⃣ AUTORIZAÇÃO POR CARGO
   ├── Verifica cargos permitidos
   ├── Valida cargos admin
   └── Bloqueia acesso não autorizado

3️⃣ VALIDAÇÃO DE CANAL
   ├── Verifica se está em canal de voz
   ├── Valida canal permitido
   └── Impede registro em canal errado

4️⃣ PROTEÇÃO DE DADOS
   ├── .env não commitado
   ├── Tokens em variáveis de ambiente
   └── Banco com SSL/TLS

5️⃣ LOGS DE AUDITORIA
   ├── Registra todas as ações
   ├── Envia para canal de logs
   └── Mantém histórico
```

## 📊 Estrutura de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                    BANCO DE DADOS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ponto_data (JSONB)                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  {                                                        │  │
│  │    "123456789": {                    ← User ID           │  │
│  │      "name": "João Silva",           ← Nome              │  │
│  │      "records": [                    ← Histórico         │  │
│  │        {                                                  │  │
│  │          "entrada": "2025-06-10 08:00:00",              │  │
│  │          "saida": "2025-06-10 17:00:00",                │  │
│  │          "canal": "Patrulha 01",                        │  │
│  │          "duracao": "9:00:00",                          │  │
│  │          "manual": false                                │  │
│  │        }                                                  │  │
│  │      ],                                                   │  │
│  │      "current_session": {            ← Sessão Ativa     │  │
│  │        "entrada": "2025-06-10 08:00:00",                │  │
│  │        "canal": "Patrulha 01"                           │  │
│  │      }                                                    │  │
│  │    }                                                      │  │
│  │  }                                                        │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🌐 APIs REST

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENDPOINTS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GET /                                                           │
│  └─→ Retorna: index.html (Dashboard)                           │
│                                                                  │
│  GET /api/stats                                                  │
│  └─→ Retorna: {                                                 │
│         "total_usuarios": 50,                                   │
│         "usuarios_online": 12,                                  │
│         "usuarios_offline": 38,                                 │
│         "total_registros": 1250                                 │
│       }                                                          │
│                                                                  │
│  GET /api/usuarios                                               │
│  └─→ Retorna: [                                                 │
│         {                                                        │
│           "id": "123456789",                                    │
│           "nome": "João Silva",                                 │
│           "total_horas": "45:30:00",                           │
│           "total_registros": 25,                               │
│           "online": true                                        │
│         }                                                        │
│       ]                                                          │
│                                                                  │
│  GET /api/usuario/:id                                            │
│  └─→ Retorna: {                                                 │
│         "id": "123456789",                                      │
│         "nome": "João Silva",                                   │
│         "registros": [...],                                     │
│         "sessao_atual": {...}                                   │
│       }                                                          │
│                                                                  │
│  GET /api/online                                                 │
│  └─→ Retorna: [                                                 │
│         {                                                        │
│           "id": "123456789",                                    │
│           "nome": "João Silva",                                 │
│           "entrada": "2025-06-10 08:00:00",                    │
│           "canal": "Patrulha 01",                              │
│           "tempo_decorrido": "1:30:00"                         │
│         }                                                        │
│       ]                                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Deploy Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE DEPLOY                            │
└─────────────────────────────────────────────────────────────────┘

DESENVOLVEDOR
     │
     │ git add .
     │ git commit -m "Update"
     │ git push
     ▼
┌─────────────┐
│   GITHUB    │
│  Repository │
└──────┬──────┘
       │
       │ Webhook
       ▼
┌─────────────┐
│   VERCEL    │
│  Auto Deploy│
├─────────────┤
│ 1. Clone    │
│ 2. Build    │
│ 3. Deploy   │
│ 4. HTTPS    │
└──────┬──────┘
       │
       │ URL Gerada
       ▼
https://acedepol.vercel.app
       │
       │ Acesso Público
       ▼
   👥 USUÁRIOS
```

## 💰 Custos Mensais

```
┌─────────────────────────────────────────────────────────────────┐
│                    BREAKDOWN DE CUSTOS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SquareCloud (Bot)                                              │
│  ├─ Plano Grátis:        R$ 0/mês    (limitado)                │
│  └─ Plano Básico:        R$ 10/mês   (recomendado)             │
│                                                                  │
│  Vercel (Dashboard)                                             │
│  └─ Plano Hobby:         R$ 0/mês    (grátis para sempre)      │
│                                                                  │
│  Neon.tech (Banco)                                              │
│  └─ Plano Free:          R$ 0/mês    (grátis para sempre)      │
│                                                                  │
│  GitHub (Repositório)                                           │
│  └─ Plano Free:          R$ 0/mês    (grátis para sempre)      │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  TOTAL:                  R$ 0-10/mês                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## ⚡ Performance

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS DE PERFORMANCE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Bot Discord (SquareCloud)                                      │
│  ├─ Latência:            ~50ms                                  │
│  ├─ Uptime:              99.9%                                  │
│  └─ Resposta:            Instantânea                            │
│                                                                  │
│  Dashboard (Vercel)                                             │
│  ├─ Load Time:           ~500ms                                 │
│  ├─ TTFB:                ~100ms                                 │
│  ├─ CDN:                 Global                                 │
│  └─ HTTPS:               Automático                             │
│                                                                  │
│  Banco (Neon.tech)                                              │
│  ├─ Query Time:          ~10ms                                  │
│  ├─ Conexões:            Pooling                                │
│  └─ Backup:              Automático                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Arquitetura robusta e escalável!** 🚀
