# 🚔 Dashboard ACEDEPOL - Polícia Civil

Sistema de controle de ponto para Discord com dashboard web.

## 🏗️ Arquitetura

```
Bot Discord (SquareCloud) ←→ Dashboard Web (Vercel)
```

## 🚀 Deploy Rápido

### Bot no SquareCloud:
1. Faça upload de `bot_ponto_acedepol.py`
2. Configure `.env` com `BOT_TOKEN`
3. Inicie o bot

### Dashboard no Vercel:
1. Conecte este repositório no Vercel
2. Deploy automático!
3. Acesse: `https://seu-projeto.vercel.app`

## 📁 Estrutura

```
├── bot_ponto_acedepol.py    # Bot Discord (SquareCloud)
├── app.py                    # Dashboard Flask (Vercel)
├── templates/
│   └── index.html           # Interface web
├── vercel.json              # Config Vercel
├── requirements.txt         # Deps do bot
└── requirements-vercel.txt  # Deps do dashboard
```

## 🔧 Tecnologias

- **Bot:** Discord.py
- **Dashboard:** Flask + HTML/CSS/JS
- **Deploy:** SquareCloud + Vercel

## 📖 Documentação Completa

Veja `DEPLOY_VERCEL.md` para instruções detalhadas.

## ✨ Features

- ✅ Controle de ponto via Discord
- ✅ Dashboard web em tempo real
- ✅ Estatísticas e relatórios
- ✅ Sistema de cargos e permissões
- ✅ Logs automáticos
- ✅ HTTPS grátis

## 🌐 URLs

- **Dashboard:** https://seu-projeto.vercel.app
- **Bot:** Discord (SquareCloud)

---

**Desenvolvido para ACEDEPOL - Polícia Civil Nova Capital** 🚔
