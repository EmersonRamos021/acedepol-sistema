# 🌐 Guia de Hospedagem - Bot + Dashboard Web

## 🎯 Opções de Hospedagem

### Opção 1: VPS (Recomendado) ⭐
**Melhor para:** Controle total, bot 24/7, dashboard público

**Provedores:**
- **Contabo** - A partir de €4/mês
- **DigitalOcean** - A partir de $6/mês
- **Vultr** - A partir de $6/mês
- **Oracle Cloud** - Tier gratuito disponível
- **AWS EC2** - Tier gratuito 12 meses

### Opção 2: Bot + Dashboard Separados ⭐⭐⭐ (RECOMENDADO)
**Melhor para:** Máxima confiabilidade e performance

**Arquitetura:**
- **Bot:** SquareCloud (R$ 0-10/mês)
- **Dashboard:** Vercel (Grátis)
- **Banco:** Neon.tech (Grátis)

**Vantagens:**
- ✅ Bot sempre online
- ✅ Dashboard com HTTPS automático
- ✅ Deploy automático via GitHub
- ✅ Escalável
- ✅ Praticamente grátis

**📖 Veja:** `DEPLOY_VERCEL.md` e `GUIA_RAPIDO.md`

### Opção 3: Hospedagem Especializada
**Melhor para:** Facilidade, sem configuração

**Provedores:**
- **Railway.app** - Gratuito (500h/mês)
- **Render.com** - Gratuito com limitações
- **Fly.io** - Gratuito até 3 VMs
- **Heroku** - Pago (a partir de $7/mês)

### Opção 3: Computador Próprio
**Melhor para:** Testes, uso local, economia

**Requisitos:**
- Computador ligado 24/7
- Internet estável
- IP fixo ou DynDNS (para dashboard público)

---

## 🚀 Opção 1: VPS (Passo a Passo)

### 1. Contratar VPS

Escolha um provedor e contrate um servidor:
- **OS:** Ubuntu 22.04 LTS
- **RAM:** Mínimo 1GB
- **CPU:** 1 core
- **Disco:** 10GB

### 2. Conectar ao Servidor

```bash
# Windows (use PuTTY ou PowerShell)
ssh root@SEU_IP

# Linux/Mac
ssh root@SEU_IP
```

### 3. Instalar Dependências

```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar Python e pip
apt install python3 python3-pip git -y

# Instalar screen (para manter bot rodando)
apt install screen -y
```

### 4. Fazer Upload dos Arquivos

**Opção A: Git (Recomendado)**
```bash
# No seu computador, crie repositório
git init
git add .
git commit -m "Initial commit"
git remote add origin SEU_REPOSITORIO
git push -u origin main

# No servidor
git clone SEU_REPOSITORIO
cd nome-do-projeto
```

**Opção B: SCP (Transferência direta)**
```bash
# No seu computador
scp -r * root@SEU_IP:/root/bot-ponto/
```

### 5. Configurar no Servidor

```bash
# Entrar na pasta
cd bot-ponto

# Criar .env
nano .env
# Cole suas configurações e salve (Ctrl+X, Y, Enter)

# Instalar dependências
pip3 install -r requirements.txt
```

### 6. Executar Bot (24/7)

```bash
# Criar sessão screen para o bot
screen -S bot-ponto

# Executar bot
python3 bot_ponto_acedepol.py

# Desanexar (bot continua rodando)
# Pressione: Ctrl+A, depois D

# Para voltar à sessão
screen -r bot-ponto
```

### 7. Executar Dashboard Web (24/7)

```bash
# Criar sessão screen para o dashboard
screen -S dashboard

# Executar dashboard
python3 web_dashboard.py

# Desanexar
# Pressione: Ctrl+A, depois D

# Para voltar à sessão
screen -r dashboard
```

### 8. Configurar Firewall

```bash
# Permitir porta do dashboard
ufw allow 5000/tcp

# Permitir SSH
ufw allow 22/tcp

# Ativar firewall
ufw enable
```

### 9. Acessar Dashboard

```
http://SEU_IP:5000
```

---

## 🎨 Opção 2: Railway.app (Gratuito)

### 1. Criar Conta

Acesse: https://railway.app

### 2. Criar Novo Projeto

- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Conecte seu repositório

### 3. Configurar Variáveis de Ambiente

No painel do Railway:
- Settings → Variables
- Adicione: `BOT_TOKEN`, `ADMIN_IDS`

### 4. Configurar Dois Serviços

**Serviço 1: Bot Discord**
```bash
# Start Command
python bot_ponto_acedepol.py
```

**Serviço 2: Dashboard Web**
```bash
# Start Command
python web_dashboard.py
```

### 5. Deploy

Railway faz deploy automático!

### 6. Acessar Dashboard

Railway fornece URL pública automaticamente.

---

## 💻 Opção 3: Computador Próprio

### 1. Manter Bot Rodando

**Windows:**
```bash
# Criar arquivo start_bot.bat
@echo off
python bot_ponto_acedepol.py
pause
```

**Executar ao iniciar Windows:**
1. Pressione Win+R
2. Digite: `shell:startup`
3. Cole o atalho do `start_bot.bat`

**Linux/Mac:**
```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/bot-ponto.service
```

```ini
[Unit]
Description=Bot Ponto ACEDEPOL
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/bot
ExecStart=/usr/bin/python3 bot_ponto_acedepol.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl enable bot-ponto
sudo systemctl start bot-ponto

# Ver status
sudo systemctl status bot-ponto
```

### 2. Dashboard Público (Opcional)

**Usar Ngrok (Túnel):**
```bash
# Instalar ngrok
# https://ngrok.com/download

# Executar
ngrok http 5000

# Ngrok fornece URL pública
# Exemplo: https://abc123.ngrok.io
```

---

## 🔧 Configuração Avançada

### Usar Nginx (Proxy Reverso)

```bash
# Instalar nginx
apt install nginx -y

# Configurar
nano /etc/nginx/sites-available/acedepol
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar site
ln -s /etc/nginx/sites-available/acedepol /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Adicionar SSL (HTTPS)

```bash
# Instalar certbot
apt install certbot python3-certbot-nginx -y

# Obter certificado
certbot --nginx -d seu-dominio.com

# Renovação automática já está configurada
```

### Usar Gunicorn (Produção)

```bash
# Instalar
pip3 install gunicorn

# Executar
gunicorn -w 4 -b 0.0.0.0:5000 web_dashboard:app

# Com systemd
nano /etc/systemd/system/dashboard.service
```

```ini
[Unit]
Description=Dashboard ACEDEPOL
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/bot
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 web_dashboard:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📊 Comparação de Opções

| Opção | Custo | Dificuldade | Uptime | Dashboard Público |
|-------|-------|-------------|--------|-------------------|
| **VPS** | €4-10/mês | Média | 99.9% | ✅ Sim |
| **Railway** | Grátis | Fácil | 99% | ✅ Sim |
| **PC Próprio** | Grátis | Fácil | Variável | ⚠️ Com Ngrok |

---

## 🎯 Recomendação

### Para Começar:
**Railway.app** - Gratuito e fácil

### Para Produção:
**VPS (Contabo/DigitalOcean)** - Controle total

### Para Testes:
**PC Próprio** - Sem custos

---

## 🔒 Segurança em Produção

### 1. Nunca Exponha o .env

```bash
# Adicione ao .gitignore
echo ".env" >> .gitignore
```

### 2. Use Variáveis de Ambiente

No servidor, configure diretamente:
```bash
export BOT_TOKEN="seu_token"
export ADMIN_IDS="123,456"
```

### 3. Firewall

```bash
# Apenas portas necessárias
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw enable
```

### 4. Atualizações

```bash
# Atualizar sistema regularmente
apt update && apt upgrade -y
```

### 5. Backups

```bash
# Criar script de backup
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz ponto_data.json server_config.json
```

```bash
chmod +x backup.sh
# Adicionar ao cron (diário às 3h)
crontab -e
# Adicione: 0 3 * * * /caminho/backup.sh
```

---

## 💡 Dicas Finais

1. **Comece simples** - Use Railway ou PC próprio
2. **Teste tudo** antes de ir para produção
3. **Faça backups** regularmente
4. **Monitore logs** para erros
5. **Use domínio** para dashboard profissional
6. **Configure SSL** para segurança
7. **Documente** suas configurações

---

**Pronto para hospedar!** 🚀
