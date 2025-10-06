"""
Dashboard Web - Sistema de Ponto ACEDEPOL
Painel web para visualização de dados em tempo real
"""
from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Arquivos de dados
DATA_FILE = 'ponto_data.json'
CONFIG_FILE = 'server_config.json'

def load_data():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_server_config():
    """Carrega configurações dos servidores"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')

@app.route('/agent/<user_id>')
def agent_view(user_id):
    """Página individual do agente"""
    return render_template('agent.html', user_id=user_id)

@app.route('/api/stats')
def get_stats():
    """API: Estatísticas gerais"""
    data = load_data()
    
    total_users = len(data)
    online_users = sum(1 for u in data.values() if u.get('current_session'))
    total_records = sum(len(u['records']) for u in data.values())
    
    # Calcula tempo total trabalhado
    total_time = timedelta()
    for user_data in data.values():
        for record in user_data['records']:
            duracao_str = record['duracao']
            is_negative = duracao_str.startswith('-')
            if is_negative:
                duracao_str = duracao_str[1:]
            
            parts = duracao_str.split(':')
            delta = timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
            
            if is_negative:
                total_time -= delta
            else:
                total_time += delta
    
    return jsonify({
        'total_users': total_users,
        'online_users': online_users,
        'offline_users': total_users - online_users,
        'total_records': total_records,
        'total_time': str(total_time).split('.')[0]
    })

@app.route('/api/users')
def get_users():
    """API: Lista de usuários com dados"""
    data = load_data()
    users_list = []
    
    for user_id, user_data in data.items():
        if user_data['records']:
            total = timedelta()
            for r in user_data['records']:
                duracao_str = r['duracao']
                is_negative = duracao_str.startswith('-')
                if is_negative:
                    duracao_str = duracao_str[1:]
                
                parts = duracao_str.split(':')
                delta = timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
                
                if is_negative:
                    total -= delta
                else:
                    total += delta
            
            users_list.append({
                'id': user_id,
                'name': user_data['name'],
                'total_time': str(total).split('.')[0],
                'records_count': len(user_data['records']),
                'online': user_data.get('current_session') is not None,
                'current_session': user_data.get('current_session')
            })
    
    # Ordena por tempo total
    users_list.sort(key=lambda x: x['total_time'], reverse=True)
    
    return jsonify(users_list)

@app.route('/api/recent')
def get_recent():
    """API: Atividades recentes"""
    data = load_data()
    recent_activities = []
    
    for user_id, user_data in data.items():
        for record in user_data['records'][-5:]:  # Últimos 5 de cada usuário
            recent_activities.append({
                'user_name': user_data['name'],
                'entrada': record['entrada'],
                'saida': record['saida'],
                'duracao': record['duracao'],
                'canal': record.get('canal', 'N/A'),
                'manual': record.get('manual', False),
                'auto_fechado': record.get('auto_fechado', False)
            })
    
    # Ordena por data (mais recente primeiro)
    recent_activities.sort(key=lambda x: x['saida'], reverse=True)
    
    return jsonify(recent_activities[:20])  # Últimos 20

@app.route('/api/config')
def get_config():
    """API: Configurações do servidor"""
    config = load_server_config()
    return jsonify(config)

@app.route('/api/user/<user_id>')
def get_user_details(user_id):
    """API: Detalhes de um usuário específico"""
    data = load_data()
    
    if user_id not in data:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    user_data = data[user_id]
    
    # Calcula tempo total
    total = timedelta()
    for r in user_data['records']:
        duracao_str = r['duracao']
        is_negative = duracao_str.startswith('-')
        if is_negative:
            duracao_str = duracao_str[1:]
        
        parts = duracao_str.split(':')
        delta = timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
        
        if is_negative:
            total -= delta
        else:
            total += delta
    
    return jsonify({
        'id': user_id,
        'name': user_data['name'],
        'total_time': str(total).split('.')[0],
        'records': user_data['records'],
        'records_count': len(user_data['records']),
        'online': user_data.get('current_session') is not None,
        'current_session': user_data.get('current_session')
    })

if __name__ == '__main__':
    print("🌐 Iniciando Dashboard Web - ACEDEPOL")
    print("📊 Acesse: http://localhost:5000")
    print("⚠️ Pressione Ctrl+C para parar")
    app.run(debug=True, host='0.0.0.0', port=5000)
