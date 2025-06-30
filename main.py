# main.py — Uji Slash Command Minimal
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# SLASH COMMAND TEST
@bot.tree.command(name="ping", description="Tes apakah bot aktif")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Bot aktif!", ephemeral=True)

@bot.event
async def on_ready():
    try:
        commands_before = bot.tree.get_commands()
        print(f"🔍 Command terdaftar sebelum sync: {len(commands_before)} → {commands_before}")

        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Bot siap sebagai {bot.user}")
        print(f"✅ Slash command berhasil disinkron: {len(synced)} command")
    except Exception as e:
        print(f"❌ Gagal sync command: {e}")

bot.run(TOKEN)
