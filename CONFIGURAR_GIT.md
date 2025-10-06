# 🔧 Configurar Git - Guia Completo

## 1️⃣ Reiniciar o Terminal

Depois de instalar o Git, você precisa **fechar e abrir novamente** o terminal (ou VS Code) para o Git funcionar.

**Feche o Kiro/VS Code e abra novamente!**

## 2️⃣ Verificar se Git Está Instalado

Abra um novo terminal e digite:

```bash
git --version
```

**Deve aparecer algo como:**
```
git version 2.43.0.windows.1
```

Se aparecer erro, o Git não foi instalado corretamente.

## 3️⃣ Configurar Git (Primeira Vez)

### Configure seu nome:
```bash
git config --global user.name "Seu Nome Aqui"
```

**Exemplo:**
```bash
git config --global user.name "João Silva"
```

### Configure seu email (use o email do GitHub):
```bash
git config --global user.email "seu.email@exemplo.com"
```

**Exemplo:**
```bash
git config --global user.email "joao.silva@gmail.com"
```

### Verificar configuração:
```bash
git config --list
```

## 4️⃣ Conectar com GitHub

### Opção A: HTTPS (Mais Fácil) ⭐

**1. Criar Token de Acesso:**
1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Dê um nome: `Token Vercel Deploy`
4. Marque: `repo` (acesso completo aos repositórios)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você não verá ele novamente!)

**2. Usar o Token:**

Quando fizer `git push`, vai pedir usuário e senha:
- **Username:** seu_usuario_github
- **Password:** cole_o_token_aqui (não a senha do GitHub!)

### Opção B: SSH (Mais Seguro)

**1. Gerar chave SSH:**
```bash
ssh-keygen -t ed25519 -C "seu.email@exemplo.com"
```

Aperte Enter 3 vezes (aceita padrões).

**2. Copiar chave pública:**
```bash
cat ~/.ssh/id_ed25519.pub
```

**3. Adicionar no GitHub:**
1. Acesse: https://github.com/settings/keys
2. Clique em **"New SSH key"**
3. Cole a chave pública
4. Clique em **"Add SSH key"**

**4. Testar conexão:**
```bash
ssh -T git@github.com
```

## 5️⃣ Criar Repositório no GitHub

### Via Site (Mais Fácil):

1. Acesse: https://github.com/new
2. Nome: `acedepol-sistema`
3. Descrição: `Sistema de Controle de Ponto ACEDEPOL`
4. Público ou Privado (sua escolha)
5. **NÃO** marque "Initialize with README"
6. Clique em **"Create repository"**

### Copie a URL que aparece:
```
https://github.com/seu_usuario/acedepol-sistema.git
```

## 6️⃣ Subir Projeto para GitHub

**No terminal, na pasta do projeto:**

```bash
# 1. Inicializar Git
git init

# 2. Adicionar arquivos
git add .

# 3. Fazer commit
git commit -m "Sistema ACEDEPOL - Primeira versão"

# 4. Adicionar repositório remoto (SUBSTITUA pela sua URL)
git remote add origin https://github.com/seu_usuario/acedepol-sistema.git

# 5. Criar branch main
git branch -M main

# 6. Enviar para GitHub
git push -u origin main
```

**Vai pedir usuário e senha:**
- Username: seu_usuario_github
- Password: cole_o_token (não a senha!)

## 7️⃣ Conectar com Vercel

### Via Site (Mais Fácil):

1. Acesse: https://vercel.com
2. Clique em **"Add New"** → **"Project"**
3. Clique em **"Import Git Repository"**
4. Conecte sua conta GitHub
5. Selecione o repositório `acedepol-sistema`
6. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (deixe vazio)
   - **Output Directory:** (deixe vazio)
7. Adicione variável de ambiente:
   - Nome: `DATABASE_URL`
   - Valor: `postgresql://neondb_owner:npg_nNvCf4Yz5DKJ@ep-rapid-sea-ack6ct21-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require`
8. Clique em **"Deploy"**

### Via CLI:

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Adicionar variável de ambiente
vercel env add DATABASE_URL
```

## 8️⃣ Atualizar Projeto

Sempre que fizer alterações:

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Fazer commit
git commit -m "Descrição da mudança"

# 4. Enviar para GitHub
git push

# Vercel faz deploy automático!
```

## 🆘 Problemas Comuns

### "git não é reconhecido"
**Solução:** Feche e abra o terminal novamente

### "Permission denied (publickey)"
**Solução:** Use HTTPS em vez de SSH, ou configure SSH corretamente

### "Authentication failed"
**Solução:** Use o token do GitHub, não a senha

### "fatal: not a git repository"
**Solução:** Execute `git init` primeiro

## 📋 Comandos Úteis

```bash
# Ver status
git status

# Ver histórico
git log --oneline

# Ver configuração
git config --list

# Ver repositório remoto
git remote -v

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Descartar todas as alterações
git reset --hard HEAD
```

## ✅ Checklist

```
[ ] Git instalado
[ ] Terminal reiniciado
[ ] git --version funciona
[ ] Nome configurado (git config user.name)
[ ] Email configurado (git config user.email)
[ ] Conta GitHub criada
[ ] Token de acesso criado
[ ] Repositório criado no GitHub
[ ] Projeto enviado para GitHub
[ ] Vercel conectado ao GitHub
[ ] Deploy funcionando
```

## 🎯 Resumo Rápido

```bash
# 1. Configurar Git (uma vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# 2. Criar repositório no GitHub (via site)
# https://github.com/new

# 3. Subir projeto
git init
git add .
git commit -m "Primeira versão"
git remote add origin https://github.com/seu_usuario/seu_repo.git
git branch -M main
git push -u origin main

# 4. Conectar Vercel (via site)
# https://vercel.com → Import Project
```

---

**Dica:** Salve o token do GitHub em um lugar seguro! Você vai precisar dele sempre que fizer push.
