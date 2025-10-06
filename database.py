"""
Módulo de conexão com banco de dados PostgreSQL (Neon.tech)
"""
import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_database():
    """Inicializa o banco de dados criando a tabela se não existir"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Criar tabela para dados do ponto
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ponto_data (
                id SERIAL PRIMARY KEY,
                data JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela para configurações dos servidores
        cur.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                id SERIAL PRIMARY KEY,
                config JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Inserir dados iniciais se não existirem
        cur.execute("SELECT COUNT(*) FROM ponto_data")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO ponto_data (data) VALUES (%s)", (json.dumps({}),))
        
        cur.execute("SELECT COUNT(*) FROM server_config")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO server_config (config) VALUES (%s)", (json.dumps({}),))
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def save_data(data):
    """Salva dados do ponto no banco"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Atualizar ou inserir dados
        cur.execute("DELETE FROM ponto_data")
        cur.execute(
            "INSERT INTO ponto_data (data) VALUES (%s)",
            (json.dumps(data),)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False

def load_data():
    """Carrega dados do ponto do banco"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("SELECT data FROM ponto_data ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return {}

def save_server_config(config):
    """Salva configurações dos servidores no banco"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Atualizar ou inserir configurações
        cur.execute("DELETE FROM server_config")
        cur.execute(
            "INSERT INTO server_config (config) VALUES (%s)",
            (json.dumps(config),)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar configurações: {e}")
        return False

def load_server_config():
    """Carrega configurações dos servidores do banco"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("SELECT config FROM server_config ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return {}
