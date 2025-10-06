# 🌐 Dashboard Web - ACEDEPOL

## 📊 Painel Web em Tempo Real

Dashboard web para visualização dos dados do sistema de ponto em tempo real.

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install flask
```

### 2. Executar o Dashboard

```bash
python web_dashboard.py
```

### 3. Acessar no Navegador

```
http://localhost:5000
```

## 📋 Funcionalidades

### 📊 Estatísticas em Tempo Real

- **Total de Policiais** - Quantidade cadastrada
- **Em Serviço** - Policiais online agora
- **Fora de Serviço** - Policiais offline
- **Tempo Total** - Soma de todas as horas trabalhadas

### 👮 Ranking de Policiais

- Lista dos 10 policiais com mais horas
- Status online/offline em tempo real
- Tempo total e quantidade de registros
- Ordenado por horas trabalhadas

### 📋 Atividades Recentes

- Últimas 20 atividades
- Mostra duração de cada sessão
- Indica registros manuais e automáticos
- Atualização em tempo real

## 🎨 Visual

- **Design Moderno** - Interface limpa e profissional
- **Responsivo** - Funciona em desktop e mobile
- **Cores** - Gradiente roxo/azul
- **Animações** - Transições suaves
- **Auto-atualização** - A cada 10 segundos

## 🔧 Configuração Avançada

### Mudar Porta

Edite `web_dashboard.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Mude 5000 para 8080
```

### Acesso Externo

Para acessar de outros computadores na rede:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Depois acesse: `http://SEU_IP:5000`

### Modo Produção

Para uso em produção, use um servidor WSGI:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_dashboard:app
```

## 📡 API Endpoints

O dashboard expõe APIs REST:

### GET /api/stats
Retorna estatísticas gerais

```json
{
  "total_users": 25,
  "online_users": 5,
  "offline_users": 20,
  "total_records": 350,
  "total_time": "125:30:00"
}
```

### GET /api/users
Retorna lista de usuários

```json
[
  {
    "id": "123456789",
    "name": "João Silva",
    "total_time": "10:30:00",
    "records_count": 25,
    "online": true
  }
]
```

### GET /api/recent
Retorna atividades recentes

```json
[
  {
    "user_name": "João Silva",
    "entrada": "2025-01-10 14:00:00",
    "saida": "2025-01-10 18:00:00",
    "duracao": "4:00:00",
    "canal": "Patrulha 1",
    "manual": false,
    "auto_fechado": false
  }
]
```

### GET /api/config
Retorna configurações do servidor

## 🔒 Segurança

### Adicionar Autenticação

Para adicionar login, instale:

```bash
pip install flask-login flask-bcrypt
```

### Usar HTTPS

Para produção, use certificado SSL:

```bash
pip install pyopenssl
```

## 💡 Dicas

1. **Mantenha o bot rodando** - O dashboard lê os mesmos arquivos
2. **Não edite arquivos** - Deixe o bot gerenciar os dados
3. **Use em rede local** - Mais seguro que expor na internet
4. **Monitore recursos** - Dashboard consome pouca memória

## 🎯 Casos de Uso

- **Monitores** - Exibir em TVs da delegacia
- **Supervisão** - Acompanhar equipe em tempo real
- **Relatórios** - Visualizar dados rapidamente
- **Transparência** - Mostrar estatísticas para equipe

## 🐛 Troubleshooting

### Porta já em uso

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Dados não aparecem

- Verifique se `ponto_data.json` existe
- Confirme que o bot está salvando dados
- Reinicie o dashboard

### Erro ao instalar Flask

```bash
pip install --upgrade pip
pip install flask --no-cache-dir
```

## 📱 Acesso Mobile

O dashboard é responsivo! Acesse pelo celular:

1. Conecte no mesmo Wi-Fi
2. Descubra o IP do computador
3. Acesse: `http://IP:5000`

## 🎨 Personalização

### Mudar Cores

Edite `templates/dashboard.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Mude para suas cores */
```

### Adicionar Logo

```html
<div class="header">
    <img src="logo.png" alt="Logo">
    <h1>🚔 Dashboard ACEDEPOL</h1>
</div>
```

## 🚀 Próximas Funcionalidades

- [ ] Gráficos interativos
- [ ] Exportar relatórios PDF
- [ ] Filtros por data
- [ ] Notificações em tempo real
- [ ] Modo escuro

---

**Dashboard Web - ACEDEPOL** 🌐
