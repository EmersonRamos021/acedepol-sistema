"""
Script para testar conexão com banco de dados
"""
from database import init_database, load_data, save_data
from datetime import datetime
import json

print("🔍 Testando conexão com banco de dados...\n")

# 1. Inicializar banco
print("1️⃣ Inicializando banco...")
if init_database():
    print("✅ Banco inicializado!\n")
else:
    print("❌ Erro ao inicializar banco\n")
    exit(1)

# 2. Carregar dados
print("2️⃣ Carregando dados...")
dados = load_data()
print(f"✅ Dados carregados: {len(dados)} usuários\n")

if dados:
    print("📊 Dados encontrados:")
    print(json.dumps(dados, indent=2, ensure_ascii=False))
else:
    print("⚠️ Banco está vazio! Vou adicionar dados de teste...\n")
    
    # 3. Adicionar dados de teste
    print("3️⃣ Adicionando dados de teste...")
    dados_teste = {
        "303184113639358464": {
            "name": "Emerson Ramos",
            "current_session": {
                "entrada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "canal": "Patrulha 01"
            },
            "records": [
                {
                    "entrada": "2025-06-10 08:00:00",
                    "saida": "2025-06-10 17:00:00",
                    "canal": "Patrulha 01",
                    "duracao": "9:00:00",
                    "manual": False
                },
                {
                    "entrada": "2025-06-09 08:00:00",
                    "saida": "2025-06-09 16:30:00",
                    "canal": "Patrulha 02",
                    "duracao": "8:30:00",
                    "manual": False
                }
            ]
        }
    }
    
    if save_data(dados_teste):
        print("✅ Dados de teste salvos!\n")
        
        # 4. Verificar se salvou
        print("4️⃣ Verificando dados salvos...")
        dados_verificacao = load_data()
        print(f"✅ Verificado: {len(dados_verificacao)} usuários")
        print(json.dumps(dados_verificacao, indent=2, ensure_ascii=False))
    else:
        print("❌ Erro ao salvar dados de teste")

print("\n" + "="*50)
print("✅ Teste concluído!")
print("="*50)
print("\n💡 Agora teste o dashboard:")
print("   python app.py")
print("   Abra: http://localhost:5000")
