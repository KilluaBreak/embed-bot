import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ Slash command HARUS ditulis sebelum on_ready()
@bot.tree.command(name="ping", description="Tes bot aktif")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Slash command berhasil!", ephemeral=True)

@bot.event
async def on_ready():
    try:
        # Periksa jumlah command yang terdaftar
        print(f"🔍 Jumlah command sebelum sync: {len(bot.tree.get_commands())}")
        for cmd in bot.tree.get_commands():
            print(f"🔹 Ditemukan command: /{cmd.name}")

        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Slash command berhasil disinkron: {len(synced)} command")
        print(f"🤖 Bot siap sebagai {bot.user}")
    except Exception as e:
        print(f"❌ Gagal sync command: {e}")

bot.run(TOKEN)
