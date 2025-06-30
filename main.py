import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Bot online sebagai {bot.user}")
        print(f"✅ Slash command tersinkron di GUILD_ID {GUILD_ID}: {len(synced)} command")
    except Exception as e:
        print(f"❌ Gagal sync slash command: {e}")

@bot.tree.command(name="cek", description="Cek apakah bot aktif")
async def cek(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Bot aktif & slash command muncul!", ephemeral=True)

bot.run(TOKEN)
