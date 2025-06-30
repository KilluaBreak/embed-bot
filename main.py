# test_slash.py
import os, discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN   = os.getenv("DISCORD_TOKEN")
GUILD   = int(os.getenv("GUILD_ID", 0))

intents = discord.Intents.default()
bot     = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="ping", description="pong test")
async def ping(inter: discord.Interaction):
    await inter.response.send_message("pong 🏓", ephemeral=True)

@bot.event
async def on_ready():
    print("Registered cmds:", bot.tree.get_commands())          # <— should show 1 command
    synced = await bot.tree.sync(guild=discord.Object(id=GUILD))
    print("Synced len:", len(synced))
    print("Bot ready:", bot.user)

bot.run(TOKEN)
