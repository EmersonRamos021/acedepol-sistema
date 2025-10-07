"""
Bot de Ponto ACEDEPOL - Polícia Civil Nova Capital
Sistema de controle de ponto com painel interativo
"""
import discord
from discord.ext import commands
from discord import ui
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importar módulo de banco de dados
try:
    from database import init_database, save_data, load_data, save_server_config, load_server_config
    USE_DATABASE = True
    print("✅ Módulo de banco de dados carregado")
except ImportError:
    USE_DATABASE = False
    print("⚠️ Banco de dados não disponível, usando arquivos JSON")

# Configurações do bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN não encontrado! Crie um arquivo .env com seu token.")

ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

# Mensagens e cores
MESSAGES = {
    "bot_name": "Bot Ponto ACEDEPOL",
    "organization": "Polícia Civil Nova Capital",
    "welcome_message": "Sistema de Ponto ACEDEPOL - Polícia Civil Nova Capital está online!",
    "voice_required": "Você precisa estar em um canal de voz para bater o ponto!",
    "admin_only": "Apenas administradores podem usar este comando!",
}

COLORS = {
    "success": 0x00ff00,
    "warning": 0xff9900,
    "error": 0xff0000,
    "info": 0x0099ff,
}

# Configurações do Discord
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Arquivos de dados
DATA_FILE = 'ponto_data.json'
CONFIG_FILE = 'server_config.json'

# Funções auxiliares
def load_data_json():
    """Carrega dados do arquivo JSON (fallback)"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data_json(data):
    """Salva dados no arquivo JSON (fallback)"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_server_config_json():
    """Carrega configurações dos servidores do JSON (fallback)"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_server_config_json(config):
    """Salva configurações dos servidores no JSON (fallback)"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# Usar banco de dados se disponível, senão usar JSON
if not USE_DATABASE:
    load_data = load_data_json
    save_data = save_data_json
    load_server_config = load_server_config_json
    save_server_config = save_server_config_json

def is_admin(user_id):
    """Verifica se o usuário é admin global"""
    return user_id in ADMIN_IDS

def has_allowed_role(member):
    """Verifica se o membro tem cargo permitido"""
    guild_id = str(member.guild.id)
    server_config = load_server_config()
    
    if guild_id not in server_config:
        return True
    
    config = server_config[guild_id]
    cargos_permitidos = config.get("cargos_permitidos", [])
    
    if not cargos_permitidos:
        return True
    
    member_roles = [role.name for role in member.roles]
    return any(cargo in member_roles for cargo in cargos_permitidos)

def is_server_admin(member):
    """Verifica se o membro é admin do servidor"""
    if is_admin(member.id):
        return True
    
    guild_id = str(member.guild.id)
    server_config = load_server_config()
    
    if guild_id not in server_config:
        return False
    
    config = server_config[guild_id]
    cargos_admin = config.get("cargos_admin", [])
    
    if not cargos_admin:
        return False
    
    member_roles = [role.name for role in member.roles]
    return any(cargo in member_roles for cargo in cargos_admin)

def is_in_voice_channel(member):
    """Verifica se o membro está em canal de voz"""
    return member.voice is not None and member.voice.channel is not None

def is_in_allowed_voice_channel(member):
    """Verifica se o membro está em um canal de voz permitido"""
    if not is_in_voice_channel(member):
        return False
    
    guild_id = str(member.guild.id)
    server_config = load_server_config()
    
    # Se não há configuração, permite todos os canais
    if guild_id not in server_config:
        return True
    
    config = server_config[guild_id]
    canais_permitidos = config.get("canais_permitidos", [])
    
    # Se não há canais configurados, permite todos
    if not canais_permitidos:
        return True
    
    # Verifica se está em um canal permitido
    channel_name = member.voice.channel.name
    return channel_name in canais_permitidos

async def enviar_log(guild, acao, usuario, detalhes="", cor=None):
    """Envia log para o canal configurado"""
    try:
        guild_id = str(guild.id)
        server_config = load_server_config()
        
        # Verifica se há canal de log configurado
        if guild_id not in server_config:
            return
        
        config = server_config[guild_id]
        canal_log_id = config.get("canal_log")
        
        if not canal_log_id:
            return
        
        # Busca o canal
        canal = guild.get_channel(int(canal_log_id))
        if not canal:
            return
        
        # Cria embed de log
        embed = discord.Embed(
            title=f"📋 {acao}",
            description=detalhes,
            color=cor or COLORS["info"],
            timestamp=datetime.now()
        )
        
        embed.add_field(name="👤 Usuário", value=usuario.mention, inline=True)
        embed.add_field(name="🆔 ID", value=f"`{usuario.id}`", inline=True)
        
        embed.set_footer(text="Sistema de Logs - ACEDEPOL")
        embed.set_thumbnail(url=usuario.display_avatar.url)
        
        await canal.send(embed=embed)
    except Exception as e:
        print(f"Erro ao enviar log: {e}")

# Eventos do bot
@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    print(f'Bot conectado como: {bot.user.name}')
    print('Sistema de Ponto ACEDEPOL - Polícia Civil Nova Capital')
    
    # Inicializar banco de dados se disponível
    if USE_DATABASE:
        print("🔄 Inicializando banco de dados...")
        if init_database():
            print("✅ Banco de dados pronto!")
        else:
            print("⚠️ Erro ao inicializar banco, usando JSON como fallback")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash commands sincronizados")
        print(f"📋 Comandos: /painel, /admin, /reset, /config")
    except Exception as e:
        print(f"❌ Erro ao sincronizar commands: {e}")
    
    bot.add_view(PainelPonto())
    bot.add_view(PainelAdmin())
    bot.add_view(PainelReset())

@bot.event
async def on_voice_state_update(member, before, after):
    """Fecha ponto automaticamente ao sair do canal de voz"""
    try:
        if before.channel is not None and after.channel is None:
            user_id = str(member.id)
            data = load_data()
            
            if user_id in data and data[user_id].get('current_session'):
                session = data[user_id]['current_session']
                entrada = session['entrada']
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                entrada_dt = datetime.strptime(entrada, '%Y-%m-%d %H:%M:%S')
                saida_dt = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                duracao = saida_dt - entrada_dt
                
                record = {
                    'entrada': entrada,
                    'saida': current_time,
                    'canal': session['canal'],
                    'duracao': str(duracao),
                    'auto_fechado': True
                }
                
                data[user_id]['records'].append(record)
                data[user_id]['current_session'] = None
                save_data(data)
                
                print(f"🔴 Ponto fechado automaticamente: {member.display_name}")
                
                # Envia log
                await enviar_log(
                    member.guild,
                    "Ponto Fechado Automaticamente",
                    member,
                    f"**Motivo:** Saiu do canal de voz\n**Entrada:** {entrada}\n**Saída:** {current_time}\n**Duração:** {duracao}\n**Canal:** {session['canal']}",
                    0xed4245
                )
                
                try:
                    embed = discord.Embed(
                        title="🔴 Ponto Fechado Automaticamente",
                        description=f"Seu ponto foi fechado ao sair do canal de voz.\n\n**Entrada:** {entrada}\n**Saída:** {current_time}\n**Duração:** {duracao}\n**Canal:** {session['canal']}",
                        color=COLORS["warning"]
                    )
                    await member.send(embed=embed)
                except:
                    pass
    except Exception as e:
        print(f"❌ Erro no on_voice_state_update: {e}")

# Painel de controle de ponto
class PainelPonto(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='Abrir Ponto', style=discord.ButtonStyle.success, emoji='🟢', custom_id='abrir_ponto_v2', row=0)
    async def abrir_ponto(self, interaction: discord.Interaction, button: ui.Button):
        await self.processar_ponto(interaction, 'entrada')
    
    @ui.button(label='Fechar Ponto', style=discord.ButtonStyle.danger, emoji='🔴', custom_id='fechar_ponto_v2', row=0)
    async def fechar_ponto(self, interaction: discord.Interaction, button: ui.Button):
        await self.processar_ponto(interaction, 'saida')
    
    @ui.button(label='Meus Horários', style=discord.ButtonStyle.primary, emoji='📊', custom_id='meus_horarios_v2', row=1)
    async def meus_horarios(self, interaction: discord.Interaction, button: ui.Button):
        await self.mostrar_horarios(interaction)
    
    @ui.button(label='Status Geral', style=discord.ButtonStyle.secondary, emoji='📈', custom_id='status_geral_v2', row=1)
    async def status_geral(self, interaction: discord.Interaction, button: ui.Button):
        await self.mostrar_status(interaction)
    
    async def processar_ponto(self, interaction: discord.Interaction, tipo):
        # OTIMIZAÇÃO: Responder imediatamente para evitar timeout de 3 segundos
        await interaction.response.defer(ephemeral=True)
        
        user_id = str(interaction.user.id)
        user_name = interaction.user.display_name
        
        if not has_allowed_role(interaction.user):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem cargo autorizado!",
                color=COLORS["error"]
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        if not is_in_voice_channel(interaction.user):
            embed = discord.Embed(
                title="❌ Erro",
                description=MESSAGES["voice_required"],
                color=COLORS["error"]
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Verifica se está em canal permitido
        if not is_in_allowed_voice_channel(interaction.user):
            embed = discord.Embed(
                title="❌ Canal Não Permitido",
                description="Este canal de voz não está autorizado para registro de ponto!\n\nContate um administrador para configurar os canais permitidos.",
                color=COLORS["error"]
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        data = load_data()
        
        if user_id not in data:
            data[user_id] = {'name': user_name, 'records': [], 'current_session': None}
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if tipo == 'entrada':
            if data[user_id]['current_session'] is not None:
                embed = discord.Embed(
                    title="⚠️ Atenção",
                    description="Você já tem um ponto aberto!",
                    color=COLORS["warning"]
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            data[user_id]['current_session'] = {
                'entrada': current_time,
                'canal': interaction.user.voice.channel.name
            }
            
            embed = discord.Embed(
                title="",
                description="",
                color=0x57f287
            )
            
            embed.add_field(
                name="✅ Ponto Aberto com Sucesso",
                value=(
                    f"**👮 Policial:** {user_name}\n"
                    f"**🕐 Horário:** {current_time}\n"
                    f"**📍 Canal:** {interaction.user.voice.channel.name}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Não esqueça de fechar o ponto ao sair!"
                ),
                inline=False
            )
            
            # Envia log
            await enviar_log(
                interaction.guild,
                "Ponto Aberto",
                interaction.user,
                f"**Canal de Voz:** {interaction.user.voice.channel.name}\n**Horário:** {current_time}",
                0x57f287
            )
        else:
            if data[user_id]['current_session'] is None:
                embed = discord.Embed(
                    title="⚠️ Atenção",
                    description="Você não tem ponto aberto!",
                    color=COLORS["warning"]
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            session = data[user_id]['current_session']
            entrada = datetime.strptime(session['entrada'], '%Y-%m-%d %H:%M:%S')
            saida = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            duracao = saida - entrada
            
            record = {
                'entrada': session['entrada'],
                'saida': current_time,
                'canal': session['canal'],
                'duracao': str(duracao)
            }
            
            data[user_id]['records'].append(record)
            data[user_id]['current_session'] = None
            
            embed = discord.Embed(
                title="",
                description="",
                color=0xfee75c
            )
            
            embed.add_field(
                name="🔴 Ponto Fechado com Sucesso",
                value=(
                    f"**👮 Policial:** {user_name}\n"
                    f"**🕐 Entrada:** {session['entrada']}\n"
                    f"**🕐 Saída:** {current_time}\n"
                    f"**⏱️ Tempo Trabalhado:** {duracao}\n"
                    f"**📍 Canal:** {session['canal']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Registro salvo com sucesso!"
                ),
                inline=False
            )
            
            # Envia log
            await enviar_log(
                interaction.guild,
                "Ponto Fechado",
                interaction.user,
                f"**Entrada:** {session['entrada']}\n**Saída:** {current_time}\n**Duração:** {duracao}\n**Canal:** {session['canal']}",
                0xfee75c
            )
        
        save_data(data)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def mostrar_horarios(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        if not has_allowed_role(interaction.user):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem cargo autorizado!",
                color=COLORS["error"]
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        data = load_data()
        
        if user_id not in data or not data[user_id]['records']:
            embed = discord.Embed(
                title="📊 Seus Horários",
                description="Você não possui registros.",
                color=COLORS["info"]
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        user_data = data[user_id]
        records = user_data['records'][-10:]
        
        embed = discord.Embed(
            title="",
            description=f"**📊 Relatório de Horários**\n👮 **{user_data['name']}**\n━━━━━━━━━━━━━━━━━━━━━━",
            color=0x5865f2
        )
        
        total_time = timedelta()
        
        for i, record in enumerate(records, 1):
            time_parts = record['duracao'].split(':')
            if len(time_parts) >= 3:
                # Remove o sinal negativo se houver
                duracao_str = record['duracao']
                is_negative = duracao_str.startswith('-')
                if is_negative:
                    duracao_str = duracao_str[1:]
                    time_parts = duracao_str.split(':')
                
                hours, minutes, seconds = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
                delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                
                if is_negative:
                    total_time -= delta
                else:
                    total_time += delta
            
            # Marca se é registro manual
            tipo_emoji = "📝" if record.get('manual') else "✅"
            tipo_texto = "Ajuste Manual" if record.get('manual') else "Registro Normal"
            motivo = f"**💬 Motivo:** {record.get('motivo', 'N/A')}\n" if record.get('manual') else ""
            
            embed.add_field(
                name=f"{tipo_emoji} Registro #{i} • {tipo_texto}",
                value=(
                    f"**🕐 Entrada:** {record['entrada']}\n"
                    f"**🕐 Saída:** {record['saida']}\n"
                    f"**⏱️ Duração:** {record['duracao']}\n"
                    f"{motivo}"
                    f"**📍 Local:** {record.get('canal', 'N/A')}"
                ),
                inline=True
            )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value=f"**⏱️ TEMPO TOTAL TRABALHADO**\n🕐 {str(total_time)}",
            inline=False
        )
        
        if user_data['current_session']:
            tempo_atual = datetime.now() - datetime.strptime(user_data['current_session']['entrada'], '%Y-%m-%d %H:%M:%S')
            embed.add_field(
                name="🟢 Sessão Ativa Agora",
                value=(
                    f"**🕐 Entrada:** {user_data['current_session']['entrada']}\n"
                    f"**📍 Canal:** {user_data['current_session']['canal']}\n"
                    f"**⏱️ Tempo Decorrido:** {str(tempo_atual).split('.')[0]}"
                ),
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def mostrar_status(self, interaction: discord.Interaction):
        data = load_data()
        
        online_count = sum(1 for u in data.values() if u['current_session'])
        
        embed = discord.Embed(
            title="",
            description="**📈 Status do Sistema - ACEDEPOL**\n🚔 Polícia Civil Nova Capital\n━━━━━━━━━━━━━━━━━━━━━━",
            color=0x5865f2
        )
        
        embed.add_field(
            name="📊 Estatísticas",
            value=(
                f"**👥 Total de Policiais:** {len(data)}\n"
                f"**🟢 Em Serviço:** {online_count}\n"
                f"**🔴 Fora de Serviço:** {len(data) - online_count}"
            ),
            inline=False
        )
        
        if online_count > 0:
            online_list = []
            for u in data.values():
                if u['current_session']:
                    tempo = datetime.now() - datetime.strptime(u['current_session']['entrada'], '%Y-%m-%d %H:%M:%S')
                    tempo_str = str(tempo).split('.')[0]
                    online_list.append(f"🟢 **{u['name']}** • {tempo_str}")
            
            embed.add_field(
                name="👮 Policiais em Serviço Agora",
                value="\n".join(online_list[:10]) if online_list else "Nenhum",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Painel administrativo
class PainelAdmin(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='📊 Relatório', style=discord.ButtonStyle.primary, custom_id='relatorio')
    async def relatorio(self, interaction: discord.Interaction, button: ui.Button):
        if not is_server_admin(interaction.user):
            await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
            return
        
        data = load_data()
        
        embed = discord.Embed(
            title="",
            description="**📊 Relatório Geral de Horas - ACEDEPOL**\n🚔 Polícia Civil Nova Capital\n━━━━━━━━━━━━━━━━━━━━━━",
            color=0x5865f2
        )
        
        # Coleta todos os usuários
        all_users = []
        online_count = 0
        
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
                
                is_online = user_data['current_session'] is not None
                if is_online:
                    online_count += 1
                
                user_info = {
                    'id': user_id,
                    'name': user_data['name'],
                    'total': total,
                    'registros': len(user_data['records']),
                    'online': is_online
                }
                
                all_users.append(user_info)
        
        # Ordena por tempo total (maior primeiro)
        all_users.sort(key=lambda x: x['total'], reverse=True)
        
        # Monta lista única com todos
        if all_users:
            user_list = []
            for user in all_users:
                status = "🟢" if user['online'] else "🔴"
                user_list.append(
                    f"{status} <@{user['id']}> • `{str(user['total']).split('.')[0]}` • {user['registros']} registros"
                )
            
            embed.add_field(
                name=f"👮 Relatório de Policiais ({len(all_users)})",
                value="\n".join(user_list),
                inline=False
            )
        
        # Estatísticas gerais
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value=f"**📈 Total:** {len(all_users)} policiais • {online_count} online • {len(all_users) - online_count} offline",
            inline=False
        )
        
        embed.set_footer(text=f"Relatório gerado por {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Painel de reset
class PainelReset(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.select(placeholder="Selecione policial...", custom_id="select_reset")
    async def select_reset(self, interaction: discord.Interaction, select: ui.Select):
        if not is_server_admin(interaction.user):
            await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
            return
        
        user_id = select.values[0]
        data = load_data()
        
        if user_id in data:
            backup_data = data[user_id].copy()
            user_name = data[user_id]['name']
            
            data[user_id] = {'name': user_name, 'records': [], 'current_session': None}
            save_data(data)
            
            backup_file = f"backup_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            await interaction.response.send_message(f"✅ Horários de {user_name} resetados!\n💾 Backup: {backup_file}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Usuário não encontrado!", ephemeral=True)

# Painel de configuração
class PainelConfig(ui.View):
    def __init__(self, guild_id, guild):
        super().__init__(timeout=None)
        self.guild_id = str(guild_id)
        self.guild = guild
    
    @ui.button(label='➕ Cargo Permitido', style=discord.ButtonStyle.success)
    async def add_permitido(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(ConfigModal(self.guild_id, "permitido", self.guild))
    
    @ui.button(label='➕ Cargo Admin', style=discord.ButtonStyle.primary)
    async def add_admin(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(ConfigModal(self.guild_id, "admin", self.guild))
    
    @ui.button(label='🎙️ Canal Permitido', style=discord.ButtonStyle.success, row=1)
    async def add_canal(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CanalModal(self.guild_id, self.guild, "adicionar"))
    
    @ui.button(label='🚫 Remover Canal', style=discord.ButtonStyle.danger, row=1)
    async def remove_canal(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CanalModal(self.guild_id, self.guild, "remover"))
    
    @ui.button(label='📋 Canal de Logs', style=discord.ButtonStyle.primary, row=2)
    async def config_log(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(LogCanalModal(self.guild_id, self.guild))
    
    @ui.button(label='📋 Ver Config', style=discord.ButtonStyle.secondary, row=2)
    async def ver_config(self, interaction: discord.Interaction, button: ui.Button):
        config = load_server_config().get(self.guild_id, {})
        
        permitidos = config.get("cargos_permitidos", [])
        admins = config.get("cargos_admin", [])
        canais = config.get("canais_permitidos", [])
        
        embed = discord.Embed(title="⚙️ Configuração Atual", color=COLORS["info"])
        
        if permitidos:
            embed.add_field(
                name="✅ Cargos Permitidos",
                value="\n".join(f"• {c}" for c in permitidos),
                inline=False
            )
        else:
            embed.add_field(name="✅ Cargos Permitidos", value="Nenhum (todos podem usar)", inline=False)
        
        if admins:
            embed.add_field(
                name="👮‍♂️ Cargos Admin",
                value="\n".join(f"• {c}" for c in admins),
                inline=False
            )
        else:
            embed.add_field(name="👮‍♂️ Cargos Admin", value="Nenhum (apenas admins globais)", inline=False)
        
        if canais:
            embed.add_field(
                name="🎙️ Canais de Voz Permitidos",
                value="\n".join(f"• {c}" for c in canais),
                inline=False
            )
        else:
            embed.add_field(name="🎙️ Canais de Voz", value="Nenhum (todos os canais permitidos)", inline=False)
        
        # Canal de logs
        canal_log_id = config.get("canal_log")
        if canal_log_id:
            canal_log = self.guild.get_channel(int(canal_log_id))
            if canal_log:
                embed.add_field(
                    name="📋 Canal de Logs",
                    value=f"• {canal_log.mention}",
                    inline=False
                )
            else:
                embed.add_field(name="📋 Canal de Logs", value="Canal não encontrado (ID inválido)", inline=False)
        else:
            embed.add_field(name="📋 Canal de Logs", value="Nenhum configurado", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @ui.button(label='🗑️ Limpar Tudo', style=discord.ButtonStyle.danger, row=2)
    async def limpar_config(self, interaction: discord.Interaction, button: ui.Button):
        config = load_server_config()
        
        if self.guild_id in config:
            del config[self.guild_id]
            save_server_config(config)
            await interaction.response.send_message("✅ Configuração limpa! Todos podem usar o sistema agora.", ephemeral=True)
        else:
            await interaction.response.send_message("ℹ️ Não há configuração para limpar.", ephemeral=True)

# Modal para configurar canal de logs
class LogCanalModal(ui.Modal):
    def __init__(self, guild_id, guild):
        super().__init__(title="Configurar Canal de Logs")
        self.guild_id = guild_id
        self.guild = guild
        
        self.canal_input = ui.TextInput(
            label="ID do Canal de Logs",
            placeholder="Cole o ID do canal de texto (ou deixe vazio para remover)",
            required=False,
            min_length=0,
            max_length=20
        )
        self.add_item(self.canal_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        canal_id_str = self.canal_input.value.strip()
        
        config = load_server_config()
        if self.guild_id not in config:
            config[self.guild_id] = {"cargos_permitidos": [], "cargos_admin": [], "canais_permitidos": []}
        
        # Se vazio, remove o canal de logs
        if not canal_id_str:
            if "canal_log" in config[self.guild_id]:
                del config[self.guild_id]["canal_log"]
            save_server_config(config)
            await interaction.response.send_message("✅ Canal de logs removido!", ephemeral=True)
            return
        
        try:
            channel_id = int(canal_id_str)
        except ValueError:
            await interaction.response.send_message(
                f"❌ '{canal_id_str}' não é um ID válido!",
                ephemeral=True
            )
            return
        
        # Busca o canal
        channel = self.guild.get_channel(channel_id)
        
        if not channel or not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                f"❌ Canal de texto com ID `{channel_id}` não encontrado!",
                ephemeral=True
            )
            return
        
        # Salva o canal de logs
        config[self.guild_id]["canal_log"] = str(channel_id)
        save_server_config(config)
        
        await interaction.response.send_message(
            f"✅ Canal de logs configurado: {channel.mention}",
            ephemeral=True
        )
        
        # Envia mensagem de teste no canal
        try:
            embed = discord.Embed(
                title="📋 Sistema de Logs Ativado",
                description="Este canal foi configurado para receber logs do sistema de ponto.\n\n**Logs registrados:**\n• Abertura de ponto\n• Fechamento de ponto\n• Fechamento automático\n• Adição/remoção de horas\n• Reset de horários",
                color=COLORS["success"]
            )
            embed.set_footer(text="ACEDEPOL - Sistema de Controle de Ponto")
            await channel.send(embed=embed)
        except:
            pass

# Modal para configurar canais de voz
class CanalModal(ui.Modal):
    def __init__(self, guild_id, guild, acao):
        super().__init__(title=f"{acao.title()} Canal de Voz")
        self.guild_id = guild_id
        self.guild = guild
        self.acao = acao
        
        self.canal_input = ui.TextInput(
            label="ID do Canal de Voz",
            placeholder="Cole o ID do canal aqui (ex: 1234567890)",
            required=True,
            min_length=17,
            max_length=20
        )
        self.add_item(self.canal_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        canal_id_str = self.canal_input.value.strip()
        
        try:
            channel_id = int(canal_id_str)
        except ValueError:
            await interaction.response.send_message(
                f"❌ '{canal_id_str}' não é um ID válido!\n\n**Como obter o ID:**\n1. Ative o Modo Desenvolvedor\n2. Clique com botão direito no canal de voz\n3. Copiar ID",
                ephemeral=True
            )
            return
        
        # Busca o canal pelo ID
        channel = self.guild.get_channel(channel_id)
        
        if not channel or not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message(
                f"❌ Canal de voz com ID `{channel_id}` não encontrado!",
                ephemeral=True
            )
            return
        
        # Adiciona ou remove o canal
        config = load_server_config()
        if self.guild_id not in config:
            config[self.guild_id] = {"cargos_permitidos": [], "cargos_admin": [], "canais_permitidos": []}
        
        if "canais_permitidos" not in config[self.guild_id]:
            config[self.guild_id]["canais_permitidos"] = []
        
        if self.acao == "adicionar":
            if channel.name not in config[self.guild_id]["canais_permitidos"]:
                config[self.guild_id]["canais_permitidos"].append(channel.name)
                save_server_config(config)
                await interaction.response.send_message(
                    f"✅ Canal **{channel.name}** (ID: `{channel.id}`) adicionado aos canais permitidos!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"⚠️ Canal **{channel.name}** já está configurado!",
                    ephemeral=True
                )
        else:  # remover
            if channel.name in config[self.guild_id]["canais_permitidos"]:
                config[self.guild_id]["canais_permitidos"].remove(channel.name)
                save_server_config(config)
                await interaction.response.send_message(
                    f"✅ Canal **{channel.name}** removido dos canais permitidos!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"⚠️ Canal **{channel.name}** não estava configurado!",
                    ephemeral=True
                )

# Modal de configuração (aceita ID do cargo)
class ConfigModal(ui.Modal):
    def __init__(self, guild_id, tipo, guild):
        super().__init__(title=f"Adicionar Cargo {tipo.title()}")
        self.guild_id = guild_id
        self.tipo = tipo
        self.guild = guild
        
        self.cargo_input = ui.TextInput(
            label="ID do Cargo",
            placeholder="Cole o ID do cargo aqui (ex: 1234567890)",
            required=True,
            min_length=17,
            max_length=20
        )
        self.add_item(self.cargo_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        cargo_id_str = self.cargo_input.value.strip()
        
        # Tenta converter para ID
        try:
            role_id = int(cargo_id_str)
        except ValueError:
            await interaction.response.send_message(
                f"❌ '{cargo_id_str}' não é um ID válido!\n\n**Como obter o ID:**\n1. Ative o Modo Desenvolvedor no Discord\n2. Clique com botão direito no cargo\n3. Copiar ID",
                ephemeral=True
            )
            return
        
        # Busca o cargo pelo ID
        role = self.guild.get_role(role_id)
        
        if not role:
            await interaction.response.send_message(
                f"❌ Cargo com ID `{role_id}` não encontrado neste servidor!",
                ephemeral=True
            )
            return
        
        # Adiciona o cargo na configuração
        config = load_server_config()
        if self.guild_id not in config:
            config[self.guild_id] = {"cargos_permitidos": [], "cargos_admin": []}
        
        key = "cargos_permitidos" if self.tipo == "permitido" else "cargos_admin"
        
        if role.name not in config[self.guild_id][key]:
            config[self.guild_id][key].append(role.name)
            save_server_config(config)
            await interaction.response.send_message(
                f"✅ Cargo **{role.name}** (ID: `{role.id}`) adicionado aos {self.tipo}s!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Cargo **{role.name}** já está configurado!",
                ephemeral=True
            )

# Slash Commands
@bot.tree.command(name="painel", description="Painel de controle de ponto")
async def criar_painel(interaction: discord.Interaction):
    """Cria o painel de controle de ponto"""
    
    # Verifica se é admin para mostrar aviso
    if is_server_admin(interaction.user) or interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "⚠️ **Atenção Admin:** Se houver painéis antigos no canal, apague-os antes de usar o novo!\n\nCriando painel...",
            ephemeral=True
        )
        
        # Envia o painel no canal
        embed = discord.Embed(
            title="🚔 Sistema de Ponto - ACEDEPOL",
            description="",
            color=0x2b2d31
        )
        
        embed.add_field(
            name="",
            value="**POLÍCIA CIVIL NOVA CAPITAL**\n━━━━━━━━━━━━━━━━━━━━━━",
            inline=False
        )
        
        embed.add_field(
            name="📋 Como Usar",
            value=(
                "🟢 **Abrir Ponto** - Registra sua entrada no serviço\n"
                "🔴 **Fechar Ponto** - Registra sua saída e calcula horas\n"
                "📊 **Meus Horários** - Consulta seus registros\n"
                "📈 **Status Geral** - Vê policiais em serviço"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Importante",
            value="• Você deve estar em um **canal de voz**\n• Registros são salvos automaticamente\n• Ponto fecha automaticamente ao sair de voz",
            inline=False
        )
        
        embed.set_footer(
            text="ACEDEPOL • Sistema de Controle de Ponto",
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None
        )
        
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        await interaction.channel.send(embed=embed, view=PainelPonto())
    else:
        # Para usuários normais, envia direto
        embed = discord.Embed(
            title="🚔 Sistema de Ponto - ACEDEPOL",
            description="",
            color=0x2b2d31
        )
        
        embed.add_field(
            name="",
            value="**POLÍCIA CIVIL NOVA CAPITAL**\n━━━━━━━━━━━━━━━━━━━━━━",
            inline=False
        )
        
        embed.add_field(
            name="📋 Como Usar",
            value=(
                "🟢 **Abrir Ponto** - Registra sua entrada no serviço\n"
                "🔴 **Fechar Ponto** - Registra sua saída e calcula horas\n"
                "📊 **Meus Horários** - Consulta seus registros\n"
                "📈 **Status Geral** - Vê policiais em serviço"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Importante",
            value="• Você deve estar em um **canal de voz**\n• Registros são salvos automaticamente\n• Ponto fecha automaticamente ao sair de voz",
            inline=False
        )
        
        embed.set_footer(
            text="ACEDEPOL • Sistema de Controle de Ponto",
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None
        )
        
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        await interaction.response.send_message(embed=embed, view=PainelPonto())

@bot.tree.command(name="admin", description="Painel administrativo")
async def painel_admin(interaction: discord.Interaction):
    if not is_server_admin(interaction.user):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    embed = discord.Embed(title="👮‍♂️ Painel Admin", color=COLORS["info"])
    await interaction.response.send_message(embed=embed, view=PainelAdmin(), ephemeral=True)

@bot.tree.command(name="reset", description="Resetar horas")
async def reset_horas(interaction: discord.Interaction):
    if not is_server_admin(interaction.user):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    data = load_data()
    view = PainelReset()
    
    options = [
        discord.SelectOption(label=u['name'], value=uid)
        for uid, u in data.items() if u['records']
    ]
    
    if options:
        view.select_reset.options = options[:25]
        await interaction.response.send_message("Selecione o policial:", view=view, ephemeral=True)
    else:
        await interaction.response.send_message("📊 Nenhum registro encontrado.", ephemeral=True)

@bot.tree.command(name="config", description="Configurar cargos")
async def config_cargos(interaction: discord.Interaction):
    if not (is_admin(interaction.user.id) or interaction.user.guild_permissions.administrator):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="⚙️ Configuração do Sistema - ACEDEPOL",
        description="""
        **Configure o sistema usando IDs:**
        
        🟢 **Cargo Permitido:** Pode usar o sistema de ponto
        🔵 **Cargo Admin:** Pode administrar o sistema
        🎙️ **Canal Permitido:** Canais de voz autorizados
        
        **Como obter IDs:**
        1. Ative o Modo Desenvolvedor (Configurações > Avançado)
        2. Clique com botão direito no cargo/canal
        3. Selecione "Copiar ID"
        4. Cole no formulário que abrir
        """,
        color=COLORS["info"]
    )
    await interaction.response.send_message(embed=embed, view=PainelConfig(interaction.guild.id, interaction.guild), ephemeral=True)

@bot.tree.command(name="adicionar_horas", description="Adicionar horas manualmente a um policial")
async def adicionar_horas(interaction: discord.Interaction, usuario: discord.Member, horas: int, minutos: int = 0, motivo: str = "Ajuste manual"):
    """Adiciona horas manualmente ao registro de um usuário"""
    if not is_server_admin(interaction.user):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    if horas < 0 or minutos < 0 or minutos >= 60:
        await interaction.response.send_message("❌ Valores inválidos! Horas e minutos devem ser positivos.", ephemeral=True)
        return
    
    user_id = str(usuario.id)
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {'name': usuario.display_name, 'records': [], 'current_session': None}
    
    # Cria um registro manual
    now = datetime.now()
    entrada = now - timedelta(hours=horas, minutes=minutos)
    
    record = {
        'entrada': entrada.strftime('%Y-%m-%d %H:%M:%S'),
        'saida': now.strftime('%Y-%m-%d %H:%M:%S'),
        'canal': 'Ajuste Manual',
        'duracao': f"{horas}:{minutos:02d}:00",
        'manual': True,
        'motivo': motivo,
        'adicionado_por': interaction.user.display_name
    }
    
    data[user_id]['records'].append(record)
    save_data(data)
    
    embed = discord.Embed(
        title="✅ Horas Adicionadas",
        description=f"**Policial:** {usuario.display_name}\n**Tempo adicionado:** {horas}h {minutos}min\n**Motivo:** {motivo}\n**Por:** {interaction.user.display_name}",
        color=COLORS["success"]
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Envia log
    await enviar_log(
        interaction.guild,
        "⏱️ Horas Adicionadas",
        usuario,
        f"**Tempo adicionado:** {horas}h {minutos}min\n**Motivo:** {motivo}\n**Por:** {interaction.user.mention}",
        COLORS["success"]
    )
    
    # Tenta notificar o usuário
    try:
        embed_user = discord.Embed(
            title="⏱️ Horas Adicionadas ao Seu Registro",
            description=f"Um administrador adicionou **{horas}h {minutos}min** ao seu registro.\n\n**Motivo:** {motivo}",
            color=COLORS["info"]
        )
        await usuario.send(embed=embed_user)
    except:
        pass

@bot.tree.command(name="zerar_todos", description="Zerar horas de TODOS os policiais (CUIDADO!)")
async def zerar_todos(interaction: discord.Interaction, confirmacao: str):
    """Zera as horas de todos os policiais - REQUER CONFIRMAÇÃO"""
    if not is_server_admin(interaction.user):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    # Verifica confirmação
    if confirmacao.upper() != "CONFIRMAR":
        embed = discord.Embed(
            title="⚠️ Confirmação Necessária",
            description=(
                "**ATENÇÃO:** Este comando irá **ZERAR** as horas de **TODOS** os policiais!\n\n"
                "Para confirmar, use o comando novamente com:\n"
                "`confirmacao: CONFIRMAR`\n\n"
                "**Isso irá:**\n"
                "• Apagar todos os registros de ponto\n"
                "• Fechar todas as sessões ativas\n"
                "• Criar backup automático\n"
                "• Enviar log da ação"
            ),
            color=COLORS["error"]
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    data = load_data()
    
    if not data:
        await interaction.response.send_message("📊 Não há dados para zerar!", ephemeral=True)
        return
    
    # Cria backup completo
    backup_filename = f"backup_geral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Conta quantos policiais serão afetados
    total_policiais = len(data)
    total_registros = sum(len(user_data['records']) for user_data in data.values())
    sessoes_ativas = sum(1 for user_data in data.values() if user_data.get('current_session'))
    
    # Zera todos os dados
    for user_id in data:
        data[user_id]['records'] = []
        data[user_id]['current_session'] = None
    
    save_data(data)
    
    # Resposta
    embed = discord.Embed(
        title="🔄 Horários Zerados - TODOS",
        description=(
            f"**Ação executada com sucesso!**\n\n"
            f"**📊 Estatísticas:**\n"
            f"• Policiais afetados: {total_policiais}\n"
            f"• Registros apagados: {total_registros}\n"
            f"• Sessões fechadas: {sessoes_ativas}\n\n"
            f"**💾 Backup:** `{backup_filename}`\n"
            f"**👤 Executado por:** {interaction.user.mention}"
        ),
        color=COLORS["warning"]
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Envia log
    await enviar_log(
        interaction.guild,
        "⚠️ RESET GERAL - Todas as Horas Zeradas",
        interaction.user,
        f"**Policiais afetados:** {total_policiais}\n**Registros apagados:** {total_registros}\n**Sessões fechadas:** {sessoes_ativas}\n**Backup:** `{backup_filename}`",
        0xed4245
    )
    
    # Tenta notificar todos os usuários afetados
    notificados = 0
    for user_id in data:
        try:
            user = await interaction.client.fetch_user(int(user_id))
            embed_user = discord.Embed(
                title="🔄 Seus Horários Foram Zerados",
                description=f"Um administrador zerou as horas de todos os policiais.\n\n**Executado por:** {interaction.user.display_name}\n\nTodos os registros foram apagados e um backup foi criado.",
                color=COLORS["warning"]
            )
            await user.send(embed=embed_user)
            notificados += 1
        except:
            pass
    
    # Envia mensagem no canal sobre notificações
    if notificados > 0:
        await interaction.followup.send(f"📨 {notificados} policiais foram notificados por DM.", ephemeral=True)

@bot.tree.command(name="remover_horas", description="Remover horas de um policial")
async def remover_horas(interaction: discord.Interaction, usuario: discord.Member, horas: int, minutos: int = 0, motivo: str = "Ajuste manual"):
    """Remove horas do registro de um usuário"""
    if not is_server_admin(interaction.user):
        await interaction.response.send_message("❌ Acesso negado!", ephemeral=True)
        return
    
    if horas < 0 or minutos < 0 or minutos >= 60:
        await interaction.response.send_message("❌ Valores inválidos! Horas e minutos devem ser positivos.", ephemeral=True)
        return
    
    user_id = str(usuario.id)
    data = load_data()
    
    if user_id not in data or not data[user_id]['records']:
        await interaction.response.send_message("❌ Este usuário não possui registros!", ephemeral=True)
        return
    
    # Cria um registro negativo
    now = datetime.now()
    entrada = now + timedelta(hours=horas, minutes=minutos)
    
    record = {
        'entrada': entrada.strftime('%Y-%m-%d %H:%M:%S'),
        'saida': now.strftime('%Y-%m-%d %H:%M:%S'),
        'canal': 'Ajuste Manual',
        'duracao': f"-{horas}:{minutos:02d}:00",
        'manual': True,
        'motivo': motivo,
        'removido_por': interaction.user.display_name
    }
    
    data[user_id]['records'].append(record)
    save_data(data)
    
    embed = discord.Embed(
        title="✅ Horas Removidas",
        description=f"**Policial:** {usuario.display_name}\n**Tempo removido:** {horas}h {minutos}min\n**Motivo:** {motivo}\n**Por:** {interaction.user.display_name}",
        color=COLORS["warning"]
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Envia log
    await enviar_log(
        interaction.guild,
        "🗑️ Horas Removidas",
        usuario,
        f"**Tempo removido:** {horas}h {minutos}min\n**Motivo:** {motivo}\n**Por:** {interaction.user.mention}",
        COLORS["warning"]
    )
    
    # Tenta notificar o usuário
    try:
        embed_user = discord.Embed(
            title="⏱️ Horas Removidas do Seu Registro",
            description=f"Um administrador removeu **{horas}h {minutos}min** do seu registro.\n\n**Motivo:** {motivo}",
            color=COLORS["warning"]
        )
        await usuario.send(embed=embed_user)
    except:
        pass

# Executar bot
if __name__ == "__main__":
    try:
        print("🚔 Iniciando Bot de Ponto ACEDEPOL...")
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"❌ Erro: {e}")
