# 📋 Comandos Prontos - Deploy Rápido

Copie e cole estes comandos para fazer o deploy rapidamente.

## 🚀 Deploy Completo (Bot + Dashboard)

### 1️⃣ Preparar Repositório GitHub

```bash
# Inicializar Git
git init

# Adicionar arquivos do dashboard
git add app.py vercel.json requirements-vercel.txt templates/ .gitignore README_VERCEL.md

# Commit
git commit -m "Dashboard ACEDEPOL - Sistema de Ponto"

# Criar branch main
git branch -M main

# Adicionar repositório remoto (SUBSTITUA SEU_USUARIO e NOME_REPO)
git remote add origin https://github.com/SEU_USUARIO/NOME_REPO.git

# Push
git push -u origin main
```

### 2️⃣ Instalar Vercel CLI (Opcional)

```bash
# Instalar globalmente
npm install -g vercel

# Ou usar npx (sem instalar)
npx vercel
```

### 3️⃣ Deploy no Vercel via CLI

```bash
# Login
vercel login

# Deploy
vercel

# Deploy para produção
vercel --prod
```

## 🗄️ Configurar Banco de Dados

### PostgreSQL (Neon.tech)

```bash
# Instalar dependência
pip install psycopg2-binary

# Adicionar ao requirements.txt
echo "psycopg2-binary>=2.9.0" >> requirements.txt

# Adicionar ao requirements-vercel.txt
echo "psycopg2-binary>=2.9.0" >> requirements-vercel.txt
```

### MongoDB (MongoDB Atlas)

```bash
# Instalar dependência
pip install pymongo

# Adicionar ao requirements.txt
echo "pymongo>=4.0.0" >> requirements.txt

# Adicionar ao requirements-vercel.txt
echo "pymongo>=4.0.0" >> requirements-vercel.txt
```

## 🔧 Configurar Variáveis de Ambiente

### No SquareCloud (Bot):

```bash
# Criar arquivo .env
echo "BOT_TOKEN=seu_token_aqui" > .env
echo "ADMIN_IDS=seu_id_aqui" >> .env
echo "DATABASE_URL=sua_url_aqui" >> .env
```

### No Vercel (Dashboard):

```bash
# Via CLI
vercel env add DATABASE_URL

# Ou via interface web:
# Settings → Environment Variables → Add
```

## 📦 Atualizar Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar todas as dependências
pip install -r requirements.txt

# Gerar requirements.txt atualizado
pip freeze > requirements.txt
```

## 🧪 Testar Localmente

### Testar Bot:

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar bot
python bot_ponto_acedepol.py
```

### Testar Dashboard:

```bash
# Instalar dependências
pip install -r requirements-vercel.txt

# Rodar servidor
python app.py

# Acessar: http://localhost:5000
```

## 🔄 Atualizar Deploy

### Atualizar Dashboard (Vercel):

```bash
# Fazer alterações nos arquivos

# Commit
git add .
git commit -m "Atualização do dashboard"

# Push (deploy automático)
git push
```

### Atualizar Bot (SquareCloud):

```bash
# 1. Fazer alterações no bot_ponto_acedepol.py
# 2. Acessar painel do SquareCloud
# 3. Upload do arquivo atualizado
# 4. Reiniciar aplicação
```

## 🗑️ Limpar e Recomeçar

```bash
# Remover Git
rm -rf .git

# Remover node_modules (se existir)
rm -rf node_modules

# Remover cache Python
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +

# Recomeçar
git init
```

## 📊 Ver Logs

### Vercel:

```bash
# Via CLI
vercel logs

# Logs em tempo real
vercel logs --follow

# Logs de produção
vercel logs --prod
```

### SquareCloud:

```bash
# Acessar painel web
# Logs → Ver logs em tempo real
```

## 🔍 Verificar Status

### Vercel:

```bash
# Listar deployments
vercel ls

# Ver detalhes do projeto
vercel inspect
```

### Git:

```bash
# Ver status
git status

# Ver histórico
git log --oneline

# Ver branches
git branch -a
```

## 🌐 Domínio Personalizado

### Adicionar Domínio no Vercel:

```bash
# Via CLI
vercel domains add seudominio.com.br

# Verificar domínios
vercel domains ls

# Remover domínio
vercel domains rm seudominio.com.br
```

## 🔐 Segurança

### Gerar .gitignore:

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
.Python
venv/
env/

# Ambiente
.env
.env.local

# Dados
ponto_data.json
server_config.json
backup_*.json

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF
```

### Verificar Segurança:

```bash
# Verificar se .env está no .gitignore
grep -q "^\.env$" .gitignore && echo "✅ .env protegido" || echo "❌ .env exposto!"

# Verificar se .env não está no Git
git ls-files | grep -q "^\.env$" && echo "❌ .env no Git!" || echo "✅ .env seguro"
```

## 🆘 Resolver Problemas

### Erro: Module not found

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Limpar cache
pip cache purge
```

### Erro: Port already in use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Erro: Git push rejected

```bash
# Forçar push (cuidado!)
git push -f origin main

# Ou pull primeiro
git pull origin main --rebase
git push origin main
```

## 📱 Comandos Úteis

### Criar Backup:

```bash
# Backup completo
tar -czf backup_$(date +%Y%m%d).tar.gz *.py *.json *.txt templates/

# Backup apenas dados
cp ponto_data.json ponto_data_backup_$(date +%Y%m%d).json
```

### Verificar Versões:

```bash
# Python
python --version

# Pip
pip --version

# Git
git --version

# Node (se usar Vercel CLI)
node --version
npm --version
```

### Limpar Espaço:

```bash
# Limpar cache pip
pip cache purge

# Limpar cache npm
npm cache clean --force

# Limpar arquivos temporários
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
```

## 🎯 Checklist Rápido

```bash
# Verificar tudo antes do deploy
echo "🔍 Verificando configuração..."

# 1. Arquivos necessários
[ -f "app.py" ] && echo "✅ app.py" || echo "❌ app.py"
[ -f "vercel.json" ] && echo "✅ vercel.json" || echo "❌ vercel.json"
[ -f "requirements-vercel.txt" ] && echo "✅ requirements-vercel.txt" || echo "❌ requirements-vercel.txt"
[ -f "templates/index.html" ] && echo "✅ templates/index.html" || echo "❌ templates/index.html"

# 2. Git configurado
[ -d ".git" ] && echo "✅ Git inicializado" || echo "❌ Git não inicializado"

# 3. .env protegido
grep -q "^\.env$" .gitignore && echo "✅ .env no .gitignore" || echo "❌ .env não protegido"

echo "✅ Verificação completa!"
```

---

**Dica:** Salve este arquivo para referência rápida! 📌
