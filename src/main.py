import discord
from discord.ext import commands
from discord import app_commands
import config
from ai_modules.llm import generate_response


TOKEN = config.TOKEN

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Синхронизация slash-команд
        await self.tree.sync()
        # await self.tree.sync()
        print(f"Slash-команды синхронизированы.")

    async def on_ready(self):
        print(f"Бот запущен как {self.user}")
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Учусь 💻"))


bot = Client()


@bot.tree.command(name="ping", description="Пинг бота")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

# Source - https://translated.turbopages.orghttps://translated.turbopages.org/proxy_u/en-ru.ru.2f93fed6-69a6d812-ec7a8cd2-74722d776562/https/stackoverflow.com/a
# Posted by Miller
# Retrieved 2026-03-03, License - CC BY-SA 4.0

# an example of a global sync command
@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if str(interaction.user.id) == config.TYTYBER_ID:
        await client.tree.sync()
        await interaction.response.send_message('Synced Successfully')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')


@bot.tree.command(name="connect", description="Подключиться к голосовому каналу")
async def connect(interaction: discord.Interaction):

    if not interaction.user.voice:
        await interaction.response.send_message(
            "Ты не в голосовом канале.",
            ephemeral=True
        )
        return

    if interaction.guild.voice_client:
        await interaction.response.send_message(
            "Я уже подключена.",
            ephemeral=True
        )
        return

    await interaction.response.defer()  # 🔥 СРАЗУ подтверждаем

    channel = interaction.user.voice.channel
    await channel.connect()

    await interaction.followup.send(f"Подключилась к {channel.name}")


@bot.tree.command(name="disconnect", description="Отключиться от голосового канала")
async def disconnect(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if not voice_client:
        await interaction.response.send_message(
            "Я не подключен к голосовому каналу.", 
            ephemeral=True
        )
        return

    await voice_client.disconnect()
    await interaction.response.send_message("Отключился")


@bot.tree.command(name="repeat", description="Повтори сообщение")
async def repeat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


print("Регистрация команды /say")
@bot.tree.command(name="mes", description="Поговорить с Touka")
async def mes(interaction: discord.Interaction, text: str):
    await interaction.response.defer()  # сразу подтверждаем

    try:
        reply = await generate_response(
            guild_id=interaction.guild.id if interaction.guild else 0,
            user_id=interaction.user.id,
            text=text
        )

        await interaction.followup.send(reply)

    except Exception as e:
        await interaction.followup.send(f"Ошибка: {e}")
    
bot.run(TOKEN)

