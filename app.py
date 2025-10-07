"""
Dashboard Web - Sistema de Ponto ACEDEPOL
Versão para Vercel (Serverless)
"""
from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Tentar usar banco de dados
try:
    from database import load_data as load_data_db
    USE_DATABASE = True
    print("✅ Usando banco de dados PostgreSQL")
except ImportError:
    USE_DATABASE = False
    print("⚠️ Usando arquivo JSON")

# Arquivo de dados (fallback)
DATA_FILE = 'ponto_data.json'

def load_data():
    """Carrega dados do banco ou arquivo JSON"""
    if USE_DATABASE:
        try:
            return load_data_db()
        except Exception as e:
            print(f"❌ Erro ao carregar do banco: {e}")
    
    # Fallback para JSON
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """API: Estatísticas gerais"""
    data = load_data()
    
    total_usuarios = len(data)
    usuarios_online = sum(1 for u in data.values() if u.get('current_session'))
    total_registros = sum(len(u.get('records', [])) for u in data.values())
    
    return jsonify({
        'total_usuarios': total_usuarios,
        'usuarios_online': usuarios_online,
        'usuarios_offline': total_usuarios - usuarios_online,
        'total_registros': total_registros
    })

@app.route('/api/usuarios')
def get_usuarios():
    """API: Lista de usuários com suas horas"""
    data = load_data()
    usuarios = []
    
    for user_id, user_data in data.items():
        total_seconds = 0
        
        for record in user_data.get('records', []):
            duracao_str = record.get('duracao', '0:0:0')
            is_negative = duracao_str.startswith('-')
            
            if is_negative:
                duracao_str = duracao_str[1:]
            
            parts = duracao_str.split(':')
            if len(parts) >= 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2].split('.')[0])
                
                delta_seconds = hours * 3600 + minutes * 60 + seconds
                
                if is_negative:
                    total_seconds -= delta_seconds
                else:
                    total_seconds += delta_seconds
        
        total_time = str(timedelta(seconds=total_seconds))
        
        usuarios.append({
            'id': user_id,
            'nome': user_data.get('name', 'Desconhecido'),
            'total_horas': total_time,
            'total_registros': len(user_data.get('records', [])),
            'online': user_data.get('current_session') is not None,
            'sessao_atual': user_data.get('current_session')
        })
    
    # Ordena por tempo total (maior primeiro)
    usuarios.sort(key=lambda x: x['total_horas'], reverse=True)
    
    return jsonify(usuarios)

@app.route('/api/usuario/<user_id>')
def get_usuario(user_id):
    """API: Detalhes de um usuário específico"""
    data = load_data()
    
    if user_id not in data:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    user_data = data[user_id]
    
    return jsonify({
        'id': user_id,
        'nome': user_data.get('name', 'Desconhecido'),
        'registros': user_data.get('records', []),
        'sessao_atual': user_data.get('current_session')
    })

@app.route('/api/online')
def get_online():
    """API: Usuários online agora"""
    data = load_data()
    online = []
    
    for user_id, user_data in data.items():
        if user_data.get('current_session'):
            session = user_data['current_session']
            entrada = datetime.strptime(session['entrada'], '%Y-%m-%d %H:%M:%S')
            tempo_decorrido = datetime.now() - entrada
            
            online.append({
                'id': user_id,
                'nome': user_data.get('name', 'Desconhecido'),
                'entrada': session['entrada'],
                'canal': session.get('canal', 'N/A'),
                'tempo_decorrido': str(tempo_decorrido).split('.')[0]
            })
    
    return jsonify(online)

# Para Vercel (serverless)
if __name__ == '__main__':
    app.run(debug=False)
