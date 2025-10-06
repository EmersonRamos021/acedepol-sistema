# 🚔 Sistema ACEDEPOL - Controle de Ponto

> Sistema completo de controle de ponto para Discord com dashboard web profissional

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0-blue)](https://github.com/Rapptz/discord.py)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Sobre o Projeto

Sistema profissional de controle de ponto desenvolvido para a **Polícia Civil Nova Capital (ACEDEPOL)**, com bot Discord para registro de ponto e dashboard web para visualização de estatísticas em tempo real.

### ✨ Features Principais

- ✅ **Bot Discord** com comandos interativos
- ✅ **Dashboard Web** responsivo e moderno
- ✅ **Controle de Ponto** automático por canal de voz
- ✅ **Sistema de Permissões** por cargos
- ✅ **Relatórios** detalhados de horas trabalhadas
- ✅ **Logs Automáticos** de todas as ações
- ✅ **APIs REST** para integração
- ✅ **Deploy Fácil** em minutos

## 🎯 Demonstração

### Bot Discord
```
/painel  → Controle de ponto interativo
/admin   → Painel administrativo
/config  → Configurações do servidor
/reset   → Resetar horários
```

### Dashboard Web
![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+ACEDEPOL)

**Acesse:** https://seu-projeto.vercel.app

## 🚀 Quick Start

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/acedepol-sistema.git
cd acedepol-sistema
```

### 2. Configure o Bot (SquareCloud)

```bash
# Criar .env
cp .env.example .env

# Editar .env com seus dados
BOT_TOKEN=seu_token_aqui
ADMIN_IDS=seu_id_aqui
DATABASE_URL=sua_url_aqui
```

### 3. Deploy do Dashboard (Vercel)

```bash
# Via GitHub (Recomendado)
git push origin main
# Conecte no Vercel e faça deploy automático

# Ou via CLI
npm i -g vercel
vercel
```

### 4. Pronto! 🎉

- **Bot:** Online no SquareCloud
- **Dashboard:** https://seu-projeto.vercel.app

## 📚 Documentação Completa

| Documento | Descrição |
|-----------|-----------|
| [📖 INDICE.md](INDICE.md) | Índice geral da documentação |
| [⚡ GUIA_RAPIDO.md](GUIA_RAPIDO.md) | Deploy em 5 minutos |
| [🔧 DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) | Guia completo de deploy |
| [📁 ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md) | Organização dos arquivos |
| [🎨 ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md) | Diagramas e fluxos |
| [📋 COMANDOS_DEPLOY.md](COMANDOS_DEPLOY.md) | Comandos prontos |
| [📊 RESUMO_COMPLETO.md](RESUMO_COMPLETO.md) | Resumo de tudo |

## 🏗️ Arquitetura

```
┌─────────────────┐         ┌─────────────────┐
│   SquareCloud   │         │     Vercel      │
│                 │         │                 │
│  🤖 Discord Bot │◄────────┤  🌐 Dashboard   │
│  (24/7 Online)  │  Sync   │  (Website)      │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     ▼
         ┌───────────────────────┐
         │   Neon.tech (DB)      │
         │   PostgreSQL          │
         └───────────────────────┘
```

## 🛠️ Tecnologias

### Backend
- **Python 3.10+**
- **Discord.py 2.3.0** - Bot Discord
- **Flask 3.0.0** - Web Framework
- **PostgreSQL** - Banco de Dados

### Frontend
- **HTML5/CSS3** - Interface
- **JavaScript** - Interatividade
- **Fetch API** - Comunicação com backend

### Deploy
- **SquareCloud** - Hospedagem do bot
- **Vercel** - Hospedagem do dashboard
- **Neon.tech** - Banco de dados
- **GitHub** - Controle de versão

## 📦 Estrutura do Projeto

```
acedepol-sistema/
├── 🤖 Bot Discord
│   ├── bot_ponto_acedepol.py
│   ├── requirements.txt
│   └── .env
│
├── 🌐 Dashboard Web
│   ├── app.py
│   ├── vercel.json
│   ├── requirements-vercel.txt
│   └── templates/
│       └── index.html
│
└── 📚 Documentação
    ├── README.md
    ├── INDICE.md
    ├── GUIA_RAPIDO.md
    └── ...
```

## 💰 Custos

| Serviço | Plano | Custo |
|---------|-------|-------|
| SquareCloud | Básico | R$ 0-10/mês |
| Vercel | Hobby | R$ 0/mês |
| Neon.tech | Free | R$ 0/mês |
| GitHub | Free | R$ 0/mês |
| **TOTAL** | | **R$ 0-10/mês** |

## 🎓 Como Usar

### Para Policiais (Usuários)

1. Entre em um canal de voz autorizado
2. Use `/painel` no Discord
3. Clique em "Abrir Ponto"
4. Trabalhe normalmente
5. Clique em "Fechar Ponto" ao sair

### Para Administradores

1. Use `/admin` para ver relatórios
2. Use `/config` para configurar:
   - Cargos permitidos
   - Canais autorizados
   - Canal de logs
3. Use `/reset` para resetar horários

### Dashboard Web

1. Acesse: https://seu-projeto.vercel.app
2. Veja estatísticas em tempo real
3. Acompanhe ranking de horas
4. Monitore policiais online

## 🔐 Segurança

- ✅ Tokens em variáveis de ambiente
- ✅ `.env` não commitado
- ✅ Permissões por cargo
- ✅ Logs de auditoria
- ✅ HTTPS automático

## 🆘 Suporte

### Problemas Comuns

**Bot não inicia:**
```bash
# Verifique o token
cat .env | grep BOT_TOKEN
```

**Dashboard em branco:**
```bash
# Configure DATABASE_URL no Vercel
vercel env add DATABASE_URL
```

**Dados não sincronizam:**
- Certifique-se que bot e dashboard usam o mesmo `DATABASE_URL`

### Documentação

- [Problemas Comuns](DEPLOY_VERCEL.md#problemas-comuns)
- [Comandos de Debug](COMANDOS_DEPLOY.md#resolver-problemas)
- [FAQ](RESUMO_COMPLETO.md#problemas-comuns)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Desenvolvedor Principal** - Sistema ACEDEPOL

## 🙏 Agradecimentos

- Discord.py pela excelente biblioteca
- Vercel pelo hosting gratuito
- Neon.tech pelo banco de dados
- Comunidade Python Brasil

## 📞 Contato

- **Discord:** [Servidor ACEDEPOL](#)
- **Email:** contato@acedepol.com.br
- **Website:** https://acedepol.vercel.app

## 🔗 Links Úteis

- [Discord.py Docs](https://discordpy.readthedocs.io)
- [Flask Docs](https://flask.palletsprojects.com)
- [Vercel Docs](https://vercel.com/docs)
- [Neon.tech Docs](https://neon.tech/docs)

---

<div align="center">

**Desenvolvido com ❤️ para ACEDEPOL - Polícia Civil Nova Capital**

⭐ Se este projeto foi útil, considere dar uma estrela!

[Documentação](INDICE.md) • [Quick Start](GUIA_RAPIDO.md) • [Deploy](DEPLOY_VERCEL.md) • [Suporte](RESUMO_COMPLETO.md)

</div>
